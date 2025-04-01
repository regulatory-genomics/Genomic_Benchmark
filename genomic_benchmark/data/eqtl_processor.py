"""
eQTL data processing module
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Union, Optional, Tuple
from .base_processor import BaseProcessor

class EQTLProcessor(BaseProcessor):
    """eQTL data processing class"""
    
    def __init__(
        self, 
        dataset_name: str, 
        cache_root: Optional[Union[str, Path]] = None,
        ):
        """
        Initialize eQTL data processor
        
        Args:
            dataset_name: Dataset name, e.g., 'GTEx_v8'
            cache_root: Cache root directory, defaults to .cache/genomics_benchmark in user's home directory
        """
        super().__init__("eqtl", dataset_name, cache_root)

    def download_and_process(self, output_dir: Optional[Union[str, Path]] = None, force: bool = False) -> pd.DataFrame:
        """
        Download and process eQTL data
        """
        raw_path = super().download(force)
        self.process(raw_path, output_dir)
        return self.data
    
    def process(self, data_path: Optional[Union[str, Path]] = None, output_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
        """
        Process data with standard pipeline
        
        Args:
            data_path: Path to input data file, if None, use self.data_path
            output_dir: Directory to save processed data
            
        Returns:
            Processed DataFrame
        """
        if data_path is None:
            data_path = self.data_path
            
        if data_path is None:
            raise ValueError("No data path provided")
            
        # Load data
        self.data = self.load_file(data_path)
        
        # Apply standard processing pipeline
        self.data = self.column_mapping(self.data)
        self.data = self.parse_variant_info(self.data)
        self.data = self.filter_output_columns(self.data)
        
        # Save processed data if output path is provided
        if output_dir is None:
            output_dir = self.cache_dir
        self.save_processed_data(output_dir)
            
        print(f"Processed data shape: {self.data.shape}")
        print(f"Processed data columns: {self.data.columns.tolist()}")
        
        return self.data

    def parse_variant_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse variant information from variant_id
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with parsed variant information
        """
        df = df.copy()
        
        # Parse variant_id (format: chr1_1291731_TG_T_b38)
        variant_info = df['variant_id'].str.split('_', expand=True)
        df['chr'] = variant_info[0]
        df['start'] = variant_info[1].astype(int)
        df['end'] = df['start']
        df['ref'] = variant_info[2]
        df['alt'] = variant_info[3]
        
        return df

    def add_gene_info(self, gtf_file: Union[str, Path]) -> pd.DataFrame:
        """
        Add gene information from GTF file
        
        Args:
            gtf_file: Path to GTF file
            
        Returns:
            DataFrame with added gene information
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        print("Reading gene annotation from GTF file...")
        # Read GTF file
        gene_annotation = pd.read_csv(
            gtf_file, sep='\t', comment='#', header=None,
            names=['chr', 'source', 'type', 'start', 'end', 'score', 'strand', 'frame', 'attribute']
        )
        
        # Extract gene information
        gene_annotation = gene_annotation[gene_annotation['type'] == 'gene']
        gene_annotation['gene_name'] = gene_annotation['attribute'].str.extract(r'gene_name "(.*?)";')
        gene_annotation['gene_name'] = gene_annotation['gene_name'].str.replace('"', '')
        
        # Convert start and end to integer
        gene_annotation['start'] = gene_annotation['start'].astype(int)
        gene_annotation['end'] = gene_annotation['end'].astype(int)
        
        # Calculate TSS position based on strand
        gene_annotation['gene_tss'] = gene_annotation.apply(
            lambda x: int(x['start']) if x['strand'] == '+' else int(x['end']),
            axis=1
        )
        
        # If there are duplicate gene_names, keep the first one
        gene_annotation = gene_annotation.drop_duplicates(subset=['gene_name'], keep='first')
        gene_annotation = gene_annotation[['gene_name', 'strand', 'gene_tss']]
        
        # Merge gene information
        print("Adding gene information...")
        self.data = self.data.merge(
            gene_annotation,
            on='gene_name',
            how='left'
        )
        
        # Check for missing information
        missing_strand = self.data['strand'].isna().sum()
        missing_tss = self.data['gene_tss'].isna().sum()
        if missing_strand > 0 or missing_tss > 0:
            print(f"Warning: {missing_strand} genes have missing strand information")
            print(f"Warning: {missing_tss} genes have missing TSS information")
            self.data = self.data.dropna(subset=['strand', 'gene_tss'])
            
        return self.data
    
    def filter_distance(self, distance_threshold: Optional[int] = None) -> pd.DataFrame:
        """
        Filter data based on distance threshold
        
        Args:
            distance_threshold: Maximum allowed distance between variant and gene TSS
            
        Returns:
            Filtered DataFrame
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        self.data['distance'] = abs(self.data['start'] - self.data['gene_tss'])
        print(f"Before filtering distance, the shape of the dataframe is {self.data.shape}")

        self.data = self.data[self.data['distance'] <= distance_threshold]
        print(f"After filtering distance, the shape of the dataframe is {self.data.shape}")
            
        return self.data
    
    def filter_protein_coding(self) -> pd.DataFrame:
        """
        Filter data based on protein coding status
        
        Returns:
            Filtered DataFrame
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        print(f"Before filtering protein coding, the shape of the dataframe is {self.data.shape}")
        self.data = self.data[self.data['biotype'] == 'protein_coding']
        print(f"After filtering protein coding, the shape of the dataframe is {self.data.shape}")
        return self.data
    
    def filter_only_snp(self) -> pd.DataFrame:
        """
        Filter data based on SNP status
        
        Returns:
            Filtered DataFrame
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        self.data['is_snp'] = (self.data['ref'].str.len() == 1) & (self.data['alt'].str.len() == 1)
        print(f"Before filtering SNP, the shape of the dataframe is {self.data.shape}")

        self.data = self.data[self.data['is_snp']]
        print(f"After filtering SNP, the shape of the dataframe is {self.data.shape}")
        return self.data

    def add_labels(self, pos_threshold: float = 0.90, neg_threshold: float = 0.01) -> pd.DataFrame:
        """
        Add binary labels based on PIP threshold
        
        Args:
            pos_threshold: Threshold for positive class
            neg_threshold: Threshold for negative class
            
        Returns:
            DataFrame with added labels
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        self.data = self.data.copy()
        
        # Initialize with negative class
        self.data['label'] = 0
        
        # Add positive and negative labels
        self.data.loc[self.data['pip'] >= pos_threshold, 'label'] = 1
        self.data.loc[self.data['pip'] <= neg_threshold, 'label'] = 0
        
        # Remove samples with PIP between thresholds
        self.data = self.data[~((self.data['pip'] > neg_threshold) & (self.data['pip'] < pos_threshold))]

        pos_count = self.data[self.data['label'] == 1].shape[0]
        neg_count = self.data[self.data['label'] == 0].shape[0]
        print(f"Positive samples: {pos_count}, Negative samples: {neg_count}")
        
        return self.data
    
    def check_snp_matching(self, fasta_file: str) -> dict:
        """
        Check if SNP bases match with reference genome and count matches/mismatches.
        
        Args:
            fasta_file: Path to the reference genome FASTA file
            
        Returns:
            dict: Dictionary containing matching statistics
                {
                    'total_snps': int,
                    'matching_bases': int,
                    'mismatching_bases': int,
                    'match_rate': float,
                    'mismatch_rate': float
                }
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        import pysam
        
        # Initialize counters
        matching_bases = 0
        mismatching_bases = 0
        
        # Open FASTA file
        fasta = pysam.FastaFile(fasta_file)
        
        # Process each SNP
        for _, row in self.data.iterrows():
            try:
                # Get reference base at SNP position
                ref_base = fasta.fetch(row['chr'], row['start']-1, row['start']).upper()
                
                # Compare with SNP base
                if ref_base == row['ref'].upper():
                    matching_bases += 1
                else:
                    mismatching_bases += 1
                    
            except Exception as e:
                print(f"Error processing SNP at {row['chr']}:{row['start']}: {str(e)}")
                continue
        
        # Close FASTA file
        fasta.close()
        
        # Calculate total and rates
        total_snps = matching_bases + mismatching_bases
        match_rate = matching_bases / total_snps if total_snps > 0 else 0
        mismatch_rate = mismatching_bases / total_snps if total_snps > 0 else 0
        
        # Create results dictionary
        results = {
            'total_snps': total_snps,
            'matching_bases': matching_bases,
            'mismatching_bases': mismatching_bases,
            'match_rate': match_rate,
            'mismatch_rate': mismatch_rate
        }        
        # Print summary
        print(f"SNP Base Matching Summary:")
        print(f"Total SNPs processed: {total_snps}")
        print(f"Matching bases: {matching_bases} ({match_rate:.2%})")
        print(f"Mismatching bases: {mismatching_bases} ({mismatch_rate:.2%})")
        
        return results
    
    def save_to_vcf(self, output_dir: Union[str, Path]) -> None:
        """
        Save processed data to VCF format, separating positive and negative samples
        
        Args:
            output_dir: Directory to save the VCF files
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        self.data = self.data.copy()
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Prepare VCF header
        vcf_header = (
            "##fileformat=VCFv4.2\n"
            "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tDISTANCE\tSTRAND\tGENE\n"
        )
        
        # Split data into positive and negative samples
        pos_data = self.data[self.data['label'] == 1]
        neg_data = self.data[self.data['label'] == 0]
        
        # Function to format a single row
        def format_vcf_row(row):
            return f"{row['chr']}\t{row['start']}\t.\t{row['ref']}\t{row['alt']}\t.\tPASS\t{int(row['distance'])}\t{row['strand']}\t{row['gene_name']}"
        
        # Save positive samples
        pos_vcf_path = output_dir / "positive.vcf"
        with open(pos_vcf_path, 'w') as f:
            f.write(vcf_header)
            for _, row in pos_data.iterrows():
                f.write(format_vcf_row(row) + "\n")
        print(f"Saved {len(pos_data)} positive samples to: {pos_vcf_path}")
        
        # Save negative samples
        neg_vcf_path = output_dir / "negative.vcf"
        with open(neg_vcf_path, 'w') as f:
            f.write(vcf_header)
            for _, row in neg_data.iterrows():
                f.write(format_vcf_row(row) + "\n")
        print(f"Saved {len(neg_data)} negative samples to: {neg_vcf_path}")
        
        print("\nVCF files saved successfully!")
        print(f"Positive samples: {len(pos_data):,}")
        print(f"Negative samples: {len(neg_data):,}")
        print(f"Total samples: {len(pos_data) + len(neg_data):,}")
        
        # Save sample counts to a summary file
        summary_path = output_dir / "vcf_summary.txt"
        with open(summary_path, 'w') as f:
            f.write(f"Positive samples: {len(pos_data)}\n")
            f.write(f"Negative samples: {len(neg_data)}\n")
            f.write(f"Total samples: {len(pos_data) + len(neg_data)}\n")
            f.write(f"\nFiles:\n")
            f.write(f"Positive VCF: {pos_vcf_path}\n")
            f.write(f"Negative VCF: {neg_vcf_path}\n")

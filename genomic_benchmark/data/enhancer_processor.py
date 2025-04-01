"""
Enhancer data processing module
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Union, Optional, Tuple
from sklearn.metrics import roc_auc_score, average_precision_score
from .base_processor import BaseProcessor

class EnhancerProcessor(BaseProcessor):
    """Enhancer data processing class"""
    
    def __init__(
        self, 
        dataset_name: str, 
        cache_root: Optional[Union[str, Path]] = None,
        ):
        """
        Initialize enhancer data processor
        
        Args:
            dataset_name: Dataset name, e.g., 'fulco'
            cache_root: Cache root directory, defaults to .cache/genomics_benchmark in user's home directory
        """
        super().__init__("enhancer", dataset_name, cache_root)

    def download_and_process(self, output_dir: Optional[Union[str, Path]] = None, force: bool = False) -> pd.DataFrame:
        """
        Download and process enhancer data
        """
        raw_path = super().download(force)
        super().process(raw_path, output_dir)

        return self.data
    
    def add_strand_info(self, gtf_file: Union[str, Path]) -> pd.DataFrame:
        """
        Add gene strand information from GTF file
        
        Args:
            gtf_file: Path to GTF file
            
        Returns:
            DataFrame with added strand information
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
        
        # if there are duplicate gene_name, keep the first one
        gene_annotation = gene_annotation.drop_duplicates(subset=['gene_name'], keep='first')
        
        # Create a dictionary for mapping
        strand_dict = dict(zip(gene_annotation['gene_name'], gene_annotation['strand']))
        
        # Add strand information using map
        print("Adding strand information...")
        self.data['strand'] = self.data['gene_name'].map(strand_dict)
        
        # Fill missing strand with '+' (positive strand)
        missing_strand = self.data['strand'].isna().sum()
        if missing_strand > 0:
            print(f"Warning: {missing_strand} genes have missing strand information, setting to positive strand")
            self.data.loc[self.data['strand'].isna(), 'strand'] = '+'
            print(f"After filling missing strand, the shape of the dataframe is {self.data.shape}")
            
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
            
        self.data = self.data[self.data['distance'] <= distance_threshold]
        print(f"After filtering distance, the shape of the dataframe is {self.data.shape}")
            
        return self.data
       
    def calculate_metrics(self, score_column: str = 'ABC Score') -> Dict[str, float]:
        """
        Calculate AUROC and AUPRC between specified column and labels
        
        Args:
            score_column: Score column name for metric calculation, defaults to 'ABC Score'
            
        Returns:
            Dictionary containing AUROC and AUPRC
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        if score_column not in self.data.columns:
            raise ValueError(f"Column not found in data: {score_column}")
        
        if 'label' not in self.data.columns:
            raise ValueError("Labels column not found in data")
            
        # Ensure no missing values
        valid_mask = ~(self.data[score_column].isna() | self.data['label'].isna())
        scores = self.data.loc[valid_mask, score_column]
        labels = self.data.loc[valid_mask, 'label']
        
        # Calculate AUROC and AUPRC
        auroc = roc_auc_score(labels, scores)
        auprc = average_precision_score(labels, scores)
        
        return {
            'AUROC': auroc,
            'AUPRC': auprc
        }
    
    
    
    
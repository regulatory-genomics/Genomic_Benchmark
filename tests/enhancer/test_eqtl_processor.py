"""
Test script for EQTLProcessor
"""
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

import genomic_benchmark as gb

def main():
    # Set cache root and output path
    dataset_name = "Adipose_Subcutaneous"  # GTEx tissue
    output_dir = "/storage/zhangkaiLab/liuyue87/Projects/Genomic_Benchmark/cache"
       
    processor = gb.EQTLProcessor(dataset_name)

    # 1. Download data
    print("1. Data download and processing...")
    processor.download_and_process(output_dir=output_dir)
    
    # 2. Add gene info
    print("\n2. Adding gene info...")
    gtf_file = "/storage/zhangkaiLab/liuyue87/Projects/Benchmark_Genomics/data/cache/reference_genome/hg38/gencode.v47.annotation.gtf"
    processor.add_gene_info(gtf_file)

    # 3. Filter distance
    print("\n3. Filtering distance...")
    processor.filter_distance(distance_threshold=100000000)

    # 4. Filter protein coding
    print("\n4. Filtering protein coding...")
    processor.filter_protein_coding()

    # 5. Filter SNP
    print("\n5. Filtering SNP...")
    processor.filter_only_snp()

    # 6. save processed data
    print("\n6. Saving processed data...")
    processor.save_processed_data(output_dir, file_name="Adipose_Subcutaneous_processed")

    # 7. Check SNP matching
    print("\n7. Checking SNP matching...")
    fasta_file = "/storage/zhangkaiLab/liuyue87/Projects/Benchmark_Genomics/data/cache/reference_genome/hg38/GRCh38.p14.genome.fa"
    snp_matching = processor.check_snp_matching(fasta_file)
    print(f"SNP matching: {snp_matching}")

    # 7. Add labels
    print("\n7. Adding labels...")
    processor.add_labels(pos_threshold=0.90, neg_threshold=0.01)

    # 8. Save to VCF
    print("\n8. Saving to VCF...")
    output_dir = "/storage/zhangkaiLab/liuyue87/Projects/Genomic_Benchmark/cache/eqtl/Adipose_Subcutaneous"
    processor.save_to_vcf(output_dir)
    
    

if __name__ == "__main__":
    main() 
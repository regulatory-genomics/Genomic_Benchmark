"""
Test script for EnhancerProcessor
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
    dataset_name = "Gasperini" # "Gasperini" # "Fulco" # "Schraivogel" # "Merged"
    output_dir = "/storage/zhangkaiLab/liuyue87/Projects/Genomic_Benchmark/cache"
       
    processor = gb.EnhancerProcessor(dataset_name)

    # 1. Download data
    print("1. Data download and processing...")
    processor.download_and_process(output_dir=output_dir)
    
    # 2. Add strand info
    print("\n2. Adding strand info...")
    gtf_file = "/storage/zhangkaiLab/liuyue87/Projects/Benchmark_Genomics/data/cache/reference_genome/hg38/gencode.v47.annotation.gtf"
    processor.add_strand_info(gtf_file)

    # 3. Filter distance
    print("\n3. Filtering distance...")
    processor.filter_distance(distance_threshold=100000000)

    # 4. save processed data
    print("\n4. Saving processed data...")
    processor.save_processed_data(output_dir, file_name="Gasperini_processed")

    # 5. calculate metrics
    print("\n5. Calculating metrics...")
    metrics = processor.calculate_metrics(score_column='ABC Score')
    print(f"Metrics: {metrics}")

    # 5. analyze label distribution
    print("\n5. Analyzing label distribution...")
    label_distribution = processor.print_label_distribution()
    print(f"Label distribution: {label_distribution}")

if __name__ == "__main__":
    main()
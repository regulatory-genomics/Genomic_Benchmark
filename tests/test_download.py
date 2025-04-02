"""
Test script for enhancer data loading
"""
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import genomic_benchmark as gb


def main():
    # task_name = "eqtl"
    # dataset_name = "Adipose_Subcutaneous"
    task_name = "enhancer"
    dataset_name = "Gasperini"
    output_dir = "/storage/zhangkaiLab/liuyue87/Projects/Genomic_Benchmark/cache"
    
    #1. Download data
    data_path_dict = gb.download_data(
        task_name, 
        dataset_name, 
        output_dir,
        download_raw=False
    )
    print(data_path_dict)

    #2. Load data
    df = gb.load_table(data_path_dict["data_path"])

    #3. Filter distance
    filtered_df = gb.filter_distance(df, (0, 100000))

    #4. Print label distribution
    gb.print_label_distribution(filtered_df)

    #5. Save data
    output_path = data_path_dict["data_path"].replace(".tsv", "_filtered.tsv")
    gb.save_table(filtered_df, output_path)

    

if __name__ == "__main__":
    main()
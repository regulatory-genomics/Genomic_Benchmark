"""
eQTL data configuration module
"""
from typing import Dict, Any

# eQTL task configuration
EQTL_CONFIG = {
    "task_config": {
            "columns": [
                "chr", "start", "end", "ref", "alt", 
                "gene_name", "gene_tss", "strand", 
                "distance", 
                "score", "label"
            ],
        },
    
    "Adipose_Subcutaneous": {
            "name": "Adipose Subcutaneous eQTL Dataset",
            "description": "eQTL data from GTEx v10 for Adipose Subcutaneous tissue",
            "genome_version": "hg38",
            "data_url": "https://osf.io/download/67ec8d1f63429550fdcf7620/",
            "data_format": "tsv",
            "info_url": "https://osf.io/download/67ec9049310f3e6d396ddb66/",
            "info_format": "md",
            "raw_url": "https://osf.io/download/67e262485178b65a1b44a8cc/",
            "raw_format": "parquet",
        }
    
} 

__all__ = ["EQTL_CONFIG"]
"""
eQTL data configuration module
"""
from typing import Dict, Any

# eQTL task configuration
EQTL_CONFIG = {
    "task_config": {
            "output_columns": [
                "gene_name",
                # 'gene_tss',
                "biotype",
                'chr', 'start', 'end', 'ref', 'alt', 
                "pip",
                # "distance",
            ],
        },
    
    "Adipose_Subcutaneous": {
            "name": "Adipose Subcutaneous eQTL Dataset",
            "description": "eQTL data from GTEx v10 for Adipose Subcutaneous tissue",
            "genome_version": "hg38",
            "data_url": "https://osf.io/download/67e262485178b65a1b44a8cc/",
            "file_format": "parquet",
            "info_url": "https://osf.io/download/67eb5d6ed7674dbd7e8b7f4f/",
            "info_file_format": "md",
            "column_mapping": {
                "gene_name": "gene_name",
                "biotype": "biotype",
                "variant_id": "variant_id",
                "pip": "pip",
            },
        }
    
} 

__all__ = ["EQTL_CONFIG"]
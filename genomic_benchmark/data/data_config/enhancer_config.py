"""
Enhancer task dataset configuration
"""
from typing import Dict, Any

ENHANCER_CONFIG = {
    # Task-level common configuration
    "task_config": {
        "columns": [
            "chr", "start", "end",  # Enhancer location
            "gene_name", "gene_tss", "strand",# Gene information
            "distance",  # Calculated distance
            "score", "label"
        ]
    },

    "Merged": {
        "name": "Merged Enhancer Dataset",
        "description": "Merged K562 enhancer dataset",
        "genome_version": "hg38",
        "data_url": "https://osf.io/download/67e25ef6be25353abd44a061/",
        "data_format": "tsv",
        "info_url": "https://osf.io/download/67e25ef6be25353abd44a061/",
        "info_format": "md",
        "raw_url": "https://osf.io/download/67e25ef6be25353abd44a061/",
        "raw_format": "tsv",
    },

    "Fulco": {
        "name": "Fulco K562 Enhancer Dataset",
        "description": "Fulco K562 enhancer dataset in TSV format",
        "genome_version": "hg38",
        "data_url": "https://osf.io/download/67e25ef239118c58a3890d04/",
        "data_format": "tsv",
        "info_url": "https://osf.io/download/67e25ef239118c58a3890d04/",
        "info_format": "md",
        "raw_url": "https://osf.io/download/67e25ef239118c58a3890d04/",
        "raw_format": "tsv",
    },
    
    "Gasperini": {
        "name": "Gasperini K562 Enhancer Dataset",
        "description": "Gasperini K562 enhancer dataset",
        "genome_version": "hg38",
        "data_url": "https://osf.io/download/67ebb6e5528b3f0f7acf6926/",
        "data_format": "tsv",
        "info_url": "https://osf.io/download/67ec9059bc1d17c436829874/",
        "info_format": "md",
        "raw_url": "https://osf.io/download/67e25ef65da5486b3e496c77/",
        "raw_format": "tsv",
    },

    "Schraivogel": {
        "name": "Schraivogel K562 Enhancer Dataset",
        "description": "Schraivogel K562 enhancer dataset",
        "genome_version": "hg38",
        "data_url": "hhttps://osf.io/download/67e25e60ad165245f0c7cff9/",
        "data_format": "tsv",
        "info_url": "https://osf.io/download/67e25e60ad165245f0c7cff9/",
        "info_format": "md",
        "raw_url": "https://osf.io/download/67e25e60ad165245f0c7cff9/",
        "raw_format": "tsv",
    },
    
}

__all__ = ["ENHANCER_CONFIG"]
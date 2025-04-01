"""
Enhancer task dataset configuration
"""
from typing import Dict, Any

ENHANCER_CONFIG = {
    # Task-level common configuration
    "task_config": {
        "output_columns": [
            "chr", "start", "end",  # Enhancer location
            "gene_name", "gene_tss", # Gene information
            "distance",  # Calculated distance
            "ABC Score",  # Effect size (if available)
            "label",  # Calculated label
            "score"
        ]
    },

    "Merged": {
        "name": "E2G Enhancer Dataset",
        "description": "E2G K562 enhancer dataset",
        "genome_version": "hg38",
        "data_url": "https://osf.io/download/67e25ef6be25353abd44a061/",
        "file_format": "tsv",
        "column_mapping": {
            "chr": "chrom",
            "start": "chromStart",
            "end": "chromEnd",
            "gene_name": "measuredGeneSymbol",
            "gene_tss": "startTSS",
            "ABC Score": "ABCScoreDNaseOnlyAvgHicTrack2",
            "distance": "distanceToTSS",
            "label": "Regulated",
            "score": "EffectSize"
        },
    },

    "Fulco": {
        "name": "Fulco K562 Enhancer Dataset",
        "description": "Fulco K562 enhancer dataset in TSV format",
        "genome_version": "hg38",
        "data_url": "https://osf.io/download/67e25ef239118c58a3890d04/",
        "file_format": "tsv",
        "column_mapping": {
            "chr": "chrom",
            "start": "chromStart",
            "end": "chromEnd",
            "gene_name": "measuredGeneSymbol",
            "gene_tss": "startTSS",
            "ABC Score": "ABCScoreDNaseOnlyAvgHicTrack2",
            "distance": "distanceToTSS",
            "label": "Regulated",
            "score": "EffectSize"
        },
    },
    
    "Gasperini": {
        "name": "Gasperini K562 Enhancer Dataset",
        "description": "Gasperini K562 enhancer dataset",
        "genome_version": "hg38",
        "data_url": "https://osf.io/download/67e25ef65da5486b3e496c77/",
        "file_format": "tsv",
        "info_url": "https://osf.io/download/67eb5c17763c88f69204eafd/",
        "info_file_format": "md",
        "column_mapping": {
            "chr": "chrom",
            "start": "chromStart",
            "end": "chromEnd",
            "gene_name": "measuredGeneSymbol",
            "gene_tss": "startTSS",
            "ABC Score": "ABCScoreDNaseOnlyAvgHicTrack2",
            "distance": "distanceToTSS",
            "label": "Regulated",
            "score": "EffectSize"
        },
    },

    "Schraivogel": {
        "name": "Schraivogel K562 Enhancer Dataset",
        "description": "Schraivogel K562 enhancer dataset",
        "genome_version": "hg38",
        "data_url": "https://osf.io/download/67e25e60ad165245f0c7cff9/",
        "file_format": "tsv",
        "column_mapping": {
            "chr": "chrom",
            "start": "chromStart",
            "end": "chromEnd",
            "gene_name": "measuredGeneSymbol",
            "gene_tss": "startTSS",
            "ABC Score": "ABCScoreDNaseOnlyAvgHicTrack2",
            "distance": "distanceToTSS",
            "label": "Regulated",
            "score": "EffectSize"
        },
    },

        # Dataset-specific configuration
    # "ABC_fulco": {
    #     "name": "Fulco Enhancer Dataset",
    #     "description": "Fulco K562 enhancer dataset",
    #     "genome_version": "hg19",  # Add genome version information
    #     "data_url": "https://osf.io/download/67e25ef3dbf123ce4b890a4e/",
    #     "file_format": "xlsx",
    #     "column_mapping": {
    #         # Mapping from source column names to standard column names
    #         "chr": "chr",
    #         "start": "start",
    #         "end": "end",
    #         "gene_name": "Gene",
    #         "gene_tss": "Gene TSS",
    #         "ABC Score": "ABC Score",
    #         "label": "Significant",
    #     },
    # },

    
}

__all__ = ["ENHANCER_CONFIG"]
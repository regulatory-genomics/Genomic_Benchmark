"""
Genomic Benchmark package
"""
from .data.data import (download_data,
                        load_table,
                        save_table,
                        print_label_distribution,
                        filter_distance
                        )

__all__ = [
    'download_data',
    'load_table',
    'save_table',
    'print_label_distribution',
    'filter_distance'
]

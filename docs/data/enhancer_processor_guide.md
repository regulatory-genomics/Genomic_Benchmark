# EnhancerProcessor User Guide

## Introduction

`EnhancerProcessor` is a tool class for processing enhancer data, supporting multiple datasets including Gasperini, Fulco, Schraivogel, and Merged datasets. This guide provides detailed instructions on how to use this tool class.

## Installation

```bash
pip install git+https://github.com/regulatory-genomics/Genomic_Benchmark.git
```

## Basic Usage

### 1. Import Package

```python
import genomic_benchmark as gb
from pathlib import Path
```

### 2. Initialize Processor
Enhancer datasets include four options: "Gasperini", "Fulco", "Schraivogel", "Merged"

```python
# Set dataset name
dataset_name = "Gasperini"

# Initialize processor
processor = gb.EnhancerProcessor(dataset_name)
```

### 3. Download and Process Data
The raw data will be downloaded to your system's default cache path. The preprocessed data (with unnecessary columns removed) will be stored in your specified path.

```python
# Set output directory
output_dir = Path("/path/to/your/output/directory")

# Download and process data
processor.download_and_process(output_dir=output_dir)
```
The preprocessed data columns include: ['chr', 'start', 'end', 'gene_name', 'gene_tss', 'distance', 'ABC Score', 'label', 'score']. Detailed descriptions can be found in info.md

If you need to download the raw data to a specific cache path, specify it during initialization:
```python
processor = gb.EnhancerProcessor("Gasperini", cache_root="/path/to/cache")
```

### 4. Add Strand Information

The raw data does not contain gene strand information. Use a GTF file to add gene strand information:

```python
# Set GTF file path
gtf_file = "/path/to/your/gencode.gtf"

# Add strand information
processor.add_strand_info(gtf_file)
```

### 5. Filter Distance

If you need to filter enhancer-to-TSS distances:

```python
# Set distance threshold (e.g., 100kb)
distance_threshold = 100000

# Filter distance
processor.filter_distance(distance_threshold)
```

### 6. Calculate Evaluation Metrics

The dataset includes ABC scores. Calculate AUROC and AUPRC for ABC Score:

```python
# Calculate evaluation metrics
metrics = processor.calculate_metrics(score_column='ABC Score')
```

### 7. Analyze Label Distribution

Analyze the distribution of positive and negative samples:

```python
# Analyze label distribution
label_distribution = processor.print_label_distribution()
```

### 8. Save Processed Data

Save the further processed data to the specified location:

```python
# Save processed data
processor.save_processed_data(output_dir, file_name="processed_data")
```

### 9. Clear Cache

If you need to clear cache data:

```python
# Clear cache for current dataset
processor.clear_cache()

# Or clear all cache
processor.clear_cache(clear_all=True)
```

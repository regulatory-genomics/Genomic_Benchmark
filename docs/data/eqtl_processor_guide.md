# eQTL Processor User Guide

This guide introduces how to use the `EQTLProcessor` class to process eQTL data. The processor is primarily designed for handling eQTL data from the GTEx dataset, supporting data download, processing, and conversion functions.

## Basic Usage

### 1. Initialize the Processor

```python
import genomic_benchmark as gb

# Initialize the processor with tissue name
processor = gb.EQTLProcessor(dataset_name="Adipose_Subcutaneous")  # Use GTEx tissue name
```

### 2. Data Download and Processing
The raw data will be downloaded to your system's default cache path. The preprocessed data (with unnecessary columns removed) will be stored in your specified path.
```python
# Set output directory
output_dir = "/path/to/output"

# Download and process data
processor.download_and_process(output_dir=output_dir)
```
The preprocessed data columns include: ['gene_name', 'biotype', 'chr', 'start', 'end', 'ref', 'alt', 'pip']. Detailed descriptions can be found in info.md

### 3. Add Gene Information

The raw data does not contain gene information (position and strand). Use a GTF file to add gene information:
```python
# Specify GTF file path
gtf_file = "/path/to/gencode.v47.annotation.gtf"

# Add gene information
processor.add_gene_info(gtf_file)
```

### 4. Data Filtering

The processor provides various data filtering methods:

```python
# Filter by distance
processor.filter_distance(distance_threshold=100000000)  # 100Mb

# Filter for protein coding genes only
processor.filter_protein_coding()

# Filter for SNPs only
processor.filter_only_snp()
```

### 5. SNP Matching Check
Check if SNPs match the corresponding bases in the reference genome:
```python
# Specify reference genome fasta file
fasta_file = "/path/to/GRCh38.p14.genome.fa"

# Check SNP matching
snp_matching = processor.check_snp_matching(fasta_file)
```

### 6. Add Labels

```python
# Set positive and negative sample thresholds
processor.add_labels(pos_threshold=0.90, neg_threshold=0.01)
```

### 7. Save Data

```python
# Save processed data
processor.save_processed_data(output_dir, file_name="processed_data")
```

### 8. Save VCF File
```python
# Save as VCF format
processor.save_to_vcf(output_dir)
```

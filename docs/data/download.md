# Data Download Guide

This guide will help you download and process datasets from the Genomic_Benchmark package.

## Supported Datasets

Currently supported task types and datasets:

### Enhancer Prediction Task
- Gasperini
- Fulco
- Schraivogel
- Merged

### eQTL Prediction Task
- Adipose_Subcutaneous
- Brain_Amygdala
- Whole_Blood
- Adding other data

## Download Steps

1. **Use the `download_data` function to download data:**

```python
import genomic_benchmark as gb

# Set parameters
task_name = "enhancer"  # or "eqtl"
dataset_name = "Gasperini"  # or "Adipose_Subcutaneous"
output_dir = "path/to/your/cache/directory"

# Download data
data_path_dict = gb.download_data(
    task_name, 
    dataset_name, 
    output_dir,
    download_raw=False  # whether to download raw data
)
```
Please refer to the downloaded demo data for details:[demo_data/](https://github.com/regulatory-genomics/Genomic_Benchmark/blob/main/demo_data/)

The download progress will be displayed:
```
Downloading from OSF: https://osf.io/download/67ebb6e5528b3f0f7acf6926/
Saving to: /storage/zhangkaiLab/liuyue87/Projects/Genomic_Benchmark/cache/Gasperini_processed.tsv
Download progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████| 360k/360k [00:01<00:00, 340kiB/s]

Downloading from OSF: https://osf.io/download/67ec9059bc1d17c436829874/
Saving to: /storage/zhangkaiLab/liuyue87/Projects/Genomic_Benchmark/cache/Gasperini_info.md
Download progress: 100%|████████████████████████████████████████████████████████████████████████████████████████| 1.08k/1.08k [00:00<00:00, 1.67MiB/s]
```

The function returns a dictionary containing file paths:
```python
{
    'data_path': '/path/to/Gasperini_processed.tsv',
    'info_path': '/path/to/Gasperini_info.md',
    'raw_path': None
}
```

2. **Load the data:**

```python
df = gb.load_table(data_path_dict["data_path"])
```

3. **Filter data (optional):**

```python
# Filter by distance range
filtered_df = gb.filter_distance(df, (0, 100000))
```

The shapes before and after filtering will be displayed:
```
Before filtering distance, the shape of the dataframe is (5318, 9)
After filtering distance, the shape of the dataframe is (933, 9)
```

4. **View label distribution:**

```python
gb.print_label_distribution(filtered_df)
```

The label distribution information will be displayed:
```
Label distribution: {
    'total_samples': 933, 
    'label_counts': {0: 640, 1: 293}, 
    'label_percentages': {0: 68.59592711682744, 1: 31.404072883172564}
}
```

5. **Save processed data:**

```python
output_path = data_path_dict["data_path"].replace(".tsv", "_filtered.tsv")
gb.save_table(filtered_df, output_path)
```

The save path will be displayed:
```
Saved table to /path/to/Gasperini_filtered.tsv
```

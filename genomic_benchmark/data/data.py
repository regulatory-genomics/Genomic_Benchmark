"""
Data download and processing module for genomic data
"""
import os
from pathlib import Path
from typing import Optional, Union, Dict, Any, Tuple
import pandas as pd
from .data_config.config_manager import get_dataset_config
from .download import DataDownloader

def download_data(
    task_name: str,
    dataset_name: str,
    save_dir: Optional[str] = None,
    download_raw: bool = True
) -> Dict[str, Union[str, Optional[str]]]:
    """
    Download genomic dataset
    
    Args:
        dataset_name: Name of the dataset (e.g., 'Merged', 'Fulco', 'Gasperini', 'Schraivogel')
        save_dir: Directory to save the files, if None use default directory
        download_info: Whether to download dataset information file
        
    Returns:
        Dict[str, Union[str, Optional[str]]]: Dictionary containing paths to data file, info file, and raw data file
        
    Raises:
        ValueError: If dataset name is invalid or download fails
    """
    # Get dataset configuration
    config = get_dataset_config(task_name, dataset_name)
    dataset_config = config["dataset_config"]
    
    downloader = DataDownloader(cache_dir = save_dir)
    
    # Download data file
    data_url = dataset_config["data_url"]
    data_format = dataset_config["data_format"]
    data_path = downloader.download(
        url=data_url,
        file_format=data_format,
        file_name=f"{dataset_name}.{data_format}"
    )
    
    # Download info file
    info_url = dataset_config["info_url"]
    info_format = dataset_config["info_format"]
    info_path = downloader.download(
        url=info_url,
        file_format=info_format,
        file_name=f"{dataset_name}_info.{info_format}"
    )

    raw_path = None
    if download_raw:
        raw_url = dataset_config["raw_url"]
        raw_format = dataset_config["raw_format"]
        raw_path = downloader.download(
            url=raw_url,
            file_format=raw_format,
            file_name=f"{dataset_name}_raw.{raw_format}"
        )

    return {
        "data_path": str(data_path),
        "info_path": str(info_path),
        "raw_path": str(raw_path) if raw_path else None
    }

def load_table(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load data based on file format
    
    Args:
        file_path: Path to the file
        
    Returns:
        Loaded DataFrame
    """
    file_path = Path(file_path)
    if file_path.suffix == '.xlsx':
        return pd.read_excel(file_path)
    elif file_path.suffix == '.csv':
        return pd.read_csv(file_path)
    elif file_path.suffix == '.tsv':
        return pd.read_csv(file_path, sep='\t')
    elif file_path.suffix == '.parquet':
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
def save_table(data: pd.DataFrame, file_path: Union[str, Path]):
    """
    Save DataFrame to file
    
    Args:
        data: DataFrame to save
        file_path: Path to save the file
    """
    file_path = Path(file_path)
    if file_path.suffix == '.xlsx':
        data.to_excel(file_path, index=False)
    elif file_path.suffix == '.csv':
        data.to_csv(file_path, index=False)
    elif file_path.suffix == '.tsv':
        data.to_csv(file_path, sep='\t', index=False)
    elif file_path.suffix == '.parquet':
        data.to_parquet(file_path, index=False)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    print(f"Saved table to {file_path}")

def print_label_distribution(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze label distribution
    
    Returns:
        Dictionary containing label distribution information
    """
        
    if 'label' not in data.columns:
        raise ValueError("Labels column not found in data")
    
    # Calculate label distribution
    label_counts = data['label'].value_counts()
    label_percentages = data['label'].value_counts(normalize=True) * 100
    
    # Calculate total samples and positive-negative ratio
    total_samples = len(data)

    res_dict = {
        'total_samples': total_samples,
        'label_counts': label_counts.to_dict(),
        'label_percentages': label_percentages.to_dict(),
    }
    print(f"\nLabel distribution: {res_dict}")
    
    return res_dict

def filter_distance(data: pd.DataFrame, distance_threshold: Tuple[int, int]) -> pd.DataFrame:
    """
    Filter data based on distance threshold
    
    Args:
        data: Input DataFrame
        distance_threshold: Tuple containing lower and upper bounds for distance
        
    Returns:
        Filtered DataFrame
    """
    if 'distance' not in data.columns:  
        raise ValueError("Distance column not found in data")
    
    lower, upper = distance_threshold
    print(f"\nBefore filtering distance, the shape of the dataframe is {data.shape}")
    
    res = data[data['distance'].between(lower, upper)]
    print(f"After filtering distance, the shape of the dataframe is {res.shape}")

    return res


__all__ = ['download_data', 
           'load_table',
           'save_table',
           'print_label_distribution',
           'filter_distance']

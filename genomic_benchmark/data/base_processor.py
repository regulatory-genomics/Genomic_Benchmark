"""
Base dataset class that integrates data download and preprocessing functionality
"""
import os
import pandas as pd
from pathlib import Path
from typing import Optional, Union, Dict, Any
from .download import DataDownloader
from .data_config.config_manager import get_dataset_config

class BaseProcessor:
    """Base dataset class"""
    
    def __init__(
        self,
        task_name: str,
        dataset_name: str,
        cache_root: Optional[Union[str, Path]] = None
    ):
        """
        Initialize dataset
        
        Args:
            task_name: Name of the task
            dataset_name: Name of the dataset
            cache_root: Cache root directory. If None, will try to read from environment variable 
                       GENOMIC_BENCHMARK_CACHE_ROOT, otherwise defaults to ~/.cache/genomics_benchmark
        """
        self.task_name = task_name
        self.dataset_name = dataset_name
        
        # Set cache root directory
        if cache_root is None:
            # Try to read from environment variable
            cache_root = os.getenv('GENOMIC_BENCHMARK_CACHE_ROOT')
            if cache_root is None:
                # Default to user's home directory
                cache_root = os.path.expanduser("~/.cache/genomics_benchmark")
        self.cache_root = Path(cache_root)
        print(f"Cache root: {cache_root}")
        
        # Create task and dataset specific cache directories
        self.cache_dir = self.cache_root / task_name / dataset_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Get configuration
        self.config = get_dataset_config(task_name, dataset_name)
        self.task_config = self.config["task_config"]
        self.dataset_config = self.config["dataset_config"]
        
        # Initialize downloader and preprocessor
        self.downloader = DataDownloader(self.cache_dir)
        
        # Data file paths
        self.data = None
        self.data_path = None
        
    def download(self, force: bool = False) -> Path:
        """
        Download dataset
        
        Args:
            force: Whether to force re-download
            
        Returns:
            Path to the downloaded file
        """
        # Get file format from config if available
        file_format = self.dataset_config.get("file_format")
        
        self.data_path = self.downloader.download(
            self.dataset_config["data_url"],
            force=force,
            file_name=self.dataset_name,
            file_format=file_format
        )

        return self.data_path
    
    def load_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
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
        
    def process(self, data_path: Optional[Union[str, Path]] = None, output_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
        """
        Process data with standard pipeline
        
        Args:
            data_path: Path to input data file, if None, use self.data_path
            output_path: Path to save processed data
            
        Returns:
            Processed DataFrame
        """
        if data_path is None:
            data_path = self.data_path
            
        if data_path is None:
            raise ValueError("No data path provided")
            
        # Load data
        self.data = self.load_file(data_path)
        
        # Apply standard processing pipeline
        self.data = self.column_mapping(self.data)
        self.data = self.filter_output_columns(self.data)
        
        # Save processed data if output path is provided
        if output_dir is None:
            output_dir = self.cache_dir
        self.save_processed_data(output_dir)
            
        print(f"Processed data shape: {self.data.shape}")
        print(f"Processed data columns: {self.data.columns.tolist()}")
        
        return self.data
        
    def column_mapping(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with standardized column names
        """
        df = df.copy()
        column_mapping = self.dataset_config["column_mapping"]
        reverse_mapping = {v: k for k, v in column_mapping.items()}
        df.rename(columns=reverse_mapping, inplace=True)
        return df
    
    def filter_output_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter output columns
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with filtered columns
        """
        df = df.copy()
        output_columns = self.task_config["output_columns"].copy()
        
        # Check if all required output columns exist
        missing_columns = [col for col in output_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Select only the output columns
        return df[output_columns]
    
    def print_label_distribution(self) -> Dict[str, Any]:
        """
        Analyze label distribution
        
        Returns:
            Dictionary containing label distribution information
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        if 'label' not in self.data.columns:
            raise ValueError("Labels column not found in data")
        
        # Calculate label distribution
        label_counts = self.data['label'].value_counts()
        label_percentages = self.data['label'].value_counts(normalize=True) * 100
        
        # Calculate total samples and positive-negative ratio
        total_samples = len(self.data)
        pos_neg_ratio = label_counts[1] / label_counts[0] if 0 in label_counts and 1 in label_counts else 0
        
        return {
            'total_samples': total_samples,
            'label_counts': label_counts.to_dict(),
            'label_percentages': label_percentages.to_dict(),
            'positive_negative_ratio': pos_neg_ratio
        }
        
    def save_processed_data(self, output_dir: Union[str, Path], file_name: Optional[str] = None):
        """
        Save processed data
        
        Args:
            output_dir: Directory to save the data
        """
        if self.data is None:
            raise ValueError("No data loaded")

        if file_name is None:
            file_name = f"{self.dataset_name}.tsv"
        else:
            file_name = f"{file_name}.tsv"

        output_dir = Path(f"{output_dir}/{self.task_name}/{self.dataset_name}")
        output_dir.mkdir(parents=True, exist_ok=True)

        self.data.to_csv(f"{output_dir}/{file_name}", sep='\t', index=False)

    def clear_cache(self, clear_all: bool = False):
        """
        Clear cache
        
        Args:
            clear_all: Whether to clear cache for all tasks, defaults to clearing only current dataset cache
        """
        if clear_all:
            # Clear all cache
            if self.cache_root.exists():
                for path in self.cache_root.glob("**/*"):
                    if path.is_file():
                        path.unlink()
                for path in reversed(list(self.cache_root.glob("**/*"))):
                    if path.is_dir():
                        path.rmdir()
        else:
            # Clear only current dataset cache
            if self.cache_dir.exists():
                for file in self.cache_dir.glob("*"):
                    file.unlink()
                self.cache_dir.rmdir()
        
        self.data_path = None
        self.data = None
    
    @property
    def cache_path(self) -> Path:
        """Get cache directory for current dataset"""
        return self.cache_dir 
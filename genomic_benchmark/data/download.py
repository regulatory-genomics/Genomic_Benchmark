"""
Data download module providing basic data download and caching functionality
"""
import os
import hashlib
import requests
from pathlib import Path
from tqdm import tqdm
from typing import Optional, Union

class DataDownloader:
    """Base data downloader class"""
    
    def __init__(self, cache_dir: Optional[Union[str, Path]] = None):
        """
        Initialize data downloader
        
        Args:
            cache_dir: Data cache directory
        """
        if cache_dir is None:
            # Try to read from environment variable
            cache_dir = os.getenv('GENOMIC_BENCHMARK_CACHE_ROOT')
            if cache_dir is None:
                # Default to user's home directory
                cache_dir = os.path.expanduser("~/.cache/genomics_benchmark")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, url: str, file_name: Optional[str] = None, file_format: Optional[str] = None) -> Path:
        """
        Generate cache file path from URL
        
        Args:
            url: URL of the data file
            file_format: File format (e.g., 'tsv', 'csv', 'xlsx')
            
        Returns:
            Cache file path
        """
        # Extract filename from URL
        filename = file_name if file_name else url.split('/')[-1]
        # If no filename in URL or filename contains query parameters, use MD5 of URL as filename
        if not filename or '?' in filename:
            filename = hashlib.md5(url.encode()).hexdigest()
        
        # Add file format extension if provided
        if file_format:
            # Remove any existing extension
            filename = os.path.splitext(filename)[0]
            # Add the correct extension
            filename = f"{filename}.{file_format}"
            
        return self.cache_dir / filename
    
    def _download_from_osf(self, url: str, cache_path: Path) -> Path:
        """
        Download file from OSF
        
        Args:
            url: OSF file URL
            cache_path: Cache file path
            
        Returns:
            Downloaded file path
        """
        print(f"\nDownloading from OSF: {url}")
        print(f"Saving to: {cache_path}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            
            with open(cache_path, 'wb') as f, tqdm(
                desc="Download progress",
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for data in response.iter_content(block_size):
                    size = f.write(data)
                    pbar.update(size)
            
            return cache_path
            
        except requests.exceptions.RequestException as e:
            print(f"Download failed: {e}")
            raise
    
    def download(self, url: str, force: bool = False, file_name: Optional[str] = None, file_format: Optional[str] = None) -> Path:
        """
        Download data file
        
        Args:
            url: URL of the data file
            force: Whether to force re-download
            file_format: File format (e.g., 'tsv', 'csv', 'xlsx')
            
        Returns:
            Path to the downloaded file
        """
        cache_path = self._get_cache_path(url, file_name, file_format)
        
        if not force and cache_path.exists():
            print(f"Using cached file: {cache_path}\n")
            return cache_path
        
        # Choose download method based on URL type
        if 'osf.io' in url:
            return self._download_from_osf(url, cache_path)
        else:
            print(f"Downloading file: {url}")
            print(f"Saving to: {cache_path}")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            
            with open(cache_path, 'wb') as f, tqdm(
                desc="Download progress",
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for data in response.iter_content(block_size):
                    size = f.write(data)
                    pbar.update(size)
            
            return cache_path
    
    def clear_cache(self):
        """Clear all cached files"""
        for file in self.cache_dir.glob("*"):
            file.unlink()
        print(f"Cache directory cleared: {self.cache_dir}")

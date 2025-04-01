"""
Configuration management module for genomic data processing
"""
from typing import Dict, Any, Optional
from .enhancer_config import ENHANCER_CONFIG
from .genome_config import GENOME_CONFIG
from .eqtl_config import EQTL_CONFIG
# 所有配置的映射
CONFIG_MAP = {
    "enhancer": ENHANCER_CONFIG,
    "eqtl": EQTL_CONFIG,
    "genome": GENOME_CONFIG,
}

def get_dataset_config(task_name: str, dataset_name: str) -> Dict[str, Any]:
    """
    Get dataset configuration by task and dataset name
    
    Args:
        task_name: Name of the task (e.g., 'enhancer', 'genome')
        dataset_name: Name of the dataset
        
    Returns:
        Dataset configuration dictionary
        
    Raises:
        ValueError: If task or dataset is not found
    """
    if task_name not in CONFIG_MAP:
        raise ValueError(f"Task '{task_name}' not found. Available tasks: {list(CONFIG_MAP.keys())}")
    
    config = CONFIG_MAP[task_name]
    if dataset_name not in config:
        raise ValueError(f"Dataset '{dataset_name}' not found in task '{task_name}'. Available datasets: {list(config.keys())}")
    
    config = {
        "task_config": config["task_config"],
        "dataset_config": config[dataset_name]
    }
    
    return config

def list_tasks() -> list:
    """List all available tasks"""
    return list(CONFIG_MAP.keys())

def list_datasets(task_name: str) -> list:
    """
    List all available datasets for a specific task
    
    Args:
        task_name: Name of the task
        
    Returns:
        List of dataset names
        
    Raises:
        ValueError: If task is not found
    """
    if task_name not in CONFIG_MAP:
        raise ValueError(f"Task '{task_name}' not found. Available tasks: {list(CONFIG_MAP.keys())}")
    return list(CONFIG_MAP[task_name].keys())

__all__ = ['get_dataset_config', 'list_tasks', 'list_datasets']
"""
Logging configuration and utilities for the Asana seed data generator.
"""
import logging
import os
from pathlib import Path
from src.utils.config import get_config


def setup_logging():
    """
    Configure logging based on config.ini settings.
    Sets up console and optionally file logging.
    """
    config = get_config()
    
    # Get log level from config
    log_level_str = config.get('logging', 'log_level', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler with custom format
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler if enabled
    if config.getboolean('logging', 'log_to_file', False):
        log_file = config.get('logging', 'log_file_path', 'logs/generator.log')
        
        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the logger (typically __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

"""
Logging configuration module.
Sets up structured logging to both console and file with proper formatting.
"""

import logging
import os
from pathlib import Path
from core.config import settings


def setup_logging() -> logging.Logger:
    """
    Configure and return the application logger.
    
    Sets up:
    - Console handler with INFO level
    - File handler with all logs
    - Structured format: timestamp | level | module | message
    - Auto-creates logs directory if it doesn't exist
    
    Returns:
        logging.Logger: Configured logger instance
    """
    try:
        # Create logs directory if it doesn't exist
        log_dir = Path(settings.LOG_FILE_PATH).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger("domain_config_backend")
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        
        # Prevent duplicate handlers if logger already configured
        if logger.handlers:
            return logger
        
        # Create formatters
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(settings.LOG_FILE_PATH, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info("Logging system initialized successfully")
        return logger
        
    except Exception as e:
        # Fallback to basic logging if setup fails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-8s | %(message)s'
        )
        logging.error(f"Failed to setup logging: {str(e)}")
        return logging.getLogger("domain_config_backend")


# Global logger instance
logger = setup_logging()

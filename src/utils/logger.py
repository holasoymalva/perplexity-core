"""
Logging utilities for the Perplexity client
"""
import os
import logging
from typing import Optional

# Default log levels based on environment
DEFAULT_LOG_LEVELS = {
    'development': logging.DEBUG,
    'test': logging.INFO,
    'production': logging.WARNING
}

def get_logger(name: str, log_level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name of the logger (usually __name__)
        log_level: Log level. If not provided, will be determined from environment.
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, assume it's already configured
    if logger.handlers:
        return logger
        
    # Determine log level
    if log_level is None:
        env = os.environ.get('PERPLEXITY_ENV', 'development').lower()
        log_level = DEFAULT_LOG_LEVELS.get(env, logging.INFO)
        
        # Allow overriding via environment variable
        log_level_str = os.environ.get('PERPLEXITY_LOG_LEVEL')
        if log_level_str:
            try:
                level_mapping = {
                    'debug': logging.DEBUG,
                    'info': logging.INFO,
                    'warning': logging.WARNING,
                    'error': logging.ERROR,
                    'critical': logging.CRITICAL
                }
                log_level = level_mapping.get(log_level_str.lower(), log_level)
            except (ValueError, AttributeError):
                pass
    
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger
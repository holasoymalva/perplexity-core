"""
Configuration utilities for the Perplexity client
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """
    Configuration manager for the Perplexity client.
    Handles loading configuration from environment variables, config files, etc.
    """
    
    DEFAULT_CONFIG_PATHS = [
        # Current directory
        './perplexity_config.json',
        # User's home directory
        str(Path.home() / '.perplexity' / 'config.json'),
        # Environment variable pointing to config
        os.environ.get('PERPLEXITY_CONFIG_PATH', '')
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration.
        
        Args:
            config_path: Path to a JSON configuration file. If not provided,
                         default locations will be checked.
        """
        self.config_data: Dict[str, Any] = {}
        
        # Try to load from the provided path first
        if config_path and self._load_from_file(config_path):
            return
            
        # Try default locations
        for path in self.DEFAULT_CONFIG_PATHS:
            if path and self._load_from_file(path):
                return
    
    def _load_from_file(self, path: str) -> bool:
        """
        Load configuration from a JSON file.
        
        Args:
            path: Path to the configuration file
            
        Returns:
            True if the file was loaded successfully, False otherwise
        """
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self.config_data = json.load(f)
                return True
        except Exception:
            pass
        return False
    
    def get_api_key(self) -> Optional[str]:
        """
        Get the Perplexity API key from configuration or environment variables.
        
        Returns:
            API key if found, None otherwise
        """
        # Try to get from environment variable first
        api_key = os.environ.get('PERPLEXITY_API_KEY')
        if api_key:
            return api_key
            
        # Try to get from loaded config
        return self.config_data.get('api_key')
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value to return if the key is not found
            
        Returns:
            Configuration value if found, default otherwise
        """
        # Try environment variable first (with PERPLEXITY_ prefix)
        env_var = f"PERPLEXITY_{key.upper()}"
        if env_var in os.environ:
            return os.environ[env_var]
            
        # Then try loaded config
        return self.config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config_data[key] = value
    
    def save(self, path: Optional[str] = None) -> bool:
        """
        Save the configuration to a file.
        
        Args:
            path: Path to save the configuration to. If not provided,
                  will try to save to the first default path.
                  
        Returns:
            True if the file was saved successfully, False otherwise
        """
        save_path = path or self.DEFAULT_CONFIG_PATHS[0]
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w') as f:
                json.dump(self.config_data, f, indent=2)
            return True
        except Exception:
            return False
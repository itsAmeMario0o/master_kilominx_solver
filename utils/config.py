"""
Configuration settings for the Master Kilominx Solver application.
"""

import os
import json
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    # UI settings
    "ui": {
        "theme": "light",  # 'light' or 'dark'
        "window_width": 900,
        "window_height": 700,
        "font_size": 12
    },
    
    # Color settings
    "colors": {
        "standard_colors": {
            "White": [255, 255, 255],
            "Yellow": [255, 255, 0],
            "Red": [255, 0, 0],
            "Orange": [255, 165, 0],
            "Green": [0, 128, 0],
            "Blue": [0, 0, 255],
            "Purple": [128, 0, 128],
            "Pink": [255, 192, 203],
            "Light Blue": [173, 216, 230],
            "Light Green": [144, 238, 144],
            "Brown": [165, 42, 42],
            "Gray": [128, 128, 128]
        },
        "color_tolerance": 30  # RGB distance tolerance for color matching
    },
    
    # Solver settings
    "solver": {
        "timeout_seconds": 60,  # Maximum time to spend solving
        "max_moves": 200,       # Maximum moves in a solution
        "simplify_solution": True  # Whether to simplify/optimize the solution
    },
    
    # Image processing settings
    "image_processing": {
        "detect_method": "contours",  # 'contours', 'hough', or 'grid'
        "min_face_size": 50,          # Minimum size of a face in pixels
        "adaptive_threshold": True,   # Use adaptive thresholding
        "blur_kernel_size": 5         # Blur kernel size for preprocessing
    }
}

class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_file=None):
        """
        Initialize the configuration.
        
        Args:
            config_file (str, optional): Path to a configuration file.
        """
        self.config = DEFAULT_CONFIG.copy()
        
        # Load configuration file if provided
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
            
        # Initialize paths
        self._init_paths()
        
    def _init_paths(self):
        """Initialize application paths."""
        # Define paths relative to user's home directory
        home_dir = str(Path.home())
        app_dir = os.path.join(home_dir, ".kilominx_solver")
        
        # Create directories if they don't exist
        os.makedirs(app_dir, exist_ok=True)
        
        # Define paths for various application data
        self.paths = {
            "app_dir": app_dir,
            "config_file": os.path.join(app_dir, "config.json"),
            "saved_states": os.path.join(app_dir, "saved_states"),
            "logs": os.path.join(app_dir, "logs")
        }
        
        # Create subdirectories
        for path in self.paths.values():
            if isinstance(path, str) and not os.path.isfile(path):
                os.makedirs(path, exist_ok=True)
                
    def load_config(self, config_file):
        """
        Load configuration from a file.
        
        Args:
            config_file (str): Path to the configuration file.
        """
        try:
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                
            # Update configuration
            self._update_dict(self.config, loaded_config)
            
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            
    def save_config(self, config_file=None):
        """
        Save configuration to a file.
        
        Args:
            config_file (str, optional): Path to save the configuration.
                                        If not provided, uses the default path.
        """
        if config_file is None:
            config_file = self.paths["config_file"]
            
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
                
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
            
    def _update_dict(self, target, source):
        """
        Recursively update a dictionary with values from another dictionary.
        
        Args:
            target (dict): Dictionary to update.
            source (dict): Dictionary with new values.
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_dict(target[key], value)
            else:
                target[key] = value
                
    def get(self, section, key=None, default=None):
        """
        Get a configuration value.
        
        Args:
            section (str): Configuration section.
            key (str, optional): Configuration key within the section.
            default: Default value to return if the key is not found.
            
        Returns:
            The configuration value, or default if not found.
        """
        if section not in self.config:
            return default
            
        if key is None:
            return self.config[section]
            
        return self.config[section].get(key, default)
        
    def set(self, section, key, value):
        """
        Set a configuration value.
        
        Args:
            section (str): Configuration section.
            key (str): Configuration key within the section.
            value: Value to set.
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
        
    def get_color(self, color_name):
        """
        Get an RGB color by name.
        
        Args:
            color_name (str): Name of the color.
            
        Returns:
            list: RGB color values, or None if not found.
        """
        colors = self.get("colors", "standard_colors", {})
        return colors.get(color_name)

# Global configuration instance
config = Config()
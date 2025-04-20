"""
Utilities for handling colors in the Master Kilominx solver.
"""

import math
import numpy as np

def rgb_to_hex(rgb):
    """
    Convert an RGB color to hex format.
    
    Args:
        rgb (list/tuple): RGB color values [r, g, b].
        
    Returns:
        str: Hex color string (e.g., "#FF0000" for red).
    """
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    """
    Convert a hex color to RGB format.
    
    Args:
        hex_color (str): Hex color string (e.g., "#FF0000").
        
    Returns:
        list: RGB color values [r, g, b].
    """
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

def color_distance(color1, color2):
    """
    Calculate the Euclidean distance between two colors in RGB space.
    
    Args:
        color1, color2: RGB color values.
        
    Returns:
        float: Distance between the colors.
    """
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

def find_nearest_standard_color(color, standard_colors):
    """
    Find the nearest standard color to a given color.
    
    Args:
        color: RGB color to match.
        standard_colors (dict): Dictionary mapping color names to RGB values.
        
    Returns:
        tuple: (color_name, rgb_value) of the nearest standard color.
    """
    min_distance = float('inf')
    nearest_color = None
    
    for name, rgb in standard_colors.items():
        dist = color_distance(color, rgb)
        if dist < min_distance:
            min_distance = dist
            nearest_color = (name, rgb)
            
    return nearest_color

def cluster_colors(colors, num_clusters=12):
    """
    Cluster a list of colors into a specified number of groups.
    
    Args:
        colors (list): List of RGB colors.
        num_clusters (int): Number of color clusters to create.
        
    Returns:
        list: Representative colors for each cluster.
    """
    from sklearn.cluster import KMeans
    
    # Convert to numpy array
    colors_array = np.array(colors)
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(colors_array)
    
    # Get cluster centers
    cluster_centers = kmeans.cluster_centers_
    
    # Convert to integer RGB values
    representative_colors = [[int(c) for c in center] for center in cluster_centers]
    
    return representative_colors

def get_color_name(rgb):
    """
    Get an approximate color name for an RGB value.
    
    Args:
        rgb (list): RGB color value.
        
    Returns:
        str: Approximate color name.
    """
    # Define standard colors with names
    standard_colors = {
        "Red": [255, 0, 0],
        "Green": [0, 255, 0],
        "Blue": [0, 0, 255],
        "Yellow": [255, 255, 0],
        "Cyan": [0, 255, 255],
        "Magenta": [255, 0, 255],
        "White": [255, 255, 255],
        "Black": [0, 0, 0],
        "Gray": [128, 128, 128],
        "Orange": [255, 165, 0],
        "Purple": [128, 0, 128],
        "Brown": [165, 42, 42]
    }
    
    # Find the nearest standard color
    name, _ = find_nearest_standard_color(rgb, standard_colors)
    return name

def normalize_colors(colors):
    """
    Normalize color values to account for lighting variations.
    
    Args:
        colors (list): List of RGB colors.
        
    Returns:
        list: Normalized colors.
    """
    # Convert to numpy array
    colors_array = np.array(colors)
    
    # Calculate mean and standard deviation
    mean = np.mean(colors_array, axis=0)
    std = np.std(colors_array, axis=0)
    
    # Normalize (z-score normalization)
    normalized = (colors_array - mean) / (std + 1e-8)  # Add small epsilon to avoid division by zero
    
    # Scale back to 0-255 range
    normalized = (normalized * 64) + 128
    
    # Clip to valid range and convert to integers
    normalized = np.clip(normalized, 0, 255)
    normalized = normalized.astype(int)
    
    return normalized.tolist()
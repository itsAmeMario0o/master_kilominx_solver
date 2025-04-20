"""
Image processing utilities for extracting colors from Kilominx images.
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
import math

def extract_colors_from_image(image_path, progress_callback=None):
    """
    Process an image of a Master Kilominx to extract face colors.
    
    Args:
        image_path (str): Path to the image file.
        progress_callback (function): Optional callback for reporting progress.
        
    Returns:
        dict: Dictionary mapping face indices to lists of colors.
    """
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image from {image_path}")
            
        # Convert to RGB (OpenCV loads as BGR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Report progress
        if progress_callback:
            progress_callback(10)
            
        # Step 1: Detect the pentagon shapes (faces)
        faces_regions = detect_faces(image_rgb)
        
        if progress_callback:
            progress_callback(30)
            
        # Step 2: Extract grid regions within each face
        all_face_colors = {}
        
        for face_idx, face_region in enumerate(faces_regions):
            # Extract a 4x4 grid of colors from this face
            grid_colors = extract_grid_colors(image_rgb, face_region)
            all_face_colors[f"face_{face_idx}"] = grid_colors
            
            # Report progress
            if progress_callback:
                # Distribute progress between 30% and 90%
                progress = 30 + (face_idx + 1) * 60 // len(faces_regions)
                progress_callback(progress)
                
        # Step 3: Standardize colors across faces
        standardized_colors = standardize_colors(all_face_colors)
        
        if progress_callback:
            progress_callback(100)
            
        return standardized_colors
        
    except Exception as e:
        # Log the error and re-raise
        print(f"Error processing image: {str(e)}")
        raise
        
def detect_faces(image):
    """
    Detect the pentagon faces in the Kilominx image.
    
    This is a placeholder for a more sophisticated detection algorithm.
    In a real implementation, this would use computer vision techniques
    to find the pentagonal faces of the Kilominx.
    
    Args:
        image: RGB image of the Kilominx.
        
    Returns:
        list: List of face regions (each defined by a bounding box or contour).
    """
    # This is a simplified placeholder implementation
    # In a real app, this would use contour detection, shape analysis, etc.
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    # For this demo, we'll create 12 synthetic face regions
    # In a real implementation, these would be detected from the image
    
    # Create a grid layout as a placeholder
    rows, cols = 3, 4
    face_width = width // cols
    face_height = height // rows
    
    face_regions = []
    
    for row in range(rows):
        for col in range(cols):
            # Define a rectangular region for this face
            x1 = col * face_width
            y1 = row * face_height
            x2 = (col + 1) * face_width
            y2 = (row + 1) * face_height
            
            face_regions.append((x1, y1, x2, y2))
            
    return face_regions
    
def extract_grid_colors(image, face_region):
    """
    Extract a 4x4 grid of colors from a face region.
    
    Args:
        image: RGB image.
        face_region: Region defining the face (x1, y1, x2, y2).
        
    Returns:
        list: List of RGB colors for the 4x4 grid.
    """
    x1, y1, x2, y2 = face_region
    
    # Extract the face sub-image
    face_image = image[y1:y2, x1:x2]
    
    # Get dimensions
    height, width = face_image.shape[:2]
    
    # Define a 4x4 grid
    grid_height = height // 4
    grid_width = width // 4
    
    grid_colors = []
    
    for row in range(4):
        for col in range(4):
            # Calculate grid cell boundaries
            gx1 = col * grid_width
            gy1 = row * grid_height
            gx2 = (col + 1) * grid_width
            gy2 = (row + 1) * grid_height
            
            # Extract grid cell sub-image
            cell_image = face_image[gy1:gy2, gx1:gx2]
            
            # Get the dominant color in this cell
            color = get_dominant_color(cell_image)
            grid_colors.append(color)
            
    return grid_colors
    
def get_dominant_color(image):
    """
    Get the dominant color in an image region.
    
    Args:
        image: RGB image region.
        
    Returns:
        list: RGB color (e.g., [255, 0, 0] for red).
    """
    # Reshape the image to be a list of pixels
    pixels = image.reshape(-1, 3)
    
    # Cluster the pixel colors
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(pixels)
    
    # Get the dominant color
    dominant_color = kmeans.cluster_centers_[0]
    
    # Convert to integer RGB
    return [int(c) for c in dominant_color]
    
def standardize_colors(face_colors):
    """
    Standardize colors across all faces to account for lighting variations.
    
    Args:
        face_colors (dict): Dictionary mapping face indices to lists of colors.
        
    Returns:
        dict: Dictionary with standardized colors.
    """
    # Collect all colors
    all_colors = []
    for colors in face_colors.values():
        all_colors.extend(colors)
        
    # Use K-means to find 12 color clusters (one for each face)
    kmeans = KMeans(n_clusters=12)
    kmeans.fit(all_colors)
    cluster_centers = kmeans.cluster_centers_
    
    # Function to find closest cluster center
    def closest_center(color):
        distances = [math.sqrt(sum((c - color_value)**2 for c, color_value in zip(center, color))) 
                    for center in cluster_centers]
        return np.argmin(distances)
    
    # Map each color to its closest cluster center
    standardized = {}
    for face_idx, colors in face_colors.items():
        standardized_colors = []
        for color in colors:
            center_idx = closest_center(color)
            std_color = [int(c) for c in cluster_centers[center_idx]]
            standardized_colors.append(std_color)
        standardized[face_idx] = standardized_colors
        
    return standardized
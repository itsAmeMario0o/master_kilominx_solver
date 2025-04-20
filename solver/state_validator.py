"""
Validation logic for Master Kilominx cube states.
Updated to match the accurate sticker layout.
"""

from collections import Counter
from solver.kilominx_model import MasterKilominx

def validate_kilominx_state(state):
    """
    Validate if a Master Kilominx state is valid and solvable.
    
    Args:
        state (dict): The state to validate, mapping face indices to sticker color lists.
        
    Returns:
        tuple: (is_valid, message) where is_valid is a boolean and message explains any issues.
    """
    # 1. Check if we have the right number of faces
    if len(state) != 12:
        return False, f"Invalid number of faces: {len(state)}. Expected 12 faces."
    
    # 2. Check if each face has exactly 16 stickers
    # The actual layout has: 1 center + 5 corners + 5 edges + 5 trapezoids = 16 stickers
    for face_idx, stickers in state.items():
        if len(stickers) != 16:
            return False, f"Face {face_idx} has {len(stickers)} stickers. Expected 16 stickers."
    
    # 3. Count the number of stickers of each color
    all_stickers = []
    for stickers in state.values():
        all_stickers.extend(stickers)
    
    # Group stickers by color
    color_counter = {}
    
    # Handle different color representations
    for sticker in all_stickers:
        # Convert the color to a hashable representation
        if isinstance(sticker, (list, tuple)):
            # For RGB values, convert to tuple for hashing
            color_key = tuple(sticker)
        else:
            color_key = sticker
            
        color_counter[color_key] = color_counter.get(color_key, 0) + 1
    
    # Check if we have the correct number of unique colors
    if len(color_counter) != 12:
        return False, f"Found {len(color_counter)} colors. Expected 12 colors."
    
    # Check if each color appears exactly 16 times
    for color, count in color_counter.items():
        if count != 16:
            color_str = str(color)
            return False, f"Color {color_str} appears {count} times. Expected 16 occurrences."
    
    # 4. Check center piece validity
    # The first sticker of each face should represent the center color
    for face_idx, stickers in state.items():
        if not stickers:
            return False, f"Face {face_idx} has no stickers."
    
    # If all checks pass, the state is valid
    return True, "The cube state is valid."

def check_color_distribution(state):
    """
    Check if the color distribution in the state is valid.
    
    Args:
        state (dict): The state to validate.
        
    Returns:
        tuple: (is_valid, message)
    """
    # Flatten all stickers
    all_stickers = []
    for stickers in state.values():
        all_stickers.extend(stickers)
    
    # Count occurrences of each color
    # Convert non-hashable types (like lists) to tuples
    hashable_stickers = []
    for sticker in all_stickers:
        if isinstance(sticker, list):
            hashable_stickers.append(tuple(sticker))
        else:
            hashable_stickers.append(sticker)
    
    color_counts = Counter(hashable_stickers)
    
    # A Master Kilominx should have 12 colors with 16 stickers each
    expected_count = 16
    
    # Check if each color appears the expected number of times
    for color, count in color_counts.items():
        if count != expected_count:
            return False, f"Color {str(color)} appears {count} times (expected {expected_count})"
    
    return True, "Color distribution is valid"
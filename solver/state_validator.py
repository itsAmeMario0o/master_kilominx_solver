"""
Validation logic for Master Kilominx cube states.
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
    
    # 2. Check if each face has the correct number of stickers (16 for a 4x4 grid)
    for face_idx, stickers in state.items():
        if len(stickers) != 16:
            return False, f"Face {face_idx} has {len(stickers)} stickers. Expected 16 stickers."
    
    # 3. Count the number of stickers of each color
    # For a Master Kilominx, there should be exactly 16 stickers of each color
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
    
    # 4. Check for parity issues
    # This is a complex check that depends on the specific puzzle constraints
    # For a real implementation, we would check things like:
    # - Corner parity (whether the corners can be solved)
    # - Edge parity (whether the edges can be solved)
    # - Center orientation (for the 4x4 puzzle)
    
    # A full parity check would require understanding the current permutation
    # relative to a solved state, which is quite complex for a Master Kilominx
    
    # 5. Check center pieces (simplified)
    # For a 4x4 puzzle, the center 2x2 pieces on each face should align
    # This is a simplified check; a real validator would be more sophisticated
    for face_idx, stickers in state.items():
        # Check if the center pieces are consistent
        # For a 4x4 grid, center pieces are at indices 5, 6, 9, 10
        center_indices = [5, 6, 9, 10]
        center_colors = [stickers[i] for i in center_indices]
        
        # Convert to hashable representation
        center_colors_hash = []
        for color in center_colors:
            if isinstance(color, (list, tuple)):
                center_colors_hash.append(tuple(color))
            else:
                center_colors_hash.append(color)
        
        # Check if all center pieces are the same color
        if len(set(center_colors_hash)) > 1:
            return False, f"Center pieces on face {face_idx} have inconsistent colors."
    
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

def is_solvable(state):
    """
    Check if the cube state is solvable.
    
    This is a complex check that would involve:
    1. Checking parity constraints
    2. Verifying that the state can be reached from a solved state
    
    Args:
        state (dict): The state to check.
        
    Returns:
        tuple: (is_solvable, message)
    """
    # This is a placeholder for a more sophisticated implementation
    # A real solvability check would require advanced algorithms
    
    # For now, we'll just check if the color distribution is valid
    is_valid, message = check_color_distribution(state)
    if not is_valid:
        return False, message
    
    # In a real implementation, we would check additional constraints
    # such as corner parity, edge parity, etc.
    
    return True, "The cube state appears to be solvable"
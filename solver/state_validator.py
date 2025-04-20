"""
Validation logic for Master Kilominx cube states with 20 stickers per face.
"""

from collections import Counter
from solver.kilominx_model import MasterKilominx, StickerType

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
    
    # 2. Check if each face has exactly 20 stickers
    for face_idx, stickers in state.items():
        if len(stickers) != 20:
            return False, f"Face {face_idx} has {len(stickers)} stickers. Expected 20 stickers."
    
    # 3. Count the number of stickers of each color
    # For a Master Kilominx, there should be exactly 20 stickers of each color
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
    
    # Check if each color appears exactly 20 times
    for color, count in color_counter.items():
        if count != 20:
            color_str = str(color)
            return False, f"Color {color_str} appears {count} times. Expected 20 occurrences."
    
    # 4. Check the super center piece
    # For a valid state, the super center (sticker index 19) should represent the face color
    for face_idx, stickers in state.items():
        super_center_color = stickers[19] if len(stickers) > 19 else None
        if super_center_color is None:
            return False, f"Face {face_idx} is missing its super center sticker."
    
    # 5. Validate center pieces structure
    # The 5 center pieces (indices 15-18) should be the same color as the super center
    for face_idx, stickers in state.items():
        super_center_color = tuple(stickers[19]) if isinstance(stickers[19], (list, tuple)) else stickers[19]
        
        for i in range(15, 19):
            center_color = tuple(stickers[i]) if isinstance(stickers[i], (list, tuple)) else stickers[i]
            if center_color != super_center_color:
                return False, f"Center piece mismatch on face {face_idx}. Center pieces should match the super center."
    
    # If all checks pass, the state is valid
    return True, "The cube state is valid."
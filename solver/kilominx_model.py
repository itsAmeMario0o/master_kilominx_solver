"""
Data model representing the Master Kilominx puzzle.
"""

import numpy as np
from enum import Enum
from typing import List, Dict, Tuple

class Face(Enum):
    """Enumeration of the 12 faces of a dodecahedron."""
    F = 0  # Front
    U = 1  # Up
    R = 2  # Right
    D = 3  # Down
    L = 4  # Left
    BR = 5  # Back-Right
    BL = 6  # Back-Left
    BU = 7  # Back-Up
    BD = 8  # Back-Down
    B = 9   # Back
    UL = 10  # Up-Left
    UR = 11  # Up-Right

class MasterKilominx:
    """
    Data structure representing a Master Kilominx (4x4 dodecahedral Rubik's cube).
    
    The Master Kilominx has 12 pentagonal faces, each with 16 stickers (4x4 grid).
    Each sticker is represented by a color value.
    """
    
    def __init__(self, state=None):
        """
        Initialize a Master Kilominx model.
        
        Args:
            state (dict, optional): Initial state of the puzzle with face indices as keys
                                  and lists of color values as values.
        """
        # Number of stickers per face
        self.stickers_per_face = 16  # 4x4 grid
        
        # Initialize with solved state if no state is provided
        if state is None:
            # Create a solved state with 12 faces
            self.state = {}
            for face in Face:
                # Create 16 stickers of the same color for each face
                self.state[face.value] = [face.value] * self.stickers_per_face
        else:
            # Convert input state to internal representation
            self.state = {}
            for face_idx, face_colors in state.items():
                if isinstance(face_idx, str) and face_idx.startswith("face_"):
                    face_num = int(face_idx.split("_")[1])
                    self.state[face_num] = face_colors
                else:
                    self.state[face_idx] = face_colors
        
        # Define the adjacency of faces
        # For each face, list the adjacent faces and the sticker indices that touch
        # This is crucial for applying moves correctly
        self._init_adjacency()
        
    def _init_adjacency(self):
        """
        Initialize the adjacency relationships between faces.
        
        For a dodecahedron, each face is adjacent to 5 other faces.
        This method defines which stickers are adjacent between faces.
        """
        # This is a simplified representation
        # In a real implementation, this would be a more detailed mapping
        # showing exactly which stickers on one face are adjacent to which
        # stickers on neighboring faces
        
        # Format: {face_idx: [(adjacent_face_idx, adjacent_stickers_mapping), ...]}
        self.adjacency = {
            # Front face adjacencies
            Face.F.value: [
                (Face.U.value, "bottom"),  # Front-Up connection
                (Face.R.value, "left"),    # Front-Right connection
                (Face.D.value, "top"),     # Front-Down connection
                (Face.L.value, "right"),   # Front-Left connection
                (Face.UR.value, "bottom-left")  # Front-UpRight connection
            ],
            
            # Additional adjacencies would be defined here for all 12 faces
            # This is a complex mapping for a dodecahedron
        }
        
    def get_face(self, face_idx):
        """
        Get the stickers for a specific face.
        
        Args:
            face_idx: The index of the face to retrieve.
            
        Returns:
            List of sticker colors for the face.
        """
        return self.state.get(face_idx, [])
    
    def get_sticker(self, face_idx, row, col):
        """
        Get a specific sticker from a face.
        
        Args:
            face_idx: The index of the face.
            row, col: The row and column of the sticker (0-3 for a 4x4 grid).
            
        Returns:
            The color value of the sticker.
        """
        if face_idx in self.state and 0 <= row < 4 and 0 <= col < 4:
            sticker_idx = row * 4 + col
            if sticker_idx < len(self.state[face_idx]):
                return self.state[face_idx][sticker_idx]
        return None
    
    def set_sticker(self, face_idx, row, col, color):
        """
        Set the color of a specific sticker.
        
        Args:
            face_idx: The index of the face.
            row, col: The row and column of the sticker (0-3 for a 4x4 grid).
            color: The color value to set.
        """
        if face_idx in self.state and 0 <= row < 4 and 0 <= col < 4:
            sticker_idx = row * 4 + col
            if sticker_idx < len(self.state[face_idx]):
                self.state[face_idx][sticker_idx] = color
                
    def is_solved(self):
        """
        Check if the puzzle is solved (all stickers on each face have the same color).
        
        Returns:
            bool: True if solved, False otherwise.
        """
        for face_idx, stickers in self.state.items():
            if not stickers:
                continue
                
            # Check if all stickers on this face have the same color
            first_color = stickers[0]
            for color in stickers[1:]:
                # Compare color values (might need a tolerance for RGB values)
                if self._colors_different(first_color, color):
                    return False
                    
        return True
    
    def _colors_different(self, color1, color2, tolerance=10):
        """
        Compare two colors with a tolerance for RGB values.
        
        Args:
            color1, color2: The colors to compare (RGB list or similar).
            tolerance: The maximum allowed difference per channel.
            
        Returns:
            bool: True if colors are different beyond tolerance, False otherwise.
        """
        # Handle different color formats
        if isinstance(color1, (int, float)) and isinstance(color2, (int, float)):
            # Simple numeric comparison
            return abs(color1 - color2) > tolerance
        
        # For RGB lists/tuples
        if isinstance(color1, (list, tuple)) and isinstance(color2, (list, tuple)):
            if len(color1) == len(color2):
                for c1, c2 in zip(color1, color2):
                    if abs(c1 - c2) > tolerance:
                        return True
                return False
                
        # Default comparison for other formats
        return color1 != color2
    
    def apply_move(self, move):
        """
        Apply a move to the puzzle.
        
        Args:
            move: The move to apply, in standard notation.
            
        Returns:
            A new MasterKilominx instance with the move applied.
        """
        # Parse the move notation
        face, direction = self._parse_move(move)
        
        # Create a copy of the current state
        new_state = {k: v.copy() for k, v in self.state.items()}
        
        # Apply the move to the copy
        new_state = self._rotate_face(new_state, face, direction)
        
        # Create and return a new instance
        return MasterKilominx(new_state)
    
    def _parse_move(self, move):
        """
        Parse a move in standard notation.
        
        Args:
            move: The move string (e.g., "F", "U'", "R2").
            
        Returns:
            tuple: (face_idx, rotation_count)
        """
        # Basic parsing (would be more sophisticated in a real implementation)
        if len(move) == 1:
            # Single clockwise rotation, e.g., "F"
            face_name = move
            direction = 1
        elif len(move) == 2:
            if move[1] == "'":
                # Counterclockwise rotation, e.g., "F'"
                face_name = move[0]
                direction = -1
            elif move[1] == "2":
                # Double rotation, e.g., "F2"
                face_name = move[0]
                direction = 2
            else:
                # Handle other notations
                face_name = move
                direction = 1
        else:
            # More complex notations would be handled here
            face_name = move[0]
            direction = 1
            
        # Convert face name to index
        try:
            face = Face[face_name].value
        except KeyError:
            # Default to front face if unknown
            face = Face.F.value
            
        return face, direction
    
    def _rotate_face(self, state, face_idx, direction):
        """
        Rotate a face and update adjacent stickers.
        
        Args:
            state: The current state to modify.
            face_idx: The face to rotate.
            direction: The rotation direction/count.
            
        Returns:
            The updated state dictionary.
        """
        # 1. Rotate the stickers on the face itself
        face_stickers = state[face_idx].copy()
        
        # For a 4x4 grid, create a 2D representation for easier rotation
        grid = []
        for row in range(4):
            grid_row = []
            for col in range(4):
                sticker_idx = row * 4 + col
                grid_row.append(face_stickers[sticker_idx])
            grid.append(grid_row)
            
        # Rotate the grid based on direction
        rotated_grid = self._rotate_grid(grid, direction)
        
        # Convert back to 1D list
        rotated_stickers = []
        for row in rotated_grid:
            rotated_stickers.extend(row)
            
        state[face_idx] = rotated_stickers
        
        # 2. Update adjacent face stickers
        # This would involve mapping the edges of the rotated face
        # to the corresponding edges of adjacent faces
        # This is complex for a dodecahedron and would be implemented
        # based on the adjacency mapping
        
        # The implementation would update the stickers on adjacent faces
        # that are affected by the rotation
        
        return state
    
    def _rotate_grid(self, grid, direction):
        """
        Rotate a 2D grid according to the specified direction.
        
        Args:
            grid: 2D list representing the face stickers.
            direction: Rotation direction (1=CW, -1=CCW, 2=180).
            
        Returns:
            The rotated 2D grid.
        """
        # Convert to numpy array for easier rotation
        array = np.array(grid)
        
        # Apply rotation
        if direction == 1:  # Clockwise
            rotated = np.rot90(array, k=3)  # k=3 is equivalent to k=-1
        elif direction == -1:  # Counter-clockwise
            rotated = np.rot90(array, k=1)
        elif direction == 2:  # 180 degrees
            rotated = np.rot90(array, k=2)
        else:
            rotated = array.copy()  # No rotation
            
        return rotated.tolist()
    
    def to_dict(self):
        """
        Convert the model to a dictionary representation.
        
        Returns:
            dict: A dictionary mapping face indices to sticker lists.
        """
        return {f"face_{k}": v for k, v in self.state.items()}
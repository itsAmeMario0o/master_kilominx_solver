"""
Data model representing the Master Kilominx puzzle with proper 20-sticker layout.
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

class StickerType(Enum):
    """Types of stickers on a Master Kilominx face."""
    CORNER = 0        # 5 corners (at pentagon vertices)
    EDGE = 1          # 5 edges (along pentagon edges)
    MIDDLE_EDGE = 2   # 5 middle edges (inner edges)
    CENTER_PIECE = 3  # 5 center pieces (around super center)
    SUPER_CENTER = 4  # 1 super center (middle of face)

class MasterKilominx:
    """
    Data structure representing a Master Kilominx (4x4 dodecahedral Rubik's cube).
    Each pentagonal face has 20 stickers arranged in a specific pattern.
    """
    
    def __init__(self, state=None):
        """
        Initialize a Master Kilominx model.
        
        Args:
            state (dict, optional): Initial state of the puzzle with face indices as keys
                                  and lists of color values as values.
        """
        # Number of stickers per face
        self.stickers_per_face = 20
        
        # Sticker distribution
        self.corners_per_face = 5
        self.edges_per_face = 5
        self.middle_edges_per_face = 5
        self.center_pieces_per_face = 5
        self.super_center_per_face = 1
        
        # Initialize with solved state if no state is provided
        if state is None:
            # Create a solved state with 12 faces
            self.state = {}
            for face in Face:
                # Create 20 stickers of the same color for each face
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
        
        # Initialize adjacency relationships
        self._init_adjacency()
        
    def _init_adjacency(self):
        """
        Initialize the adjacency relationships between faces.
        Maps which stickers on adjacent faces are affected by face rotations.
        """
        # Adjacency mapping for a dodecahedron
        # Each face is adjacent to 5 other faces
        self.adjacency = {
            Face.F.value: [
                (Face.U.value, [1, 2, 3]),  # Up face: corner 1, edge 1, corner 2
                (Face.R.value, [0, 5, 1]),  # Right face: corner 0, edge 0, corner 1
                (Face.D.value, [0, 7, 4]),  # Down face: corner 0, edge 2, corner 4
                (Face.L.value, [4, 9, 3]),  # Left face: corner 4, edge 4, corner 3
                (Face.BR.value, [2, 6, 3])  # Back-Right face: corner 2, edge 3, corner 3
            ],
            # Additional adjacencies would be defined here for all 12 faces
            # This is a simplified representation
        }
        
    def get_sticker(self, face_idx, sticker_type, type_index):
        """
        Get a specific sticker from a face.
        
        Args:
            face_idx: The index of the face.
            sticker_type: Type of sticker (CORNER, EDGE, etc.)
            type_index: Index within that sticker type (0-4 for most types)
            
        Returns:
            The color value of the sticker.
        """
        if face_idx not in self.state:
            return None
            
        # Calculate sticker index based on type and index
        if sticker_type == StickerType.CORNER:
            idx = type_index
        elif sticker_type == StickerType.EDGE:
            idx = 5 + type_index
        elif sticker_type == StickerType.MIDDLE_EDGE:
            idx = 10 + type_index
        elif sticker_type == StickerType.CENTER_PIECE:
            idx = 15 + type_index
        elif sticker_type == StickerType.SUPER_CENTER:
            idx = 19
        else:
            return None
            
        if 0 <= idx < len(self.state[face_idx]):
            return self.state[face_idx][idx]
        return None
        
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
        
        # Implement rotation logic based on direction
        # This would handle the complex mapping of sticker positions
        
        # 2. Update adjacent face stickers
        # This would handle the effects of rotation on neighboring faces
        
        return state
"""
Utilities for handling Kilominx move notation and translating between formats.
"""

class MoveNotation:
    """Utilities for Kilominx move notation."""
    
    # Standard face notation
    FACE_NAMES = {
        'F': 'Front',
        'U': 'Up',
        'R': 'Right',
        'D': 'Down',
        'L': 'Left',
        'BR': 'Back-Right',
        'BL': 'Back-Left',
        'BU': 'Back-Up',
        'BD': 'Back-Down',
        'B': 'Back',
        'UL': 'Up-Left',
        'UR': 'Up-Right'
    }
    
    # Move modifiers
    MODIFIERS = {
        '': 'clockwise',
        "'": 'counter-clockwise',
        "2": 'half-turn (180°)'
    }
    
    @staticmethod
    def to_human_readable(move):
        """
        Convert a move in standard notation to a human-readable description.
        
        Args:
            move (str): Move in standard notation (e.g., "F", "U'", "R2").
            
        Returns:
            str: Human-readable description of the move.
        """
        if not move:
            return "No move"
            
        # Check if it's a comment
        if move.startswith('#'):
            return move[1:].strip()
            
        # Parse the basic move
        face = move[0]
        if len(move) > 1 and face in MoveNotation.FACE_NAMES:
            # Check for a two-character face name (e.g., BR)
            if len(move) > 1 and face + move[1] in MoveNotation.FACE_NAMES:
                face = face + move[1]
                modifier = move[2:] if len(move) > 2 else ''
            else:
                modifier = move[1:] if len(move) > 1 else ''
        else:
            modifier = ''
            
        # Get the face name and direction
        face_name = MoveNotation.FACE_NAMES.get(face, f"Unknown face '{face}'")
        direction = MoveNotation.MODIFIERS.get(modifier, "unknown direction")
        
        return f"Turn the {face_name} face {direction}"
    
    @staticmethod
    def parse_algorithm(algorithm):
        """
        Parse an algorithm string into individual moves.
        
        Args:
            algorithm (str): Algorithm string (e.g., "F U R F' U'").
            
        Returns:
            list: List of individual moves.
        """
        if not algorithm:
            return []
            
        # Split by spaces but preserve comments
        parts = []
        current_part = ""
        in_comment = False
        
        for char in algorithm:
            if char == '#':
                in_comment = True
                if current_part:
                    parts.append(current_part)
                    current_part = "#"
                else:
                    current_part = "#"
            elif in_comment:
                if char == '\n':
                    in_comment = False
                    parts.append(current_part)
                    current_part = ""
                else:
                    current_part += char
            elif char.isspace():
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
                
        if current_part:
            parts.append(current_part)
            
        # Clean up and return the moves
        return [part.strip() for part in parts if part.strip()]
    
    @staticmethod
    def algorithm_to_human_readable(algorithm):
        """
        Convert an algorithm string to human-readable instructions.
        
        Args:
            algorithm (str or list): Algorithm string or list of moves.
            
        Returns:
            list: List of human-readable instructions.
        """
        # Parse the algorithm if it's a string
        if isinstance(algorithm, str):
            moves = MoveNotation.parse_algorithm(algorithm)
        else:
            moves = algorithm
            
        # Convert each move
        return [MoveNotation.to_human_readable(move) for move in moves]
    
    @staticmethod
    def simplify_algorithm(algorithm):
        """
        Simplify an algorithm by combining consecutive moves on the same face.
        
        Args:
            algorithm (str or list): Algorithm to simplify.
            
        Returns:
            list: Simplified list of moves.
        """
        # Parse the algorithm if it's a string
        if isinstance(algorithm, str):
            moves = MoveNotation.parse_algorithm(algorithm)
        else:
            moves = algorithm.copy()
            
        # Simplify consecutive moves on the same face
        i = 0
        while i < len(moves) - 1:
            current = moves[i]
            next_move = moves[i + 1]
            
            # Skip comments or non-standard moves
            if current.startswith('#') or next_move.startswith('#'):
                i += 1
                continue
                
            # Check if they're moves on the same face
            if len(current) > 0 and len(next_move) > 0:
                current_face = current[0]
                next_face = next_move[0]
                
                # Handle two-character face names
                if len(current) > 1 and not current[1] in ["'", "2"]:
                    current_face += current[1]
                if len(next_move) > 1 and not next_move[1] in ["'", "2"]:
                    next_face += next_move[1]
                    
                if current_face == next_face:
                    # Determine the combined move
                    combined = MoveNotation._combine_moves(current, next_move)
                    if combined:
                        moves[i] = combined
                        moves.pop(i + 1)
                        continue
            
            i += 1
            
        return moves
    
    @staticmethod
    def _combine_moves(move1, move2):
        """
        Combine two consecutive moves on the same face.
        
        Args:
            move1, move2: Two moves to combine.
            
        Returns:
            str: Combined move, or None if they cancel out.
        """
        # Extract face and modifiers
        face1 = move1[0]
        if len(move1) > 1 and not move1[1] in ["'", "2"]:
            face1 += move1[1]
            mod1 = move1[len(face1):]
        else:
            mod1 = move1[1:]
            
        face2 = move2[0]
        if len(move2) > 1 and not move2[1] in ["'", "2"]:
            face2 += move2[1]
            mod2 = move2[len(face2):]
        else:
            mod2 = move2[1:]
            
        # Calculate combined rotation
        rot1 = 1  # Clockwise
        if mod1 == "'":
            rot1 = 3  # Counter-clockwise (3 quarter turns)
        elif mod1 == "2":
            rot1 = 2  # Half turn
            
        rot2 = 1  # Clockwise
        if mod2 == "'":
            rot2 = 3  # Counter-clockwise
        elif mod2 == "2":
            rot2 = 2  # Half turn
            
        # Combine rotations (mod 4 for quarter turns)
        combined_rot = (rot1 + rot2) % 4
        
        # Convert back to move notation
        if combined_rot == 0:
            return None  # Moves cancel out
        elif combined_rot == 1:
            return face1  # Clockwise
        elif combined_rot == 2:
            return face1 + "2"  # Half turn
        else:  # combined_rot == 3
            return face1 + "'"  # Counter-clockwise
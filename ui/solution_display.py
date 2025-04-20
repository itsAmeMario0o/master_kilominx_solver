"""
Widget for displaying the step-by-step solution for the Master Kilominx.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QListWidget, QListWidgetItem, QPushButton,
                           QGroupBox, QGridLayout, QScrollArea, QSplitter)
from PyQt5.QtGui import QColor, QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt, QSize

class KilominxFaceWidget(QWidget):
    """Widget for displaying a single face of the Kilominx in the solution display."""
    
    def __init__(self, face_data, parent=None):
        super().__init__(parent)
        self.face_data = face_data
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the UI for this face."""
        layout = QGridLayout(self)
        layout.setSpacing(2)
        
        # Create a 4x4 grid of colored squares
        for row in range(4):
            for col in range(4):
                color_idx = row * 4 + col
                if color_idx < len(self.face_data):
                    color_data = self.face_data[color_idx]
                    color = QColor(*color_data)
                else:
                    color = QColor(200, 200, 200)  # Default gray
                    
                square = QLabel()
                square.setFixedSize(20, 20)
                palette = square.palette()
                palette.setColor(QPalette.Window, color)
                square.setPalette(palette)
                square.setAutoFillBackground(True)
                
                layout.addWidget(square, row, col)
                
        self.setLayout(layout)

class SolutionDisplayWidget(QWidget):
    """Widget for displaying the solution to the Master Kilominx."""
    
    def __init__(self):
        super().__init__()
        self.solution_steps = []
        self.current_step = -1
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the UI components."""
        main_layout = QVBoxLayout(self)
        
        # Split view: steps list on left, visualization on right
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side: Solution steps list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Instructions
        instructions = QLabel("Here's the step-by-step solution for your Master Kilominx.")
        instructions.setWordWrap(True)
        left_layout.addWidget(instructions)
        
        # Steps list
        self.steps_list = QListWidget()
        self.steps_list.currentRowChanged.connect(self._on_step_selected)
        left_layout.addWidget(self.steps_list)
        
        # Step navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Previous Step")
        self.prev_button.clicked.connect(self._prev_step)
        self.prev_button.setEnabled(False)
        nav_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Next Step")
        self.next_button.clicked.connect(self._next_step)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button)
        
        left_layout.addLayout(nav_layout)
        
        # Right side: Visualization of the current step
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Current step description
        self.step_description = QLabel("No solution loaded")
        self.step_description.setWordWrap(True)
        self.step_description.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.step_description)
        
        # Kilominx visualization
        self.visualization = QScrollArea()
        self.visualization.setWidgetResizable(True)
        
        # Create a widget to hold the faces
        vis_content = QWidget()
        self.vis_layout = QGridLayout(vis_content)
        
        # We'll populate this when a solution is loaded
        self.visualization.setWidget(vis_content)
        right_layout.addWidget(self.visualization)
        
        # Add widgets to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        
        # Set initial sizes
        splitter.setSizes([300, 600])
        
        main_layout.addWidget(splitter)
        
    def display_solution(self, initial_state, solution_steps):
        """Display the solution for the given cube state."""
        self.initial_state = initial_state
        self.solution_steps = solution_steps
        self.current_states = [initial_state]  # Start with initial state

# Generate intermediate states by applying steps
        current_state = initial_state.copy()
        for step in solution_steps:
            # This would call a function to apply the move to the current state
            # and generate a new state, which we store for visualization
            new_state = self._apply_move_to_state(current_state, step)
            self.current_states.append(new_state)
            current_state = new_state
            
        # Populate the steps list
        self.steps_list.clear()
        self.steps_list.addItem("Initial State")
        for i, step in enumerate(solution_steps):
            self.steps_list.addItem(f"Step {i+1}: {step}")
            
        # Show initial state
        self.current_step = 0
        self._show_step(0)
        
        # Enable navigation buttons
        self.next_button.setEnabled(len(solution_steps) > 0)
        self.prev_button.setEnabled(False)
        
    def _on_step_selected(self, row):
        """Handle selection of a step in the list."""
        if row >= 0 and row <= len(self.solution_steps):
            self.current_step = row
            self._show_step(row)
            
            # Update button states
            self.prev_button.setEnabled(row > 0)
            self.next_button.setEnabled(row < len(self.solution_steps))
            
    def _prev_step(self):
        """Go to the previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.steps_list.setCurrentRow(self.current_step)
            self._show_step(self.current_step)
            
    def _next_step(self):
        """Go to the next step."""
        if self.current_step < len(self.solution_steps):
            self.current_step += 1
            self.steps_list.setCurrentRow(self.current_step)
            self._show_step(self.current_step)
            
    def _show_step(self, step_index):
        """Display the cube state at the given step."""
        if not self.current_states or step_index < 0 or step_index >= len(self.current_states):
            return
            
        # Update step description
        if step_index == 0:
            self.step_description.setText("Initial State")
        else:
            self.step_description.setText(f"Step {step_index}: {self.solution_steps[step_index-1]}")
            
        # Clear existing visualization
        while self.vis_layout.count():
            item = self.vis_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Create the face grid for the current state
        state = self.current_states[step_index]
        
        # Create a layout that resembles the unfolded dodecahedron
        # This is a simplified representation
        
        # Row 0: Face 0
        self.vis_layout.addWidget(KilominxFaceWidget(state.get("face_0", [])), 0, 1)
        
        # Row 1: Faces 1-5
        for i in range(5):
            self.vis_layout.addWidget(KilominxFaceWidget(state.get(f"face_{i+1}", [])), 1, i)
            
        # Row 2: Faces 6-10
        for i in range(5):
            self.vis_layout.addWidget(KilominxFaceWidget(state.get(f"face_{i+6}", [])), 2, i)
            
        # Row 3: Face 11
        self.vis_layout.addWidget(KilominxFaceWidget(state.get("face_11", [])), 3, 1)
        
    def _apply_move_to_state(self, current_state, move):
        """
        Apply a move to the current state and return the new state.
        This would call into the solver's move application logic.
        """
        # In a real implementation, this would use the solver module
        # For this demo, we just return a copy of the current state
        # as a placeholder (the actual implementation would transform the state)
        new_state = current_state.copy()
        
        # Here we would transform the state according to the move
        # This is highly dependent on the internal representation
        # and move notation used by the solver
        
        return new_state
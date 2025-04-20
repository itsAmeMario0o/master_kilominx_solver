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
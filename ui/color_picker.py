"""
Widget for manually inputting the colors of the Master Kilominx faces.
"""

from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QComboBox,
                           QLabel, QVBoxLayout, QHBoxLayout, QGroupBox,
                           QScrollArea, QSizePolicy, QFrame)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal

class ColorButton(QPushButton):
    """Button representing a sticker on the Kilominx."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setColor(QColor(200, 200, 200))  # Default gray
        
    def setColor(self, color):
        """Set the button's color."""
        self.color = color
        palette = self.palette()
        palette.setColor(QPalette.Button, color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.update()
        
    def getColor(self):
        """Get the button's current color."""
        return self.color

class ColorPickerWidget(QWidget):
    """Widget for manually selecting colors for each face of the Master Kilominx."""
    
    state_ready = pyqtSignal(dict)
    
    # Define standard colors for the Master Kilominx
    COLORS = {
        "White": QColor(255, 255, 255),
        "Yellow": QColor(255, 255, 0),
        "Red": QColor(255, 0, 0),
        "Orange": QColor(255, 165, 0),
        "Green": QColor(0, 128, 0),
        "Blue": QColor(0, 0, 255),
        "Purple": QColor(128, 0, 128),
        "Pink": QColor(255, 192, 203),
        "Light Blue": QColor(173, 216, 230),
        "Light Green": QColor(144, 238, 144),
        "Brown": QColor(165, 42, 42),
        "Gray": QColor(128, 128, 128)
    }
    
    def __init__(self, on_state_ready_callback):
        super().__init__()
        
        self.on_state_ready_callback = on_state_ready_callback
        self.current_color = QColor(255, 255, 255)  # Start with white
        self.current_face = 0  # Start with face 0
        self.face_buttons = []
        self.face_frames = []  # NEW: Keep track of face frames/containers
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the UI components."""
        main_layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Select a color from the palette, then click on the stickers to color them. "
            "Use the face selector to switch between the 12 faces of the Master Kilominx."
        )
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Color palette
        color_group = QGroupBox("Color Palette")
        color_layout = QGridLayout()
        
        row, col = 0, 0
        for color_name, color in self.COLORS.items():
            btn = QPushButton(color_name)
            palette = btn.palette()
            palette.setColor(QPalette.Button, color)
            btn.setPalette(palette)
            btn.setAutoFillBackground(True)
            btn.clicked.connect(lambda checked, c=color: self._select_color(c))
            
            color_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:  # 4 colors per row
                col = 0
                row += 1
                
        color_group.setLayout(color_layout)
        main_layout.addWidget(color_group)
        
        # Current color indicator
        color_indicator_layout = QHBoxLayout()
        color_indicator_layout.addWidget(QLabel("Current Color:"))
        
        self.color_indicator = QPushButton()
        self.color_indicator.setFixedSize(30, 30)
        self.color_indicator.setEnabled(False)
        palette = self.color_indicator.palette()
        palette.setColor(QPalette.Button, self.current_color)
        self.color_indicator.setPalette(palette)
        self.color_indicator.setAutoFillBackground(True)
        
        color_indicator_layout.addWidget(self.color_indicator)
        color_indicator_layout.addStretch()
        
        main_layout.addLayout(color_indicator_layout)
        
        # Face selector
        face_selector_layout = QHBoxLayout()
        face_selector_layout.addWidget(QLabel("Current Face:"))
        
        self.face_selector = QComboBox()
        for i in range(12):
            self.face_selector.addItem(f"Face {i+1}")
        self.face_selector.currentIndexChanged.connect(self._change_face)
        
        face_selector_layout.addWidget(self.face_selector)
        face_selector_layout.addStretch()
        
        main_layout.addLayout(face_selector_layout)
        
        # Face grid (4x4 for Master Kilominx)
        face_container = QWidget()
        self.face_layout = QVBoxLayout(face_container)
        self.face_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a 4x4 grid for each face - NEW: Using QFrame for each face
        for face in range(12):
            face_frame = QFrame()
            face_frame_layout = QGridLayout(face_frame)
            face_frame_layout.setSpacing(2)
            face_buttons = []
            
            for row in range(4):
                row_buttons = []
                for col in range(4):
                    btn = ColorButton()
                    btn.clicked.connect(lambda checked, r=row, c=col, f=face: 
                                       self._set_sticker_color(f, r, c))
                    face_frame_layout.addWidget(btn, row, col)
                    row_buttons.append(btn)
                face_buttons.append(row_buttons)
            
            self.face_buttons.append(face_buttons)
            self.face_frames.append(face_frame)
            
            # Initially hide all faces except the first
            face_frame.setVisible(face == 0)
            self.face_layout.addWidget(face_frame)
            
        # Add the face container to the main layout with a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(face_container)
        main_layout.addWidget(scroll_area, 1)
        
        # Solve button
        solve_button = QPushButton("Validate & Solve")
        solve_button.clicked.connect(self._on_solve_clicked)
        main_layout.addWidget(solve_button)
        
    def _select_color(self, color):
        """Handle color selection from the palette."""
        self.current_color = color
        palette = self.color_indicator.palette()
        palette.setColor(QPalette.Button, color)
        self.color_indicator.setPalette(palette)
        
    def _change_face(self, index):
        """Switch between faces of the Master Kilominx."""
        self.current_face = index
        
        # Update visibility of face frames
        for i, face_frame in enumerate(self.face_frames):
            face_frame.setVisible(i == index)
        
    def _set_sticker_color(self, face, row, col):
        """Set the color of a sticker on the current face."""
        if face != self.current_face:
            # This should not happen with the current UI,
            # but included for potential future changes
            return
            
        button = self.face_buttons[face][row][col]
        button.setColor(self.current_color)
        
    def _on_solve_clicked(self):
        """Prepare the cube state and emit the state_ready signal."""
        # Collect the colors from all stickers
        cube_state = {}
        
        for face_idx, face_buttons in enumerate(self.face_buttons):
            face_colors = []
            for row_buttons in face_buttons:
                for button in row_buttons:
                    # Store the RGB values of each sticker
                    color = button.getColor()
                    face_colors.append([color.red(), color.green(), color.blue()])
            
            cube_state[f"face_{face_idx}"] = face_colors
            
        # Call the callback with the collected state
        self.on_state_ready_callback(cube_state)
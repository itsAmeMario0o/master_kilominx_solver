"""
Widget for manually inputting the colors of the Master Kilominx faces.
Revised for proper 20-sticker pentagonal face layout.
"""

from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QComboBox,
                           QLabel, QVBoxLayout, QHBoxLayout, QGroupBox,
                           QScrollArea, QSizePolicy, QFrame)
from PyQt5.QtGui import QColor, QPalette, QPainter, QPolygon
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
import math

class PentagonalSticker(QPushButton):
    """Button representing a sticker on the Kilominx pentagonal face."""
    
    def __init__(self, position_type, parent=None):
        super().__init__(parent)
        self.position_type = position_type  # corner, edge, middle_edge, center_piece, super_center
        self.setFixedSize(40, 40)
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

class PentagonalFaceWidget(QWidget):
    """Widget representing a pentagonal face with proper sticker layout."""
    
    def __init__(self, face_id, on_sticker_clicked_callback, parent=None):
        super().__init__(parent)
        self.face_id = face_id
        self.on_sticker_clicked = on_sticker_clicked_callback
        self.stickers = []
        self.setMinimumSize(300, 300)
        self._setup_pentagonal_layout()
    
    def _setup_pentagonal_layout(self):
        """Create a proper pentagonal layout with 20 stickers:
        - 5 corners (on the pentagon vertices)
        - 5 edges (along the pentagon edges)
        - 5 middle edges (inside the edges)
        - 5 center pieces (forming a smaller pentagon)
        - 1 super center (in the middle)
        """
        layout = QVBoxLayout(self)
        
        # Create a container for absolute positioning
        container = QWidget()
        container.setFixedSize(300, 300)
        layout.addWidget(container)
        
        # Center of the pentagon
        center_x, center_y = 150, 150
        radius = 110  # Main pentagon radius
        
        # Create stickers in layers from outer to inner
        
        # 1. Corner stickers (5) - on pentagon vertices
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2  # Start from top
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            
            sticker = PentagonalSticker('corner', container)
            sticker.move(x-20, y-20)
            sticker.clicked.connect(lambda checked, idx=i: 
                                  self.on_sticker_clicked(self.face_id, 'corner', idx))
            self.stickers.append(sticker)
        
        # 2. Edge stickers (5) - midpoints between corners
        for i in range(5):
            angle_start = i * 2 * math.pi / 5 - math.pi / 2
            angle_end = (i + 1) * 2 * math.pi / 5 - math.pi / 2
            
            x1 = center_x + radius * math.cos(angle_start)
            y1 = center_y + radius * math.sin(angle_start)
            x2 = center_x + radius * math.cos(angle_end)
            y2 = center_y + radius * math.sin(angle_end)
            
            x = int((x1 + x2) / 2)
            y = int((y1 + y2) / 2)
            
            sticker = PentagonalSticker('edge', container)
            sticker.move(x-20, y-20)
            sticker.clicked.connect(lambda checked, idx=i: 
                                  self.on_sticker_clicked(self.face_id, 'edge', idx))
            self.stickers.append(sticker)
        
        # 3. Middle edge stickers (5) - closer to center than edges
        inner_radius = radius * 0.6
        for i in range(5):
            angle_start = i * 2 * math.pi / 5 - math.pi / 2
            angle_end = (i + 1) * 2 * math.pi / 5 - math.pi / 2
            
            x1 = center_x + inner_radius * math.cos(angle_start)
            y1 = center_y + inner_radius * math.sin(angle_start)
            x2 = center_x + inner_radius * math.cos(angle_end)
            y2 = center_y + inner_radius * math.sin(angle_end)
            
            x = int((x1 + x2) / 2)
            y = int((y1 + y2) / 2)
            
            sticker = PentagonalSticker('middle_edge', container)
            sticker.move(x-20, y-20)
            sticker.clicked.connect(lambda checked, idx=i: 
                                  self.on_sticker_clicked(self.face_id, 'middle_edge', idx))
            self.stickers.append(sticker)
        
        # 4. Center pieces (5) - forming a small pentagon around the super center
        center_radius = radius * 0.3
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2
            x = int(center_x + center_radius * math.cos(angle))
            y = int(center_y + center_radius * math.sin(angle))
            
            sticker = PentagonalSticker('center_piece', container)
            sticker.move(x-20, y-20)
            sticker.clicked.connect(lambda checked, idx=i: 
                                  self.on_sticker_clicked(self.face_id, 'center_piece', idx))
            self.stickers.append(sticker)
        
        # 5. Super center sticker (1) - in the middle
        sticker = PentagonalSticker('super_center', container)
        sticker.move(center_x-20, center_y-20)
        sticker.clicked.connect(lambda checked: 
                              self.on_sticker_clicked(self.face_id, 'super_center', 0))
        self.stickers.append(sticker)
    
    def get_color_state(self):
        """Return the color state of all stickers."""
        return [sticker.getColor().getRgb()[:3] for sticker in self.stickers]
    
    def set_sticker_color(self, sticker_type, index, color):
        """Set the color of a specific sticker."""
        # Map sticker type and index to the correct sticker in our list
        if sticker_type == 'corner':
            sticker_idx = index
        elif sticker_type == 'edge':
            sticker_idx = 5 + index
        elif sticker_type == 'middle_edge':
            sticker_idx = 10 + index
        elif sticker_type == 'center_piece':
            sticker_idx = 15 + index
        elif sticker_type == 'super_center':
            sticker_idx = 20
        else:
            return
        
        if 0 <= sticker_idx < len(self.stickers):
            self.stickers[sticker_idx].setColor(color)

class MasterKilominxColorPicker(QWidget):
    """Updated color picker widget for proper Master Kilominx with 20 stickers per face."""
    
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
        self.face_widgets = []
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the UI components."""
        main_layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Select a color from the palette, then click on the stickers to color them. "
            "Each face has 20 stickers: 5 corners, 5 edges, 5 middle edges, 5 center pieces, and 1 super center."
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
        self.color_indicator.setFixedSize(40, 40)
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
        
        # Pentagon face widget container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        face_container = QWidget()
        self.face_layout = QVBoxLayout(face_container)
        
        # Create pentagonal face widgets
        for face in range(12):
            face_widget = PentagonalFaceWidget(face, self._on_sticker_clicked)
            face_widget.setVisible(face == 0)  # Show only the first face initially
            self.face_widgets.append(face_widget)
            self.face_layout.addWidget(face_widget)
        
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
        
        # Update visibility of face widgets
        for i, face_widget in enumerate(self.face_widgets):
            face_widget.setVisible(i == index)
            
    def _on_sticker_clicked(self, face_id, sticker_type, index):
        """Handle sticker click to apply current color."""
        if face_id == self.current_face:
            self.face_widgets[face_id].set_sticker_color(sticker_type, index, self.current_color)
        
    def _on_solve_clicked(self):
        """Prepare the cube state and emit the state_ready signal."""
        # Collect the colors from all faces
        cube_state = {}
        
        for face_idx, face_widget in enumerate(self.face_widgets):
            cube_state[f"face_{face_idx}"] = face_widget.get_color_state()
            
        # Call the callback with the collected state
        self.on_state_ready_callback(cube_state)
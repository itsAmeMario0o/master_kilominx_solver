"""
Widget for manually inputting the colors of the Master Kilominx faces.
Layout: Small black pentagon center (mechanism) + 5 edge pieces with 4 stickers each = 20 stickers.
"""

from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QComboBox,
                           QLabel, QVBoxLayout, QHBoxLayout, QGroupBox,
                           QScrollArea, QSizePolicy, QFrame)
from PyQt5.QtGui import QColor, QPalette, QPainter, QPolygon, QPainterPath, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
import math

class PentagonalSticker(QPushButton):
    """Button representing a sticker on the Kilominx pentagonal face."""
    
    def __init__(self, edge_id, sticker_id, parent=None):
        super().__init__(parent)
        self.edge_id = edge_id      # 0-4 for the five edges
        self.sticker_id = sticker_id  # 0-3 for the four stickers on each edge
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

class PentagonWidget(QWidget):
    """Widget that displays a small black pentagon in the center."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)  # Smaller size
        
    def paintEvent(self, event):
        """Draw a black pentagon."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set black fill and no outline for the pentagon
        painter.setBrush(QColor(0, 0, 0))  # Pure black
        painter.setPen(Qt.NoPen)  # No outline
        
        # Create a pentagon
        center = QPoint(25, 25)
        radius = 20  # Smaller radius
        
        pentagon_path = QPainterPath()
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            
            if i == 0:
                pentagon_path.moveTo(x, y)
            else:
                pentagon_path.lineTo(x, y)
        
        pentagon_path.closeSubpath()
        painter.drawPath(pentagon_path)

class PentagonalFaceWidget(QWidget):
    """Widget representing a pentagonal face with 5 edges, 4 stickers per edge."""
    
    def __init__(self, face_id, on_sticker_clicked_callback, parent=None):
        super().__init__(parent)
        self.face_id = face_id
        self.on_sticker_clicked = on_sticker_clicked_callback
        self.stickers = []
        self.setMinimumSize(400, 400)
        self._setup_pentagonal_layout()
    
    def _setup_pentagonal_layout(self):
        """Create the Master Kilominx layout with 20 stickers."""
        layout = QVBoxLayout(self)
        
        # Create a container for absolute positioning
        container = QWidget()
        container.setFixedSize(400, 400)
        layout.addWidget(container)
        
        # Center of the pentagon
        center_x, center_y = 200, 200
        
        # Add the small black pentagon mechanism (visual only, not interactive)
        pentagon_widget = PentagonWidget(container)
        pentagon_widget.move(center_x - 25, center_y - 25)  # Center the smaller pentagon
        
        # Create 5 edges, each with 4 stickers
        for edge in range(5):
            # Each edge is at 72-degree increments
            angle = edge * 2 * math.pi / 5 - math.pi / 2  # Start from top
            
            # For each edge, position 4 stickers in a trapezoidal pattern
            # Arranged from outside to inside: corner, outer edge, inner edge, center edge
            
            # Base positions for this edge
            base_angle = angle
            
            # 1. Corner sticker - outermost point, exactly on pentagon vertex
            corner_radius = 170
            corner_x = int(center_x + corner_radius * math.cos(base_angle) - 15)
            corner_y = int(center_y + corner_radius * math.sin(base_angle) - 15)
            corner_sticker = PentagonalSticker(edge, 0, container)
            corner_sticker.move(corner_x, corner_y)
            corner_sticker.clicked.connect(lambda checked, e=edge, s=0: 
                                        self.on_sticker_clicked(self.face_id, e, s))
            self.stickers.append(corner_sticker)
            
            # 2. Outer edge sticker - along the pentagon's outer edge
            edge_radius = 140
            next_angle = (edge + 1) * 2 * math.pi / 5 - math.pi / 2
            edge_angle = (base_angle + next_angle) / 2
            outer_edge_x = int(center_x + edge_radius * math.cos(edge_angle) - 15)
            outer_edge_y = int(center_y + edge_radius * math.sin(edge_angle) - 15)
            outer_edge_sticker = PentagonalSticker(edge, 1, container)
            outer_edge_sticker.move(outer_edge_x, outer_edge_y)
            outer_edge_sticker.clicked.connect(lambda checked, e=edge, s=1: 
                                            self.on_sticker_clicked(self.face_id, e, s))
            self.stickers.append(outer_edge_sticker)
            
            # 3. Inner edge sticker - midway between outer edge and center
            inner_edge_radius = 100
            inner_edge_x = int(center_x + inner_edge_radius * math.cos(edge_angle) - 15)
            inner_edge_y = int(center_y + inner_edge_radius * math.sin(edge_angle) - 15)
            inner_edge_sticker = PentagonalSticker(edge, 2, container)
            inner_edge_sticker.move(inner_edge_x, inner_edge_y)
            inner_edge_sticker.clicked.connect(lambda checked, e=edge, s=2: 
                                            self.on_sticker_clicked(self.face_id, e, s))
            self.stickers.append(inner_edge_sticker)
            
            # 4. Center edge sticker - closest to the central pentagon
            center_edge_radius = 60  # Adjusted to leave space for the smaller pentagon
            center_edge_x = int(center_x + center_edge_radius * math.cos(base_angle) - 15)
            center_edge_y = int(center_y + center_edge_radius * math.sin(base_angle) - 15)
            center_edge_sticker = PentagonalSticker(edge, 3, container)
            center_edge_sticker.move(center_edge_x, center_edge_y)
            center_edge_sticker.clicked.connect(lambda checked, e=edge, s=3: 
                                             self.on_sticker_clicked(self.face_id, e, s))
            self.stickers.append(center_edge_sticker)
    
    def get_color_state(self):
        """Return the color state of all stickers."""
        return [sticker.getColor().getRgb()[:3] for sticker in self.stickers]
    
    def set_sticker_color(self, edge_id, sticker_id, color):
        """Set the color of a specific sticker."""
        sticker_index = edge_id * 4 + sticker_id
        if 0 <= sticker_index < len(self.stickers):
            self.stickers[sticker_index].setColor(color)

class MasterKilominxColorPicker(QWidget):
    """Color picker widget for Master Kilominx with 20 stickers per face."""
    
    state_ready = pyqtSignal(dict)
    
    # Define standard colors for the Master Kilominx
    COLORS = {
        "White": QColor(255, 255, 255),
        "Yellow": QColor(255, 255, 0),
        "Blue": QColor(0, 0, 255),
        "Red": QColor(255, 0, 0),
        "Green": QColor(0, 200, 0),
        "Purple": QColor(150, 0, 150),
        "Orange": QColor(255, 165, 0),
        "Pink": QColor(255, 105, 180),
        "Light Blue": QColor(0, 191, 255),
        "Light Green": QColor(144, 238, 144),
        "Dark Green": QColor(0, 100, 0),
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
            "Each face has 5 edges around a small black pentagon mechanism, with 4 stickers per edge. "
            "Total: 20 stickers per face."
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
            
    def _on_sticker_clicked(self, face_id, edge_id, sticker_id):
        """Handle sticker click to apply current color."""
        if face_id == self.current_face:
            self.face_widgets[face_id].set_sticker_color(edge_id, sticker_id, self.current_color)
        
    def _on_solve_clicked(self):
        """Prepare the cube state and emit the state_ready signal."""
        # Collect the colors from all faces
        cube_state = {}
        
        for face_idx, face_widget in enumerate(self.face_widgets):
            cube_state[f"face_{face_idx}"] = face_widget.get_color_state()
            
        # Call the callback with the collected state
        self.on_state_ready_callback(cube_state)
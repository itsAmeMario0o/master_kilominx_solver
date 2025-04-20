"""
Main application window for the Master Kilominx Solver.
Revised to use the proper 20-sticker color picker.
"""

from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QAction, QFileDialog, 
                            QVBoxLayout, QWidget, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Make sure you have the correct import
from ui.color_picker import MasterKilominxColorPicker
from ui.image_input import ImageInputWidget
from ui.solution_display import SolutionDisplayWidget
from solver.state_validator import validate_kilominx_state
from solver.solver_algorithm import solve_kilominx
from utils.image_processor import extract_colors_from_image

class MainWindow(QMainWindow):
    """Main window of the application containing all UI elements."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Master Kilominx Solver")
        self.setMinimumSize(1000, 700)  # Slightly larger to accommodate pentagonal layout
        
        # Initialize cube state
        self.cube_state = None
        
        self._setup_ui()
        self._create_menu()
        
    def _setup_ui(self):
        """Set up the main UI components."""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tab widget for different input methods
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create and add tabs
        self.manual_input_tab = MasterKilominxColorPicker(self._on_manual_state_ready)
        self.image_input_tab = ImageInputWidget(self._on_image_processed)
        self.solution_tab = SolutionDisplayWidget()
        
        self.tab_widget.addTab(self.manual_input_tab, "Manual Input")
        self.tab_widget.addTab(self.image_input_tab, "Image Input")
        self.tab_widget.addTab(self.solution_tab, "Solution")
        
        # Initially disable the solution tab
        self.tab_widget.setTabEnabled(2, False)
        
    def _create_menu(self):
        """Create the application menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        # Open image action
        open_action = QAction("Open Image...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_image)
        file_menu.addAction(open_action)
        
        # Save solution action
        save_action = QAction("Save Solution...", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_solution)
        save_action.setEnabled(False)
        self.save_action = save_action
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _open_image(self):
        """Open an image file for processing."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.tab_widget.setCurrentIndex(1)  # Switch to image input tab
            self.image_input_tab.load_image(file_path)
            
    def _save_solution(self):
        """Save the current solution to a text file."""
        if not hasattr(self, 'solution_steps'):
            QMessageBox.warning(self, "No Solution", "No solution available to save.")
            return
            
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save Solution", "", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("Master Kilominx Solution Steps\n")
                    f.write("============================\n\n")
                    for i, step in enumerate(self.solution_steps):
                        f.write(f"Step {i+1}: {step}\n")
                        
                QMessageBox.information(self, "Success", "Solution saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save solution: {str(e)}")
    
    def _on_manual_state_ready(self, state):
        """Callback when manual input is complete."""
        self.cube_state = state
        self._validate_and_solve()
        
    def _on_image_processed(self, state):
        """Callback when image processing is complete."""
        self.cube_state = state
        self._validate_and_solve()
        
    def _validate_and_solve(self):
        """Validate the cube state and solve if valid."""
        if not self.cube_state:
            QMessageBox.warning(self, "Invalid State", "No cube state available.")
            return
            
        # Validate the cube state
        is_valid, message = validate_kilominx_state(self.cube_state)
        if not is_valid:
            QMessageBox.warning(self, "Invalid Configuration", 
                               f"The cube state is not valid: {message}")
            return
            
        # Solve the cube
        try:
            self.solution_steps = solve_kilominx(self.cube_state)
            
            # Update the solution display
            self.solution_tab.display_solution(self.cube_state, self.solution_steps)
            
            # Enable solution tab and save action
            self.tab_widget.setTabEnabled(2, True)
            self.tab_widget.setCurrentIndex(2)  # Switch to solution tab
            self.save_action.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Solver Error", 
                                f"Failed to solve the cube: {str(e)}")
    
    def _show_about(self):
        """Show the about dialog."""
        QMessageBox.about(self, "About Master Kilominx Solver",
                         "Master Kilominx Solver v1.0\n\n"
                         "A tool to solve a 4x4 dodecahedral Rubik's cube.\n"
                         "Created with PyQt5 and Python.\n\n"
                         "Created by Cakanaka for a Technogel.")
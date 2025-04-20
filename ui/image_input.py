"""
Widget for processing images of a Master Kilominx to extract colors.
"""

import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QFileDialog, QMessageBox, QProgressBar)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot

from utils.image_processor import extract_colors_from_image

class ImageProcessorThread(QThread):
    """Thread for processing images without blocking the UI."""
    
    processing_complete = pyqtSignal(dict)
    processing_error = pyqtSignal(str)
    processing_progress = pyqtSignal(int)
    
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        
    def run(self):
        """Run the image processing."""
        try:
            # Extract colors from the image
            # This is a mock function call - the actual implementation would be more complex
            cube_state = extract_colors_from_image(
                self.image_path, progress_callback=self._progress_callback
            )
            
            self.processing_complete.emit(cube_state)
            
        except Exception as e:
            self.processing_error.emit(str(e))
            
    def _progress_callback(self, progress):
        """Report progress back to the UI."""
        self.processing_progress.emit(progress)

class ImageInputWidget(QWidget):
    """Widget for handling image input for the Master Kilominx solver."""
    
    def __init__(self, on_image_processed_callback):
        super().__init__()
        
        self.on_image_processed_callback = on_image_processed_callback
        self.image_path = None
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the UI components."""
        main_layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Upload an image of your Master Kilominx. For best results, ensure good lighting "
            "and that all faces are clearly visible. The app will try to detect the colors "
            "automatically."
        )
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Image preview
        self.image_preview = QLabel("No image selected")
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setMinimumSize(400, 300)
        self.image_preview.setStyleSheet("border: 1px solid gray;")
        main_layout.addWidget(self.image_preview)
        
        # Upload button
        button_layout = QHBoxLayout()
        
        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self._upload_image)
        button_layout.addWidget(upload_button)
        
        # Process button (initially disabled)
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self._process_image)
        self.process_button.setEnabled(False)
        button_layout.addWidget(self.process_button)
        
        main_layout.addLayout(button_layout)
        
        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)
        
    def load_image(self, file_path):
        """Load an image from the given file path."""
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "File Not Found", 
                              f"The file {file_path} does not exist.")
            return
            
        self.image_path = file_path
        self._display_image(file_path)
        self.process_button.setEnabled(True)
        self.status_label.setText(f"Image loaded: {os.path.basename(file_path)}")
        
    def _upload_image(self):
        """Open a file dialog to select an image."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.load_image(file_path)
            
    def _display_image(self, image_path):
        """Display the image in the preview area."""
        try:
            # Load and resize the image to fit the preview area
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(
                self.image_preview.width(), self.image_preview.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_preview.setPixmap(pixmap)
            
        except Exception as e:
            QMessageBox.warning(self, "Image Loading Error", 
                              f"Failed to load image: {str(e)}")
            
    def _process_image(self):
        """Process the loaded image to extract Kilominx colors."""
        if not self.image_path:
            QMessageBox.warning(self, "No Image", "Please upload an image first.")
            return
            
        # Disable UI elements during processing
        self.process_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Processing image...")
        
        # Start processing thread
        self.processor_thread = ImageProcessorThread(self.image_path)
        self.processor_thread.processing_complete.connect(self._on_processing_complete)
        self.processor_thread.processing_error.connect(self._on_processing_error)
        self.processor_thread.processing_progress.connect(self._update_progress)
        self.processor_thread.start()
        
    @pyqtSlot(dict)
    def _on_processing_complete(self, cube_state):
        """Handle completion of image processing."""
        self.progress_bar.setValue(100)
        self.status_label.setText("Image processing complete!")
        
        # Re-enable UI elements
        self.process_button.setEnabled(True)
        
        # Call the callback with the extracted state
        self.on_image_processed_callback(cube_state)
        
    @pyqtSlot(str)
    def _on_processing_error(self, error_message):
        """Handle image processing errors."""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Error: {error_message}")
        self.process_button.setEnabled(True)
        
        QMessageBox.critical(self, "Processing Error", 
                           f"Failed to process image: {error_message}")
        
    @pyqtSlot(int)
    def _update_progress(self, progress):
        """Update the progress bar."""
        self.progress_bar.setValue(progress)
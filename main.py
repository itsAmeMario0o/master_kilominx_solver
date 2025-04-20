#!/usr/bin/env python3
"""
Master Kilominx Solver - Main Application Entry Point
A tool to solve a 4x4 dodecahedral Rubik's cube (Master Kilominx).
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """
    Main application entry point.
    Initializes the UI and starts the application.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Master Kilominx Solver")
    app.setOrganizationName("PuzzleSolver")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
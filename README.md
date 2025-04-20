# Master Kilominx Solver

A Python application to solve a 4x4 dodecahedral Rubik's cube (Master Kilominx).

## Features

- **Dual Input Methods**:
  - Upload an image of your Master Kilominx for automated color detection
  - Manually input colors using an intuitive UI
  
- **Validation**: Ensures the cube state is valid before attempting to solve
  
- **Step-by-step Solution**: Provides human-readable instructions with visual guidance
  
- **Modular Architecture**: Clean separation between UI and solving logic

## Installation

### Requirements

- macOS (10.14 or newer recommended)
- Python 3.8 or newer
- pip package manager

### Setup

1. **Clone the repository**:
   ```
   git clone https://github.com/itsAmeMario0o/master_kilominx_solver
   cd master-kilominx-solver
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Launch the application**:
   ```
   python main.py
   ```

2. **Input your cube state** using one of the following methods:
   
   - **Manual Input**: Click on "Manual Input" tab, select colors from the palette, and apply them to the cube faces.
   
   - **Image Input**: Click on "Image Input" tab, upload a photo of your Master Kilominx, and let the app detect the colors.

3. **Validate and solve**: Once your cube state is entered, click "Validate & Solve" to generate a solution.

4. **Follow the solution**: The app will display step-by-step instructions in the "Solution" tab. Use the "Next Step" and "Previous Step" buttons to navigate through the solution.

5. **Save the solution**: You can save the solution to a text file using File → Save Solution.

## Application Structure

The application follows a modular structure:

- `main.py`: Entry point
- `ui/`: User interface components
- `solver/`: Solving algorithms and data models
- `utils/`: Helper utilities (image processing, color handling, etc.)
- `tests/`: Unit tests

## Solving Method

The solver uses a reduction method similar to solving a 4x4 Rubik's cube:

1. **Centers**: First solve the center pieces of each face
2. **Edge Pairing**: Group matching edge pieces together
3. **3x3 Reduction**: Solve the puzzle as if it were a 3x3 Kilominx (Megaminx)

## Troubleshooting

- **Image detection issues**: Ensure good lighting and that all faces are clearly visible. Try manual input if automatic detection fails.
  
- **Validation errors**: Make sure all stickers are correctly colored. The most common issue is incorrect color distribution.
  
- **Long solving times**: The solving algorithm can take time for complex states. The app includes a timeout setting in the configuration file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
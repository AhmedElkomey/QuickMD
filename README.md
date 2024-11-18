# Markdown Editor and Viewer

A feature-rich Markdown editor and viewer built with PyQt5 and Pygments, incorporating best practices like proper project structure, configuration management, robust error handling, type hints, command-line argument parsing, and comprehensive documentation.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features
- **Live Markdown Editing**: Write Markdown text and see the rendered HTML in real-time
- **Syntax Highlighting**: Enhanced editing experience with syntax highlighting using Pygments
- **Customizable Interface**: Adjust editor and viewer settings via easy-to-edit .ini configuration files
- **Robust Error Handling**: Comprehensive logging and exception handling for a smooth user experience
- **Type Annotations**: Clean and maintainable codebase with type hints throughout
- **Command-Line Support**: Customize application behavior using command-line arguments
- **Well-Documented**: Clear documentation with docstrings and a detailed README

## Screenshots
*(You can add screenshots of your application here to showcase the UI and features.)*

## Prerequisites
- Python 3.6 or higher
- Virtual Environment (optional but recommended)

## Installation

### Clone the Repository
```bash
git clone https://github.com/yourusername/QuickMD.git
cd QuickMD
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
Run the application with:
```bash
python main.py
```

## Command-Line Arguments
`--config`: Specify a custom path to the configuration .ini file.
```bash
python main.py --config path/to/your_config.ini
```

## Configuration
The application uses an .ini file for configuration, located at `resources/styles.ini` by default.

### Editing the Configuration
Open `resources/styles.ini` in a text editor to customize settings.

#### Example styles.ini
```ini
[Editor]
font_size = 12
font_family = Courier

[Viewer]
background_color = #FFFFFF
text_color = #000000
```

### Editor Settings
- `font_size`: Set the font size of the editor text
- `font_family`: Choose the font family for the editor

### Viewer Settings
- `background_color`: Set the background color of the viewer (hex code)
- `text_color`: Set the text color of the viewer (hex code)

## Project Structure
```
QuickMD/
├── QuickMD/
│   ├── __init__.py
│   ├── config.py
│   ├── editor.py
│   ├── gui.py
│   ├── highlighter.py
│   ├── utils.py
│   └── viewer.py
├── resources/
│   └── styles.ini
├── tests/
│   ├── __init__.py
│   └── test_editor.py
├── logs/
│   └── app.log
├── main.py
├── requirements.txt
└── README.md
```

### Core Modules
- `QuickMD/`: Core application modules
  - `config.py`: Handles configuration management
  - `editor.py`: Implements the Markdown editor widget
  - `gui.py`: Sets up the main application window and UI components
  - `highlighter.py`: Provides syntax highlighting functionality
  - `utils.py`: Contains utility functions like logging setup
  - `viewer.py`: Implements the Markdown viewer widget
- `resources/`: Contains configuration files and other resources
- `tests/`: Contains unit tests for the application
- `logs/`: Directory where log files are stored
- `main.py`: Entry point of the application
- `requirements.txt`: Lists all Python dependencies
- `README.md`: Project documentation

## Development

### Setting Up the Development Environment

#### Install Development Dependencies
All necessary dependencies are listed in requirements.txt. Install them with:
```bash
pip install -r requirements.txt
```

#### Activate Virtual Environment
Ensure your virtual environment is active:
```bash
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Running Tests
Run unit tests using:
```bash
python -m unittest tests/test_editor.py -v
```

### Code Style and Linting
Please adhere to PEP 8 standards. You can use tools like flake8 and black for linting and formatting.

## Contributing
Contributions are welcome! Here's how you can help:

1. **Fork the Repository**: Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/yourusername/QuickMD.git
   ```

3. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Add new features or fix bugs
   - Write unit tests for your code
   - Update documentation if necessary

5. **Commit Your Changes**
   ```bash
   git commit -am 'Add new feature'
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Submit a Pull Request**
   - Go to the original repository
   - Click on "Pull Requests" and submit your PR

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- **PyQt5**: For providing a comprehensive set of Python bindings for Qt
- **Pygments**: For syntax highlighting
- **Markdown Library**: For Markdown to HTML conversion
- **Contributors**: Thanks to all who have contributed to this project
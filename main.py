import sys
import logging
from QuickMD.ui import MainWindow
from QuickMD.config import Config
from QuickMD.utils import setup_logging
from PyQt5.QtWidgets import QApplication
import argparse

def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description='Markdown Editor and Viewer')
    parser.add_argument(
        '--config',
        type=str,
        default='resources/styles.ini',
        help='Path to the configuration file'
    )
    return parser.parse_args()

def main() -> None:
    """Main entry point of the application."""
    setup_logging()
    args = parse_args()
    try:
        app = QApplication(sys.argv)
        config = Config()
        window = MainWindow(config)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.exception("An unexpected error occurred:")
        sys.exit(1)

if __name__ == '__main__':
    main()

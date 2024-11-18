import configparser
import os
from typing import Dict

class Config:
    """Handles application configuration."""

    def __init__(self, config_file: str = 'resources/styles.ini') -> None:
        self.config_file = config_file
        self.parser = configparser.ConfigParser()
        self.load_config()

    def load_config(self) -> None:
        """Loads configuration from the ini file."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} not found.")
        self.parser.read(self.config_file)

    def get_editor_config(self) -> Dict[str, str]:
        """Returns editor configuration."""
        return dict(self.parser.items('Editor'))

    def get_viewer_config(self) -> Dict[str, str]:
        """Returns viewer configuration."""
        return dict(self.parser.items('Viewer'))

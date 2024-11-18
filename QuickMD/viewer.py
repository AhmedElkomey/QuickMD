from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextOption
from PyQt5.QtCore import Qt
from markdown import markdown
from typing import Dict

class Viewer(QTextEdit):
    """Markdown viewer widget."""

    def __init__(self, config: Dict[str, str]) -> None:
        super().__init__()
        self.config = config
        self.setReadOnly(True)
        self.apply_config()

    def apply_config(self) -> None:
        """Applies configuration settings to the viewer."""
        self.setStyleSheet(f"""
            background-color: {self.config.get('background_color', '#FFFFFF')};
            color: {self.config.get('text_color', '#000000')};
        """)
        self.setWordWrapMode(QTextOption.WordWrap)

    def render_markdown(self, text: str) -> None:
        """Renders Markdown text to HTML."""
        html = markdown(text)
        self.setHtml(html)

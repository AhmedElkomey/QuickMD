from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont
from typing import Dict
from .highlighter import MarkdownHighlighter


class Editor(QTextEdit):
    """Markdown editor widget."""

    def __init__(self, config: Dict[str, str]) -> None:
        super().__init__()
        self.config = config
        self.apply_config()

    def apply_config(self) -> None:
        """Applies configuration settings to the editor."""
        font_family = self.config.get('font_family', 'Courier')
        font_size = int(self.config.get('font_size', '12'))
        font = QFont(font_family, font_size)
        self.setFont(font)
        self.setTabStopWidth(int(self.config.get('tab_width', '40')))
        self.highlighter = MarkdownHighlighter(self.document())


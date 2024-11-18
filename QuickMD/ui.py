from PyQt5.QtWidgets import QMainWindow, QTextEdit, QWidget, QVBoxLayout, QApplication
from typing import Optional
import sys

from .config import Config
from .editor import Editor
from .viewer import Viewer

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self) -> None:
        """Initializes the UI components."""
        self.setWindowTitle('Markdown Editor and Viewer')

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.editor = Editor(self.config.get_editor_config())
        self.viewer = Viewer(self.config.get_viewer_config())

        layout.addWidget(self.editor)
        layout.addWidget(self.viewer)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.editor.textChanged.connect(self.update_viewer)

    def update_viewer(self) -> None:
        """Updates the viewer with the latest Markdown content."""
        markdown_text = self.editor.toPlainText()
        self.viewer.render_markdown(markdown_text)

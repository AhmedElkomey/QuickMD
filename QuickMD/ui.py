from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QWidget, QVBoxLayout, 
                           QApplication, QMenuBar, QMenu, QAction, QFileDialog,
                           QColorDialog, QFontDialog, QToolBar, QStatusBar)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from pathlib import Path
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from typing import Optional, Dict
import logging

from .config import Config
from .editor import Editor
from .viewer import Viewer

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config
        self.init_ui()

    def __init__(self, config: 'Config') -> None:
        super().__init__()
        self.config = config
        self.current_file: Optional[Path] = None
        self.init_ui()
        self.setup_markdown_extensions()
        self.setup_statusbar()
        
    def init_ui(self) -> None:
        """Initializes the enhanced UI components."""
        self.setWindowTitle('QuickMD')
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Initialize editor and viewer
        self.editor = Editor(self.config.get_editor_config())
        self.viewer = Viewer(self.config.get_viewer_config())
        
        # Setup UI components
        self.create_menubar()
        self.create_toolbar()
        
        # Add widgets to layout
        layout.addWidget(self.editor)
        layout.addWidget(self.viewer)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Connect signals
        self.editor.textChanged.connect(self.update_viewer)
        self.editor.textChanged.connect(self.update_status)
        
    def setup_markdown_extensions(self) -> None:
        """Sets up advanced Markdown extensions."""
        self.markdown_extensions = [
            TableExtension(),
            FencedCodeExtension(),
            CodeHiliteExtension(guess_lang=False),
            'markdown.extensions.toc',
            'markdown.extensions.footnotes',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.abbr',
            'markdown.extensions.meta'
        ]
        
    def create_menubar(self) -> None:
        """Creates the enhanced menu bar with all options."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('&File')
        
        new_action = QAction('&New', self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction('&Open', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('&Save', self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save &As...', self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu('&Edit')
        
        undo_action = QAction('&Undo', self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('&Redo', self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Format Menu
        format_menu = menubar.addMenu('F&ormat')
        
        font_action = QAction('&Font...', self)
        font_action.triggered.connect(self.change_font)
        format_menu.addAction(font_action)
        
        editor_color_action = QAction('Editor &Color...', self)
        editor_color_action.triggered.connect(self.change_editor_color)
        format_menu.addAction(editor_color_action)
        
        viewer_color_action = QAction('&Viewer Color...', self)
        viewer_color_action.triggered.connect(self.change_viewer_color)
        format_menu.addAction(viewer_color_action)
        
    def create_toolbar(self) -> None:
        """Creates the enhanced toolbar with formatting options."""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # Add toolbar actions for common Markdown formatting
        bold_action = QAction('Bold', self)
        bold_action.triggered.connect(lambda: self.insert_markdown_syntax('**'))
        toolbar.addAction(bold_action)
        
        italic_action = QAction('Italic', self)
        italic_action.triggered.connect(lambda: self.insert_markdown_syntax('*'))
        toolbar.addAction(italic_action)
        
        code_action = QAction('Code', self)
        code_action.triggered.connect(lambda: self.insert_markdown_syntax('`'))
        toolbar.addAction(code_action)
        
        link_action = QAction('Link', self)
        link_action.triggered.connect(self.insert_link)
        toolbar.addAction(link_action)
        
        image_action = QAction('Image', self)
        image_action.triggered.connect(self.insert_image)
        toolbar.addAction(image_action)
        
    def setup_statusbar(self) -> None:
        """Sets up the status bar with word count and file info."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready')
        
    def update_status(self) -> None:
        """Updates the status bar with current document info."""
        text = self.editor.toPlainText()
        words = len(text.split())
        chars = len(text)
        filename = self.current_file.name if self.current_file else 'Untitled'
        self.statusbar.showMessage(f'{filename} - Words: {words}, Characters: {chars}')
        
    def new_file(self) -> None:
        """Creates a new file."""
        self.editor.clear()
        self.current_file = None
        self.setWindowTitle('QuickMD - Untitled')
        
    def open_file(self) -> None:
        """Opens a Markdown file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'Markdown Files (*.md);;All Files (*)'
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.editor.setPlainText(file.read())
                self.current_file = Path(file_path)
                self.setWindowTitle(f'QuickMD - {self.current_file.name}')
                logging.info(f'Opened file: {file_path}')
            except Exception as e:
                logging.error(f'Error opening file: {e}')
                
    def save_file(self) -> None:
        """Saves the current file."""
        if self.current_file is None:
            self.save_file_as()
        else:
            self._save_to_file(self.current_file)
            
    def save_file_as(self) -> None:
        """Saves the file with a new name."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save File', '', 'Markdown Files (*.md);;All Files (*)'
        )
        if file_path:
            self.current_file = Path(file_path)
            self._save_to_file(self.current_file)
            self.setWindowTitle(f'QuickMD - {self.current_file.name}')
            
    def _save_to_file(self, file_path: Path) -> None:
        """Helper method to save content to file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.editor.toPlainText())
            logging.info(f'Saved file: {file_path}')
        except Exception as e:
            logging.error(f'Error saving file: {e}')
            
    def change_font(self) -> None:
        """Opens font dialog and changes editor font."""
        font, ok = QFontDialog.getFont(self.editor.font(), self)
        if ok:
            self.editor.setFont(font)
            
    def change_editor_color(self) -> None:
        """Changes editor background color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.editor.setStyleSheet(f'background-color: {color.name()};')
            
    def change_viewer_color(self) -> None:
        """Changes viewer background color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.viewer.setStyleSheet(f'background-color: {color.name()};')
            
    def insert_markdown_syntax(self, syntax: str) -> None:
        """Inserts Markdown syntax around selected text."""
        cursor = self.editor.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            cursor.insertText(f'{syntax}{selected_text}{syntax}')
        else:
            cursor.insertText(syntax)
            
    def insert_link(self) -> None:
        """Inserts a Markdown link."""
        cursor = self.editor.textCursor()
        selected_text = cursor.selectedText()
        cursor.insertText(f'[{selected_text or "link text"}](url)')
        
    def insert_image(self) -> None:
        """Inserts a Markdown image."""
        cursor = self.editor.textCursor()
        cursor.insertText('![alt text](image_url)')
        
    def update_viewer(self) -> None:
        """Updates the viewer with the latest Markdown content."""
        markdown_text = self.editor.toPlainText()
        html = markdown.markdown(
            markdown_text,
            extensions=self.markdown_extensions
        )
        self.viewer.setHtml(html)

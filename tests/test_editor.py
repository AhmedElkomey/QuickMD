import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Create QApplication instance for tests
app = QApplication(sys.argv)

from QuickMD.config import Config
from QuickMD.ui import MainWindow, Editor, Viewer

class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_config = """
                            [Editor]
                            font_size = 14
                            font_family = Arial
                            tab_width = 40

                            [Viewer]
                            background_color = #FFFFFF
                            text_color = #000000
                            """
        self.config_path = Path('test_config.ini')
        self.config_path.write_text(self.test_config)
        self.config = Config(str(self.config_path))

    def tearDown(self):
        """Clean up test fixtures."""
        self.config_path.unlink()

    def test_load_config(self):
        """Test configuration loading."""
        self.config.load_config()
        editor_config = self.config.get_editor_config()
        viewer_config = self.config.get_viewer_config()

        self.assertEqual(editor_config['font_size'], '14')
        self.assertEqual(editor_config['font_family'], 'Arial')
        self.assertEqual(viewer_config['background_color'], '#FFFFFF')
        self.assertEqual(viewer_config['text_color'], '#000000')

    def test_missing_config_file(self):
        """Test handling of missing configuration file."""
        with self.assertRaises(FileNotFoundError):
            Config('nonexistent.ini')

    def test_invalid_config_format(self):
        """Test handling of invalid configuration format."""
        invalid_config_path = Path('invalid_config.ini')
        invalid_config_path.write_text('invalid config format')
        
        try:
            with self.assertRaises(Exception):
                Config(str(invalid_config_path))
        finally:
            invalid_config_path.unlink()


class TestEditor(unittest.TestCase):
    """Test cases for the Editor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            'font_family': 'Arial',
            'font_size': '14',
            'tab_width': '40'
        }
        self.editor = Editor(self.config)

    def test_initial_configuration(self):
        """Test initial editor configuration."""
        font = self.editor.font()
        self.assertEqual(font.family(), 'Arial')
        self.assertEqual(font.pointSize(), 14)
        self.assertEqual(self.editor.tabStopWidth(), 40)

    def test_text_input(self):
        """Test basic text input functionality."""
        test_text = "Test markdown text"
        self.editor.setPlainText(test_text)
        self.assertEqual(self.editor.toPlainText(), test_text)

    def test_font_change(self):
        """Test font change functionality."""
        new_font = QFont('Courier', 12)
        self.editor.setFont(new_font)
        current_font = self.editor.font()
        self.assertEqual(current_font.family(), 'Courier')
        self.assertEqual(current_font.pointSize(), 12)


class TestViewer(unittest.TestCase):
    """Test cases for the Viewer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            'background_color': '#FFFFFF',
            'text_color': '#000000'
        }
        self.viewer = Viewer(self.config)

    def test_initial_configuration(self):
        """Test initial viewer configuration."""
        self.assertTrue(self.viewer.isReadOnly())
        style = self.viewer.styleSheet()
        self.assertIn('#FFFFFF', style)
        self.assertIn('#000000', style)

    def test_html_rendering(self):
        """Test HTML rendering functionality."""
        test_html = "<p>Test HTML content</p>"
        self.viewer.setHtml(test_html)
        self.assertIn("Test HTML content", self.viewer.toPlainText())


class TestMainWindow(unittest.TestCase):
    """Test cases for the MainWindow class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = MagicMock()
        self.config.get_editor_config.return_value = {
            'font_family': 'Arial',
            'font_size': '14',
            'tab_width': '40'
        }
        self.config.get_viewer_config.return_value = {
            'background_color': '#FFFFFF',
            'text_color': '#000000'
        }
        self.window = MainWindow(self.config)

    def test_initial_setup(self):
        """Test initial window setup."""
        self.assertEqual(self.window.windowTitle(), 'QuickMD')
        self.assertIsNone(self.window.current_file)
        self.assertIsNotNone(self.window.editor)
        self.assertIsNotNone(self.window.viewer)

    def test_new_file(self):
        """Test new file functionality."""
        self.window.editor.setPlainText("Some text")
        self.window.new_file()
        self.assertEqual(self.window.editor.toPlainText(), "")
        self.assertIsNone(self.window.current_file)

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_open_file(self, mock_file_dialog):
        """Test file opening functionality."""
        test_content = "Test markdown content"
        test_file = Path('test.md')
        try:
            # Create test file
            test_file.write_text(test_content)
            mock_file_dialog.return_value = (str(test_file), 'Markdown Files (*.md)')

            self.window.open_file()

            self.assertEqual(self.window.editor.toPlainText(), test_content)
            self.assertEqual(self.window.current_file, test_file)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_markdown_extensions(self):
        """Test Markdown extensions setup."""
        self.assertTrue(hasattr(self.window, 'markdown_extensions'))
        self.assertTrue(len(self.window.markdown_extensions) > 0)

    def test_viewer_update(self):
        """Test viewer update on editor changes."""
        test_markdown = "# Test Heading"
        self.window.editor.setPlainText(test_markdown)
        # Allow event loop to process
        QApplication.processEvents()
        viewer_content = self.window.viewer.toPlainText()
        self.assertIn("Test Heading", viewer_content)

    @patch('PyQt5.QtWidgets.QFileDialog.getSaveFileName')
    def test_save_file_as(self, mock_file_dialog):
        """Test save as functionality."""
        test_content = "Test content to save"
        test_file = Path('test_save.md')
        try:
            mock_file_dialog.return_value = (str(test_file), 'Markdown Files (*.md)')
            
            self.window.editor.setPlainText(test_content)
            self.window.save_file_as()

            self.assertTrue(test_file.exists())
            self.assertEqual(test_file.read_text(), test_content)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_insert_markdown_syntax(self):
        """Test Markdown syntax insertion."""
        self.window.editor.setPlainText("test")
        cursor = self.window.editor.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.movePosition(cursor.End, cursor.KeepAnchor)
        self.window.editor.setTextCursor(cursor)

        self.window.insert_markdown_syntax('**')
        self.assertEqual(self.window.editor.toPlainText(), "**test**")


def run_tests():
    """Run all test cases."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases to suite
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestEditor))
    suite.addTests(loader.loadTestsFromTestCase(TestViewer))
    suite.addTests(loader.loadTestsFromTestCase(TestMainWindow))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    run_tests()
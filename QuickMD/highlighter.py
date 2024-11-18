# markdown_editor/highlighter.py

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp

class MarkdownHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Markdown."""

    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Heading
        heading_format = QTextCharFormat()
        heading_format.setForeground(QColor('blue'))
        heading_format.setFontWeight(QFont.Bold)
        heading_pattern = QRegExp('^#{1,6} .+')
        self.highlighting_rules.append((heading_pattern, heading_format))

        # Bold
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        bold_pattern = QRegExp(r'\*\*(.*?)\*\*')
        self.highlighting_rules.append((bold_pattern, bold_format))

        # Italic
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        italic_pattern = QRegExp(r'\*(.*?)\*')
        self.highlighting_rules.append((italic_pattern, italic_format))

        # Code
        code_format = QTextCharFormat()
        code_format.setForeground(QColor('darkGreen'))
        code_font = QFont('Courier New')
        code_format.setFont(code_font)
        code_pattern = QRegExp(r'`([^`]+)`')
        self.highlighting_rules.append((code_pattern, code_format))

    def highlightBlock(self, text: str) -> None:
        """Applies syntax highlighting to the given block of text."""
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

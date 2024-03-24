from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget,  QPlainTextEdit, QHBoxLayout, QSizePolicy 

class OcrTextEdit(QPlainTextEdit):
    textSelectionReady= pyqtSignal(QPoint, str)
    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == 1:  # Left mouse button
            selected_text = self.textCursor().selectedText()
            if selected_text:
                self.textSelectionReady.emit(event.globalPos(), selected_text)

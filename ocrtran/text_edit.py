from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget,  QPlainTextEdit, QHBoxLayout, QSizePolicy, QMenu, QAction


class OcrTextEdit(QPlainTextEdit):
    textSelectionReady= pyqtSignal(QPoint, str)
    saveToVocabularyTriggered= pyqtSignal(QPoint, str)
    def __init__(self, parent=None):
        super().__init__(parent)


    def contextMenuEvent(self, event):
        print('creating context')
        menu = self.createStandardContextMenu()
        save_action = QAction(QIcon('./ocrtran/icons/bookmark.png'), "Save to my vocabulary", self)
        save_action.triggered.connect(self.save_to_vocabulary)
        menu.addAction(save_action)
        menu.exec_(event.globalPos())

    def save_to_vocabulary(self):
        
        selected_text = self.textCursor().selectedText()
        self.saveToVocabularyTriggered.emit(selected_text)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == 1:  # Left mouse button
            selected_text = self.textCursor().selectedText()
            if selected_text:
                self.textSelectionReady.emit(event.globalPos(), selected_text)

from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget,  QPlainTextEdit, QHBoxLayout, QSizePolicy, QMenu, QAction, QMessageBox
from ocrtran import speech
from ocrtran.utils import abspath

class FloatingButtonWidget(QPushButton):

    def __init__(self, parent, qicon=None, offset_x=0, offset_y=0):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.paddingLeft = 5
        self.paddingTop = 5
        self.offset_y=offset_y
        self.offset_x=offset_x
        if qicon:
            self.setIcon(qicon)
    def update_position(self):
        if hasattr(self.parent(), 'viewport'):
            parent_rect = self.parent().viewport().rect()
        else:
            parent_rect = self.parent().rect()

        if not parent_rect:
            return

        x = parent_rect.width() - self.width() - self.paddingLeft + self.offset_x
        y = parent_rect.height() - self.height()- self.paddingTop +self.offset_y
        self.setGeometry(x, y, self.width(), self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_position()

    #def mousePressEvent(self, event):
    #    self.parent().floatingButtonClicked.emit()


class OcrTextEdit(QPlainTextEdit):
    textSelectionReady= pyqtSignal(QPoint, str)
    saveToVocabularyTriggered= pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.language= 'en'
        self.bookmark_button = FloatingButtonWidget(self, QIcon(abspath('icons/bookmark.png')))
        self.bookmark_button.clicked.connect(self.save_to_vocabulary)

        self.playsound_button = FloatingButtonWidget(self, QIcon(abspath('icons/speaker.png')), -40,0)
        self.playsound_button.clicked.connect(self.to_speach)
        self.parent=parent
    def set_lang(self, lan):
        self.language=lan

    def to_speach(self):
        self.playsound_button.setEnabled(False)
        self.parent.set_textEdit_lang()
        #set the lang


        selected_text = self.textCursor().selectedText()
        if not selected_text:
            selected_text=self.toPlainText()
        if selected_text:
            speech.speak(selected_text, self.language)
        else:
            self.parent.showStatus('Empty words!')
        self.playsound_button.setEnabled(True)
            

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bookmark_button.update_position()
        self.playsound_button.update_position()

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        save_action = QAction(QIcon('icons/bookmark.png'), "Save to my vocabulary", self)
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

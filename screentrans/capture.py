
import sys
import io
import pytesseract
from PIL import Image

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextBrowser, QHBoxLayout,QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal 






def get_ocr_result(img, lang=None):
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_img = Image.open(io.BytesIO(buffer.data()))
    buffer.close()
    print(lang)

    try:
        return pytesseract.image_to_string(pil_img, timeout=5, lang=lang).strip()
    except RuntimeError as error:
        
        return 'Failed to ocr the screen'



class CaptureScreenWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    closed = pyqtSignal(str)
    def __init__(self, langs):
        super().__init__()
        flags=Qt.WindowFlags()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self._screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(self.getWindow()))
        self.setPalette(palette)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()


        self.langs = langs
    def get_result(self):
        return self.ocr_result

    def getWindow(self):
        return self._screen.grabWindow(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        if self.start == self.end:
            return super().paintEvent(event)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(painter.background())
        painter.drawRect(QtCore.QRect(self.start, self.end))
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        self.start = self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def snipOcr(self):
        self.hide()
        ocr_result = self.ocrOfDrawnRectangle()
        return ocr_result

    def hide(self):
        super().hide()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QApplication.processEvents()

    def ocrOfDrawnRectangle(self):
        return get_ocr_result(
            self.getWindow().copy(
                min(self.start.x(), self.end.x()),
                min(self.start.y(), self.end.y()),
                abs(self.start.x() - self.end.x()),
                abs(self.start.y() - self.end.y()),
            ),
            self.langs,
        )

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        ocr_result = self.snipOcr()
        self.closed.emit(ocr_result)
        self.close()




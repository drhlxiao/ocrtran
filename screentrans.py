#!/usr/bin/python
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
import pyperclip
from deep_translator import GoogleTranslator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Translation")
        self.setGeometry(100, 100, 500, 400)

        # Create text area
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setGeometry(50, 50, 400, 340)

        # Call translate_text automatically
        self.translate_text()

    def translate_text(self):
        # Read text from clipboard
        text_from_clipboard = pyperclip.paste()

        # Translate text
        english = GoogleTranslator(source='auto', target='en').translate(text_from_clipboard)
        # Update text in the text area
        self.text_area.clear()

        chinese= GoogleTranslator(source='auto', target='zh-CN').translate(text_from_clipboard)
        divider='-'*20

        self.text_area.insertPlainText(f"Original Text:\n{text_from_clipboard}\n\n{divider}\n English :\n{english} \n\n{divider}\n Chinese:\n{chinese}")

if __name__ == "__main__":
    # Call the executable program "textshot"
    subprocess.run(["textshot"])

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


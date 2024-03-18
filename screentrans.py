#!/usr/bin/python
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout, QTextBrowser
import pyperclip
from deep_translator import GoogleTranslator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen translator")
        self.setGeometry(100, 100, 500, 400)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        # Create text browser
        self.text_browser = QTextBrowser(self)
        layout.addWidget(self.text_browser)
        self.text_browser.setReadOnly(True)

        # Call translate_text automatically
        self.translate_text()

    def translate_text(self):
        # Read text from clipboard
        text_from_clipboard = pyperclip.paste()

        # Translate text
        english = GoogleTranslator(source='auto', target='en').translate(text_from_clipboard)
        # Update text in the text browser
        self.text_browser.clear()

        chinese= GoogleTranslator(source='auto', target='zh-CN').translate(text_from_clipboard)
        divider='-'*20
        html=f"<b>Original Text</b><br>{text_from_clipboard} <br><br> <b>English</b> <br> {english} <br><br><b> Chinese</b><br>{chinese}"
        self.text_browser.setHtml(html)

if __name__ == "__main__":
    # Call the executable program "textshot"
    subprocess.run(["textshot"])

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

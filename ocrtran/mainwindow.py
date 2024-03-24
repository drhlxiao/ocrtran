
import sys
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox, QPlainTextEdit, QHBoxLayout, QSizePolicy, QStatusBar, QMessageBox, QToolTip
from PyQt5.QtCore import Qt
from googletrans import Translator, LANGUAGES
from ocrtran.capture import CaptureScreenWindow
from ocrtran import lang 
from ocrtran import text_edit


translator = Translator()

stylesheet = """

QStatusBar QLabel {
    color: #808080; /* Muted text color */
    font-size:0.7em;
}
"""
class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()

        # Set window title
        self.setWindowTitle("Screen OCR Translator")
        self.resize(650, 500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Row #1: Label "Screen Translator"
        label = QLabel("Screen OCR Translator", self)
        #label.setText("<a href=\"https://github.com/drhlxiao/ocrtran\">Screen OCR Translator</a>");
        #label.setTextInteractionFlags(Qt.TextBrowserInteraction);
        layout.addWidget(label)

        # Row #2: Two combo boxes (comboBoxInput and comboBoxOutput)

        combo_box_layout = QHBoxLayout()
        self.comboBoxInput = QComboBox(self)
        self.label_2 = QLabel(" ➡️ ", self)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.comboBoxOutput = QComboBox(self)
        combo_box_layout.addWidget(self.comboBoxInput)
        combo_box_layout.addWidget(self.label_2)
        combo_box_layout.addWidget(self.comboBoxOutput)
        layout.addLayout(combo_box_layout)

        # Row #3: QPlainTextEdit, can be expanded in both directions
        self.source_textEdit = text_edit.OcrTextEdit(self)
        self.source_textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.translated_textEdit = QPlainTextEdit(self)
        self.translated_textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.source_textEdit)
        layout.addWidget(self.translated_textEdit)

        # Row #4: Two buttons ("Translate" and "Capture")
        button_capture = QPushButton("Capture Screen", self)

        layout.addWidget(button_capture)

        # Set the layout to the central widget
        central_widget.setLayout(layout)

        self.AddLanguages()

        # Connect button signals to slots (optional)
        #button_translate.clicked.connect(self.translate_text)
        button_capture.clicked.connect(self.capture_text)
        self.comboBoxOutput.currentIndexChanged.connect(self.translate)
        self.comboBoxInput.currentIndexChanged.connect(self.translate)

        self.source_textEdit.textChanged.connect(self.translate)
        self.source_textEdit.textSelectionReady.connect(self.translate_selected_text)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # Initialize status bar message
        self.statusBar.showMessage("Click the button [Capture screen] to start...")
        self.setStyleSheet(stylesheet)
        self.args=args
        self.translate_text=''
        if args.s:
            self.capture_text()


    def AddLanguages(self):
        self.comboBoxInput.addItem('Auto detection')
        langs=['English'] + [i.capitalize() for i in LANGUAGES.values() if i !='english' ]
        
        for i in langs:
            self.comboBoxInput.addItem(i)
            self.comboBoxOutput.addItem(i)


    def update_and_translate(self, text):
        self.statusBar.showMessage("Translating...")
        self.source_textEdit.setPlainText(text)
        self.translate()

    def translate_selected_text(self,pos, text):
        if not text:
            QToolTip.hideText()
            return

        new_translated_text =self.get_translation(text)
        if new_translated_text:
            tooltip = f"<b>{new_translated_text}</b>"
            QToolTip.showText(pos, tooltip, self)

    def get_translation(self, text):
        if not text:
            return ''
        inputlang = self.comboBoxInput.currentText()
        if not self.args.lan:
            outputlang = self.comboBoxOutput.currentText()
        else:
            outputlang=self.args.lan

        if inputlang=='Auto detection':
            translated = translator.translate(text,
                                          dest=outputlang)
        else:
            translated = translator.translate(text,
                                          src=inputlang,
                                          dest=outputlang)
        return translated.text

    def translate(self):
        text = self.source_textEdit.toPlainText()

        _tranlated_text=self.get_translation(text)

        self.translated_textEdit.setPlainText(_tranlated_text)
        self.statusBar.showMessage("")
    
    def ocr_error_handler(self,msg):
        QMessageBox.warning(self, 'Warning',msg, 
                                       QMessageBox.Ok | QMessageBox.Cancel)
    
    def capture_text(self):
        #QtWidgets.QApplication.processEvents()


        self.statusBar.showMessage("Taking screenshot...")
        inputlang = self.comboBoxInput.currentText()
        if inputlang=='Auto detection':
            language =None
        else:
            language =lang.get_tesseract_code(inputlang)

        self.w = CaptureScreenWindow(language)
        self.w.closed.connect(self.update_and_translate)
        self.w.error.connect(self.ocr_error_handler)

        self.w.show()
def parse_args():
    parser = argparse.ArgumentParser(description='OCR translator')
    # Add your command line arguments here
    parser.add_argument('--s', help='Take screenshot immediately', action='store_true', default=False)
    parser.add_argument('-lan', help='Destination languages')
    return parser.parse_args()
def main():
    args=parse_args()
    app = QApplication(sys.argv)
    w = MainWindow(args)
    w.show()
    app.exec()


if __name__=='__main__':
    main()


import sys
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox, QPlainTextEdit, QHBoxLayout, QSizePolicy, QStatusBar, QMessageBox, QToolTip, QFileDialog, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from googletrans import Translator, LANGUAGES
from ocrtran.capture import CaptureScreenWindow
from ocrtran import lang 
from ocrtran import text_edit
from ocrtran import vocabulary
from ocrtran.utils import abspath



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

        self.translated_textEdit = text_edit.OcrTextEdit(self)
        self.translated_textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.source_textEdit)
        layout.addWidget(self.translated_textEdit)

        # Row #4: Two buttons ("Translate" and "Capture")
        button_capture = QPushButton("Capture Screen", self)
        icon = QIcon(abspath("icons/capture.png"))  # Replace "icon.png" with the actual path to your icon file
        button_capture.setIcon(icon)
        layout.addWidget(button_capture)

        # Set the layout to the central widget
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        # Initialize status bar message
        self.statusBar.showMessage("Click the button [Capture screen] to start...")
        central_widget.setLayout(layout)

        # create menu bar
        menubar = self.menuBar()
        # File menu
        file_menu = menubar.addMenu("&File")
        open_file_action=file_menu.addAction("&Open")
        save_file_action=file_menu.addAction("&Save")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        open_vocabulary_action= QAction(QIcon('./ocrtran/icons/vocabulary.png'), "Open my vocabulary", self)
        tools_menu.addAction(open_vocabulary_action)


        # Help menu
        help_menu = menubar.addMenu("&Help")
        about_action=help_menu.addAction("&About")


        self.AddLanguages()

        # Connect button signals to slots (optional)
        button_capture.clicked.connect(self.capture_text)
        self.comboBoxOutput.currentIndexChanged.connect(self.translate)
        self.comboBoxInput.currentIndexChanged.connect(self.translate)

        self.source_textEdit.textChanged.connect(self.translate)
        self.source_textEdit.textSelectionReady.connect(self.translate_selected_text)
        self.source_textEdit.saveToVocabularyTriggered.connect(self.save_to_vocabulary)

        about_action.triggered.connect(self.showAboutMessageBox)
        open_vocabulary_action.triggered.connect(self.open_vocabulary)

        open_file_action.triggered.connect(self.open_file)
        save_file_action.triggered.connect(self.save_file)


        self.setStyleSheet(stylesheet)

        self.args=args
        self.translate_text=''
        if args.s:
            self.capture_text()

    def showStatus(self,msg):
        self.statusBar.showMessage(msg)



    def save_to_vocabulary(self, text):
        try:
            translated_text=self.get_translation(text)
        except Exception:
            translated_text=' '
        msg=vocabulary.save(text, translated_text)
        self.statusBar.showMessage(msg)


    def showAboutMessageBox(self):
        QMessageBox.about(self, "About", "OCR Screen Translator v1.0 <br> Author: hualin.xiao@outlook.com <br> Github: https://github.com/drhlxiao/ocrtran")

    def open_vocabulary(self):
        stat, msg=vocabulary.open_vocabulary()
        
        if stat:
            self.statusBar.showMessage(msg)
        else:
            QMessageBox.warning(self, 'Warning',msg, 
                                       QMessageBox.Ok | QMessageBox.Cancel)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File")
        if filename:
            with open(filename, 'r') as file:
                self.source_textEdit.setPlainText(file.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File")
        if filename:
            with open(filename, 'w') as file:
                file.write(self.source_textEdit.toPlainText())

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

    def set_textEdit_lang(self):
        in_lan,out_lan=self.get_current_lang()
        self.source_textEdit.set_lang(in_lan)
        self.translated_textEdit.set_lang(out_lan)


    def get_current_lang(self):
        inputlang = self.comboBoxInput.currentText()
        if inputlang=='Auto detection':
            inputlang=None

        if not self.args.lan:
            outputlang = self.comboBoxOutput.currentText()
        else:
            outputlang=self.args.lan

        return inputlang, outputlang



    def get_translation(self, text):
        if not text:
            return ''
        inputlang, outputlang=self.get_current_lang()

        if not inputlang:
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

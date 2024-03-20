
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox, QPlainTextEdit, QHBoxLayout, QSizePolicy, QStatusBar
from PyQt5.QtCore import Qt
from googletrans import Translator, LANGUAGES
from screentrans.capture import CaptureScreenWindow
from screentrans import lang 

translator = Translator()

stylesheet = """

QStatusBar QLabel {
    color: #808080; /* Muted text color */
    font-size:0.7em;
}
"""
class MainWindow(QMainWindow):
    def __init__(self):
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
        self.label_2 = QLabel(" => ", self)
        self.comboBoxOutput = QComboBox(self)
        combo_box_layout.addWidget(self.comboBoxInput)
        combo_box_layout.addWidget(self.label_2)
        combo_box_layout.addWidget(self.comboBoxOutput)
        layout.addLayout(combo_box_layout)

        # Row #3: QPlainTextEdit, can be expanded in both directions
        self.plain_text_source = QPlainTextEdit(self)
        self.plain_text_source.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.plain_text_dest = QPlainTextEdit(self)
        self.plain_text_dest.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.plain_text_source)
        layout.addWidget(self.plain_text_dest)

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

        self.plain_text_source.textChanged.connect(self.translate)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # Initialize status bar message
        self.statusBar.showMessage("Click the button [Capture screen] to start...")
        self.setStyleSheet(stylesheet)



    def AddLanguages(self):
        self.comboBoxInput.addItem('Auto detection')
        langs=['English'] + [i.capitalize() for i in LANGUAGES.values() if i !='english' ]
        
        for i in langs:
            self.comboBoxInput.addItem(i)
            self.comboBoxOutput.addItem(i)


    def update_and_translate(self, text):
        self.statusBar.showMessage("Translating...")
        self.plain_text_source.setPlainText(text)
        self.translate()

    def translate(self):
        text = self.plain_text_source.toPlainText()
        if not text:
            return
        inputlang = self.comboBoxInput.currentText()
        outputlang = self.comboBoxOutput.currentText()
        if inputlang=='Auto detection':
            translated = translator.translate(text,
                                          dest=outputlang)
        else:
            translated = translator.translate(text,
                                          src=inputlang,
                                          dest=outputlang)

        self.plain_text_dest.setPlainText(translated.text)
        self.statusBar.showMessage("")
    
    
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
        self.w.show()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


if __name__=='__main__':
    main()

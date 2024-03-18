
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox, QTextBrowser, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from googletrans import Translator, LANGUAGES
from screentrans.capture import CaptureScreenWindow

translator = Translator()

stylesheet = """
#Form {
    background-color: #f0f0f0;
}

QLabel {
    font-size: 1rem;
}

QPushButton {
    background-color: #d3d3d3; /* Light grey color */
    color: white;
    border: none;
    padding: .5rem 1rem;
    text-align: center;
    text-decoration: none;
    font-size: 1rem;
    margin: .25rem .5rem;
    border-radius: .5rem;
}

QPushButton:hover {
    background-color: #bfbfbf; /* Slightly darker grey color on hover */
}

QPlainTextEdit {
    background-color: #fff;
    border: 2px solid #d3d3d3; /* Corresponding border color */
    border-radius: .5rem;
}

QComboBox {
    background-color: #fff;
    border: 2px solid #d3d3d3; /* Corresponding border color */
    border-radius: .5rem;
    padding: .3125rem; /* Corresponds to Bootstrap 5 default padding */
}
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Screen Translator")
        self.resize(350, 500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Row #1: Label "Screen Translator"
        label = QLabel("Screen Translator", self)
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

        # Row #3: QTextBrowser, can be expanded in both directions
        self.text_browser_source = QTextBrowser(self)
        self.text_browser_source.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.text_browser_dest = QTextBrowser(self)
        self.text_browser_dest.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.text_browser_source)
        layout.addWidget(self.text_browser_dest)

        # Row #4: Two buttons ("Translate" and "Capture")
        button_capture = QPushButton("Selection", self)
        layout.addWidget(button_capture)

        # Set the layout to the central widget
        central_widget.setLayout(layout)

        self.AddLanguages()

        # Connect button signals to slots (optional)
        #button_translate.clicked.connect(self.translate_text)
        button_capture.clicked.connect(self.capture_text)
        self.comboBoxOutput.currentIndexChanged.connect(self.translate)
        self.comboBoxInput.currentIndexChanged.connect(self.translate)





    def AddLanguages(self):
        self.comboBoxInput.addItem('Auto detection')
        langs=['English'] + [i.capitalize() for i in LANGUAGES.values() if i !='english' ]
        
        for i in langs:
            self.comboBoxInput.addItem(i)
            self.comboBoxOutput.addItem(i)


    def update_and_translate(self, text):
        self.text_browser_source.setPlainText(text)
        self.translate()

    def translate(self):
        text = self.text_browser_source.toPlainText()
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

        self.text_browser_dest.setPlainText(translated.text)
    
    
    def capture_text(self):
        #QtWidgets.QApplication.processEvents()
        self.w = CaptureScreenWindow()
        self.w.closed.connect(self.update_and_translate)
        self.w.show()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


if __name__=='__main__':
    main()
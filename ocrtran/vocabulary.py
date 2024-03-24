from PyQt5.QtCore import QStandardPaths
from pathlib import Path
import platform

USER_DATA_DIR = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
VOC_PATH=Path(USER_DATA_DIR)/"ocrtran"
VOC_FILE= VOC_PATH/"vocabulary.txt"

def save(text, translated_text):
    #Create the directory if it doesn't exist
    VOC_PATH.mkdir(parents=True, exist_ok=True)    # Append text to the file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text_with_timestamp = f"{timestamp}, {text}, {translated_text}\n"
    # Append text to the file
    with open(VOC_FILE, "a") as file:
        file.write(text_with_timestamp)
    return VOC_FILE
def open():
    filename = VOC_FILE
    if not filename.exists():
        return False, f'{filename} does not exist!'

    if platform.system() == 'Windows':
        os.startfile(filename)
    else:
        import subprocess
        subprocess.Popen(["xdg-open", filename])

    return True, f'{filename} opened using system default app!'

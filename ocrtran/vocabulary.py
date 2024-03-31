from PyQt5.QtCore import QStandardPaths
from pathlib import Path
import platform
from datetime import datetime

USER_DATA_DIR = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
VOC_PATH=Path(USER_DATA_DIR)/"ocrtran"
VOC_FILE= VOC_PATH/"vocabulary.jsonl"

def save(inlan, text, outlan,  translated_text):
    if not text:
        return "No words selected!"
    #Create the directory if it doesn't exist
    VOC_PATH.mkdir(parents=True, exist_ok=True)    # Append text to the file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "timestamp": timestamp,
        "source": text,
        'source_lang':inlan,
        "translation": translated_text,
        'out_lang':outlan
    }
    # Append text to the file
    with open(VOC_FILE, "a") as file:
        json.dump(data, file)
        file.write('\n')
    return f"Saved to vocabulary: {VOC_FILE} !"
def open_vocabulary():
    filename = VOC_FILE
    if not filename.exists():
        return False, f'{filename} does not exist!'

    if platform.system() == 'Windows':
        os.startfile(filename)
    else:
        import subprocess
        subprocess.Popen(["xdg-open", filename])

    return True, f'{filename} opened using system default app!'

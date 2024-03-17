import subprocess
import tkinter as tk
import pyperclip
import textshot
from deep_translator import GoogleTranslator

def translate_text(text_area):
    # Read text from clipboard
    text_from_clipboard = pyperclip.paste()
    print(text_from_clipboard)

    # Translate text
    translated_text = GoogleTranslator(source='auto', target='en').translate(text_from_clipboard)

    # Update text in the text area
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"Original Text:\n{text_from_clipboard}\n\nTranslated Text:\n{translated_text}")

# Call the executable program "textshot"
subprocess.run(["textshot"])
#textshot.main()

# Create the Tkinter window
window = tk.Tk()
window.title("Text Translation")

# Create a text area
text_area = tk.Text(window, height=10, width=50)
text_area.pack()

# Button to translate text
#translate_button = tk.Button(window, text="Translate Text", command=translate_text)
#translate_button.pack()
translate_text(text_area)


# Start the Tkinter event loop
window.mainloop()

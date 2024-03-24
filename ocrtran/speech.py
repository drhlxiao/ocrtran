from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time
mixer.init()
TTS_LAN={
        'English':'en',
        'Chinese (simplified)':'Zh-CN',
        'German':'de',
        'French':'fr',
        'Spanish':'es',
        'Portuguese':'pt'}

def get_tts_lang_code(lan):
    return TTS_LAN.get(lan,None)

def to_mp3(text, lang='en'):
    lang=TTS_LAN.get(lang,lang)
    if not lang:
        lang='en'
    mp3_fp = BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(mp3_fp)
    return mp3_fp
def speak(text,lang='en'):
    sound = to_mp3(text,lang)
    sound.seek(0)
    mixer.music.load(sound, "mp3")
    mixer.music.play()
    time.sleep(1)

from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import time

TTS_LAN = {
    'English': 'en',
    'Chinese (simplified)': 'zh-CN',
    'German': 'de',
    'French': 'fr',
    'Spanish': 'es',
    'Portuguese': 'pt'
}

def get_tts_lang_code(lan):
    return TTS_LAN.get(lan, None)

def to_mp3(text, lang='en'):
    lang = TTS_LAN.get(lang, lang)
    if not lang:
        lang = 'en'
    mp3_fp = BytesIO()
    tts = gTTS(text, lang=lang)
    tts.write_to_fp(mp3_fp)
    return mp3_fp

def speak(text, lang='en'):
    sound = to_mp3(text, lang)
    sound.seek(0)
    audio = AudioSegment.from_mp3(sound)
    play(audio)
    time.sleep(audio.duration_seconds)


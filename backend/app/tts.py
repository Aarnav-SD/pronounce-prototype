from gtts import gTTS
from uuid import uuid4
from pathlib import Path

def create_tts(text: str, language="hi"):
    filename = f"tts_{uuid4().hex}.mp3"
    path = Path("uploads") / filename

    tts = gTTS(text=text, lang=language)
    tts.save(path)

    return path

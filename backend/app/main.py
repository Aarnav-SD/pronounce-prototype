from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from backend.app.transcribe import transcribe_audio
from backend.app.scoring import score_text
from backend.app.tts import create_tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.post("/process-audio/")
async def process_audio(
    file: UploadFile = File(...),
    target_text: str = Form(...),
    language: str = Form("hi")
):
    filepath = UPLOAD_DIR / file.filename

    with filepath.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    transcription, segments = transcribe_audio(str(filepath), language)

    results = score_text(transcription, target_text)

    tts_path = create_tts(target_text, language)
    tts_url = f"/static/{tts_path.name}"

    return {
        "transcription": transcription,
        "word_results": results,
        "tts_url": tts_url
    }

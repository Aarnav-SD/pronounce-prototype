import whisper

# Load a better model for Hindi
model = whisper.load_model("medium")   # or "medium" if your CPU/GPU allows

def transcribe_with_words(audio_path: str, language: str = "hi"):
    result = model.transcribe(
        audio_path,
        language=language,
        task="transcribe",
        word_timestamps=True,
        fp16=False   # important for CPU stability
    )

    words = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": float(w["start"]),
                "end": float(w["end"])
            })

    return {
        "text": result["text"],
        "words": words
    }

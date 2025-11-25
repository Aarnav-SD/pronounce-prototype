import whisper

model = whisper.load_model("tiny")  # or "medium", "large" if GPU available

def transcribe_audio(filepath: str, language="hi"):
    result = model.transcribe(filepath, language=language)
    text = result.get("text", "").strip()
    segments = result.get("segments", [])
    
    normalized_segments = []
    for s in segments:
        normalized_segments.append({
            "text": s.get("text", "").strip(),
            "start": float(s.get("start", 0)),
            "end": float(s.get("end", 0))
        })
    
    return text, normalized_segments

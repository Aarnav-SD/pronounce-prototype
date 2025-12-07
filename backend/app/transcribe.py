import re
from .model_loader import get_model

def transcribe_with_words(audio_path: str, language: str = "hi"):
    """
    Transcribes audio with forced native-script output for Indic languages.
    Solves transliteration + Gujarati vowel repetition issues.
    """

    model = get_model()

    # Native script prompts
    SCRIPT_PROMPTS = {
        "hi": "नमस्ते, यह हिन्दी भाषा है। कृपया देवनागरी लिपि में लिखें।",
        "ta": "வணக்கம், இது தமிழ். தயவுசெய்து தமிழ் எழுத்தில் எழுதுங்கள்.",
        "te": "నమస్కారం, ఇది తెలుగు. దయచేసి తెలుగు లిపిలో రాయండి.",
        "kn": "ನಮಸ್ಕಾರ, ಇದು ಕನ್ನಡ. ದಯವಿಟ್ಟು ಕನ್ನಡ ಲಿಪಿಯಲ್ಲಿ ಬರೆಯಿರಿ.",
        "gu": "નમસ્તે, આ ગુજરાતી છે. કૃપા કરી ગુજરાતી લિપિમાં લખો.",
        "mr": "नमस्कार, ही मराठी भाषा आहे.",
        "en": "Hello, this is English transcription."
    }

    selected_prompt = SCRIPT_PROMPTS.get(language, "")
    print(f"🤖 AI Config -> Language='{language}' | Prompt='{selected_prompt[:25]}...'")

    # FIRST TRANSCRIPTION ATTEMPT
    segments, info = model.transcribe(
        audio_path,
        language=language,
        task="transcribe",
        initial_prompt=selected_prompt,
        word_timestamps=True,
        beam_size=5,
        temperature=0.0
    )

    # join text properly
    full_text = "".join([s.text for s in segments if hasattr(s, "text")]).strip()
    print(f"📝 Raw Output: {full_text}")

    # ----------------------------------------------
    # FIX 1: Prevent English transliteration
    # ----------------------------------------------
    if language in ["kn", "ta", "te", "gu", "ml"]:
        english_count = len(re.findall(r"[A-Za-z]", full_text))
        
        if english_count > len(full_text) * 0.15:
            print("⚠️ Detected English transliteration! Retrying with higher temperature...")

            segments_retry, info2 = model.transcribe(
                audio_path,
                language=language,
                task="transcribe",
                initial_prompt=selected_prompt,
                word_timestamps=True,
                beam_size=5,
                temperature=0.3   # helps native script decoding
            )

            full_text = "".join([s.text for s in segments_retry if hasattr(s, "text")]).strip()
            print(f"🔄 Retry Output: {full_text}")

            segments = segments_retry  # use retry segments
    

    # ----------------------------------------------
    # FIX 2: Gujarati vowel-flooding clean-up
    # ----------------------------------------------
    if language == "gu":
        cleaned = re.sub("ા{2,}", "ા", full_text)
        full_text = cleaned.strip()


    # ----------------------------------------------
    # WORD TIMESTAMPS
    # ----------------------------------------------
    words = []
    for seg in segments:
        if seg.words:
            for w in seg.words:
                words.append({
                    "word": w.word,
                    "start": w.start,
                    "end": w.end
                })

    return {
        "text": full_text,
        "words": words
    }

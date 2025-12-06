import whisper
import torch
import os
from .model_loader import get_model




def transcribe_with_words(audio_path: str, language: str = "hi"):
    """
    Transcribes audio while forcefully preventing English translation.
    """
    model = get_model()
    # 1. AGGRESSIVE SCRIPT PROMPTS
    # These tell the AI: "The following audio is in THIS language. Write in THIS script."
    SCRIPT_PROMPTS = {
        # Hindi: Devanagari
        "hi": "नमस्ते, मेरा नाम राज है। यह हिन्दी भाषा है।",
        
        # Tamil: Tamil Script (Not English!)
        "ta": "வணக்கம், இது தமிழ் மொழி. ஆங்கிலத்தில் எழுத வேண்டாம்.",
        
        # Telugu: Telugu Script
        "te": "నమస్కారం, ఇది తెలుగు భాష. దయచేసి తెలుగులోనే రాయండి.",
        
        # Kannada: Kannada Script
        "kn": "ನಮಸ್ಕಾರ, ಇದು ಕನ್ನಡ ಭಾಷೆ. ದಯచేಸಿ ಕನ್ನಡದಲ್ಲಿ ಬರೆಯಿರಿ.",
        
        # Gujarati: Gujarati Script
        "gu": "નમસ્તે, આ ગુજરાતી ભાષા છે. કૃપા કરીને ગુજરાતીમાં લખો.",
        
        # Marathi: Devanagari
        "mr": "नमस्कार, ही मराठी भाषा आहे.",
        
        # English
        "en": "Hello, this is an English transcription."
    }

    # Get the specific prompt (Default to Hindi if missing)
    selected_prompt = SCRIPT_PROMPTS.get(language, "")
    
    print(f"   🤖 AI Config -> Language: '{language}' | Prompt: '{selected_prompt[:20]}...'")

    # 2. RUN TRANSCRIPTION
    result = model.transcribe(
        audio_path,
        language=language,      # Forces the specific language decoder
        task="transcribe",      # Forces Transcription (NOT Translation)
        initial_prompt=selected_prompt, # <--- The Magic Key
        
        # Technical Settings for Accuracy
        fp16=False,             # False ensures CPU compatibility
        temperature=0.0,        # 0.0 makes it factual (no creativity)
        condition_on_previous_text=False, # Prevents looping
        word_timestamps=True    # Needed for detailed scoring
    )

    # 3. FORMAT OUTPUT
    words = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            words.append({
                "word": w.get("word", "").strip(),
                "start": float(w.get("start", 0.0)),
                "end": float(w.get("end", 0.0)),
            })

    full_text = result.get("text", "").strip()
    
    # Debug: Show what the AI actually wrote
    print(f"   📝 Raw AI Output: {full_text}")

    return {
        "text": full_text,
        "words": words
    }
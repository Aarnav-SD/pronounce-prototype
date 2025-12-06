import difflib
from .transcribe import transcribe_with_words

# We don't need librosa or TTS for this stage. 
# We focus on intelligent text comparison.

def compute_per_word_scores(target_text, lang_code, audio_path):
    """
    Compares Target Text vs AI Recognized Text using Fuzzy Logic.
    Solves the 'Mujhe' vs 'Muje' 0% score issue.
    """
    
    # 1. TRANSCRIBE
    # We pass the file to Whisper to get the text
    transcription_result = transcribe_with_words(audio_path, lang_code)
    recognized_text = transcription_result["text"]
    
    # 2. PREPARE LISTS
    target_words = target_text.strip().split()
    recog_words = recognized_text.strip().split()
    
    # 3. ALIGNMENT & SCORING
    # SequenceMatcher finds the best alignment between the two sentences
    matcher = difflib.SequenceMatcher(None, target_words, recog_words)
    
    detailed_words = []
    total_score = 0
    matched_count = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        
        # --- CASE 1: EXACT MATCH ---
        if tag == 'equal':
            for i in range(i1, i2):
                word_score = 100.0
                detailed_words.append({
                    "word": target_words[i],
                    "recognized": target_words[i],
                    "status": "correct",
                    "total_score": word_score
                })
                total_score += word_score
                matched_count += 1
        
        # --- CASE 2: SUBSTITUTION (The Fix) ---
        # Example: Target="मुझे", Recog="मूजे"
        elif tag == 'replace':
            len_target = i2 - i1
            len_recog = j2 - j1
            
            # Compare words one-by-one in this chunk
            for k in range(max(len_target, len_recog)):
                t_word = target_words[i1 + k] if k < len_target else ""
                r_word = recog_words[j1 + k] if k < len_recog else ""
                
                if t_word and r_word:
                    # Calculate Character Similarity Ratio
                    # This gives partial points for close spellings
                    similarity = difflib.SequenceMatcher(None, t_word, r_word).ratio()
                    word_score = round(similarity * 100, 1)
                else:
                    word_score = 0.0

                # Determine if it's "Good Enough" (Green) or "Bad" (Red)
                # We use 80% as the threshold for 'Green'
                status = "correct" if word_score >= 80 else "incorrect"
                
                detailed_words.append({
                    "word": t_word if t_word else "(Extra)",
                    "recognized": r_word if r_word else "(Missed)",
                    "status": status,
                    "total_score": word_score
                })
                
                if t_word:
                    total_score += word_score
                    matched_count += 1

        # --- CASE 3: DELETION (Missed Word) ---
        elif tag == 'delete':
            for i in range(i1, i2):
                detailed_words.append({
                    "word": target_words[i],
                    "recognized": "-",
                    "status": "incorrect",
                    "total_score": 0.0
                })
                matched_count += 1
        
        # --- CASE 4: INSERTION (Extra Noise) ---
        elif tag == 'insert':
            # We generally don't penalize for background noise words, 
            # we just ignore them in the count but show them in UI if needed.
            for j in range(j1, j2):
                pass 

    # 4. FINAL CALCULATIONS
    if matched_count > 0:
        final_pronunciation_score = round(total_score / matched_count, 1)
    else:
        final_pronunciation_score = 0.0

    # Reading Accuracy: strictly how many were > 90% match
    perfect_matches = len([w for w in detailed_words if w['total_score'] >= 90])
    reading_accuracy = round((perfect_matches / len(target_words) * 100), 1) if target_words else 0

    return {
        "overall_pronunciation_score": final_pronunciation_score,
        "overall_text_score": reading_accuracy,
        "words": detailed_words
    }
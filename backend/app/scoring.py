import re
from difflib import SequenceMatcher

def clean(t: str):
    t = t.lower()
    t = re.sub(r"[^a-zA-Z\u0900-\u097F ]", "", t)
    return t.strip()

def score_text(transcription: str, expected: str):
    expected_words = clean(expected).split()
    spoken_words = clean(transcription).split()

    sm = SequenceMatcher(a=expected_words, b=spoken_words)
    results = []

    for tag, e0, e1, s0, s1 in sm.get_opcodes():
        if tag == "equal":
            for i in range(e1 - e0):
                word = expected_words[e0 + i]
                results.append({"word": word, "correct": True})
        else:
            for i in range(e0, e1):
                word = expected_words[i]
                results.append({"word": word, "correct": False})

    return results

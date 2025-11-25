import streamlit as st
import requests
import tempfile

BACKEND_URL = "http://localhost:8000/process-audio/"

st.title("Hindi Pronunciation Checker (Local Whisper)")
st.write("Record your voice and check pronunciation — works fully offline.")

target_text = st.text_input("Enter Hindi sentence:", "यह एक सरल परीक्षण है")

audio_data = st.audio_input("Record your voice")

if audio_data and st.button("Check Pronunciation"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_data.read())
        filepath = tmp.name

    files = {"file": open(filepath, "rb")}
    data = {"target_text": target_text, "language": "hi"}

    with st.spinner("Processing..."):
        response = requests.post(BACKEND_URL, data=data, files=files)

    if response.status_code == 200:
        res = response.json()
        st.write("DEBUG WORD RESULTS:", res["word_results"])

        st.write("### Transcription:")
        st.write(res["transcription"])

        st.write("### Word Analysis:")
        for w in res["word_results"]:
            color = "green" if w["correct"] else "red"
            st.markdown(f"<span style='color:{color}'>{w['word']}</span>", unsafe_allow_html=True)

        st.write("### Correct Pronunciation (TTS):")
        st.audio("http://localhost:8000" + res["tts_url"])

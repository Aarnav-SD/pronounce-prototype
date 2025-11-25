<h1>🗣️ Multilingual Pronunciation Learning System (Prototype)</h1>

<p>
An open-source, offline pronunciation-learning tool for Indian languages, using:
</p>

<ul>
<li><b>Whisper</b> (Speech-to-Text)</li>
<li><b>FastAPI Backend</b></li>
<li><b>Streamlit Frontend</b></li>
<li><b>gTTS</b> for TTS</li>
<li><b>Hybrid Scoring (Text + Pronunciation)</b> — coming soon</li>
</ul>

<hr>

<h2>🚀 Features (Current)</h2>
<ul>
<li>Speech recording/upload</li>
<li>Offline transcription using Whisper</li>
<li>Hindi support</li>
<li>Basic text matching</li>
<li>TTS playback of expected sentence</li>
<li>Streamlit UI</li>
<li>FastAPI backend</li>
</ul>

<h2>📌 Planned Features</h2>
<ul>
<li>Word-level scoring</li>
<li>Pronunciation evaluation (speech embeddings)</li>
<li>Hybrid scoring (text + audio)</li>
<li>Forced alignment with WhisperX</li>
<li>Multi-language support</li>
<li>Improved UI visualization</li>
<li>Latency optimization</li>
</ul>

<hr>

<h2>📂 Project Structure</h2>

<pre>
backend/
  app/
    main.py           → FastAPI server
    transcribe.py     → Whisper transcription
    scoring.py        → text scoring (to be upgraded)
    tts.py            → gTTS output
frontend/
  app.py              → Streamlit UI
uploads/
requirements.txt
</pre>

<hr>

<h2>🛠️ Installation Guide</h2>

<h3>1️⃣ Clone the repository</h3>
<pre>
git clone &lt;your-repo-url&gt;
cd pronounce-prototype
</pre>

<h3>2️⃣ Create and activate virtual environment</h3>

<b>Windows:</b>
<pre>
python -m venv .venv
.\.venv\Scripts\activate
</pre>

<b>Mac/Linux:</b>
<pre>
python3 -m venv .venv
source .venv/bin/activate
</pre>

<h3>3️⃣ Install dependencies</h3>
<pre>
pip install --upgrade pip
pip install -r requirements.txt
</pre>

<hr>

<h2>🎧 Installing FFmpeg</h2>

<h3>Windows</h3>
<ol>
<li>Download FFmpeg from: <a href="https://www.gyan.dev/ffmpeg/builds/">https://www.gyan.dev/ffmpeg/builds/</a></li>
<li>Extract to: <code>C:\ffmpeg\</code></li>
<li>Add to PATH:
<pre>
C:\ffmpeg\bin
</pre>
</li>
<li>Verify:
<pre>ffmpeg -version</pre></li>
</ol>

<h3>Mac</h3>
<pre>brew install ffmpeg</pre>

<h3>Ubuntu/Linux</h3>
<pre>sudo apt install ffmpeg</pre>

<hr>

<h2>▶️ Running Backend</h2>
<pre>
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
</pre>

<h2>▶️ Running Frontend</h2>
<pre>
cd frontend
streamlit run app.py
</pre>

<hr>

<h2>📣 Contributing</h2>
<p>Tasks your team will build next:</p>
<ul>
<li>Hybrid scoring engine</li>
<li>Speech embeddings with Wav2Vec2-XLSR</li>
<li>Multilingual support</li>
<li>Word-level segmentation</li>
<li>Forced alignment improvements</li>
<li>UI visualization</li>
</ul>

<h2>📝 License</h2>
<p>MIT License</p>

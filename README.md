# 🗣️ Pronunciation Evaluator (German, can be multilingual) — Local Whisper App

This is a local Python application to evaluate spoken German sentences using OpenAI's Whisper model. Users upload audio (`.webm`, usually connected with a frontend sending request to this), and the app provides a pronunciation score and feedback compared to a set of expected sentences.

## 📁 Project Structure

```
├── main.py                # Backend logic (or whisper_utils.py for modular usage)
├── whisper_utils.py       # (Optional) Modular Whisper processing
├── requirements.txt       # Python dependencies
├── render.yaml            # (Ignore if using locally)
├── temp_audio.webm        # Temp uploaded audio file (auto-created/deleted)
└── __pycache__/           # Python cache
```

## 🧠 How It Works

1. Accepts an audio recording (WebM format).
2. Transcribes the audio using [OpenAI Whisper](https://github.com/openai/whisper).
3. Compares it against a predefined sentence (based on `phrase_id`).
4. Scores the pronunciation using character-level similarity.
5. Outputs:
   - Expected vs Spoken sentence
   - Accuracy Score
   - Mispronounced letters

---

## 🖥️ Setup & Run Locally

### 1. Clone this repo

```bash
git clone https://github.com/krish-1010/whisper-voice-processing
cd whisper-voice-processing
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

- `openai-whisper`
- `ffmpeg-python` (ensure system ffmpeg is installed)
- `uvicorn`, `fastapi` (for API usage)

### 4. Install ffmpeg (required)

Download ffmpeg:

- Windows: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
- Linux/macOS: via `brew` or `apt`

Ensure `ffmpeg` is in your system PATH.

### 5. Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 6. Test the API (Example with curl)

```bash
curl -X POST "http://localhost:8000/evaluate/1-1" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_audio_file.webm"
```

---

## 🗂️ Supported Sentences

You can find all supported sentence IDs and phrases inside `main.py` or `whisper_utils.py` under `EXPECTED_PHRASES`.

Example:

```python
"1-1": "Ich bin müde"
"2-3": "Kannst du helfen?"
```

---

## 📄 Sample Output

```json
{
  "expected": "Ich bin müde",
  "spoken": "und bin mut",
  "score": 50.0,
  "feedback": "🗣️ Mispronounced letters: i, c, h, ü, d, e"
}
```

---

## 💡 Notes

- WebM audio is expected (convert if needed).
- You may extend this with a frontend or voice recording interface.
- For offline usage, small or tiny Whisper models are ideal.

---

## 📜 License

MIT

---

## 🙏 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- [FastAPI](https://fastapi.tiangolo.com/)

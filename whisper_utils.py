import whisper
import difflib
import re
import tempfile
import os

# Load model once globally
model = whisper.load_model("small")  # or 'tiny' if you prefer super fast but lower accuracy

EXPECTED_PHRASES = {
    "1-1": "Ich bin müde",
    "1-2": "Wie geht es dir?",
    "1-3": "Guten Morgen",
    "2-1": "Ich liebe Schokolade",
    "2-2": "Wo ist der Bahnhof?",
    "2-3": "Kannst du helfen?",
    "3-1": "Es regnet heute",
    "3-2": "Ich verstehe nicht",
    "3-3": "Wie spät ist es?",
    "4-1": "Ich habe Hunger",
    "4-2": "Der Apfel ist rot",
    "4-3": "Ich lerne Deutsch",
    "5-1": "Das Wetter ist schön",
    "5-2": "Was machst du?",
    "5-3": "Ich bin Student",

}

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.strip()
    return text

def transcribe_and_evaluate(audio_bytes: bytes, phrase_id: str):
    # Save to a temporary file in memory
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_path = temp_audio_file.name

    try:
        # Direct transcription from the webm file itself (no manual ffmpeg needed separately)
        result = model.transcribe(temp_audio_path, language="de")
        spoken = result.get("text", "").strip()

        expected = EXPECTED_PHRASES.get(phrase_id, "")

        expected_clean = clean_text(expected)
        spoken_clean = clean_text(spoken)

        similarity = difflib.SequenceMatcher(None, expected_clean, spoken_clean).ratio()

        return {
            "expected": expected,
            "spoken": spoken,
            "score": round(similarity * 100, 2),
            "feedback": generate_feedback(expected, spoken)
        }
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)  # Always delete temp file after done

def generate_feedback(expected: str, actual: str) -> str:
    expected_clean = clean_text(expected)
    actual_clean = clean_text(actual)

    diffs = list(difflib.ndiff(expected_clean, actual_clean))
    wrongs = [d[2] for d in diffs if d.startswith('- ') or d.startswith('+ ')]

    if not wrongs:
        return "✅ Perfect pronunciation!"
    return f"🗣️ Mispronounced letters: {', '.join(wrongs)}"

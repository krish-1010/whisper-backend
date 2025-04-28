from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from whisper_utils import transcribe_and_evaluate
import os

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate/{phrase_id}")
async def evaluate(phrase_id: str, file: UploadFile = File(...)):
    # Read the uploaded file content
    audio_bytes = await file.read()

    # Pass bytes directly to function
    result = transcribe_and_evaluate(audio_bytes, phrase_id)

    return result

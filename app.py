from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from tts_engine import init_chapters, generate_chapter_audio

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    chapter: int

@app.post("/generate")
def generate(req: TTSRequest):
    init_chapters(req.text)
    path = generate_chapter_audio(f"chapter_{req.chapter}")
    return FileResponse(path, media_type="audio/wav")
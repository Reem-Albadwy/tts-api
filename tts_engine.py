import os
import re
from pydub import AudioSegment
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.to("cuda")
wav_path = os.path.join(os.path.dirname(__file__), "voice_ref.wav")

chapter_store = {}

def split_chapters(text):
    pattern = r'ف[\u064B-\u0652]*ص[\u064B-\u0652]*ل[\u064B-\u0652]*\s*\d+\s*:'
    splits = re.split(pattern, text)
    headers = re.findall(pattern, text)

    chapters = []
    for header, body in zip(headers, splits[1:]):
        chapters.append((header.strip(), body.strip()))
    return chapters

def split_sentences(text):
    return [s.strip() for s in re.split(r'[.،!?؟]', text) if s.strip()]

def init_chapters(text):
    global chapter_store
    chapters = split_chapters(text)
    chapter_store = {
        f"chapter_{i+1}": {
            "text": content,
            "audio_path": None,
            "generated": False
        }
        for i, (_, content) in enumerate(chapters)
    }

def generate_chapter_audio(chapter_id):
    chapter = chapter_store[chapter_id]

    if chapter["generated"]:
        return chapter["audio_path"]

    sentences = split_sentences(chapter["text"])
    final_audio = AudioSegment.empty()

    for i, sentence in enumerate(sentences):
        temp_path = f"tmp_{chapter_id}_{i}.wav"

        tts.tts_to_file(
            text=sentence,
            speaker_wav=wav_path,
            language="ar",
            file_path=temp_path,
            split_sentences=False
        )

        audio = AudioSegment.from_wav(temp_path)
        final_audio += audio

    out_path = f"{chapter_id}.wav"
    final_audio.export(out_path, format="wav")

    chapter["audio_path"] = out_path
    chapter["generated"] = True

    return out_path

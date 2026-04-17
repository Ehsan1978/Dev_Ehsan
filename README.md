# Voice Memo Recorder

A simple desktop app for:

- Recording voice memos
- Playing back saved memos
- Transcribing a selected memo

## Requirements

- Python 3.10+
- A working microphone and speaker output

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python voice_memo_app.py
```

## Notes

- Memos are saved as `.wav` files in the `memos/` folder.
- Transcription uses the `faster-whisper` library with the `tiny` model.
- The first transcription may take longer while model files download.

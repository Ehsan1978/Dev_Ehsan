# Voice Memo Recorder (Browser App)

This app is browser-based and should be launched through a local server (not by opening `index.html` directly with `file://`).

## Features

- Record voice memos from your microphone
- Playback recordings immediately
- Optional live transcription while recording (browser speech recognition)
- Download or delete individual memos

## Easiest Way to Open

Use one of these launcher files in this folder:

- **Windows:** double-click `run_app.bat`
- **Linux/macOS:** run `./run_app.sh` in terminal
- **Any OS with Python:** run `python launch_voice_memo.py`

The launcher starts a local server and opens the browser automatically.

## Manual Start (alternative)

```bash
python -m http.server 8000
```

Then open:

- http://127.0.0.1:8000/index.html

## Browser Notes

- Recording requires a modern browser with `MediaRecorder` support.
- Transcription uses SpeechRecognition API (`webkitSpeechRecognition` on many Chromium browsers).
- If transcription is unsupported, recording/playback still work.

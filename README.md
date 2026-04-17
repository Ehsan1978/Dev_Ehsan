# Voice Memo Recorder (Browser App)

This app is now browser-based so you can open and use it more easily.

## Features

- Record voice memos from your microphone
- Playback recordings immediately
- Optional live transcription while recording (browser speech recognition)
- Download or delete individual memos

## Quick Start

From this repository folder:

```bash
python -m http.server 8000
```

Then open:

- http://localhost:8000/index.html

> Tip: microphone access works best when served over `http://localhost` (not `file://`).

## Browser Notes

- Recording requires a modern browser with `MediaRecorder` support.
- Transcription uses the browser SpeechRecognition API (`webkitSpeechRecognition` on many Chromium browsers).
- If transcription is unsupported, recording/playback still work.

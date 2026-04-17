# Voice Memo Recorder (Browser App)

If the app was "not launching" before, use the launcher scripts below (instead of double-clicking `index.html`).

## Launch

- **Windows:** double-click `run_app.bat`
- **Linux/macOS:** run `./run_app.sh`
- **Any OS:** run `python launch_voice_memo.py` (or `py launch_voice_memo.py` on Windows)

The launcher will:

1. Start a local web server from this folder
2. Pick an available port automatically
3. Print the exact URL
4. Try to open your default browser

If the browser does not open automatically, copy/paste the printed URL manually.

## Features

- Record voice memos from microphone
- Playback recordings immediately
- Optional live transcription while recording (browser speech recognition)
- Download or delete memos

## Browser Notes

- Recording requires `MediaRecorder` support.
- Transcription uses SpeechRecognition / `webkitSpeechRecognition`.
- If transcription is unsupported, recording/playback still work.

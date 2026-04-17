import queue
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

import sounddevice as sd
import soundfile as sf


MEMO_DIR = Path("memos")
SAMPLE_RATE = 16_000
CHANNELS = 1


class VoiceMemoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Voice Memo Recorder")
        self.root.geometry("760x520")

        MEMO_DIR.mkdir(parents=True, exist_ok=True)

        self.is_recording = False
        self.stream = None
        self.recorded_chunks = []
        self.record_queue: queue.Queue = queue.Queue()

        self._build_ui()
        self.refresh_memos()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(0, 10))

        self.record_btn = ttk.Button(actions, text="Start Recording", command=self.toggle_recording)
        self.record_btn.pack(side="left")

        self.play_btn = ttk.Button(actions, text="Play Selected", command=self.play_selected)
        self.play_btn.pack(side="left", padx=8)

        self.transcribe_btn = ttk.Button(actions, text="Transcribe Selected", command=self.transcribe_selected)
        self.transcribe_btn.pack(side="left")

        self.status_var = tk.StringVar(value="Ready")
        status = ttk.Label(actions, textvariable=self.status_var)
        status.pack(side="right")

        list_frame = ttk.LabelFrame(container, text="Saved Memos", padding=8)
        list_frame.pack(fill="both", expand=True)

        self.memo_list = tk.Listbox(list_frame, height=8)
        self.memo_list.pack(fill="both", expand=True)

        refresh_btn = ttk.Button(list_frame, text="Refresh", command=self.refresh_memos)
        refresh_btn.pack(anchor="e", pady=(8, 0))

        transcript_frame = ttk.LabelFrame(container, text="Transcript", padding=8)
        transcript_frame.pack(fill="both", expand=True, pady=(12, 0))

        self.transcript_box = tk.Text(transcript_frame, wrap="word", height=10)
        self.transcript_box.pack(fill="both", expand=True)

    def toggle_recording(self) -> None:
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def _audio_callback(self, indata, frames, time_info, status) -> None:  # noqa: ANN001
        if status:
            print(status)
        self.record_queue.put(indata.copy())

    def _collect_audio(self) -> None:
        while self.is_recording:
            try:
                chunk = self.record_queue.get(timeout=0.2)
                self.recorded_chunks.append(chunk)
            except queue.Empty:
                continue

    def start_recording(self) -> None:
        self.recorded_chunks = []
        self.is_recording = True
        self.record_btn.configure(text="Stop Recording")
        self.status_var.set("Recording...")

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=self._audio_callback,
        )
        self.stream.start()

        threading.Thread(target=self._collect_audio, daemon=True).start()

    def stop_recording(self) -> None:
        if not self.is_recording:
            return

        self.is_recording = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        self.record_btn.configure(text="Start Recording")
        self.status_var.set("Saving memo...")

        if not self.recorded_chunks:
            self.status_var.set("No audio captured")
            return

        audio = self._merge_chunks()
        filename = MEMO_DIR / f"memo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        sf.write(filename, audio, SAMPLE_RATE)

        self.status_var.set(f"Saved: {filename.name}")
        self.refresh_memos()

    def _merge_chunks(self):
        import numpy as np

        return np.concatenate(self.recorded_chunks, axis=0)

    def refresh_memos(self) -> None:
        self.memo_list.delete(0, tk.END)
        files = sorted(MEMO_DIR.glob("*.wav"), reverse=True)
        for file in files:
            self.memo_list.insert(tk.END, file.name)

    def _selected_file(self) -> Path | None:
        selected = self.memo_list.curselection()
        if not selected:
            messagebox.showinfo("Select a memo", "Please select a memo first.")
            return None
        return MEMO_DIR / self.memo_list.get(selected[0])

    def play_selected(self) -> None:
        file_path = self._selected_file()
        if file_path is None:
            return

        try:
            data, samplerate = sf.read(file_path)
            sd.play(data, samplerate)
            self.status_var.set(f"Playing: {file_path.name}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Playback error", str(exc))
            self.status_var.set("Playback failed")

    def transcribe_selected(self) -> None:
        file_path = self._selected_file()
        if file_path is None:
            return

        self.status_var.set("Transcribing...")
        self.transcribe_btn.configure(state="disabled")

        thread = threading.Thread(target=self._run_transcription, args=(file_path,), daemon=True)
        thread.start()

    def _run_transcription(self, file_path: Path) -> None:
        try:
            from faster_whisper import WhisperModel

            model = WhisperModel("tiny", compute_type="int8")
            segments, _info = model.transcribe(str(file_path))
            text = " ".join(segment.text.strip() for segment in segments).strip()
            if not text:
                text = "No speech recognized."

            self.root.after(0, self._display_transcript, file_path.name, text)
        except ModuleNotFoundError:
            msg = (
                "Transcription requires 'faster-whisper'.\n"
                "Install dependencies from requirements.txt and try again."
            )
            self.root.after(0, self._transcription_error, msg)
        except Exception as exc:  # noqa: BLE001
            self.root.after(0, self._transcription_error, str(exc))

    def _display_transcript(self, filename: str, text: str) -> None:
        self.transcript_box.delete("1.0", tk.END)
        self.transcript_box.insert(tk.END, f"{filename}\n\n{text}")
        self.transcribe_btn.configure(state="normal")
        self.status_var.set("Transcription complete")

    def _transcription_error(self, message: str) -> None:
        self.transcribe_btn.configure(state="normal")
        self.status_var.set("Transcription failed")
        messagebox.showerror("Transcription error", message)


def main() -> None:
    root = tk.Tk()
    app = VoiceMemoApp(root)

    def on_close() -> None:
        if app.is_recording:
            app.stop_recording()
        sd.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()

"""Trisakra Transcript Studio - Week 1
Transcripts, subtitles and meeting notes, fully offline.
Powered by faster-whisper (open source). MIT License.
"""
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_NAME = "Trisakra Transcript Studio"
MODELS = ["tiny", "base", "small", "medium"]  # faster -> more accurate


def ts(seconds, sep=","):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02}{sep}{ms:03}"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("820x600")
        self.file_path = None
        self.segments = []  # (start, end, text)
        self.busy = False

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")
        ttk.Button(top, text="Choose audio/video file", command=self.pick_file).pack(side="left")
        self.file_label = ttk.Label(top, text="No file selected")
        self.file_label.pack(side="left", padx=10)

        opts = ttk.Frame(self, padding=(10, 0))
        opts.pack(fill="x")
        ttk.Label(opts, text="Accuracy:").pack(side="left")
        self.model_var = tk.StringVar(value="small")
        ttk.Combobox(opts, textvariable=self.model_var, values=MODELS,
                     state="readonly", width=8).pack(side="left", padx=5)
        self.go_btn = ttk.Button(opts, text="Transcribe", command=self.start)
        self.go_btn.pack(side="left", padx=10)

        words = ttk.Frame(self, padding=(10, 6, 10, 0))
        words.pack(fill="x")
        ttk.Label(words, text="Auto-corrections (wrong=right; wrong=right):").pack(side="left")
        self.words_var = tk.StringVar(value="transcripts studio=Trisakra Transcript Studio")
        ttk.Entry(words, textvariable=self.words_var).pack(side="left", fill="x", expand=True, padx=6)

        self.progress = ttk.Progressbar(self, mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=10, pady=8)
        self.status = ttk.Label(self, text="Ready. First run downloads the model (one time).")
        self.status.pack(fill="x", padx=10)

        self.text = tk.Text(self, wrap="word", font=("Segoe UI", 11))
        self.text.pack(fill="both", expand=True, padx=10, pady=8)

        bottom = ttk.Frame(self, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Save as TXT", command=lambda: self.save("txt")).pack(side="left")
        ttk.Button(bottom, text="Save as SRT", command=lambda: self.save("srt")).pack(side="left", padx=5)
        ttk.Button(bottom, text="Save as VTT", command=lambda: self.save("vtt")).pack(side="left")

    def pick_file(self):
        p = filedialog.askopenfilename(
            filetypes=[("Audio/Video", "*.mp3 *.wav *.m4a *.flac *.ogg *.mp4 *.mkv *.mov *.avi *.webm"),
                       ("All files", "*.*")])
        if p:
            self.file_path = p
            self.file_label.config(text=p.split("/")[-1].split("\\")[-1])

    def start(self):
        if self.busy:
            return
        if not self.file_path:
            messagebox.showinfo(APP_NAME, "Please choose a file first.")
            return
        self.busy = True
        self.custom_words = self.words_var.get().strip()
        self.go_btn.config(state="disabled")
        self.text.delete("1.0", "end")
        self.segments = []
        self.progress["value"] = 0
        threading.Thread(target=self.work, daemon=True).start()

    def set_status(self, msg):
        self.after(0, lambda: self.status.config(text=msg))

    def work(self):
        try:
            self.set_status("Loading model...")
            from faster_whisper import WhisperModel
            model = WhisperModel(self.model_var.get(), device="cpu", compute_type="int8")
            self.set_status("Transcribing...")
            pairs = []
            for item in self.custom_words.split(";"):
                if "=" in item:
                    a, b = item.split("=", 1)
                    if a.strip():
                        pairs.append((a.strip(), b.strip()))

            def fix(t):
                for a, b in pairs:
                    t = re.sub(re.escape(a), b, t, flags=re.IGNORECASE)
                return t

            segs, info = model.transcribe(self.file_path, vad_filter=True)
            total = info.duration or 1
            for s in segs:
                text = fix(s.text.strip())
                self.segments.append((s.start, s.end, text))
                line = f"[{ts(s.start, '.')[:-4]}] {text}\n"
                pct = min(100, s.end / total * 100)
                self.after(0, lambda l=line, p=pct: self.add_line(l, p))
            self.set_status(f"Done. Detected language: {info.language}")
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(APP_NAME, f"Something went wrong:\n{e}"))
            self.set_status("Error. See message.")
        finally:
            self.after(0, self.finish)

    def add_line(self, line, pct):
        self.text.insert("end", line)
        self.text.see("end")
        self.progress["value"] = pct

    def finish(self):
        self.busy = False
        self.go_btn.config(state="normal")
        self.progress["value"] = 100

    def save(self, kind):
        if not self.segments:
            messagebox.showinfo(APP_NAME, "Nothing to save yet.")
            return
        path = filedialog.asksaveasfilename(defaultextension=f".{kind}",
                                            filetypes=[(kind.upper(), f"*.{kind}")])
        if not path:
            return
        out = []
        if kind == "txt":
            out = [t for _, _, t in self.segments]
        elif kind == "srt":
            for i, (a, b, t) in enumerate(self.segments, 1):
                out += [str(i), f"{ts(a)} --> {ts(b)}", t, ""]
        else:
            out = ["WEBVTT", ""]
            for a, b, t in self.segments:
                out += [f"{ts(a, '.')} --> {ts(b, '.')}", t, ""]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        messagebox.showinfo(APP_NAME, "Saved.")


if __name__ == "__main__":
    App().mainloop()

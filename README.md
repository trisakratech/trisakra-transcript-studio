# Trisakra Transcript Studio

**Transcripts, subtitles and meeting notes, fully offline.**

Turn audio or video into text on your own Windows PC. No account, no uploads.
Powered by [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (open source).

> **Status: early version (v0.1).** It works, but expect rough edges. Feedback welcome.

## Features
- Transcribe audio/video files (MP3, WAV, M4A, MP4, MKV and more)
- Automatic language detection
- Choose speed vs accuracy (tiny, base, small, medium)
- Auto-corrections for names and brands (`wrong=right; wrong=right`)
- Export as TXT, SRT and VTT subtitles
- Runs fully offline (the model downloads once on first use)

## How to run
1. Install [Python 3.11 or newer](https://www.python.org/downloads/) and tick **"Add Python to PATH"**.
2. Download this project into a folder.
3. Open a command window in that folder and run:
   ```
   pip install -r requirements.txt
   python app.py
   ```

## Roadmap
- Editable transcript before saving
- One-click Windows installer (.exe)
- Meeting recording, summaries, speaker labels, translation (Pro)

## License
MIT. Made by Trisakra Technologies.

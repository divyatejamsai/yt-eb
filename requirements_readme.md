# YouTube Podcast → Book Pipeline

This project converts selected YouTube podcast episodes into a structured book using automated transcript processing and LLM-based summarization.

The pipeline processes podcast episodes through several stages:

1. Download audio from YouTube
2. Convert audio to WAV
3. Transcribe audio using Whisper
4. Extract chapter timestamps
5. Split transcripts by chapters
6. Extract key bullet points
7. Clean bullet points
8. Convert bullets into explanatory paragraphs
9. Build chapters
10. Combine chapters into a final book

---

# System Requirements

Before running the project, make sure the following are installed.

### Python
Python **3.10 or higher** is required.

Check your version:

```bash
python3 --version
```

---

# Install Required System Dependencies

These tools are required for downloading audio and processing it.

### macOS (using Homebrew)

Install Homebrew if needed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install required tools:

```bash
brew install ffmpeg
brew install yt-dlp
```

---

### Ubuntu / Linux

```bash
sudo apt update
sudo apt install ffmpeg
pip install yt-dlp
```

---

# Project Setup

Clone the repository and enter the project directory.

```bash
git clone <repo-url>
cd <repo-name>
```

---

# Create Virtual Environment

Create a Python virtual environment.

```bash
python3 -m venv venv
```

---

# Activate the Virtual Environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

After activation your terminal should show:

```
(venv)
```

---

# Install Python Dependencies

The Python dependencies are listed in:

```
scripts/requirements.txt
```

Install them using:

```bash
pip install -r scripts/requirements.txt
```

This installs:

- openai-whisper
- torch
- tqdm
- requests
- numpy

---

# Project Structure

```
data/
  audio/                # downloaded audio files
  chapters/             # youtube chapter timestamps
  transcripts/
      raw/              # full transcripts from whisper
      chunks/           # transcripts split by chapter
  bullets/              # extracted bullet points
  corrections/          # manual corrections if needed
  episode_links.txt     # youtube episode links

scripts/
  download_audio.py
  convert_to_wav.py
  transcribe_audio.py
  chapter_timeline.py
  split_transcripts_by_chapters.py
  bullets_extraction.py
  clean_bullets.py
  bullets_to_paragraphs.py
  build_chapters.py
  build_book.py
  build_book.sh
  requirements.txt
```

---

# Adding Episodes

Add the YouTube episode links to:

```
data/episode_links.txt
```

Example:

```
https://youtu.be/xxxx
https://youtu.be/yyyy
https://youtu.be/zzzz
```

One link per line.

---

# Running the Full Pipeline

From the project root directory run:

```bash
chmod +x scripts/build_book.sh
./scripts/build_book.sh
```

This executes the full pipeline:

```
YouTube
  ↓
audio download
  ↓
wav conversion
  ↓
Whisper transcription
  ↓
chapter extraction
  ↓
transcript splitting
  ↓
bullet extraction
  ↓
paragraph generation
  ↓
chapter generation
  ↓
final book
```

---

# Output

The final generated book will be produced as:

```
book.md
```

(or whichever format `build_book.py` outputs)

---

# Notes

- Whisper **base model** is used for transcription.
- Audio is converted to **16kHz mono WAV** for optimal speech recognition.
- Chapter timestamps are extracted directly from YouTube metadata.

---

# Possible Improvements

Future improvements could include:

- Faster transcription using `faster-whisper`
- Parallel processing of episodes
- Automatic PDF / EPUB export
- Improved summarization models
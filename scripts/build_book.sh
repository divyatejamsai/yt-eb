#!/bin/bash

set -euo pipefail

echo "========================================"
echo "STEP 1: Downloading audio from YouTube"
echo "========================================"
python scripts/download_audio.py


echo "========================================"
echo "STEP 2: Converting audio to WAV"
echo "========================================"
python scripts/convert_to_wav.py


echo "========================================"
echo "STEP 3: Transcribing audio with Whisper"
echo "========================================"
python scripts/transcribe_audio.py


echo "========================================"
echo "STEP 4: Generating chapter timestamps"
echo "========================================"
python scripts/chapter_timeline.py


echo "========================================"
echo "STEP 5: Splitting transcripts by chapters"
echo "========================================"
python scripts/split_transcripts_by_chapters.py


echo "========================================"
echo "STEP 6: Extracting bullets"
echo "========================================"
python scripts/bullets_extraction.py


echo "========================================"
echo "STEP 7: Cleaning bullets"
echo "========================================"
python scripts/clean_bullets.py


echo "========================================"
echo "STEP 8: Converting bullets → paragraphs"
echo "========================================"
python scripts/bullets_to_paragraphs.py


echo "========================================"
echo "STEP 9: Building chapters"
echo "========================================"
python scripts/build_chapters.py


echo "========================================"
echo "STEP 10: Building final book"
echo "========================================"
python scripts/build_book.py


echo "========================================"
echo "BOOK BUILD COMPLETE"
echo "========================================"
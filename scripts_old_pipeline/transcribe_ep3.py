from pathlib import Path
import mlx_whisper

# Pointing to the clean WAV file to prevent FFmpeg hangs
AUDIO_FILE = "data/audio/ep3_vc.wav"
OUT_FILE = Path("data/transcripts/raw/ep3_vc.txt")

# Fixed the repository name (using turbo for speed on Mac)
MODEL = "mlx-community/whisper-large-v3-turbo"

def main():

    print("Loading MLX Whisper model:", MODEL)

    print("\n--- TRANSCRIPTION START ---\n")

    result = mlx_whisper.transcribe(
        AUDIO_FILE,
        path_or_hf_repo=MODEL,
        word_timestamps=False,
        verbose=True   # Enables live printing
    )

    segments = result["segments"]

    lines = []

    for seg in segments:
        text = seg["text"].strip()
        if text:
            lines.append(text)

    print("\n--- TRANSCRIPTION COMPLETE ---\n")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Added utf-8 encoding to prevent crash on save
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Saved transcript →", OUT_FILE)

if __name__ == "__main__":
    main()
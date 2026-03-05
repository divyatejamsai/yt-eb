import subprocess
from pathlib import Path

AUDIO_DIR = Path("data/audio")

def main():
    if not AUDIO_DIR.exists() or not AUDIO_DIR.is_dir():
        print(f"Error: Directory '{AUDIO_DIR}' not found!")
        return

    print("Starting batch conversion of WebM files to WAV...")
    print("-" * 48)

    # Strictly target ONLY .webm files
    webm_files = list(AUDIO_DIR.glob("*.webm"))
    
    if not webm_files:
        print("No .webm files found in the directory.")
        return

    for file_path in webm_files:
        out_file = file_path.with_suffix(".wav")
        
        print(f"Converting: {file_path.name} -> {out_file.name}")

        command = [
            "ffmpeg", 
            "-y",                # Overwrite existing files
            "-v", "quiet",       # Suppress output unless it's an error
            "-i", str(file_path),
            "-ar", "16000",      # Force 16kHz sample rate
            "-ac", "1",          # Force mono channel
            "-c:a", "pcm_s16le", # Force 16-bit PCM codec
            str(out_file)
        ]

        try:
            subprocess.run(command, check=True)
            print("  ✓ Success")
        except subprocess.CalledProcessError:
            print("  ✗ Failed")

    print("-" * 48)
    print("All done! Your WebM files are now WAVs.")

if __name__ == "__main__":
    main()
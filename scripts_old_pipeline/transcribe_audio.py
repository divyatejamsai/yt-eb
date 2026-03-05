import whisper
import json
from pathlib import Path

AUDIO_DIR = Path("data/audio")
OUTPUT_DIR = Path("data/transcripts/raw")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("Loading Whisper base model...")
    model = whisper.load_model("base")

    wav_files = sorted(AUDIO_DIR.glob("*.wav"))

    if not wav_files:
        print("No wav files found in data/audio/")
        return

    for wav in wav_files:

        episode = wav.stem  # ep3, ep7, ep9 ...

        print(f"\nTranscribing {episode}...")

        result = model.transcribe(
            str(wav),
            fp16=False,
            verbose=False,
            condition_on_previous_text=False
        )

        output_file = OUTPUT_DIR / f"{episode}.json"

        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Saved transcript -> {output_file}")


if __name__ == "__main__":
    main()
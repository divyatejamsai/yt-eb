import os
import json
import re

RAW_TRANSCRIPTS_DIR = "data/transcripts/raw"
CHAPTERS_DIR = "data/chapters"
OUTPUT_DIR = "data/transcripts/chunks"


def clean_title(title):
    """
    Convert chapter title into safe filename
    """
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]", "", title)
    title = title.replace(" ", "_")
    return title


def load_chapters(chapter_file):
    """
    Load chapter timestamps
    Format inside chapters.txt:
    start|end|title
    """

    chapters = []

    with open(chapter_file, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            start, end, title = line.split("|")

            chapters.append({
                "start": float(start),
                "end": float(end),
                "title": title
            })

    return chapters


def split_transcript(transcript_path, chapters, episode):

    with open(transcript_path, "r") as f:
        transcript = json.load(f)

    segments = transcript["segments"]

    episode_output_dir = os.path.join(OUTPUT_DIR, episode)
    os.makedirs(episode_output_dir, exist_ok=True)

    for i, chapter in enumerate(chapters):

        start = chapter["start"]
        end = chapter["end"]
        title = chapter["title"]

        cleaned_title = clean_title(title)

        chapter_segments = []

        for seg in segments:

            seg_start = seg["start"]

            if start <= seg_start < end:
                chapter_segments.append(seg["text"])

        chapter_text = " ".join(chapter_segments)

        filename = f"{i+1:02d}_{cleaned_title}.txt"

        output_path = os.path.join(episode_output_dir, filename)

        with open(output_path, "w") as f:
            f.write(title + "\n\n")
            f.write(chapter_text)

        print(f"Saved: {output_path}")


def main():

    for file in os.listdir(RAW_TRANSCRIPTS_DIR):

        if not file.endswith(".json"):
            continue

        transcript_path = os.path.join(RAW_TRANSCRIPTS_DIR, file)

        # ep3_vc.json -> ep3
        episode = file.split("_")[0]

        chapter_file = os.path.join(CHAPTERS_DIR, episode, "chapters.txt")

        if not os.path.exists(chapter_file):
            print(f"No chapters found for {episode}")
            continue

        print(f"\nProcessing {episode}")

        chapters = load_chapters(chapter_file)

        split_transcript(transcript_path, chapters, episode)


if __name__ == "__main__":
    main()
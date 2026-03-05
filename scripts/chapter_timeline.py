import subprocess
import json
from pathlib import Path

EPISODES = [3,7,9,14,15,16,18,20,21,24]

LINK_FILE = "episode_links.txt"
CHAPTER_ROOT = Path("data/chapters")

CHAPTER_ROOT.mkdir(parents=True, exist_ok=True)


def get_video_json(url):
    """Run yt-dlp --dump-json and return parsed JSON"""
    
    result = subprocess.run(
        ["yt-dlp", "--dump-json", url],
        capture_output=True,
        text=True,
        check=True
    )

    return json.loads(result.stdout)


def main():

    with open(LINK_FILE) as f:
        links = [l.strip() for l in f if l.strip()]

    for ep, url in zip(EPISODES, links):

        print(f"Extracting chapters for ep{ep}")

        data = get_video_json(url)

        chapters = data.get("chapters", [])

        ep_dir = CHAPTER_ROOT / f"ep{ep}"
        ep_dir.mkdir(parents=True, exist_ok=True)

        output_file = ep_dir / "chapters.txt"

        with open(output_file, "w") as f:
            for c in chapters:

                start = c["start_time"]
                end = c["end_time"]
                title = c["title"]

                f.write(f"{start}|{end}|{title}\n")


if __name__ == "__main__":
    main()
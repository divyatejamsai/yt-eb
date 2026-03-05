import subprocess
from pathlib import Path

# Episodes in the same order as links
EPISODES = [3,7,9,14,15,16,18,20,21,24]

LINK_FILE = "episode_links.txt"
AUDIO_DIR = Path("data/audio")

AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


def main():

    with open(LINK_FILE) as f:
        links = [l.strip() for l in f if l.strip()]

    for ep, url in zip(EPISODES, links):

        output_file = AUDIO_DIR / f"ep{ep}.webm"

        cmd = f"""
        yt-dlp -f bestaudio \
        -o "{output_file}" \
        "{url}"
        """

        print(f"\nDownloading EP{ep}")
        run(cmd)


if __name__ == "__main__":
    main()
import subprocess
from pathlib import Path

AUDIO_DIR = Path("data/audio")


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


def main():

    webm_files = list(AUDIO_DIR.glob("*.webm"))

    for webm in webm_files:

        wav = webm.with_suffix(".wav")

        cmd = f"""
        ffmpeg -y -i "{webm}" -ar 16000 -ac 1 "{wav}"
        """

        print(f"Converting {webm.name} → {wav.name}")

        run(cmd)


if __name__ == "__main__":
    main()
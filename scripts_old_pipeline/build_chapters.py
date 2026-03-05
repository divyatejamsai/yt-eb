from pathlib import Path

SECTIONS_ROOT = Path("data/sections")
CHAPTERS_ROOT = Path("data/chapters")


def format_title(filename):
    """
    Convert filenames to readable titles.

    Example:
    02_vidit_aatreys_story.txt -> Vidit Aatreys Story
    """

    name = filename.stem

    # remove leading numbers
    parts = name.split("_")

    if parts[0].isdigit():
        parts = parts[1:]

    title = " ".join(parts).title()

    return title


def build_episode_chapter(ep_dir):

    print(f"Building chapter for {ep_dir.name}")

    section_files = sorted(ep_dir.glob("*.txt"))

    sections = []

    for file in section_files:

        text = file.read_text().strip()

        if not text:
            continue

        title = format_title(file)

        sections.append(f"## {title}\n\n{text}")

    chapter_text = "\n\n".join(sections)

    out_file = CHAPTERS_ROOT / f"{ep_dir.name}.txt"

    out_file.write_text(chapter_text)


def main():

    CHAPTERS_ROOT.mkdir(parents=True, exist_ok=True)

    for ep in sorted(SECTIONS_ROOT.iterdir()):

        if ep.is_dir():
            build_episode_chapter(ep)


if __name__ == "__main__":
    main()
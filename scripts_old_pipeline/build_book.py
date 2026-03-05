from pathlib import Path

CHAPTERS_ROOT = Path("data/chapters")
BOOK_ROOT = Path("data/book")

BOOK_TITLE = "Startup Conversations"
AUTHOR = "Podcast Knowledge Extractor"


def clean_title(filename):
    """
    Convert file names into readable titles
    Example:
    ep3_old.txt -> Episode 3
    """

    name = filename.stem

    if name.startswith("ep"):
        num = name[2:]
        return f"Episode {num}"

    return name.replace("_", " ").title()


def build_book():

    BOOK_ROOT.mkdir(parents=True, exist_ok=True)

    book_file = BOOK_ROOT / "book.md"

    chapters = sorted(CHAPTERS_ROOT.glob("*.txt"))

    parts = []

    # book title
    parts.append(f"# {BOOK_TITLE}\n")
    parts.append(f"### {AUTHOR}\n\n")

    for ch in chapters:

        title = clean_title(ch)

        print(f"Adding {title}")

        text = ch.read_text().strip()

        if not text:
            continue

        parts.append(f"\n\n# {title}\n\n")
        parts.append(text)

    book_text = "\n".join(parts)

    book_file.write_text(book_text)

    print("\nBook written to:", book_file)


if __name__ == "__main__":
    build_book()
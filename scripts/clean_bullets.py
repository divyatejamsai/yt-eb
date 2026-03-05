from pathlib import Path

# -------------------------
# CONFIG
# -------------------------

BULLET_ROOT = Path("data/bullets")

MIN_BULLET_LENGTH = 25


# -------------------------
# NAME CORRECTIONS
# -------------------------

NAME_CORRECTIONS = {
    "Vidith Atre": "Vidit Aatrey",
    "Vidit Atrey": "Vidit Aatrey",
    "Misho": "Meesho",
    "Micho": "Meesho",
    "Kishor Biyani": "Kishore Biyani",
    "Rameshwaram Café": "Rameshwaram Cafe",
}


# -------------------------
# NORMALIZE NAMES
# -------------------------

def normalize_names(text):

    for wrong, correct in NAME_CORRECTIONS.items():
        text = text.replace(wrong, correct)

    return text


# -------------------------
# CLEAN BULLETS
# -------------------------

def clean_bullets(bullets):

    cleaned = []
    seen = set()

    for bullet in bullets:

        bullet = bullet.strip()

        if not bullet:
            continue

        # ensure bullet starts with bullet character
        if not bullet.startswith("•"):
            continue

        # remove very short bullets
        if len(bullet) < MIN_BULLET_LENGTH:
            continue

        # normalize names
        bullet = normalize_names(bullet)

        # remove duplicates
        if bullet in seen:
            continue

        seen.add(bullet)
        cleaned.append(bullet)

    return cleaned


# -------------------------
# PROCESS FILE
# -------------------------

def process_file(file_path):

    text = file_path.read_text()

    bullets = text.splitlines()

    cleaned = clean_bullets(bullets)

    file_path.write_text("\n".join(cleaned))


# -------------------------
# MAIN
# -------------------------

def main():

    episodes = sorted(BULLET_ROOT.iterdir())

    for episode_dir in episodes:

        if not episode_dir.is_dir():
            continue

        print(f"Cleaning episode: {episode_dir.name}")

        files = sorted(episode_dir.glob("*.txt"))

        for file in files:

            try:
                process_file(file)

            except Exception as e:

                print(f"Failed cleaning {file}: {e}")


if __name__ == "__main__":
    main()
from pathlib import Path

INPUT_ROOT = Path("data/sections")
OUTPUT_ROOT = Path("chapters")

OUTPUT_ROOT.mkdir(exist_ok=True)


def combine_episode(ep_dir):

    paras = []

    para_files = sorted(ep_dir.glob("para_*.txt"))

    for p in para_files:

        with open(p) as f:
            text = f.read().strip()

            if text:
                paras.append(text)

    chapter = "\n\n".join(paras)

    out_file = OUTPUT_ROOT / f"{ep_dir.name}.md"

    with open(out_file, "w") as f:
        f.write(chapter)

    print(f"Built chapter → {out_file.name}")


def main():

    for ep in INPUT_ROOT.iterdir():

        if ep.is_dir():
            combine_episode(ep)


if __name__ == "__main__":
    main()
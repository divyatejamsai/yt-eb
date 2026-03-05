from pathlib import Path
import json

BULLET_ROOT = Path("data/bullets")
OUT_ROOT = Path("data/topic_maps")

OUT_ROOT.mkdir(exist_ok=True)


def parse_topic_file(path):

    topic_map = {}
    current_topic = None

    with open(path) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("•"):

                if current_topic is None:
                    continue

                topic_map[current_topic].append(line)

            else:

                current_topic = line
                topic_map.setdefault(current_topic, [])

    return topic_map


def process_episode(ep_dir):

    episode_map = {}

    topic_files = sorted(ep_dir.glob("*topics*.txt"))

    for file in topic_files:

        topic_map = parse_topic_file(file)

        for topic, bullets in topic_map.items():

            episode_map.setdefault(topic, []).extend(bullets)

    out_file = OUT_ROOT / f"{ep_dir.name}_topic_map.json"

    with open(out_file, "w") as f:
        json.dump(episode_map, f, indent=2)

    print(f"Saved topic map → {ep_dir.name}")


def main():

    for ep in BULLET_ROOT.iterdir():

        if ep.is_dir():
            process_episode(ep)


if __name__ == "__main__":
    main()
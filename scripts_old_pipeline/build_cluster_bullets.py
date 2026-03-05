from pathlib import Path
import json

MAP_ROOT = Path("data/topic_maps")
CLUSTER_ROOT = Path("data/topic_clusters")

OUT_ROOT = Path("data/final_clusters")

OUT_ROOT.mkdir(exist_ok=True)


def build_episode(cluster_file):

    episode = cluster_file.stem.replace("_clusters", "")

    topic_map_file = MAP_ROOT / f"{episode}_topic_map.json"

    with open(cluster_file) as f:
        clusters = json.load(f)

    with open(topic_map_file) as f:
        topic_map = json.load(f)

    episode_dir = OUT_ROOT / episode
    episode_dir.mkdir(exist_ok=True)

    for cluster_id, topics in clusters.items():

        bullets = []

        for topic in topics:

            bullets += topic_map.get(topic, [])

        # remove duplicates but preserve order
        bullets = list(dict.fromkeys(bullets))

        out_file = episode_dir / f"cluster_{cluster_id}.txt"

        with open(out_file, "w") as f:

            for b in bullets:
                f.write(b + "\n")

    print(f"Built cluster bullet files → {episode}")


def main():

    for cluster_file in CLUSTER_ROOT.glob("*.json"):
        build_episode(cluster_file)


if __name__ == "__main__":
    main()
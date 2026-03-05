# pip install sentence-transformers scikit-learn

from pathlib import Path
import json
import re

from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering


MAP_ROOT = Path("data/topic_maps")
OUT_ROOT = Path("data/topic_clusters")

OUT_ROOT.mkdir(exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

DIST_THRESHOLD = 0.6


def normalize(title):

    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()

    return title


def cluster_episode(file):

    with open(file) as f:
        topic_map = json.load(f)

    original_topics = list(topic_map.keys())

    normalized_topics = [normalize(t) for t in original_topics]

    embeddings = model.encode(normalized_topics)

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=DIST_THRESHOLD
    )

    labels = clustering.fit_predict(embeddings)

    clusters = {}

    for topic, label in zip(original_topics, labels):

        clusters.setdefault(int(label), []).append(topic)

    episode = file.stem.replace("_topic_map", "")

    out_file = OUT_ROOT / f"{episode}_clusters.json"

    with open(out_file, "w") as f:
        json.dump(clusters, f, indent=2)

    print(f"Clustered topics → {episode}")


def main():

    for file in MAP_ROOT.glob("*.json"):
        cluster_episode(file)


if __name__ == "__main__":
    main()
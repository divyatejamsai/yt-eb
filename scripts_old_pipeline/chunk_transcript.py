import sys
from pathlib import Path


def split_into_chunks(text, max_words=1200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk_words = words[i:i + max_words]
        chunks.append(" ".join(chunk_words))

    return chunks


def main(input_txt, output_dir):
    with open(input_txt) as f:
        text = f.read()

    chunks = split_into_chunks(text)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for i, chunk in enumerate(chunks, 1):
        with open(f"{output_dir}/chunk_{i:03}.txt", "w") as f:
            f.write(chunk)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
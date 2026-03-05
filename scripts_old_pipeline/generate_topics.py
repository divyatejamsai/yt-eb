import os
import requests
from pathlib import Path

MODEL = "qwen2.5:7b"

INPUT_ROOT = Path("data/bullets")
OUTPUT_ROOT = Path("data/topics")

PROMPT = """
You are organizing factual statements into thematic groups.

Group the following bullet points into logical topics.

Rules:
- Each topic must have a short title.
- Place relevant bullets under each topic.
- Do NOT modify bullet wording.
- Do NOT invent information.
- Do NOT remove bullets.
- Use the bullets exactly as given.
- Use every bullet exactly once.
- Do NOT duplicate bullets.
- Do NOT add markdown formatting.
- Do NOT use # or ###.
- Topic titles must be plain text.
- Create multiple specific topics instead of one large topic.Seperate topics when possible 
Format Rules:

- Topic title on one line
- Bullets below it
- Each bullet must start with "•"

Example:

Title1

• bullet
• bullet

Title2

• bullet
• bullet
"""


def call_llm(prompt):

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0
        }
    )

    return r.json()["response"]


def process_episode(ep_dir):

    input_file = ep_dir / "filtered_bullets.txt"

    if not input_file.exists():
        return

    with open(input_file) as f:
        bullets = f.read()

    full_prompt = PROMPT + "\n\nBullets:\n\n" + bullets

    print(f"Clustering {ep_dir.name}")

    output = call_llm(full_prompt)

    out_dir = OUTPUT_ROOT / ep_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "topics.txt", "w") as f:
        f.write(output)


def main():

    for ep in INPUT_ROOT.iterdir():
        if ep.is_dir():
            process_episode(ep)


if __name__ == "__main__":
    main()
import requests
from pathlib import Path

MODEL = "qwen2.5:7b"

INPUT_ROOT = Path("data/final_clusters")
OUTPUT_ROOT = Path("data/sections")

PROMPT = """
You are converting factual bullet points into clear explanatory prose.

This is NOT a summarization task.
This is NOT creative writing.

Your task is to convert the bullet points into readable paragraphs while preserving the factual information exactly.

STRICT RULES

- Use ONLY the information contained in the bullets.
- Do NOT add any new facts.
- Do NOT add interpretations, conclusions, or explanations.
- Do NOT introduce background knowledge.
- Do NOT exaggerate or generalize.
- Do NOT add motivational or business advice language.
- Do NOT add section titles or introductions.
- Do NOT mention speakers, podcasts, or discussions.
- Preserve all numbers exactly.
- Preserve all names exactly.
- If multiple consecutive sentences refer to the same person, use pronouns such as "he" or "she" after the first mention when the reference is unambiguous.
- Treat each numbered fact independently. Each fact should correspond to one sentence in the output when possible.

CONTENT RULES

- Every statement in the output must correspond directly to a bullet.
- Do not merge unrelated bullets into speculative claims.
- If two bullets describe separate facts, they should remain separate sentences.
- If a bullet is unclear, skip it.

STYLE RULES

- Write in neutral explanatory prose.
- Convert bullet points into full sentences.
- Maintain factual tone.
- Avoid repetition.

BULLETS
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

    print(f"\nProcessing {ep_dir.name}")

    out_dir = OUTPUT_ROOT / ep_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)

    cluster_files = sorted(ep_dir.glob("cluster_*.txt"))

    for i, cluster_file in enumerate(cluster_files):

        with open(cluster_file) as f:
            raw = [l.strip("• ").strip() for l in f.readlines() if l.strip()]

        facts = []
        for i, b in enumerate(raw, 1):
            facts.append(f"{i}. {b}")

        bullets = "\n".join(facts)

        full_prompt = PROMPT + "\n\n" + bullets

        print(f"  cluster {i+1}")

        response = call_llm(full_prompt)

        with open(out_dir / f"para_{i+1}.txt", "w") as f:
            f.write(response)


def main():

    for ep in INPUT_ROOT.iterdir():
        if ep.is_dir():
            process_episode(ep)


if __name__ == "__main__":
    main()
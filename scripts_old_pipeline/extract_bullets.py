import requests
from pathlib import Path
from tqdm import tqdm

# -------------------------
# CONFIG
# -------------------------

MODEL = "qwen2.5:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

CHUNK_ROOT = Path("data/transcripts/chunks")
BULLET_ROOT = Path("data/bullets")

# -------------------------
# PROMPT
# -------------------------

PROMPT = """
You are extracting factual statements from a podcast transcript.

Your task is to convert valid transcript sentences into short factual bullet points.

STRICT RULES

- Use ONLY information explicitly present in the text.
- Each bullet must represent ONE factual statement.
- Do not combine multiple facts into one bullet.
- Do not summarize discussions.
- Do not interpret meaning.
- Do not infer missing details.
- Do not mention the conversation or speakers.
- Do not write phrases like "the episode discusses" or "someone says".
- Skip sentences that are unclear, garbled, or incomplete.
- Skip jokes, greetings, and conversational filler.
- Preserve numbers exactly as written.
- NEVER describe the structure of the episode, discussion, or podcast.
Only extract concrete facts about people, events, numbers, companies, or actions.
- If two facts appear in the same sentence, output them as separate bullets.
- Prefer copying wording directly from the transcript instead of rewriting.
- Convert first-person statements into third-person statements when the person is identifiable.

STYLE

- Write each fact as a simple declarative sentence.
- Keep the wording close to the transcript.
- Each bullet should be independent and self-contained.
- Output ONLY bullet points.

EXAMPLE

Transcript:
"I run Misho."

Output:
• Vidith Atre runs Misho.

Transcript:
"I was the first engineer in my family."

Output:
• Vidith Atre was the first engineer in his family.

Transcript:
"My cousins still do farming."

Output:
• Some of Vidith Atre's cousins work in farming.

TEXT:
---
{transcript}
---
"""


# -------------------------
# LLM CALL
# -------------------------

def call_llm(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=600
    )

    response.raise_for_status()
    return response.json()["response"]


# -------------------------
# PROCESS ONE CHUNK
# -------------------------

def process_chunk(chunk_path, output_path):

    transcript = chunk_path.read_text()

    prompt = PROMPT.format(transcript=transcript)

    bullets = call_llm(prompt)

    output_path.write_text(bullets)


# -------------------------
# MAIN PIPELINE
# -------------------------

def main():

    episodes = sorted(CHUNK_ROOT.iterdir())

    for episode_dir in episodes:

        if not episode_dir.is_dir():
            continue

        print(f"\nProcessing episode: {episode_dir.name}")

        chunk_files = sorted(episode_dir.glob("*.txt"))

        bullet_episode_dir = BULLET_ROOT / episode_dir.name
        bullet_episode_dir.mkdir(parents=True, exist_ok=True)

        for chunk_file in tqdm(chunk_files):

            output_file = bullet_episode_dir / chunk_file.name

            try:
                process_chunk(chunk_file, output_file)

            except Exception as e:
                print(f"Error processing {chunk_file}: {e}")


if __name__ == "__main__":
    main()
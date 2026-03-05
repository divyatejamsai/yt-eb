import requests
from pathlib import Path
from tqdm import tqdm

# -------------------------
# CONFIG
# -------------------------

BULLET_MODEL = "qwen2.5:7b"
SPEAKER_MODEL = "qwen2.5:1.5b"

OLLAMA_URL = "http://localhost:11434/api/generate"

CHUNK_ROOT = Path("data/transcripts/chunks")
BULLET_ROOT = Path("data/bullets")

# -------------------------
# PROMPTS
# -------------------------

BULLET_PROMPT = """
You are extracting factual statements from a podcast transcript.

Each transcript belongs to one chapter of a podcast episode.

CURRENT SPEAKER:
{speaker}

The CURRENT SPEAKER is the person speaking in this chapter unless the text clearly states otherwise.

If the transcript contains first-person statements such as:
I
we
my
our

assume they refer to the CURRENT SPEAKER and convert them to third-person statements.

--------------------------------
STRICT EXTRACTION RULES
--------------------------------

• Use ONLY information explicitly present in the transcript.
• NEVER invent facts or add missing information.
• NEVER guess names or details not written in the text.

• Each bullet must represent ONE factual statement.
• If a sentence contains multiple facts, split them.

• Skip sentences that are:
  - greetings
  - jokes
  - filler conversation
  - unclear or broken speech

• Do NOT summarize discussions.
• Do NOT describe the conversation.
• Do NOT write phrases like:
  - "the speaker says"
  - "the podcast discusses"
  - "they talk about"

• Only extract concrete facts about:
  - people
  - companies
  - events
  - numbers
  - timelines
  - actions
  - roles

--------------------------------
STYLE
--------------------------------

• Write simple declarative sentences.
• Keep wording close to the transcript.
• Each bullet must be independent.
• Each bullet must begin with the character:

•

• Output ONLY bullet points.

--------------------------------
INPUT
--------------------------------

CHAPTER TITLE:
{title}

TRANSCRIPT:
---
{transcript}
---
"""


SPEAKER_PROMPT = """
You are identifying the main speaker of a podcast chapter.

If the chapter title clearly contains the name of a person who is the speaker, return ONLY that person's name.

If no person is mentioned, return exactly:

NONE

Rules:
- Return only the name.
- Do not add explanations.
- Do not add titles like CEO or Founder.

Examples

Title: Sai Divya's Startup Journey
Output:
Sai Divya

Title: Talking to Nithin Kamath about Zerodha
Output:
Nithin Kamath

Title: India's Economy
Output:
NONE

Title:
{title}
"""

# -------------------------
# LLM CALL
# -------------------------

def call_llm(prompt, model):

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0}
            },
            timeout=600
        )

        response.raise_for_status()

        return response.json()["response"].strip()

    except Exception as e:
        print(f"LLM call failed ({model}): {e}")
        return None


# -------------------------
# SPEAKER DETECTION
# -------------------------

def detect_speaker(title):

    try:
        prompt = SPEAKER_PROMPT.format(title=title)

        response = call_llm(prompt, SPEAKER_MODEL)

        if not response:
            return None

        if response.upper() == "NONE":
            return None

        return response.strip()

    except Exception:
        print(f"Speaker detection failed for: {title}")
        return None


# -------------------------
# PROCESS ONE CHAPTER
# -------------------------

def process_chunk(chunk_path, output_path, current_speaker):

    try:
        text = chunk_path.read_text().strip()
    except Exception:
        print(f"Failed to read file: {chunk_path}")
        return current_speaker

    lines = text.splitlines()

    if len(lines) < 2:
        return current_speaker

    title = lines[0].strip()
    transcript = "\n".join(lines[1:]).strip()

    # detect speaker
    detected = detect_speaker(title)

    if detected:
        print(f"Detected speaker: {detected}")
        current_speaker = detected

    prompt = BULLET_PROMPT.format(
        title=title,
        transcript=transcript,
        speaker=current_speaker if current_speaker else "Unknown"
    )

    bullets = call_llm(prompt, BULLET_MODEL)

    if bullets:
        output_path.write_text(bullets)
    else:
        print(f"Bullet generation failed for {chunk_path}")
        output_path.write_text("")

    return current_speaker


# -------------------------
# MAIN PIPELINE
# -------------------------

def main():

    if not CHUNK_ROOT.exists():
        print("Transcript folder not found.")
        return

    BULLET_ROOT.mkdir(parents=True, exist_ok=True)

    episodes = sorted(CHUNK_ROOT.iterdir())

    for episode_dir in episodes:

        if not episode_dir.is_dir():
            continue

        print(f"\nProcessing episode: {episode_dir.name}")

        chunk_files = sorted(episode_dir.glob("*.txt"))

        bullet_episode_dir = BULLET_ROOT / episode_dir.name
        bullet_episode_dir.mkdir(parents=True, exist_ok=True)

        current_speaker = None

        for chunk_file in tqdm(chunk_files):

            # skip intro chapters
            if "intro" in chunk_file.name.lower():
                continue

            output_file = bullet_episode_dir / chunk_file.name

            try:

                current_speaker = process_chunk(
                    chunk_file,
                    output_file,
                    current_speaker
                )

            except Exception as e:

                print(f"Error processing {chunk_file}: {e}")


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":
    main()
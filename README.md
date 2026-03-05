
# Podcast → Book Pipeline

This project converts long-form podcast conversations into **structured book-style chapters** using automated transcription, knowledge extraction, and controlled text generation.

The goal is to transform **conversational audio content into readable structured knowledge**.

The repository contains two different pipelines developed during the project:

- **Old Pipeline** — automatic topic discovery using clustering
- **New Pipeline** — chapter-based segmentation using YouTube metadata

The new pipeline was developed after realizing that YouTube videos already contain **high-quality chapter timestamps**, which provide reliable topic boundaries.

---

# Selected Episodes

The pipeline was tested on **10 podcast episodes**, each focusing on a different industry or theme.

| Episode | Topic |
|-------|------|
| Ep 3 | E-commerce |
| Ep 7 | Biotech / Kiran Mazumdar Shaw |
| Ep 9 | Venture Capital (India) |
| Ep 14 | Electric Vehicles |
| Ep 15 | Climate Change |
| Ep 16 | Entrepreneurial Traits |
| Ep 18 | Alcohol Industry |
| Ep 20 | Real Estate |
| Ep 21 | Longevity |
| Ep 24 | Silicon Valley VC Playbook |

These episodes were chosen to ensure coverage across **multiple industries and discussion formats**, including founder stories, industry analysis, and venture capital discussions.

---

# Repository Structure

```
scripts/
scripts_old_pipeline/
data/
old_pipeline/
new_pipeline/
```

The repository contains two different approaches for generating structured knowledge from podcasts.

---
# Design Constraints

The podcast episodes contain **multiple speakers**, which normally requires **speaker diarization** to accurately identify who is speaking at each point in the conversation.

During development, I initially explored using speaker diarization models such as **pyannote.audio** and other voice segmentation approaches.

However, these models typically require:

- CUDA-enabled GPUs
- significant memory resources
- long processing times for multi-hour audio

Since the project was developed on a **MacBook without CUDA support**, running these diarization models locally was either extremely slow or impractical.

As a result, I adapted the pipeline design to work **without full speaker diarization**.

Instead, the system uses alternative strategies:

- **Chapter-based segmentation** using YouTube chapter metadata  
- **LLM-based speaker inference** from chapter titles  
- **Context-aware fact extraction** that converts first-person statements into third-person facts when a speaker can be inferred

These adaptations allowed the pipeline to extract structured knowledge from the podcast **without requiring heavy diarization models**, while still maintaining reasonable accuracy in factual attribution.
# Old Pipeline

The **old pipeline** attempts to reconstruct the structure of the podcast automatically using topic discovery.

Key steps include:

- transcript chunking
- factual bullet extraction
- topic generation using LLMs
- semantic topic clustering
- paragraph generation

You can read the detailed explanation here:

```
docs/old_pipeline.md
```

---

# New Pipeline (Final Approach)

The **new pipeline** uses a simpler and more reliable approach by leveraging **YouTube chapter metadata**.

Instead of detecting topics automatically, the pipeline:

1. downloads podcast audio
2. transcribes the audio using Whisper
3. extracts chapter timestamps from YouTube metadata
4. splits the transcript using those chapters
5. extracts factual information from each chapter
6. converts facts into structured explanatory text
7. compiles the output into a book

You can read the detailed explanation here:

```
docs/new_pipeline.md
```

---

# Requirements

To run the **new pipeline**, install the required dependencies.

The required Python packages are listed in:

```
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

Additional system dependencies:

- **FFmpeg** (audio processing)
- **yt-dlp** (YouTube metadata and audio download)
- **Ollama** (for running local LLM models)

---



---






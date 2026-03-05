# New Pipeline: Chapter-Based Knowledge Extraction

## Overview

After developing the initial topic-clustering pipeline, I realized that the YouTube videos already contained **manually defined chapter timestamps**.

These chapters are typically created by the content creators and already represent **meaningful topic boundaries within the podcast**.

Instead of attempting to infer topic structure automatically, the new pipeline uses these **existing chapter boundaries as the primary structural signal**.

This significantly simplifies the system while improving segmentation accuracy.

The goal of this pipeline is to convert podcast episodes into structured book-style chapters by:

- Extracting chapter boundaries directly from YouTube metadata
- Transcribing podcast audio
- Splitting transcripts according to chapter timestamps
- Extracting factual information from each chapter
- Converting factual information into readable explanatory prose
- Compiling the results into a structured book

The pipeline uses a combination of:

- Speech-to-text models
- Large Language Models (LLMs)
- Metadata extraction tools
- Automated text processing scripts

---

# Pipeline Architecture

The pipeline consists of the following stages:

```
YouTube Podcast Video
        ↓
Download Audio
        ↓
Convert Audio to WAV
        ↓
Speech-to-text Transcription
        ↓
Extract Chapter Metadata
        ↓
Split Transcript by Chapters
        ↓
Bullet Extraction
        ↓
Bullet Cleaning
        ↓
Paragraph Generation
        ↓
Chapter Construction
        ↓
Book Compilation
```

This architecture converts **long conversational audio → structured written chapters**.

---

# 1. Audio Acquisition

The first step downloads podcast audio directly from YouTube.

The pipeline uses **yt-dlp**, a widely used command-line tool for downloading media from YouTube.

Each episode is downloaded as a high-quality audio file and saved as:

```
data/audio/epX.webm
```

Where `X` represents the episode number.

Downloading the best available audio ensures better transcription quality during the speech recognition stage.

---

# 2. Audio Conversion

The downloaded audio files are converted into a format suitable for speech recognition.

The pipeline converts `.webm` audio files into **16kHz mono WAV files** using **FFmpeg**.

Key processing steps include:

- converting audio format to WAV
- resampling to **16kHz**
- converting to **mono channel**

Speech recognition models such as Whisper perform best when audio is provided in this standardized format.

Converted files are stored as:

```
data/audio/epX.wav
```

---

# 3. Speech-to-Text Transcription

Once the audio is prepared, the pipeline generates transcripts using **OpenAI Whisper**.

The transcription model used is:

**Whisper (base model)**

Whisper is a transformer-based speech recognition model trained on large-scale multilingual speech datasets.

The transcription process produces structured JSON output containing:

- text segments
- timestamps
- metadata

Example output location:

```
data/transcripts/raw/
```

These timestamps are essential for later aligning transcript segments with chapter boundaries.

---

# 4. Chapter Metadata Extraction

Instead of discovering topics automatically, the pipeline extracts **chapter timestamps directly from YouTube metadata**.

This step again uses **yt-dlp**, which can return detailed metadata about the video.

For each episode, the script retrieves:

- chapter start time
- chapter end time
- chapter title

Example chapter record:

```
start_time | end_time | chapter_title
```

These timestamps are stored as:

```
data/chapters/epX/chapters.txt
```

Using creator-defined chapters ensures that transcript segmentation aligns with **the actual structure of the podcast episode**.

---

# 5. Transcript Splitting by Chapters

Once chapter timestamps are available, the transcript is divided into **chapter-level segments**.

Each Whisper transcript contains timestamped speech segments.

The pipeline compares these timestamps with chapter boundaries and groups transcript segments that fall within each chapter.

For each chapter:

- all transcript segments between the start and end timestamps are collected
- the chapter title is placed at the beginning of the file

Each chapter transcript is saved as:

```
data/transcripts/chunks/epX/
```

Example:

```
01_vidit_aatreys_story.txt
02_starting_meesho.txt
03_building_the_marketplace.txt
```

This step converts the full episode transcript into **independent chapter transcripts**.

---

# 6. Bullet Extraction

The bullet extraction stage is the **core information extraction component of the pipeline**.  
Its purpose is to convert conversational transcript text into **atomic factual statements** that can later be used to generate structured knowledge.

This step is implemented using **local Large Language Models running through Ollama**, allowing the pipeline to run entirely offline once models are downloaded.

Two models are used in this stage:

| Task | Model |
|-----|------|
Speaker identification | Qwen 2.5 (1.5B parameters) |
Factual extraction | Qwen 2.5 (7B parameters) |

The use of two models improves efficiency: the smaller model performs lightweight classification tasks, while the larger model handles deeper semantic extraction.

---

## Chapter Structure Used for Extraction

Each chapter transcript file has the following structure:

```
Chapter Title

Transcript text...
```

The title and transcript are handled separately during processing.

The title is used for:

- speaker identification
- contextual grounding for the LLM

The transcript body is used for factual extraction.

---

## Speaker Detection

Podcasts often contain multiple speakers.  
When a speaker refers to themselves using **first-person pronouns** (such as *I*, *we*, or *my*), extracting factual statements requires identifying **who that person actually is**.

To address this, the pipeline attempts to detect the **primary speaker for each chapter**.

The system sends the chapter title to the smaller Qwen model with a classification prompt:

Example input:

```
Title: Talking to Nithin Kamath about Zerodha
```

Expected output:

```
Nithin Kamath
```

If no clear person name is present, the model returns:

```
NONE
```

When a speaker is detected, it becomes the **current speaker context**.

This context persists across chapters until a new speaker is detected, allowing the pipeline to maintain conversational continuity.

---

## Context-Aware Fact Extraction

The larger **Qwen 2.5 7B model** performs the actual bullet extraction.

The prompt contains three main inputs:

- Chapter title
- Transcript text
- Current speaker context

The speaker context allows the model to correctly convert first-person statements.

Example transformation:

Transcript:

```
I started Meesho in 2015.
```

Detected speaker:

```
Vidit Aatrey
```

Extracted bullet:

```
• Vidit Aatrey started Meesho in 2015.
```

Without speaker context, this conversion would not be possible.

---

## Strict Fact Extraction Rules

To prevent hallucination and maintain factual integrity, the prompt enforces strict rules.

The model is instructed to:

- use **only information explicitly present in the transcript**
- never invent missing details
- extract **one fact per bullet**
- split sentences containing multiple facts
- skip filler conversation, jokes, or greetings
- avoid describing the conversation itself

The extraction is restricted to concrete factual content such as:

- people
- companies
- events
- numbers
- timelines
- actions
- roles

Each bullet must:

- be a **self-contained factual statement**
- start with the bullet symbol `•`
- avoid referencing the conversation structure

---

## Example Extraction

Input transcript:

```
I joined IIT Bombay in 2008 and later worked at Flipkart.
```

Extracted bullets:

```
• Vidit Aatrey joined IIT Bombay in 2008.
• Vidit Aatrey later worked at Flipkart.
```

By splitting compound statements into separate bullets, the pipeline ensures that each bullet represents a **single atomic piece of information**.

---

## Chapter-Level Processing

Each chapter file is processed independently.

For each chapter:

1. The title is extracted
2. The speaker detection model is run
3. The transcript is processed by the bullet extraction model
4. The resulting bullets are written to disk

Example output location:

```
data/bullets/epX/
```

Each chapter produces a corresponding bullet file.

---

# 7. Bullet Cleaning

After bullet extraction, a cleaning stage removes low-quality or redundant bullets.

This step performs several operations:

- removing very short bullet points
- eliminating duplicate facts
- normalizing names and spelling variations
- ensuring all bullets follow a consistent format

Example corrections include:

```
Vidith Atre → Vidit Aatrey
Misho → Meesho
```

This stage improves the **accuracy and consistency** of extracted information.

---

# 8. Paragraph Generation

The cleaned bullet points are then converted into **explanatory prose**.

This step again uses the **Qwen 2.5 7B model**.

The prompt enforces strict rules:

- each bullet becomes a sentence
- no additional information is introduced
- numbers and names are preserved exactly
- factual tone must be maintained

The output is a set of **clear explanatory paragraphs**.

These paragraphs are saved as:

```
data/sections/epX/
```

Each paragraph corresponds to a chapter.

---

# 9. Chapter Construction

Once paragraphs are generated, they are grouped together to form **complete chapters**.

Each chapter includes:

- a formatted chapter title
- the generated explanatory text

Chapters are saved as:

```
data/chapters/epX.txt
```

This stage organizes the extracted information into **structured readable sections**.

---

# 10. Book Compilation

The final stage compiles all chapters into a single Markdown book.

The script sequentially merges all chapter files and adds:

- book title
- author name
- chapter headings

The final output is written to:

```
data/book/book.md
```

This file represents the **complete book generated from the podcast episodes**.

---

# Advantages of the Chapter-Based Pipeline

Compared to the original clustering pipeline, the chapter-based approach provides several advantages:

- significantly simpler architecture
- fewer processing stages
- improved topic segmentation
- reduced computational cost

Since the segmentation relies on **human-created chapter metadata**, the resulting structure aligns closely with the actual flow of the podcast.

---

# Summary

The final pipeline converts podcast episodes into structured book chapters using a hybrid approach combining:

- automated speech recognition
- chapter metadata extraction
- factual knowledge extraction
- controlled text generation

By leveraging YouTube chapter metadata, the system avoids complex topic discovery algorithms while producing **more reliable and coherent chapter structures**.
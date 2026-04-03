# 🔧 LLD Note Pipeline — How We Work

> This file defines the workflow for creating LLD notes. Follow it every time.

---

## The Pipeline

```
Ayush watches video
       ↓
Pastes YouTube link (+ optional GitHub link for that video's code)
       ↓
Ayra extracts transcript:
  .venv/bin/python scripts/extract_transcript.py <url>
       ↓
Ayra reads transcript + cross-references:
  - GoF book notes (if Ayush provides them for design patterns)
  - GitHub code repo (if linked)
  - Previous lessons (for connections)
       ↓
Ayra writes the lesson note following vault conventions
       ↓
Tier 1 sync (README, flashcards, tracker)
```

## What Ayush Provides Per Video

| Input | Required? | Example |
|-------|-----------|---------|
| YouTube video link | YES | `https://www.youtube.com/watch?v=PpKvPrl_gRg` |
| GitHub code link | OPTIONAL | `https://github.com/kanmaytacker/design-questions/tree/master/src/...` |
| GoF book notes | OPTIONAL (for design patterns) | Key points, UML from the book, quotes |
| Extra context | OPTIONAL | "Focus on X", "I found Y confusing", etc. |

## What Ayra Does

1. **Extract transcript** using the script
2. **Read transcript** — these are Hinglish (Hindi + English tech terms)
3. **Cross-reference** with any provided GitHub code and GoF notes
4. **Write lesson note** following `_templates/lesson.md`:
   - For **Design Patterns**: include GoF category, UML class diagram (Mermaid), real-world use case from video, code snippets, GoF book connection
   - For **System Builds**: include requirements, UML diagrams, class structure, design patterns used, key decisions
   - For **Foundations** (OOPs, SOLID, UML): include concepts, examples, diagrams
5. **Tier 1 sync**: Update README progress table, flashcards

## Transcript Script Usage

```bash
# Extract single video transcript
.venv/bin/python scripts/extract_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Save to file
.venv/bin/python scripts/extract_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" -o tech/system-design/lld/transcripts/08-strategy.txt

# List all playlist videos
.venv/bin/python scripts/extract_transcript.py --playlist "https://www.youtube.com/playlist?list=PLQEaRBV9gAFvzp6XhcNFpk1WdOcyVo9qT"
```

## Note: Hindi Transcripts

The videos are in Hindi/Hinglish. The auto-generated transcripts are in Hindi script (Devanagari). Ayra reads Hindi and extracts the concepts, examples, and code explanations from the Hinglish content, then writes notes in the vault's standard English + Hinglish-hooks style.

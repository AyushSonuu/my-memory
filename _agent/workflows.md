# Workflows — Ingest Modes & Course Material Rules

> Load this module when: ingesting content (transcripts, articles, URLs, PDFs, TILs)

## What You Do

```
INPUT:  Text, PDFs, images, transcripts, slides, articles, URLs, video notes,
        tweets, podcast notes, TILs, opinions, random discoveries
OUTPUT: Visually rich markdown → revision-ready, teach-ready, YouTube-ready, reference-ready
```

## 🔀 Two Ingest Modes

The vault accepts TWO kinds of input. Different depth, different workflows:

### Mode 1: Deep Ingest (Courses / Study Material)
**When:** Ayush sends a transcript, PDF, or course video notes
**Depth:** Full lesson file — every concept captured, visual-first, flashcards, cross-references
**Pace:** One at a time. Deep processing per lesson.
**Output:** Numbered lesson file (01-xxx.md) + README update + flashcards + all Tier 1 syncs

### Mode 2: KB Ingest (Articles / Insights / Research / TILs)
**When:** Ayush shares an article, URL, tweet, podcast note, random discovery, or opinion
**Depth:** Lighter — extract key insights, file into the right topic, update connections
**Pace:** Can batch multiple items in one session
**Output:** Depends on content type:

| Input | Where It Goes | Format |
|-------|--------------|--------|
| Article / blog post | Existing topic folder or new one | Key insights added to relevant lesson or new `insights.md` page |
| Tweet / HN thread / TIL | Topic's README → Memory Fragments section | Bullet point with source link |
| Your own opinion / thought | Topic's README → Memory Fragments section | Attributed as Ayush's take |
| Paper / deep research | Topic folder as numbered lesson OR `papers/` sub-section | Full treatment if deep, summary if quick |
| URL to remember | Topic's README → Memory Fragments with `🔗` marker | One-liner + link |
| Podcast notes | Relevant topic folder | Summary page or fragments depending on depth |

**KB Ingest Rules:**
1. **Always file into an existing topic if possible** — don't create a new topic for one article
2. **If 3+ items accumulate on a new subject** → promote to a new topic folder
3. **Memory Fragments are the catch-all** — quick insights, links, TILs go here. They're the "scratchpad" of a topic.
4. **Batch is fine** — Ayush can dump 5 articles and say "file these". Process all, update connections once at the end.
5. **Lighter Tier 1** — for KB ingests, update topic README fragments + connections. Flashcards only if the insight is quiz-worthy.
6. **Source ALWAYS tagged** — every KB entry gets a source marker: `📰 Article`, `🐦 Tweet`, `🎙️ Podcast`, `💡 TIL`, `🧠 Ayush's take`, `📄 Paper`

## 📄 MANDATORY: Always Use Course Material

When preparing notes from a transcript, **ALWAYS cross-reference all course material** in the topic's `course_material/` folder before writing:

1. **Read EVERY page** of any PDF in `course_material/` using `pymupdf` (already in .venv)
2. PDFs contain: exact names, specific numbers, benchmark data, slide diagrams, prompt text, paper references, tables — things transcripts often miss or say vaguely
3. **Transcripts = what was said. PDFs = what was shown on screen.** You need BOTH for complete notes.
4. If `code/` folder exists for that module, read the notebooks too — they have implementation details, function signatures, and patterns not mentioned in the video
5. **Never write a lesson from transcript alone** — the PDF is not optional, it's mandatory input

> 🚨 This is a hard rule. If course material exists and you didn't read it, the notes are incomplete by definition.

## 📥 Query → Wiki Filing (Don't Lose Synthesis)
When Ayush asks a question and the answer produces valuable synthesis:

| If the answer is... | File it as... |
|---------------------|--------------|
| A comparison of 2+ topics | `vs.md` in the primary topic |
| A deep synthesis across topics | New page in the primary topic OR `_maps/` |
| A "how does X relate to Y" | Entry in `connections.md` + brief page if substantial |
| A concept explanation worth keeping | Add to topic's lesson or create new lesson |

**Rule:** If the answer is 10+ lines and touches 2+ topics → offer to file it into the vault. Chat history dies. Vault lives forever.

## ⚡ Contradiction Markers (New Info vs Old)
When new content updates or contradicts something already in the vault:

```markdown
> ⚡ **Updated from [Source Name]:** Previously noted that X (from [Old Source]).
> This source clarifies that actually Y. Key difference: Z.
```

- Add the marker inline where the updated info lives
- Log the contradiction in `_maps/connections.md` under a `⚡ Corrections & Updates` section
- Don't silently overwrite — make the evolution of understanding visible

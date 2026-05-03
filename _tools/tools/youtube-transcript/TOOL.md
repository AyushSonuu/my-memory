---
name: youtube-transcript
description: "Extract transcripts from YouTube videos for note-taking. Use when: user provides a YouTube URL/ID and wants the transcript, needs to ingest video content into the vault, or wants to create lesson notes from a video. NOT for: non-YouTube videos, creating the notes themselves (that's the ingest workflow), or downloading video files."
version: 1.0.0
runtime: python
status: stable
tags: [youtube, transcript, ingest, video, learning]
created: 2026-05-03
author: ayra
---

# YouTube Transcript Tool

Extract transcripts from YouTube videos using video URLs or IDs.

## When to Use

✅ **USE this tool when:**
- "Get me the transcript for this YouTube video"
- "Extract transcript from https://www.youtube.com/watch?v=..."
- User shares a YouTube URL and wants to create notes from it
- Ingesting video content into the vault
- Need the raw transcript text for lesson creation
- Extract captions/subtitles from educational videos

## When NOT to Use

❌ **DON'T use this tool when:**
- Creating lesson notes from the transcript → use the ingest workflow
- Non-YouTube videos (Vimeo, etc.) → not supported
- Downloading video files → this extracts text only
- The video has no captions/subtitles available
- Playlist processing → extract one video at a time

## Execution Modes

### Mode 1: Schema (Introspection)
Any agent's first step — discover what this tool expects and returns.
```bash
cd _tools && uv run youtube-transcript --schema
```
Returns full JSON schema: inputs, types, required, defaults, enums, examples.

### Mode 2: Programmatic (Agent Execution)
Structured JSON in → structured JSON out. No terminal I/O.
```bash
cd _tools && uv run youtube-transcript --input '{"url": "https://www.youtube.com/watch?v=7AMjmCTumuo"}'
```
Returns standard `ToolOutput` envelope:
```json
{
  "status": "success",
  "tool": "youtube-transcript",
  "version": "1.0.0",
  "data": {
    "video_id": "7AMjmCTumuo",
    "title": "Threading in Python",
    "channel": "Corey Schafer",
    "duration_seconds": 1234,
    "transcript": "Welcome to this video...",
    "word_count": 5432,
    "language": "en"
  },
  "message": "Extracted transcript from 'Threading in Python' (20:34)",
  "errors": [],
  "timestamp": "2026-05-03T12:00:00+05:30"
}
```

### Mode 3: Interactive (Human Use)
Pretty terminal output with transcript.
```bash
cd _tools && uv run youtube-transcript --url "https://www.youtube.com/watch?v=7AMjmCTumuo"
cd _tools && uv run youtube-transcript --video-id "7AMjmCTumuo"
cd _tools && uv run youtube-transcript --url "..." --output transcript.txt
```

## Inputs

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `url` | string | ✅* | — | Full YouTube URL (any format: watch?v=, youtu.be/, embed/, etc.) |
| `video-id` | string | ✅* | — | YouTube video ID (11 characters, e.g., `7AMjmCTumuo`) |
| `language` | string | ❌ | en | Preferred language code (e.g., `en`, `hi`, `es`) |
| `format` | string | ❌ | text | Output format: `text`, `json`, `markdown` |
| `output` | string | ❌ | — | Optional file path to save transcript |

*Either `url` OR `video-id` must be provided (not both).

## Output (ToolOutput Envelope)

Every response follows the standard envelope:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` \| `error` \| `partial` |
| `tool` | string | Always `youtube-transcript` |
| `version` | string | Tool version (semver) |
| `data` | object | Transcript data (video_id, title, channel, transcript, etc.) |
| `message` | string | Human-readable summary |
| `errors` | array | Error messages (empty on success) |
| `timestamp` | string | ISO timestamp (IST) |

## Error Handling

| Error | Status | Message |
|-------|--------|---------|
| Missing both url and video-id | `error` | "Must provide either 'url' or 'video-id'" |
| Invalid video ID | `error` | "Invalid YouTube video ID: {id}" |
| Video not found | `error` | "Video not found: {id}" |
| No transcript available | `error` | "No transcript available for video: {id}" |
| Network error | `error` | "Failed to fetch transcript: {details}" |

## Examples

```bash
# Agent: extract transcript as structured data
uv run youtube-transcript --input '{"url": "https://www.youtube.com/watch?v=7AMjmCTumuo"}'

# Agent: extract with specific language preference
uv run youtube-transcript --input '{"video-id": "7AMjmCTumuo", "language": "en"}'

# Human: extract and display
uv run youtube-transcript --url "https://www.youtube.com/watch?v=7AMjmCTumuo"

# Human: extract and save to file
uv run youtube-transcript --video-id "7AMjmCTumuo" --output transcript.txt

# Human: extract as markdown
uv run youtube-transcript --url "..." --format markdown
```

## Architecture

```
youtube_transcript/
├── cli.py        → Composition root (instantiate + dispatch)
├── tool.py       → YouTubeTranscriptTool(BaseTool) — schema, execute
├── extractor.py  → Video ID parsing, transcript fetching, metadata extraction
└── formatter.py  → Output formatting (text, JSON, markdown)

External dependency:
└── youtube-transcript-api → actual transcript extraction library
```

## Dependencies

- `youtube-transcript-api` — for fetching YouTube transcripts
- `pytubefix` (optional) — for video metadata (title, channel, duration)

## Installation

After creating the tool, run:
```bash
cd _tools && uv sync
```

---
name: flashcard-quiz
description: "Interactive quiz from vault flashcards. Use when: user wants to revise, test knowledge, practice recall on any topic, or an agent needs to fetch flashcard Q&A data. NOT for: creating flashcards (that's the ingest workflow), editing flashcard content, or spaced repetition scheduling."
version: 1.1.0
runtime: python
status: stable
tags: [revision, flashcards, quiz, learning, recall]
created: 2026-04-07
author: ayra
---

# Flashcard Quiz Tool

Parse and quiz from any topic's `flashcards.md` file in the vault.

## When to Use

✅ **USE this tool when:**
- "Quiz me on agent memory"
- "What flashcards do I have for RAG?"
- "Test me on 5 random questions from asyncio"
- "List all flashcards for agentic-ai"
- Agent needs structured Q&A data from a topic
- Revision session — self-testing on any topic

## When NOT to Use

❌ **DON'T use this tool when:**
- Creating or editing flashcards → use the ingest workflow
- Scheduling revisions → future tool (revision-scheduler)
- Searching across all topics → future tool (vault-search)
- The topic has no `flashcards.md` file yet

## Execution Modes

### Mode 1: Schema (Introspection)
Any agent's first step — discover what this tool expects and returns.
```bash
cd _tools && uv run flashcard-quiz --schema
```
Returns full JSON schema: inputs, types, required, defaults, enums, examples.

### Mode 2: Programmatic (Agent Execution)
Structured JSON in → structured JSON out. No terminal I/O.
```bash
cd _tools && uv run flashcard-quiz --input '{"topic": "agent-memory", "count": 5, "mode": "random"}'
```
Returns standard `ToolOutput` envelope:
```json
{
  "status": "success",
  "tool": "flashcard-quiz",
  "version": "1.1.0",
  "data": {
    "cards_found": 37,
    "cards_selected": 5,
    "cards": [
      {"index": 0, "question": "...", "answer": "...", "section": "..."},
      ...
    ]
  },
  "message": "Selected 5 of 37 flashcards for topic 'agent-memory'",
  "errors": [],
  "timestamp": "2026-04-07T15:00:00+05:30"
}
```

### Mode 3: Interactive (Human Use)
Pretty terminal quiz with self-rating.
```bash
cd _tools && uv run flashcard-quiz --topic agent-memory --count 5
cd _tools && uv run flashcard-quiz --topic agent-memory --list
cd _tools && uv run flashcard-quiz --topic python/asyncio --mode sequential --show-hint
```

## Inputs

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `topic` | string | ✅ | — | Topic name or path (e.g., `agent-memory`, `python/asyncio`) |
| `count` | integer | ❌ | 10 | Number of questions (0 = all) |
| `mode` | string | ❌ | random | Selection strategy: `random`, `sequential`, `reverse` |
| `show-hint` | boolean | ❌ | false | Show section name as hint before answering |
| `list` | boolean | ❌ | false | List all cards and exit (no quiz) |

## Output (ToolOutput Envelope)

Every response follows the standard envelope:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` \| `error` \| `partial` |
| `tool` | string | Always `flashcard-quiz` |
| `version` | string | Tool version (semver) |
| `data` | object | Tool-specific payload (cards, counts, etc.) |
| `message` | string | Human-readable summary |
| `errors` | array | Error messages (empty on success) |
| `timestamp` | string | ISO timestamp (IST) |

## Error Handling

| Error | Status | Message |
|-------|--------|---------|
| Topic not found | `error` | "No flashcards.md found for topic: {name}" |
| No cards in file | `error` | "No flashcard blocks found in: {path}" |
| Missing required input | `error` | "Missing required input: 'topic'" |
| Invalid enum value | `error` | "Invalid value for 'mode': '{val}'" |

## Examples

```bash
# Agent: get all agent-memory flashcards as structured data
uv run flashcard-quiz --input '{"topic": "agent-memory", "list": true}'

# Agent: get 5 random questions for a quiz
uv run flashcard-quiz --input '{"topic": "agent-memory", "count": 5}'

# Human: interactive quiz
uv run flashcard-quiz --topic agent-memory --count 10

# Human: see all available cards
uv run flashcard-quiz --topic agent-memory --list
```

## Architecture

```
flashcard_quiz/
├── cli.py        → Composition root (4 lines — instantiate + dispatch)
├── tool.py       → FlashcardQuizTool(BaseTool) — schema, execute, interactive
├── quiz.py       → Selection strategies + result computation
└── display.py    → ANSI terminal formatting (decoupled from logic)

Shared (ayra-lib):
├── parsers.py    → VaultFlashcardParser (parses <details>/<summary> format)
├── types.py      → Flashcard, QuizResult (frozen dataclasses)
└── tool_interface.py → BaseTool, ToolOutput, ToolSchema (universal protocol)
```

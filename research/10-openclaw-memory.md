# OpenClaw Memory Management Research

> Additional research for memharness project

---

## Executive Summary

OpenClaw is an **open-source personal AI assistant** that uses a **file-based memory system**. Its approach is remarkably simple: **markdown files are the source of truth**. This pattern, similar to Claude Code's CLAUDE.md, offers insights for memharness's optional file-based memory export.

---

## 1. OpenClaw Overview

| Aspect | Details |
|--------|---------|
| **Type** | Personal AI assistant |
| **Deployment** | Local (Mac, Windows, Linux) |
| **LLM Support** | Claude, OpenAI, local models |
| **Communication** | WhatsApp, Telegram, Discord, Slack, Signal, iMessage |
| **License** | Open source |

### Core Capabilities

- Full filesystem read/write
- Shell command execution (with sandboxing)
- Browser automation
- 50+ third-party integrations
- Self-modifying skills (hot reload)
- Scheduled tasks (cron jobs)
- Proactive "heartbeat" check-ins

---

## 2. Memory Architecture

### 2.1 Core Principle

> "The files are the source of truth; the model only 'remembers' what gets written to disk."

OpenClaw uses **plain Markdown files** for all memory storage. No database, no vector store for primary memory — just files.

### 2.2 Two-Layer Memory

```
~/.openclaw/workspace/
├── MEMORY.md           # Long-term memory (curated, persistent)
└── memory/
    ├── 2026-03-20.md   # Daily log
    ├── 2026-03-21.md   # Daily log
    └── 2026-03-22.md   # Today's log
```

| Layer | File | Purpose | Behavior |
|-------|------|---------|----------|
| **Long-term** | `MEMORY.md` | Strategic decisions, durable facts | Curated, manually maintained |
| **Daily Logs** | `memory/YYYY-MM-DD.md` | Day-to-day notes, observations | Append-only, auto-read |

### 2.3 Memory Loading

At session start, OpenClaw automatically loads:
1. `MEMORY.md` (always)
2. Today's daily log
3. Yesterday's daily log

This provides immediate context without loading entire history.

### 2.4 Memory Tools

| Tool | Purpose |
|------|---------|
| `memory_search` | Semantic search across indexed snippets |
| `memory_get` | Targeted file/line retrieval |

### 2.5 Writing Guidelines

| Information Type | Where to Store |
|-----------------|----------------|
| Strategic decisions | `MEMORY.md` |
| User preferences | `MEMORY.md` |
| Session observations | Daily log |
| Temporary context | Daily log |
| "Remember this" requests | Immediate write to disk |

---

## 3. Advanced Features

### 3.1 Semantic Search

OpenClaw supports vector-based semantic search with multiple embedding providers:
- OpenAI
- Gemini
- Voyage
- Mistral
- Ollama (local)
- GGUF models (local)

**Hybrid search**: BM25 (keyword) + vector matching

### 3.2 Automatic Memory Flush

Before **context compaction** (when conversation gets too long), OpenClaw:
1. Prompts the model to identify important information
2. Writes important info to disk before compression
3. Compresses conversation

This prevents losing critical information during summarization.

### 3.3 Multi-Agent Memory

- Memory can be shared across different communication channels
- Group vs. private session distinction
- `MEMORY.md` excluded from group contexts (privacy)

---

## 4. Comparison: OpenClaw vs Other Systems

| Aspect | OpenClaw | Claude Code | Mem0 | MemGPT |
|--------|----------|-------------|------|--------|
| **Storage** | Markdown files | Markdown files | Vector DB | Tiered (context + archival) |
| **Primary** | `MEMORY.md` | `CLAUDE.md` | Managed service | Main context |
| **Daily logs** | Yes | No | No | No |
| **Semantic search** | Yes (optional) | No | Yes | Yes |
| **Auto-load** | Today + yesterday | Always | Query-based | Always in context |
| **Self-editing** | Yes | Limited | Via API | Yes (core memory) |

---

## 5. Key Patterns for memharness

### 5.1 Adopt: File-Based Memory Export

```python
# memharness should support markdown export (like OpenClaw/Claude Code)
class MemoryHarness:
    async def export_to_markdown(
        self,
        path: str = "./MEMORY.md",
        memory_types: Optional[list[str]] = None,
        namespace: Optional[tuple] = None,
    ):
        """Export memories to markdown file."""
        ...

    async def import_from_markdown(self, path: str):
        """Import memories from markdown file."""
        ...

    async def sync_with_files(
        self,
        workspace: str = "./memory/",
        daily_logs: bool = True,
    ):
        """Sync memory with file system (OpenClaw style)."""
        ...
```

### 5.2 Adopt: Two-Layer Pattern

```python
# memharness can support OpenClaw-style daily logs
memory = MemoryHarness(
    backend="postgresql://...",
    daily_log_enabled=True,
    daily_log_path="./memory/",
)

# Daily log auto-loaded
await memory.write_daily_log("User mentioned preference for Python")

# Long-term memory
await memory.write_persona("preferences", "User prefers Python over JavaScript")
```

### 5.3 Adopt: Pre-Compaction Flush

```python
# Before context compaction, save important info
async def compact_context(memory: MemoryHarness, llm):
    # 1. Ask LLM what's important
    important = await llm.extract_important(current_context)

    # 2. Save to persistent memory
    for item in important:
        await memory.add(item.content, item.memory_type)

    # 3. Then compact
    await memory.summarize_conversation(thread_id)
```

### 5.4 Don't Adopt: File-Only Storage

OpenClaw's file-only approach is simple but limited:
- No structured queries
- No proper indexing
- No semantic search on primary storage
- Manual curation required

memharness should use databases as primary storage, with file export as an **optional feature**.

---

## 6. Integration Opportunity

### 6.1 OpenClaw Backend for memharness

```python
# memharness could serve as OpenClaw's memory backend
from memharness.integrations.openclaw import OpenClawBackend

# Use memharness with OpenClaw
backend = OpenClawBackend(
    harness=memory,
    workspace="~/.openclaw/workspace/",
    sync_interval=60,  # Sync files to DB every 60s
)
```

### 6.2 File Sync Feature

```python
# memharness file sync (bidirectional)
memory = MemoryHarness(
    backend="postgresql://...",
    file_sync={
        "enabled": True,
        "workspace": "./memory/",
        "sync_mode": "bidirectional",  # or "export_only", "import_only"
        "format": "markdown",
    }
)
```

---

## 7. Summary

| Pattern | OpenClaw | memharness Adoption |
|---------|----------|-------------------|
| File-based primary | Yes | No (DB primary, file export) |
| Daily logs | Yes | Optional feature |
| Two-layer memory | Yes | Persona + Daily |
| Semantic search | Optional | Built-in |
| Pre-compaction flush | Yes | Adopt |
| Markdown format | Yes | Export format |
| Multi-channel | Yes | Namespace isolation |

---

## Sources

- OpenClaw website (openclaw.ai)
- OpenClaw documentation (docs.openclaw.ai)
- OpenClaw memory concepts documentation

---

*Research completed: 2026-03-22*

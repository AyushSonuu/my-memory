# memharness Research & Design

> Complete research and design documentation for the Agent Memory Harness project

---

## Quick Links

| Document | Purpose |
|----------|---------|
| **[09-HLD-memharness.md](09-HLD-memharness.md)** | 📐 **START HERE** — Full technical specification |
| [00-project-brief.md](00-project-brief.md) | Vision, decisions, scope |
| [07-consolidated-report.md](07-consolidated-report.md) | All findings synthesized |

---

## Research Documents

### Systems Analyzed

| # | System | Report | Key Takeaway |
|---|--------|--------|--------------|
| 1 | LangChain/LangGraph | [01-langchain-langgraph-memory.md](01-langchain-langgraph-memory.md) | 2-tier model, namespaces, checkpointers |
| 2 | Mem0/MemGPT/Letta | [02-mem0-memgpt-letta.md](02-mem0-memgpt-letta.md) | Simple API, agent-controlled memory, tiered storage |
| 3 | Infrastructure | [03-infrastructure-vectordb-cache.md](03-infrastructure-vectordb-cache.md) | pgvector HNSW, Redis caching, hybrid search |
| 4 | Agent Harnesses | [04-agent-harness-memory-patterns.md](04-agent-harness-memory-patterns.md) | Framework diversity, need for adapters |
| 5 | Existing Packages | [05-existing-memory-packages.md](05-existing-memory-packages.md) | No complete solution, market opportunity |
| 6 | Memory Theory | [06-memory-taxonomy-theory.md](06-memory-taxonomy-theory.md) | Cognitive alignment, lifecycle critical |
| 7 | DeepAgents | [08-deepagents-patterns.md](08-deepagents-patterns.md) | Pluggable backends, composite router |
| 8 | OpenClaw | [10-openclaw-memory.md](10-openclaw-memory.md) | File-based memory, daily logs |
| 9 | **Tool Lens VFS** | [11-tool-lens-vfs-pattern.md](11-tool-lens-vfs-pattern.md) | **VFS tool discovery, 96% token savings** |

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                     ANY AGENT FRAMEWORK                          │
│  (LangChain | LangGraph | CrewAI | Claude Code | Custom)        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        memharness                                │
├─────────────────────────────────────────────────────────────────┤
│  API: add() | search() | update() | delete() | get_tools()     │
├─────────────────────────────────────────────────────────────────┤
│  Memory Types: Conv | KB | Entity | Workflow | Toolbox |        │
│                Summary | ToolLog | Skills | File | Persona      │
├─────────────────────────────────────────────────────────────────┤
│  Lifecycle: summarize | consolidate | expire | gc               │
├─────────────────────────────────────────────────────────────────┤
│  Memory Agents: Summarizer | Consolidator | GC | Extractor      │
├─────────────────────────────────────────────────────────────────┤
│  Backends: PostgreSQL | SQLite | Redis | In-Memory              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Package name | `memharness` | Short, memorable |
| Primary backend | PostgreSQL + pgvector | Production-grade, hybrid SQL+vector |
| Memory types | 10 built-in + extensible | Complete coverage |
| LLM dependency | Agnostic (user provides) | Flexibility |
| API style | Async-first | Performance |
| Framework support | Adapters pattern | Works with any framework |

---

## Implementation Roadmap

### Phase 1 (v0.1) — Core
- [ ] Memory Manager
- [ ] 5 memory types (Conv, KB, Entity, Workflow, Toolbox)
- [ ] PostgreSQL backend
- [ ] SQLite backend
- [ ] Simple API

### Phase 2 (v0.2) — Complete
- [ ] All 10 memory types
- [ ] Redis caching
- [ ] Memory tools API
- [ ] LangChain adapter
- [ ] Lifecycle engine

### Phase 3 (v1.0) — Production
- [ ] Memory agents
- [ ] All framework adapters
- [ ] Server mode (REST)
- [ ] Full documentation

---

## File Statistics

| Metric | Value |
|--------|-------|
| Total documents | 13 |
| Total size | ~200KB |
| Systems analyzed | 9 |
| Memory types designed | 10 |
| Backends planned | 4 |

---

*Research completed: 2026-03-22*
*Status: Ready for implementation*

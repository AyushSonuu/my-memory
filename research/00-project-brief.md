# memharness — Project Brief

> **Generic Agent Memory Harness** — A pluggable memory infrastructure for any agentic AI system

---

## Vision

Build an open-source Python package (`memharness`) that serves as the **memory infrastructure layer** for ANY agentic AI system — completely decoupled from agent logic. Whether you're using Claude Code, LangChain, LangGraph, AutoGPT, or a custom agent, `memharness` provides the memory backbone.

**Core Philosophy:**
- Memory is **infrastructure**, not a feature
- Completely **separable** from agent harness
- **Plug and play** into any framework
- **Agents manage memory** (memory management agents built-in)

---

## Key Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Package Name** | `memharness` | Short, catchy, memorable |
| **Deployment** | Embedded library + Standalone server | Flexibility for all use cases |
| **API Design** | Layered (simple + powerful) | Serve both app devs and framework authors |
| **LLM Dependency** | Agnostic | User provides extraction/summarization functions |
| **Multi-tenancy** | Extensible design | User handles isolation, design supports it |
| **Memory Agents** | Built-in | Consolidation, summarization, cleanup, GC |

---

## Storage Backends (v1)

| Backend | Use Case | Priority |
|---------|----------|----------|
| **PostgreSQL + pgvector** | Production, hybrid SQL + vector | Must-have |
| **SQLite + local vectors** | Local-first, zero-dependency | Must-have |
| **Redis** | Caching, real-time, pub/sub | Must-have |
| **In-memory** | Testing, prototyping | Must-have |

**Design Principle:** Storage backend should be swappable via configuration. Same API, different backends.

---

## Memory Types

### Core Types (from DeepLearning.AI course)
1. **Conversational Memory** — Chat history, thread-based, time-ordered
2. **Knowledge Base (Semantic)** — Documents, facts, vector-searchable
3. **Entity Memory** — People, places, systems, relationships
4. **Workflow Memory** — Reusable step patterns, procedures
5. **Summary Memory** — Compressed context, expandable
6. **Toolbox Memory** — Tool definitions, semantic tool retrieval
7. **Tool Log Memory** — Audit trail, raw execution logs

### Extended Types (user-requested)
8. **Skills Memory** — Agent capabilities, learned behaviors
9. **File System Memory** — File references, document tracking
10. **Custom Types** — User-defined, fully extensible schema

### Memory Taxonomy

```
memharness Memory Types
├── Short-Term
│   ├── Working Memory (session scratchpad)
│   └── Semantic Cache (cached LLM responses)
└── Long-Term
    ├── Episodic
    │   ├── Conversational
    │   ├── Summary
    │   └── Tool Log
    ├── Semantic
    │   ├── Knowledge Base
    │   ├── Entity
    │   └── File System
    └── Procedural
        ├── Workflow
        ├── Toolbox
        └── Skills
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     ANY AGENT HARNESS                           │
│  (Claude Code | LangChain | LangGraph | AutoGPT | Custom)      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      memharness API                             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ Simple API  │  │ Advanced API │  │ Framework Integration  │ │
│  │ (App Devs)  │  │ (Power Users)│  │ (LangChain, etc.)      │ │
│  └─────────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Memory Manager                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  CRUD Operations per Memory Type                           │ │
│  │  read_*() | write_*() | update_*() | delete_*() | search() │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Memory Lifecycle Hooks                                    │ │
│  │  on_write | on_read | on_consolidate | on_expire          │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Memory Agents (Built-in)                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Consolidator │ │ Summarizer   │ │ GC Agent     │            │
│  │ (merge dups) │ │ (compress)   │ │ (cleanup)    │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Entity       │ │ Relationship │ │ Index        │            │
│  │ Extractor    │ │ Builder      │ │ Optimizer    │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Storage Layer                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ PostgreSQL │  │  SQLite    │  │   Redis    │  │ In-Memory │ │
│  │ + pgvector │  │ + vectors  │  │ + vectors  │  │  (dict)   │ │
│  └────────────┘  └────────────┘  └────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pluggability Design

### How Agents Plug In

```python
# Option 1: Direct instantiation
from memharness import MemoryHarness

memory = MemoryHarness(
    backend="postgresql",  # or "sqlite", "redis", "memory"
    connection_string="postgresql://...",
)

# Use in any agent
memory.write_conversation(thread_id="123", role="user", content="Hello")
context = memory.read_all(query="user question", thread_id="123")

# Option 2: LangChain integration
from memharness.integrations import LangChainMemory
memory = LangChainMemory(backend="sqlite")
agent = create_react_agent(llm, tools, memory=memory)

# Option 3: As a tool for agents
from memharness.tools import memory_tools
agent_tools = [..., *memory_tools(memory)]
```

### Extensibility

```python
# Custom memory type
from memharness import BaseMemoryStore, register_memory_type

@register_memory_type("custom_type")
class MyCustomMemory(BaseMemoryStore):
    def write(self, data): ...
    def read(self, query): ...
    def search(self, query, k=5): ...
```

---

## Framework Integrations (Planned)

| Framework | Integration Type | Priority |
|-----------|-----------------|----------|
| **LangChain** | BaseMemory subclass, VectorStore interface | High |
| **LangGraph** | Checkpointer, MemorySaver | High |
| **Claude Code** | File-based memory, CLAUDE.md sync | High |
| **AutoGPT** | Workspace memory provider | Medium |
| **CrewAI** | Shared memory interface | Medium |
| **Semantic Kernel** | Memory plugin | Medium |

---

## Research Completed ✅

| # | Topic | Report |
|---|-------|--------|
| 1 | LangChain/LangGraph memory | [01-langchain-langgraph-memory.md](01-langchain-langgraph-memory.md) |
| 2 | Mem0/MemGPT/Letta | [02-mem0-memgpt-letta.md](02-mem0-memgpt-letta.md) |
| 3 | Infrastructure (pgvector, Redis) | [03-infrastructure-vectordb-cache.md](03-infrastructure-vectordb-cache.md) |
| 4 | Agent harness patterns | [04-agent-harness-memory-patterns.md](04-agent-harness-memory-patterns.md) |
| 5 | Existing packages (gap analysis) | [05-existing-memory-packages.md](05-existing-memory-packages.md) |
| 6 | Memory taxonomy & theory | [06-memory-taxonomy-theory.md](06-memory-taxonomy-theory.md) |
| 7 | Consolidated findings | [07-consolidated-report.md](07-consolidated-report.md) |
| 8 | DeepAgents patterns | [08-deepagents-patterns.md](08-deepagents-patterns.md) |
| 9 | **HLD Document** | [09-HLD-memharness.md](09-HLD-memharness.md) |
| 10 | OpenClaw memory | [10-openclaw-memory.md](10-openclaw-memory.md) |

---

## Key Patterns Adopted

| Source | Pattern | Adoption |
|--------|---------|----------|
| **LangGraph** | 2-tier memory (short + long term) | ✅ |
| **LangGraph** | Namespace hierarchy | ✅ |
| **Mem0** | Simple API (add/search/update/delete) | ✅ |
| **MemGPT** | Agent-controlled memory (tools) | ✅ |
| **MemGPT** | Self-editing persona blocks | ✅ |
| **DeepAgents** | Pluggable backend protocol | ✅ |
| **DeepAgents** | CompositeBackend (router) | ✅ |
| **OpenClaw** | File-based memory export | ✅ Optional |
| **OpenClaw** | Daily logs pattern | ✅ Optional |
| **OpenClaw** | Pre-compaction flush | ✅ |

---

## Success Criteria

1. **Plug and Play**: 3-line setup for basic usage
2. **Framework Agnostic**: Works with any agent framework
3. **Production Ready**: PostgreSQL backend with proper indexing
4. **Developer Experience**: Great docs, type hints, async support
5. **Extensible**: Custom memory types, custom backends
6. **Observable**: Logging, metrics, debugging tools

---

## Open Questions — RESOLVED ✅

| Question | Resolution |
|----------|------------|
| LangChain VectorStore interface? | Support it via adapters, but own interface primary |
| Embedding model agnosticism? | User provides, we accept any callable |
| Memory agent abstraction? | User provides LLM, we provide agent logic |
| Schema migrations? | Auto-migration on version bump |
| Async-first or sync-first? | Async-first, sync wrappers available |
| Cross-thread memory? | Namespace-based sharing (configurable) |

---

*Created: 2026-03-22*
*Status: HLD Complete — Ready for Implementation*

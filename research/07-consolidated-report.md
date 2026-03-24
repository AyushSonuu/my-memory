# memharness — Consolidated Research Report

> Synthesis of all research for the Agent Memory Harness project

---

## Executive Summary

After researching **8 systems** (LangChain/LangGraph, Mem0, MemGPT/Letta, DeepAgents, OpenClaw, infrastructure options, existing packages, and memory theory), we have a clear picture of:

1. **What exists**: Good individual solutions, but no complete framework-agnostic harness
2. **What's missing**: Built-in memory agents, lifecycle management, 10+ memory types
3. **What memharness should be**: The definitive open-source agent memory infrastructure

---

## 1. Key Findings Summary

### 1.1 From LangChain/LangGraph (Report 01)

| Finding | Implication for memharness |
|---------|---------------------------|
| 2-tier model (short-term + long-term) | Adopt this architecture |
| Namespace hierarchy | Use `(org, user, thread)` |
| Checkpointer pattern | Create similar interface |
| VectorStore interface | Support for compatibility |

### 1.2 From Mem0/MemGPT/Letta (Report 02)

| Finding | Implication for memharness |
|---------|---------------------------|
| Simple API (add/search/update/delete) | Use this pattern |
| Agent-controlled memory (MemGPT) | Memory ops as tools |
| Tiered storage (main/archival/recall) | 3-tier hot/warm/cold |
| Self-editing blocks (MemGPT) | Editable memory sections |

### 1.3 From Infrastructure (Report 03)

| Finding | Implication for memharness |
|---------|---------------------------|
| pgvector HNSW best for queries | Default index type |
| Hybrid SQL + vector critical | PostgreSQL primary |
| Redis excellent for caching | Layer for hot paths |
| SQLite viable for local | Development backend |

### 1.4 From Agent Harnesses (Report 04)

| Finding | Implication for memharness |
|---------|---------------------------|
| Every framework different | Need adapters |
| File-based memory (Claude) | Support markdown export |
| Thread model (OpenAI) | Use thread_id pattern |
| Pluggable connectors (SK) | Backend abstraction |

### 1.5 From Existing Packages (Report 05)

| Finding | Implication for memharness |
|---------|---------------------------|
| No complete solution exists | Opportunity |
| Framework lock-in common | Be framework-agnostic |
| No memory agents | Build them in |
| Limited memory types | Support 10+ |

### 1.6 From Memory Theory (Report 06)

| Finding | Implication for memharness |
|---------|---------------------------|
| Cognitive alignment | Map to human memory |
| Lifecycle is critical | Build lifecycle engine |
| Consistency varies by type | Per-type policies |
| Multi-agent patterns | Namespace isolation |

### 1.7 From DeepAgents (Report 08) — NEW

| Finding | Implication for memharness |
|---------|---------------------------|
| Pluggable backend protocol | Create `BackendProtocol` interface |
| CompositeBackend (router) | Route by memory type |
| StateBackend vs StoreBackend | Ephemeral vs persistent separation |
| Context offloading | Store large content, reference in context |
| Policy wrapper pattern | Enforce access rules |

### 1.9 From Tool Lens via VFS (Report 11) — NEW

| Finding | Implication for memharness |
|---------|---------------------------|
| VFS abstraction for tools | Toolbox uses virtual filesystem |
| Progressive discovery | Don't load all tools at once |
| Familiar operations (ls, cat, grep) | LLMs know these commands |
| 96% token savings | Major cost reduction |
| Scales to 10K+ tools | Enterprise-ready |

---

## 2. memharness Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER APPLICATION                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ LangChain   │  │ LangGraph   │  │ CrewAI      │  │ Custom      │    │
│  │ Agent       │  │ Agent       │  │ Agent       │  │ Agent       │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
        ┌───────────────────┐           ┌───────────────────┐
        │ Framework Adapters │           │ Direct API        │
        │ (langchain, etc.) │           │ (for any agent)   │
        └───────────────────┘           └───────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            memharness                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                         PUBLIC API                                  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐   │ │
│  │  │ Simple API   │  │ Advanced API │  │ Memory Tools           │   │ │
│  │  │ add/search/  │  │ transactions │  │ (for agent use)        │   │ │
│  │  │ update/del   │  │ lifecycle    │  │ archival_insert, etc.  │   │ │
│  │  └──────────────┘  └──────────────┘  └────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                       MEMORY MANAGER                                │ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │  Memory Types (CRUD per type)                                │   │ │
│  │  │  ┌─────┐ ┌────┐ ┌──────┐ ┌────────┐ ┌───────┐ ┌───────┐    │   │ │
│  │  │  │Conv.│ │ KB │ │Entity│ │Workflow│ │Toolbox│ │Summary│    │   │ │
│  │  │  └─────┘ └────┘ └──────┘ └────────┘ └───────┘ └───────┘    │   │ │
│  │  │  ┌────────┐ ┌──────┐ ┌────┐ ┌───────┐                       │   │ │
│  │  │  │Tool Log│ │Skills│ │File│ │Persona│  + Custom Types       │   │ │
│  │  │  └────────┘ └──────┘ └────┘ └───────┘                       │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  │                                                                     │ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │  Lifecycle Engine                                            │   │ │
│  │  │  consolidation | summarization | expiration | GC             │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  │                                                                     │ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │  Memory Agents (Built-in)                                    │   │ │
│  │  │  ┌───────────┐ ┌──────────┐ ┌────────┐ ┌─────────────────┐  │   │ │
│  │  │  │Summarizer │ │Consolidat│ │GC Agent│ │Entity Extractor │  │   │ │
│  │  │  └───────────┘ └──────────┘ └────────┘ └─────────────────┘  │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                       STORAGE LAYER                                 │ │
│  │  ┌────────────────────────────────────────────────────────────┐    │ │
│  │  │  Storage Abstraction (same interface, multiple backends)   │    │ │
│  │  └────────────────────────────────────────────────────────────┘    │ │
│  │         │              │              │              │             │ │
│  │         ▼              ▼              ▼              ▼             │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐       │ │
│  │  │PostgreSQL│   │ SQLite   │   │  Redis   │   │In-Memory │       │ │
│  │  │+pgvector │   │+vectors  │   │ (cache)  │   │ (test)   │       │ │
│  │  └──────────┘   └──────────┘   └──────────┘   └──────────┘       │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

| Component | Responsibility |
|-----------|---------------|
| **Public API** | Simple interface for all users |
| **Memory Manager** | CRUD operations, type registry |
| **Lifecycle Engine** | Automated maintenance |
| **Memory Agents** | LLM-powered memory tasks |
| **Storage Layer** | Backend abstraction |
| **Adapters** | Framework integrations |

---

## 3. Memory Types (Final Taxonomy)

### 3.1 The 10 Core Types

```
memharness Memory Types
│
├── EPISODIC (experiences)
│   ├── 1. Conversational   → Chat history, thread-scoped
│   ├── 2. Summary          → Compressed conversations
│   └── 3. Tool Log         → Execution audit trail
│
├── SEMANTIC (facts)
│   ├── 4. Knowledge Base   → Documents, passages
│   ├── 5. Entity           → People, orgs, concepts
│   ├── 6. File             → Document references
│   └── 7. Persona          → Agent identity
│
└── PROCEDURAL (how-to)
    ├── 8. Workflow         → Reusable step patterns
    ├── 9. Toolbox          → Tool definitions
    └── 10. Skills          → Learned capabilities
```

### 3.2 Storage Strategy

| Type | Primary Storage | Index | Access Pattern |
|------|----------------|-------|----------------|
| Conversational | SQL | B-tree (thread_id, timestamp) | Exact + temporal |
| Summary | Vector | HNSW | Semantic search |
| Tool Log | SQL | B-tree (thread_id, timestamp) | Exact + temporal |
| Knowledge Base | Vector | HNSW | Semantic search |
| Entity | Vector | HNSW | Semantic + exact |
| File | SQL + Vector | B-tree + HNSW | Hybrid |
| Persona | Vector | HNSW | Semantic search |
| Workflow | Vector | HNSW | Semantic search |
| Toolbox | Vector | HNSW | Semantic search |
| Skills | Vector | HNSW | Semantic search |

---

## 4. API Design

### 4.1 Simple API (App Developers)

```python
from memharness import MemoryHarness

# Initialize with backend
memory = MemoryHarness(backend="postgresql://...")

# Basic operations
memory.add(
    content="User prefers Python",
    memory_type="entity",
    namespace=("user", "alice"),
)

results = memory.search(
    query="programming preferences",
    memory_type="entity",
    namespace=("user", "alice"),
    k=5,
)

memory.update(memory_id="xxx", content="User prefers TypeScript now")

memory.delete(memory_id="xxx")
```

### 4.2 Advanced API (Framework Authors)

```python
from memharness import MemoryHarness, LifecyclePolicy

memory = MemoryHarness(backend="postgresql://...")

# Transactions
async with memory.transaction() as txn:
    txn.write_conversational(thread_id, "user", content)
    txn.write_entity(namespace, entity)
    # Atomic commit

# Lifecycle policies
memory.configure_lifecycle([
    LifecyclePolicy(
        memory_type="conversational",
        condition=lambda m: m.age > timedelta(days=7),
        action="summarize",
    ),
])

# Custom memory types
@memory.register_type("my_custom")
class MyCustomMemory(BaseMemoryType):
    ...
```

### 4.3 Memory Tools API (For Agents)

```python
from memharness import MemoryHarness
from memharness.tools import get_memory_tools

memory = MemoryHarness(backend="...")

# Get tools for agent use
tools = get_memory_tools(memory, include=[
    "archival_memory_insert",
    "archival_memory_search",
    "core_memory_edit",
    "conversation_search",
])

# Use with any agent framework
agent = YourAgent(tools=tools)
```

---

## 5. Framework Integrations

### 5.1 LangChain Integration

```python
from memharness.integrations.langchain import MemharnessMemory

memory = MemharnessMemory(backend="postgresql://...")

# Use as LangChain memory
from langchain.chains import ConversationChain
chain = ConversationChain(llm=llm, memory=memory)
```

### 5.2 LangGraph Integration

```python
from memharness.integrations.langgraph import MemharnessCheckpointer, MemharnessStore

# As checkpointer (short-term)
checkpointer = MemharnessCheckpointer(backend="postgresql://...")
graph = builder.compile(checkpointer=checkpointer)

# As store (long-term)
store = MemharnessStore(backend="postgresql://...")
```

### 5.3 Claude Code Integration

```python
from memharness.integrations.claude import sync_with_claude_memory

# Sync memharness with CLAUDE.md / .claude/memory/
sync_with_claude_memory(memory, project_root="/path/to/project")
```

---

## 6. Memory Agents

### 6.1 Built-in Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| **Summarizer** | Compress old conversations | Age threshold |
| **Consolidator** | Merge duplicate memories | Similarity threshold |
| **GC Agent** | Remove expired/stale memories | TTL / policy |
| **Entity Extractor** | Extract structured facts | On write |
| **Relationship Builder** | Link related entities | Periodic |

### 6.2 Agent Interface

```python
from memharness.agents import SummarizerAgent, ConsolidatorAgent

# Configure agents
summarizer = SummarizerAgent(
    memory=memory,
    llm=your_llm,  # User provides LLM
    policy=SummarizationPolicy(
        threshold_age=timedelta(days=7),
        threshold_tokens=1000,
    ),
)

# Run agents
await summarizer.run()

# Or schedule
memory.schedule_agent(summarizer, cron="0 3 * * *")  # 3 AM daily
```

---

## 7. Storage Backends

### 7.1 Backend Selection

| Use Case | Recommended Backend |
|----------|-------------------|
| **Production** | PostgreSQL + pgvector |
| **Development** | SQLite + sqlite-vss |
| **Testing** | In-memory |
| **Caching layer** | Redis (on top of primary) |

### 7.2 Configuration

```python
# PostgreSQL (production)
memory = MemoryHarness(
    backend="postgresql://user:pass@localhost/db",
    cache="redis://localhost:6379",
)

# SQLite (development)
memory = MemoryHarness(backend="sqlite:///./memory.db")

# In-memory (testing)
memory = MemoryHarness(backend="memory://")

# With custom embedding model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

memory = MemoryHarness(
    backend="postgresql://...",
    embedding_model=model,
)
```

---

## 8. Implementation Priorities

### 8.1 Phase 1: Core (v0.1)

| Component | Priority |
|-----------|----------|
| Memory Manager | P0 |
| 5 memory types (Conv, KB, Entity, Workflow, Toolbox) | P0 |
| PostgreSQL backend | P0 |
| SQLite backend | P0 |
| Simple API | P0 |
| Basic tests | P0 |

### 8.2 Phase 2: Complete (v0.2)

| Component | Priority |
|-----------|----------|
| All 10 memory types | P1 |
| In-memory backend | P1 |
| Redis caching | P1 |
| Memory tools API | P1 |
| Lifecycle engine (basic) | P1 |
| LangChain adapter | P1 |

### 8.3 Phase 3: Production (v1.0)

| Component | Priority |
|-----------|----------|
| Memory agents | P2 |
| All framework adapters | P2 |
| Full lifecycle management | P2 |
| Server mode (REST API) | P2 |
| Documentation | P2 |
| Performance optimization | P2 |

---

## 9. Success Metrics

| Metric | Target |
|--------|--------|
| **Setup time** | < 3 lines of code |
| **Memory types** | 10+ out of box |
| **Backends** | 4 (PostgreSQL, SQLite, Redis, Memory) |
| **Framework adapters** | 3+ (LangChain, LangGraph, CrewAI) |
| **Test coverage** | > 80% |
| **Documentation** | Complete API docs + tutorials |

---

## 10. Open Questions (For HLD)

1. **Embedding model handling**: Bundle default or require user to provide?
2. **Async-first or sync-first**: Which API style is primary?
3. **Server mode protocol**: REST vs gRPC vs both?
4. **Graph memory**: Include in v1 or post-v1?
5. **Multi-tenancy**: Full support or extensible design only?

---

## 11. Next Steps

1. ✅ Research complete (8 systems analyzed)
2. ✅ HLD designed with detailed interfaces
3. ⏳ Create project structure
4. ⏳ Implement Phase 1
5. ⏳ Write tests
6. ⏳ Publish to PyPI

---

## 12. Research Documents Index

| # | Document | Content |
|---|----------|---------|
| 00 | [Project Brief](00-project-brief.md) | Vision, decisions, scope |
| 01 | [LangChain/LangGraph](01-langchain-langgraph-memory.md) | Memory patterns, checkpointers |
| 02 | [Mem0/MemGPT/Letta](02-mem0-memgpt-letta.md) | Memory-first architectures |
| 03 | [Infrastructure](03-infrastructure-vectordb-cache.md) | pgvector, Redis, SQLite |
| 04 | [Agent Harnesses](04-agent-harness-memory-patterns.md) | Claude Code, OpenAI, AutoGPT |
| 05 | [Existing Packages](05-existing-memory-packages.md) | Gap analysis |
| 06 | [Memory Theory](06-memory-taxonomy-theory.md) | Taxonomy, lifecycle |
| 07 | [Consolidated Report](07-consolidated-report.md) | This document |
| 08 | [DeepAgents](08-deepagents-patterns.md) | Pluggable backends |
| 09 | [HLD](09-HLD-memharness.md) | Technical specification |
| 10 | [OpenClaw](10-openclaw-memory.md) | File-based memory |
| 11 | [Tool Lens VFS](11-tool-lens-vfs-pattern.md) | **VFS tool discovery (96% token savings)** |

---

*Consolidated: 2026-03-22*
*Updated: 2026-03-22 (added DeepAgents + OpenClaw findings)*
*Total research files: 11*
*Total research content: ~165KB*

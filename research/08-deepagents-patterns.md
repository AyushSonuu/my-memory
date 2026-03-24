# DeepAgents Research — File System & Memory Patterns

> Additional research for memharness project

---

## Executive Summary

DeepAgents (by LangChain) is an **agent harness** built on LangGraph that provides sophisticated file system access, memory management, and sub-agent patterns. Its architecture offers valuable patterns for memharness, especially around **pluggable backends** and **context management**.

---

## 1. DeepAgents Overview

| Aspect | Details |
|--------|---------|
| **Package** | `deepagents` (PyPI) |
| **Maintainer** | LangChain team |
| **Built On** | LangGraph |
| **Version** | 0.4.12 (March 2026) |
| **License** | MIT |

### Core Capabilities

1. **Planning Tool** — `write_todos` for task decomposition
2. **File System** — `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`
3. **Shell Access** — `execute` tool with sandboxing
4. **Sub-agents** — `task` function for isolated child agents
5. **Context Management** — Automatic summarization for long conversations
6. **Memory** — LangGraph Memory Store for cross-thread persistence

---

## 2. File System Architecture

### 2.1 Pluggable Backend Pattern

DeepAgents uses a **pluggable backend system** where file operations route through configurable backends:

```python
from deepagents import create_deep_agent
from deepagents.backends import StateBackend, FilesystemBackend, StoreBackend

# Choose backend based on use case
agent = create_deep_agent(backend=StateBackend())  # Ephemeral
agent = create_deep_agent(backend=FilesystemBackend(root_dir="./workspace"))  # Local
agent = create_deep_agent(backend=StoreBackend(store=my_store))  # Persistent
```

### 2.2 Backend Types

| Backend | Persistence | Scope | Use Case |
|---------|-------------|-------|----------|
| **StateBackend** | Thread-only | Ephemeral | Scratchpad, temp files |
| **FilesystemBackend** | Disk | Local | Real file access |
| **LocalShellBackend** | Disk + Shell | Local | Full system access |
| **StoreBackend** | Cross-thread | Durable | LangGraph store (Redis, Postgres) |
| **CompositeBackend** | Mixed | Router | Route by path prefix |

### 2.3 CompositeBackend Pattern

Routes operations to different backends based on path:

```python
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

composite = CompositeBackend(routes={
    "/scratch/": StateBackend(),      # Ephemeral
    "/memories/": StoreBackend(...),  # Persistent
    "/workspace/": FilesystemBackend(root_dir="./"),  # Local disk
})

agent = create_deep_agent(backend=composite)
```

### 2.4 Custom Backend Protocol

```python
class BackendProtocol:
    """Interface for custom file system backends."""

    def ls_info(self, path: str) -> List[FileInfo]: ...
    def read(self, path: str) -> bytes: ...
    def write(self, path: str, content: bytes) -> None: ...
    def edit(self, path: str, edits: List[Edit]) -> None: ...
    def glob_info(self, pattern: str) -> List[FileInfo]: ...
    def grep_raw(self, pattern: str, path: str) -> List[Match]: ...
```

---

## 3. Memory Management

### 3.1 Memory Sources

DeepAgents uses multiple memory sources:

| Source | Description |
|--------|-------------|
| **AGENTS.md** | Persistent context files loaded automatically |
| **LangGraph Checkpoints** | Thread-scoped state persistence |
| **LangGraph Store** | Cross-thread durable storage |
| **StoreBackend** | Files persisted across threads |

### 3.2 Context Management

**Automatic Summarization:**
- Triggered for long conversations
- Compresses history to fit context window
- Large outputs routed to files instead of context

**Context Budget:**
- File system operations offload content from context
- Sub-agents get isolated context windows
- Results stored in files, references in context

### 3.3 Memory Pattern

```python
# Memory flows in DeepAgents:
#
# 1. AGENTS.md → Loaded at start (project context)
# 2. Checkpoints → State saved after each step (thread memory)
# 3. StoreBackend → Cross-thread file persistence
# 4. Summarization → Automatic context compression
```

---

## 4. Sub-Agent Architecture

### 4.1 Context Isolation

Sub-agents have **isolated context windows**:

```python
# Main agent delegates to sub-agent
result = agent.task(
    prompt="Research topic X",
    tools=[search_tool],  # Limited tool set
    system_prompt="You are a researcher...",  # Custom prompt
)
# Sub-agent returns result, main context stays clean
```

### 4.2 Sub-Agent Benefits

1. **Context Protection**: Main agent context not polluted
2. **Specialization**: Different prompts/tools per sub-agent
3. **Parallelization**: Multiple sub-agents can run concurrently
4. **Failure Isolation**: Sub-agent failure doesn't crash main agent

---

## 5. Key Patterns for memharness

### 5.1 Adopt: Pluggable Backend Pattern

```python
# memharness should have similar pluggable backends
class MemoryBackend(Protocol):
    async def read(self, namespace: tuple, key: str) -> Optional[dict]: ...
    async def write(self, namespace: tuple, key: str, value: dict) -> str: ...
    async def search(self, namespace: tuple, query: str, k: int) -> List[dict]: ...
    async def delete(self, namespace: tuple, key: str) -> bool: ...

# Implementations
class PostgresBackend(MemoryBackend): ...
class SqliteBackend(MemoryBackend): ...
class RedisBackend(MemoryBackend): ...
class InMemoryBackend(MemoryBackend): ...
```

### 5.2 Adopt: Composite/Router Pattern

```python
# Route different memory types to different backends
from memharness import CompositeBackend

backend = CompositeBackend(routes={
    "conversational": PostgresBackend(...),  # SQL for ordered data
    "knowledge_base": PostgresBackend(...),  # pgvector for semantic
    "cache": RedisBackend(...),              # Hot path caching
    "working": InMemoryBackend(),            # Session scratchpad
})
```

### 5.3 Adopt: Context Offloading

```python
# Large memory content → stored, reference in context
memory.write_knowledge_base(large_document)
# Returns: "Stored as kb_12345. Use expand_memory('kb_12345') to retrieve."

# Agent can expand when needed
content = memory.expand_memory("kb_12345")
```

### 5.4 Adopt: Memory Agents with Isolation

```python
# Memory management agents run in isolated context
summarizer_agent = memory.create_agent(
    "summarizer",
    tools=[summarize_tool, write_summary_tool],
    isolated=True,  # Doesn't pollute main context
)
```

---

## 6. Comparison: DeepAgents vs memharness

| Aspect | DeepAgents | memharness (Planned) |
|--------|------------|---------------------|
| **Focus** | Agent harness | Memory infrastructure |
| **File System** | Full access | Memory-specific |
| **Memory Types** | Generic files | 10+ structured types |
| **Persistence** | LangGraph Store | Multi-backend (PG, SQLite, Redis) |
| **Memory Agents** | Sub-agents | Purpose-built memory agents |
| **Lifecycle** | Manual | Automated policies |
| **Framework** | LangGraph only | Framework agnostic |

---

## 7. Recommendations

### 7.1 What memharness Should Borrow

1. **Pluggable Backend Protocol** — Same interface, multiple implementations
2. **CompositeBackend Pattern** — Route by memory type/path
3. **Context Offloading** — Store large content, reference in context
4. **Policy Wrapper** — Enforce access rules
5. **Sub-agent Isolation** — Memory agents with isolated context

### 7.2 What memharness Should Add

1. **Structured Memory Types** — Not just files, but typed memories
2. **Semantic Search** — Vector similarity built-in
3. **Lifecycle Automation** — Summarize, consolidate, expire
4. **Multi-Framework Support** — Not just LangGraph
5. **Memory-Specific Agents** — Summarizer, Consolidator, GC

---

## 8. Updated Architecture

Based on DeepAgents patterns, updated memharness architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                       memharness API                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Memory Manager                         │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Memory Types (typed, not just files)               │  │   │
│  │  │  Conv | KB | Entity | Workflow | Toolbox | ...     │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 Backend Router (Composite)                │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐ │   │
│  │  │ SQL     │ │ Vector  │ │ Cache   │ │ In-Memory       │ │   │
│  │  │ Backend │ │ Backend │ │ Backend │ │ Backend         │ │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 Storage Implementations                   │   │
│  │  ┌──────────┐ ┌────────┐ ┌───────┐ ┌──────────────────┐  │   │
│  │  │PostgreSQL│ │ SQLite │ │ Redis │ │ Dict (testing)   │  │   │
│  │  │+pgvector │ │+vss    │ │       │ │                  │  │   │
│  │  └──────────┘ └────────┘ └───────┘ └──────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Memory Agents (Isolated Context)             │   │
│  │  Summarizer | Consolidator | GC | Entity Extractor       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Sources

- DeepAgents PyPI (pypi.org/project/deepagents)
- DeepAgents Documentation (docs.langchain.com/oss/python/deepagents)
- LangChain/LangGraph documentation

---

*Research completed: 2026-03-22*

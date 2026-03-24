# Existing Memory Packages — Gap Analysis

> Research Report for memharness project

---

## Executive Summary

The Python ecosystem has several agent memory packages, but none provide a complete, framework-agnostic memory harness. This report analyzes existing packages to identify gaps that memharness can fill.

---

## 1. Existing Packages Overview

### 1.1 Dedicated Memory Packages

| Package | Focus | Status | Stars |
|---------|-------|--------|-------|
| **Mem0** | Memory as a service | Active | ~20k |
| **Zep** | Memory server for LLM apps | Active | ~2k |
| **LangMem** | LangChain memory utils | Active | ~1k |
| **Motorhead** | Rust memory server | Stale | ~500 |

### 1.2 Framework-Embedded Memory

| Framework | Memory Module | Scope |
|-----------|--------------|-------|
| **LangChain** | `langchain.memory` | LangChain only |
| **LangGraph** | Checkpointers, Stores | LangGraph only |
| **LlamaIndex** | `ChatMemoryBuffer` | LlamaIndex only |
| **Haystack** | `ConversationMemory` | Haystack only |

---

## 2. Package Deep Dives

### 2.1 Mem0

**Focus:** Managed memory layer with graph capabilities

```python
from mem0 import Memory
m = Memory()
m.add("User likes Python", user_id="alice")
results = m.search("programming", user_id="alice")
```

**Strengths:**
- Simple API (add/search/update/delete)
- Auto-extraction of facts
- Graph memory for relationships
- Multi-framework support

**Limitations:**
- Managed service focus (self-host limited)
- No memory lifecycle management
- Limited memory types (user/agent/session)
- No built-in memory agents

### 2.2 Zep

**Focus:** Memory server with knowledge graphs

```python
from zep_cloud.client import Zep
client = Zep(api_key="...")

# Add memory
client.memory.add_session(session_id="123", ...)
client.memory.add(session_id="123", messages=[...])

# Search
results = client.memory.search_sessions(
    text="programming preferences",
    user_id="alice"
)
```

**Strengths:**
- Temporal knowledge graphs
- Fact extraction
- Session management
- LangGraph integration

**Limitations:**
- Server-based (requires infrastructure)
- Cloud-focused
- Limited memory types

### 2.3 LangMem

**Focus:** LangChain memory utilities

```python
from langmem import create_manage_memory_tool

tool = create_manage_memory_tool(
    storage=...,
    instructions="Store user preferences"
)
```

**Strengths:**
- LangGraph native
- Memory as tools pattern

**Limitations:**
- LangChain/LangGraph only
- Limited functionality

### 2.4 Motorhead

**Focus:** Rust-based memory server

```rust
// Server-side Rust implementation
// Provides REST API for memory operations
```

**Strengths:**
- High performance (Rust)
- REST API

**Limitations:**
- Appears stale/unmaintained
- Server-only (no embedded)
- Limited documentation

---

## 3. Feature Comparison

| Feature | Mem0 | Zep | LangMem | LangChain | memharness (planned) |
|---------|------|-----|---------|-----------|---------------------|
| **Memory Types** | 3 | 2 | 1 | 7 | 10+ |
| **Framework Agnostic** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Embedded Mode** | Limited | ❌ | ✅ | ✅ | ✅ |
| **Server Mode** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Graph Memory** | ✅ | ✅ | ❌ | ❌ | Planned |
| **Memory Agents** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Lifecycle Mgmt** | ❌ | Partial | ❌ | ❌ | ✅ |
| **Multi-backend** | Limited | ❌ | ❌ | Partial | ✅ |
| **Open Source** | Partial | Partial | ✅ | ✅ | ✅ |

---

## 4. Identified Gaps

### 4.1 No Complete Solution

**Problem:** No single package provides:
- All memory types (conversational, semantic, procedural, episodic)
- Framework-agnostic interface
- Both embedded and server modes
- Built-in memory management agents
- Full lifecycle management

**memharness Opportunity:** Be the complete solution.

### 4.2 Framework Lock-in

**Problem:** Most memory solutions are tied to specific frameworks:
- LangChain memory only works with LangChain
- LangGraph stores only work with LangGraph
- No way to share memory across frameworks

**memharness Opportunity:** Single memory layer, multiple framework adapters.

### 4.3 No Memory Agents

**Problem:** No package provides built-in agents for:
- Memory consolidation (merging duplicates)
- Summarization (compressing old memories)
- Garbage collection (removing stale memories)
- Entity extraction (structured fact extraction)

**memharness Opportunity:** Built-in memory management agents.

### 4.4 Limited Memory Types

**Problem:** Most packages support 2-3 memory types:

| Package | Types |
|---------|-------|
| Mem0 | User, Agent, Session |
| Zep | Facts, Summaries |
| LangChain | Buffer, Summary, Entity, Vector, KG |

**memharness Opportunity:** 10+ memory types out of the box, extensible for custom types.

### 4.5 No Lifecycle Management

**Problem:** No package provides:
- Automatic memory expiration
- Memory consolidation policies
- Context window budget management
- Memory versioning

**memharness Opportunity:** Full lifecycle management with policies.

### 4.6 Backend Limitations

**Problem:** Most packages support 1-2 backends:

| Package | Backends |
|---------|----------|
| Mem0 | Managed only |
| Zep | Managed / self-host |
| LangChain | Many via VectorStore |

**memharness Opportunity:** PostgreSQL, SQLite, Redis, In-memory with same API.

---

## 5. Architectural Patterns to Adopt

### 5.1 From Mem0

```python
# Simple API pattern
memory.add(content, user_id=..., metadata=...)
memory.search(query, user_id=..., filters=...)
memory.update(memory_id, content)
memory.delete(memory_id)
```

### 5.2 From LangGraph

```python
# Namespace-based isolation
namespace = ("org", "user", "thread")
store.put(namespace, key, value)
store.get(namespace, key)
store.search(namespace, query)
```

### 5.3 From MemGPT

```python
# Memory as tools
memory_tools = [
    ArchivalMemoryInsert(),
    ArchivalMemorySearch(),
    CoreMemoryEdit(),
]
agent = Agent(tools=memory_tools)
```

### 5.4 From Semantic Kernel

```python
# Pluggable connectors
class MemoryStore(ABC):
    @abstractmethod
    async def save(self, collection, id, text, metadata): ...
    @abstractmethod
    async def search(self, collection, query, limit): ...

# Implementations
class PostgresStore(MemoryStore): ...
class SqliteStore(MemoryStore): ...
class RedisStore(MemoryStore): ...
```

---

## 6. Competitive Positioning

### 6.1 memharness Differentiators

| Differentiator | Why It Matters |
|----------------|----------------|
| **Framework Agnostic** | Use with any agent framework |
| **10+ Memory Types** | Complete memory taxonomy |
| **Built-in Memory Agents** | Automated maintenance |
| **Both Embedded & Server** | Flexibility in deployment |
| **Full Lifecycle Mgmt** | Production-ready |
| **Open Source** | Community-driven, auditable |

### 6.2 Target Users

| User Type | Pain Point | memharness Value |
|-----------|-----------|------------------|
| **Framework Author** | Need low-level memory control | Extensible interfaces |
| **App Developer** | Need simple, working memory | High-level API |
| **Enterprise** | Need production-grade | PostgreSQL, multi-tenant |
| **Researcher** | Need to experiment | SQLite, in-memory |

---

## 7. Recommendations

### 7.1 Must-Have for v1

1. **Core memory types**: All 10+ types
2. **Multi-backend**: PostgreSQL, SQLite, Redis, In-memory
3. **Simple API**: add/search/update/delete
4. **Framework adapters**: LangChain, LangGraph, CrewAI
5. **Memory agents**: Summarizer, Consolidator, GC

### 7.2 Nice-to-Have for v1

1. Graph memory (entity relationships)
2. Server mode (REST API)
3. Memory versioning
4. Observability (metrics, logging)

### 7.3 Post-v1

1. More framework integrations
2. Advanced memory agents
3. Memory analytics
4. Cloud-managed option

---

## 8. Package Name Research

| Name | Available on PyPI | Notes |
|------|------------------|-------|
| `memharness` | Likely available | Short, catchy |
| `agentmemory` | Taken | - |
| `agent-memory` | Taken | - |
| `memory-harness` | Likely available | Longer |
| `memorykit` | Taken | - |

**Recommendation:** Check `memharness` availability, register early.

---

## Sources

- PyPI package listings
- GitHub repositories for each package
- Package documentation
- Community discussions (Discord, Reddit)

---

*Research completed: 2026-03-22*

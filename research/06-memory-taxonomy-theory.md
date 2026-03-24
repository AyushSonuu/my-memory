# Memory Taxonomy & Theoretical Foundations

> Research Report for memharness project

---

## Executive Summary

Agent memory systems are inspired by cognitive science models of human memory. This report maps cognitive memory types to technical implementations and proposes a comprehensive taxonomy for memharness.

---

## 1. Cognitive Science Foundations

### 1.1 Human Memory Model

```
Human Memory
├── Sensory Memory (milliseconds)
│   └── Iconic, echoic, haptic
│
├── Short-Term / Working Memory (seconds-minutes)
│   └── Limited capacity (~7 items)
│   └── Active manipulation
│
└── Long-Term Memory (permanent)
    ├── Explicit (Declarative)
    │   ├── Episodic (events, experiences)
    │   └── Semantic (facts, concepts)
    │
    └── Implicit (Non-declarative)
        ├── Procedural (skills, habits)
        └── Priming, conditioning
```

### 1.2 Mapping to AI Agents

| Human Memory | AI Agent Equivalent | Implementation |
|--------------|-------------------|----------------|
| **Sensory** | Input buffer | Token stream, embeddings |
| **Working** | Context window | LLM context, scratchpad |
| **Episodic** | Conversation history | Message logs, experiences |
| **Semantic** | Knowledge base | Facts, documents, entities |
| **Procedural** | Workflows, tools | Step patterns, tool configs |

---

## 2. Memory Taxonomy for Agents

### 2.1 Temporal Dimension

```
Agent Memory (Temporal View)
│
├── Ephemeral (session only)
│   ├── Working Memory (scratchpad)
│   └── Semantic Cache (LLM response cache)
│
├── Short-Term (hours-days)
│   ├── Recent Conversations
│   └── Active Task Context
│
└── Long-Term (persistent)
    ├── User Preferences
    ├── Knowledge Base
    ├── Entity Facts
    ├── Workflow Patterns
    └── Tool Configurations
```

### 2.2 Functional Dimension

```
Agent Memory (Functional View)
│
├── Episodic (experiences)
│   ├── Conversational Memory
│   ├── Tool Log (execution history)
│   └── Summary Memory (compressed episodes)
│
├── Semantic (facts)
│   ├── Knowledge Base (documents)
│   ├── Entity Memory (people, orgs)
│   └── File Memory (document references)
│
└── Procedural (how-to)
    ├── Workflow Memory (step patterns)
    ├── Toolbox Memory (tool definitions)
    └── Skills Memory (learned behaviors)
```

### 2.3 Access Patterns

| Memory Type | Write Pattern | Read Pattern |
|-------------|--------------|--------------|
| **Conversational** | Every turn | Thread context |
| **Knowledge Base** | Ingestion | Semantic search |
| **Entity** | Extraction | Lookup + search |
| **Workflow** | Post-task | Pattern match |
| **Toolbox** | Registration | Semantic search |
| **Summary** | Consolidation | Expand on demand |
| **Tool Log** | Every tool call | Audit, JIT |
| **Skills** | Learning events | Capability match |
| **File** | Document events | Reference lookup |

---

## 3. Complete Memory Type Taxonomy for memharness

### 3.1 The 10 Core Memory Types

| # | Type | Category | Description | Storage |
|---|------|----------|-------------|---------|
| 1 | **Conversational** | Episodic | Chat history per thread | SQL (ordered) |
| 2 | **Knowledge Base** | Semantic | Documents, facts | Vector |
| 3 | **Entity** | Semantic | People, orgs, concepts | Vector |
| 4 | **Workflow** | Procedural | Reusable step patterns | Vector |
| 5 | **Toolbox** | Procedural | Tool definitions | Vector |
| 6 | **Summary** | Episodic | Compressed conversations | Vector |
| 7 | **Tool Log** | Episodic | Execution audit trail | SQL |
| 8 | **Skills** | Procedural | Learned agent capabilities | Vector |
| 9 | **File** | Semantic | Document references | SQL + Vector |
| 10 | **Persona** | Semantic | Agent identity, behavior | Vector |

### 3.2 Extended Types (User-Defined)

```python
# memharness supports custom memory types
from memharness import BaseMemoryType, register_memory_type

@register_memory_type("custom")
class CustomMemory(BaseMemoryType):
    schema = {
        "content": str,
        "category": str,
        "priority": int,
        "metadata": dict,
    }

    def write(self, content, **kwargs): ...
    def read(self, query, **kwargs): ...
    def search(self, query, k=5, **kwargs): ...
```

---

## 4. Memory Lifecycle

### 4.1 Lifecycle Stages

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY LIFECYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. CREATION      2. ENRICHMENT     3. STORAGE             │
│   ┌─────────┐      ┌─────────┐       ┌─────────┐           │
│   │ Ingest  │ ──►  │ Embed   │ ──►   │ Persist │           │
│   │ Extract │      │ Augment │       │ Index   │           │
│   └─────────┘      └─────────┘       └─────────┘           │
│                                           │                 │
│                                           ▼                 │
│   6. EXPIRATION    5. RETRIEVAL      4. ORGANIZATION       │
│   ┌─────────┐      ┌─────────┐       ┌─────────┐           │
│   │ Archive │ ◄──  │ Search  │ ◄──   │ Cluster │           │
│   │ Delete  │      │ Rank    │       │ Link    │           │
│   └─────────┘      └─────────┘       └─────────┘           │
│                         │                                   │
│                         ▼                                   │
│                    7. CONSOLIDATION                         │
│                    ┌─────────────┐                          │
│                    │ Summarize   │                          │
│                    │ Deduplicate │                          │
│                    │ Merge       │                          │
│                    └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Lifecycle Operations

| Stage | Operation | Description |
|-------|-----------|-------------|
| **Creation** | Ingest | Accept raw data |
| | Extract | Pull structured facts |
| **Enrichment** | Embed | Generate vectors |
| | Augment | Add metadata, timestamps |
| **Storage** | Persist | Write to backend |
| | Index | Create search indexes |
| **Organization** | Cluster | Group similar items |
| | Link | Create relationships |
| **Retrieval** | Search | Semantic + exact |
| | Rank | Relevance scoring |
| **Expiration** | Archive | Move to cold storage |
| | Delete | Remove permanently |
| **Consolidation** | Summarize | Compress old data |
| | Deduplicate | Remove duplicates |
| | Merge | Combine related items |

### 4.3 Lifecycle Policies

```python
# memharness lifecycle policies
from memharness import LifecyclePolicy

policies = [
    # Auto-summarize conversations older than 7 days
    LifecyclePolicy(
        memory_type="conversational",
        condition=lambda m: m.age > timedelta(days=7),
        action="summarize",
    ),

    # Archive tool logs older than 30 days
    LifecyclePolicy(
        memory_type="tool_log",
        condition=lambda m: m.age > timedelta(days=30),
        action="archive",
    ),

    # Delete expired memories
    LifecyclePolicy(
        memory_type="*",
        condition=lambda m: m.expires_at and m.expires_at < now(),
        action="delete",
    ),
]

memory.configure_lifecycle(policies)
```

---

## 5. Memory Consistency Models

### 5.1 Consistency Requirements

| Memory Type | Consistency | Rationale |
|-------------|-------------|-----------|
| **Conversational** | Strong | Order matters |
| **Knowledge Base** | Eventual | Search tolerates delay |
| **Entity** | Eventual | Facts can be stale briefly |
| **Workflow** | Eventual | Patterns are stable |
| **Toolbox** | Strong | Tools must be accurate |
| **Tool Log** | Strong | Audit trail integrity |

### 5.2 ACID for Agent Memory

| Property | Application |
|----------|-------------|
| **Atomicity** | Multi-memory writes succeed/fail together |
| **Consistency** | Memory state always valid |
| **Isolation** | Threads don't interfere |
| **Durability** | Writes persist after confirmation |

```python
# Transactional memory operations
async with memory.transaction() as txn:
    txn.write_conversation(msg)
    txn.write_entity(extracted_entity)
    txn.write_tool_log(tool_result)
    # All succeed or all fail
```

---

## 6. Multi-Agent Memory Patterns

### 6.1 Isolation Levels

```
Multi-Agent Memory Isolation
│
├── Full Isolation
│   └── Each agent has separate memory
│   └── No sharing whatsoever
│
├── Selective Sharing
│   └── Some memory types shared
│   └── Others private
│
├── Hierarchical Sharing
│   └── Organization → User → Thread
│   └── Higher levels visible to lower
│
└── Full Sharing
    └── All agents share all memory
    └── Collaborative scenarios
```

### 6.2 Namespace Design

```python
# Hierarchical namespace for isolation
namespace = (
    "org:acme",        # Organization level
    "user:alice",      # User level
    "agent:assistant", # Agent level
    "thread:123",      # Thread level
)

# Sharing controlled by namespace scope
memory.read(namespace[:2], ...)  # Org + User level (shared)
memory.read(namespace, ...)       # Full isolation
```

### 6.3 Cross-Agent Communication via Memory

```python
# Pattern: Message passing through shared memory
agent_a.write_memory(
    namespace=("shared", "task_queue"),
    content={"task": "research X", "for_agent": "agent_b"}
)

# Agent B reads shared memory
tasks = agent_b.read_memory(
    namespace=("shared", "task_queue"),
    filter={"for_agent": "agent_b"}
)
```

---

## 7. Memory Retrieval Strategies

### 7.1 Retrieval Methods

| Method | Use Case | Implementation |
|--------|----------|----------------|
| **Exact Match** | ID lookup, thread_id | SQL WHERE |
| **Semantic Search** | Find similar content | Vector similarity |
| **Keyword Search** | Specific terms | Full-text search |
| **Hybrid** | Best of both | Vector + keyword + filter |
| **Graph Traversal** | Relationships | Entity links |
| **Temporal** | Time-based | ORDER BY timestamp |

### 7.2 Ranking and Reranking

```python
# Multi-stage retrieval
async def retrieve(query, k=10):
    # Stage 1: Broad vector search
    candidates = await memory.vector_search(query, k=50)

    # Stage 2: Apply filters
    filtered = [c for c in candidates if c.type == "knowledge_base"]

    # Stage 3: Rerank with cross-encoder
    reranked = reranker.rerank(query, filtered)

    # Stage 4: Return top-k
    return reranked[:k]
```

### 7.3 Context Assembly

```python
# Assemble optimal context from memory
def assemble_context(query, thread_id, max_tokens=4000):
    context = []
    budget = max_tokens

    # Priority 1: Recent conversation
    conv = memory.read_conversational(thread_id, limit=10)
    context.append(("## Conversation", conv))
    budget -= count_tokens(conv)

    # Priority 2: Relevant knowledge
    if budget > 1000:
        kb = memory.search_knowledge_base(query, k=5)
        context.append(("## Knowledge Base", kb))
        budget -= count_tokens(kb)

    # Priority 3: Relevant entities
    if budget > 500:
        entities = memory.search_entity(query, k=5)
        context.append(("## Entities", entities))

    return format_context(context)
```

---

## 8. Theoretical Framework for memharness

### 8.1 Core Principles

1. **Memory is Infrastructure**: Separate from agent logic
2. **Cognitive Alignment**: Map to human memory types
3. **Lifecycle Awareness**: Memory evolves over time
4. **Consistency Guarantees**: Appropriate for each type
5. **Flexible Isolation**: From full sharing to full isolation
6. **Retrieval Diversity**: Multiple access patterns

### 8.2 Design Axioms

| Axiom | Implication |
|-------|-------------|
| **Memory ≠ Storage** | Memory includes lifecycle, retrieval, agents |
| **Context is Finite** | Must manage what enters LLM context |
| **Freshness Decays** | Older memories need consolidation |
| **Relevance is Dynamic** | What's relevant depends on current task |
| **Agents Learn** | Memory enables adaptation over time |

---

## 9. Recommendations for memharness

### 9.1 Memory Type Implementation

| Type | Priority | Rationale |
|------|----------|-----------|
| Conversational | P0 | Core to any agent |
| Knowledge Base | P0 | RAG foundation |
| Entity | P0 | Structured facts |
| Workflow | P1 | Reusable patterns |
| Toolbox | P1 | Dynamic tool selection |
| Summary | P1 | Context management |
| Tool Log | P1 | Audit, debugging |
| Skills | P2 | Advanced learning |
| File | P2 | Document management |
| Persona | P2 | Agent identity |

### 9.2 Lifecycle Implementation

| Stage | Priority |
|-------|----------|
| Creation, Storage, Retrieval | P0 |
| Enrichment (embedding) | P0 |
| Consolidation (summarize) | P1 |
| Expiration (archive, delete) | P1 |
| Organization (cluster, link) | P2 |

### 9.3 Consistency Implementation

| Level | Priority |
|-------|----------|
| Single-write consistency | P0 |
| Transaction support | P1 |
| Multi-agent isolation | P1 |
| Cross-backend consistency | P2 |

---

## Sources

- Cognitive science literature on human memory
- AI/ML papers on agent memory systems
- MemGPT paper (virtual context management)
- LangGraph documentation (memory concepts)
- DeepLearning.AI Agent Memory course

---

*Research completed: 2026-03-22*

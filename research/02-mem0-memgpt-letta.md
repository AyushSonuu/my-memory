# Mem0, MemGPT & Letta — Memory-First Architectures

> Research Report for memharness project

---

## Executive Summary

Mem0 and MemGPT/Letta represent the cutting edge of agent memory systems. Mem0 provides a managed memory layer with graph capabilities, while MemGPT pioneered the concept of "virtual context management" - treating LLM context as a limited resource managed by the agent itself.

---

## 1. Mem0 (mem0.ai)

### 1.1 Overview

Mem0 is a **context engineering platform** that provides:
- Managed memory infrastructure
- Temporal knowledge graphs
- Multi-modal memory support
- Framework integrations (LangChain, CrewAI, Vercel AI SDK)

### 1.2 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Mem0 Platform                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │ Memory API  │  │ Graph API   │  │ Search/Rerank   │ │
│  │ add/search  │  │ nodes/edges │  │ vector + graph  │ │
│  │ update/del  │  │ episodes    │  │                 │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────┤
│                  Managed Infrastructure                  │
│  Vector Store | Graph DB | Reranking | Embeddings       │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Memory Types

| Type | Scope | Description |
|------|-------|-------------|
| **User Memory** | Per-user | Persistent across all interactions |
| **Agent Memory** | Per-agent | Agent-specific context and learning |
| **Session Memory** | Per-conversation | Thread-scoped, short-term |

### 1.4 Core API

```python
from mem0 import Memory

# Initialize
m = Memory()

# Add memory (with automatic extraction)
m.add("I am working on improving my tennis skills", user_id="alice")

# Search
results = m.search("What sports does the user play?", user_id="alice")
# Returns: "Working on improving tennis skills"

# Update
m.update(memory_id="xxx", data="Plays tennis professionally now")

# Delete
m.delete(memory_id="xxx")

# Get all for user
all_memories = m.get_all(user_id="alice")
```

### 1.5 Graph Memory

Mem0's graph capability builds **temporal knowledge graphs**:

```python
# Relationships extracted automatically
m.add("Alice works at TechCorp with Bob", user_id="alice")

# Creates nodes: Alice, TechCorp, Bob
# Creates edges: works_at, works_with
# Timestamps for temporal tracking
```

**Graph Structure:**
- **Nodes**: Entities (people, orgs, concepts)
- **Edges**: Relationships with types
- **Episodes**: Time-scoped event groups
- **Communities**: Detected clusters

### 1.6 Key Features

| Feature | Description |
|---------|-------------|
| **Auto-extraction** | LLM extracts facts from text automatically |
| **Metadata filtering** | Query with filters on custom metadata |
| **Webhook events** | Memory lifecycle events for integrations |
| **MCP Protocol** | Model Context Protocol for AI assistants |
| **Multimodal** | Images, audio alongside text |
| **Async-first** | v1.0+ is async by default |

### 1.7 What memharness Can Learn

1. **Simple API**: add/search/update/delete is intuitive
2. **Auto-extraction**: LLM-powered fact extraction
3. **Graph relationships**: Beyond flat key-value
4. **User/Agent/Session scoping**: Multi-level isolation

---

## 2. MemGPT (Berkeley Research)

### 2.1 The Innovation: Virtual Context Management

MemGPT's key insight: **LLMs can manage their own memory** like an OS manages virtual memory.

```
Traditional Agent:
┌──────────────────────────────┐
│  Fixed Context Window        │
│  [All messages crammed in]   │
│  → Overflow = Error          │
└──────────────────────────────┘

MemGPT Agent:
┌──────────────────────────────┐
│  Main Context (Limited)      │  ← Active "RAM"
│  [System + Recent + Summary] │
├──────────────────────────────┤
│  Archival Memory (Unlimited) │  ← "Disk" storage
│  [Full history, documents]   │
├──────────────────────────────┤
│  Recall Memory (Searchable)  │  ← Indexed retrieval
│  [Conversation search]       │
└──────────────────────────────┘
     Agent controls paging ↑↓
```

### 2.2 Tiered Memory System

| Tier | Capacity | Access | Purpose |
|------|----------|--------|---------|
| **Main Context** | Limited (~8K tokens) | Always loaded | Active working memory |
| **Archival Memory** | Unlimited | Write + Search | Long-term storage |
| **Recall Memory** | Unlimited | Search only | Conversation history |

### 2.3 Memory Functions (Tools)

MemGPT gives the agent tools to manage its own memory:

```python
# Core memory editing (in main context)
core_memory_append(section: str, content: str)
core_memory_replace(section: str, old: str, new: str)

# Archival memory (long-term storage)
archival_memory_insert(content: str)
archival_memory_search(query: str, k: int) -> List[str]

# Recall memory (conversation history)
conversation_search(query: str, k: int) -> List[Message]
```

### 2.4 Core Memory Blocks

The main context has structured **blocks**:

```
CORE MEMORY (always in context):
┌─────────────────────────────────────┐
│ [persona]                           │
│ "I am a helpful assistant named..." │
├─────────────────────────────────────┤
│ [human]                             │
│ "User: Alice, prefers formal..."    │
├─────────────────────────────────────┤
│ [custom_block_1]                    │
│ "Project context: Building..."      │
└─────────────────────────────────────┘
```

The agent can **edit these blocks** to update its working knowledge.

### 2.5 Self-Editing Memory

Key capability: Agent modifies its own persona and understanding:

```
Agent: "The user mentioned they prefer bullet points."
→ Calls: core_memory_replace("human",
         old="prefers formal",
         new="prefers bullet points")
→ Next turn: Agent automatically uses bullet points
```

### 2.6 What memharness Can Learn

1. **Agent-controlled memory**: Give agents tools to manage memory
2. **Tiered storage**: Hot (context) + Warm (recall) + Cold (archival)
3. **Editable blocks**: Structured, updatable memory sections
4. **Self-improvement**: Agent learns by editing its own memory

---

## 3. Letta (MemGPT Evolution)

### 3.1 Overview

Letta is the **productionized version** of MemGPT, offering:
- Managed infrastructure
- Multi-agent support
- API-first design
- Enterprise features

### 3.2 Architecture

```
Letta Platform
├── Letta Code (Terminal agent)
├── Letta Code SDK (Application building)
└── Letta API (Memory + context management)

Key Concepts:
- Agents (stateful, memory-aware)
- Memory Blocks (editable context)
- Tools (actions + memory operations)
- Data Sources (external knowledge)
```

### 3.3 Memory Model

Letta inherits MemGPT's tiered model:

| Component | Description |
|-----------|-------------|
| **Core Memory** | Always in context, editable blocks |
| **Archival Memory** | Vector-indexed long-term storage |
| **Recall Memory** | Conversation history search |
| **Data Sources** | External documents/knowledge |

### 3.4 API Design

```python
from letta import Letta

client = Letta()

# Create agent with memory
agent = client.create_agent(
    name="assistant",
    memory_blocks=[
        {"name": "persona", "content": "I am helpful..."},
        {"name": "user", "content": ""},
    ],
    tools=["archival_memory_search", "archival_memory_insert"],
)

# Agent manages its own memory
response = agent.chat("Remember that I like Python")
# Agent internally calls archival_memory_insert
```

---

## 4. Comparison Table

| Feature | Mem0 | MemGPT | Letta |
|---------|------|--------|-------|
| **Focus** | Memory as service | Self-managing memory | Productionized MemGPT |
| **Memory Control** | External API | Agent-controlled | Agent-controlled |
| **Graph Support** | Yes (temporal) | No | Limited |
| **Self-Editing** | No | Yes | Yes |
| **Tiered Storage** | Implicit | Explicit 3-tier | Explicit 3-tier |
| **Multi-agent** | Yes | Limited | Yes |
| **Open Source** | Partially | Yes | Partially |
| **Deployment** | Managed/Self-host | Self-host | Managed/Self-host |

---

## 5. Key Takeaways for memharness

### 5.1 Must-Have Features

1. **Tiered storage**: Main context + Recall + Archival
2. **Agent-controlled memory**: Memory operations as tools
3. **Editable blocks**: Structured, updateable sections
4. **Auto-extraction**: LLM-powered fact extraction (optional)
5. **Graph relationships**: Entity linking (nice-to-have)

### 5.2 API Design Principles

```python
# memharness should support both patterns:

# Pattern 1: External control (like Mem0)
memory.add("User likes Python", user_id="alice")
results = memory.search("programming preferences", user_id="alice")

# Pattern 2: Agent-controlled (like MemGPT)
memory_tools = [
    memory.as_tool("archival_insert"),
    memory.as_tool("archival_search"),
    memory.as_tool("core_memory_edit"),
]
agent = Agent(tools=memory_tools)
```

### 5.3 Architecture Principles

1. **Separation of concerns**: Storage vs. retrieval vs. management
2. **Pluggable backends**: Same API, different storage
3. **Framework agnostic**: Works with any agent framework
4. **Observable**: Logging, metrics, debugging

---

## Sources

- Mem0 Documentation (docs.mem0.ai)
- MemGPT Paper: "MemGPT: Towards LLMs as Operating Systems"
- Letta Documentation (docs.letta.com)

---

*Research completed: 2026-03-22*

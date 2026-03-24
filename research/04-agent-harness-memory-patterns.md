# Agent Harness Memory Patterns

> Research Report for memharness project

---

## Executive Summary

Different agent frameworks handle memory in vastly different ways. This report analyzes memory patterns across 6 major agent harnesses to identify common patterns and gaps that memharness can address.

---

## 1. Claude Code (Anthropic CLI)

### 1.1 Memory Architecture

Claude Code uses a **file-based memory system**:

```
Project Root
├── CLAUDE.md           # Project-level instructions (always loaded)
├── .claude/
│   └── memory/         # Auto-memory directory
│       └── MEMORY.md   # Persistent learnings
└── ~/.claude/
    └── projects/
        └── {project}/
            └── memory/ # Cross-session memory
```

### 1.2 Memory Types

| Type | File | Scope | Persistence |
|------|------|-------|-------------|
| **Project Instructions** | CLAUDE.md | Project | Permanent |
| **Auto Memory** | .claude/memory/MEMORY.md | Project | Persistent |
| **Session State** | In-context | Session | Ephemeral |
| **User Settings** | ~/.claude/settings.json | Global | Permanent |

### 1.3 Auto-Memory Pattern

```markdown
# MEMORY.md (auto-generated)

## User Preferences
- Prefers TypeScript over JavaScript
- Uses pnpm as package manager

## Project Patterns
- API routes in src/api/
- Tests use Vitest

## Learned Corrections
- Don't use relative imports from root
```

### 1.4 Key Insights

- **File-based**: No database, just markdown files
- **Always loaded**: CLAUDE.md in every context
- **User-initiated save**: Agent can write to memory when told
- **Simple but effective**: Works for single-user, single-project

### 1.5 Limitations for memharness

- No semantic search (just file content)
- No multi-user support
- No structured memory types
- No memory lifecycle management

---

## 2. OpenAI Assistants API

### 2.1 Architecture

```
OpenAI Platform
├── Assistants (persistent agents)
├── Threads (conversation containers)
├── Messages (conversation history)
├── Runs (execution instances)
└── Vector Stores (file search)
```

### 2.2 Memory Types

| Type | Managed By | Persistence | Access |
|------|------------|-------------|--------|
| **Thread Messages** | Platform | Persistent | Per-thread |
| **File Search** | Vector Store | Persistent | Per-assistant |
| **Code Interpreter** | Sandbox | Per-run | Ephemeral files |
| **Assistant Instructions** | Config | Permanent | Always |

### 2.3 Thread Pattern

```python
from openai import OpenAI
client = OpenAI()

# Create thread (memory container)
thread = client.beta.threads.create()

# Add messages (builds history)
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Remember: I prefer Python"
)

# Run assistant (uses thread history)
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Thread persists across runs
# Resume anytime with thread_id
```

### 2.4 Key Insights

- **Platform-managed**: Memory is API state
- **Thread = conversation memory**: Simple model
- **File Search = knowledge base**: Uploaded files
- **No cross-thread memory**: Each thread isolated

### 2.5 Implications for memharness

- Thread model is intuitive (adopt for conversations)
- Need cross-thread memory (user-level, org-level)
- File search useful but limited

---

## 3. AutoGPT / AgentGPT

### 3.1 Architecture

```
AutoGPT Workspace
├── workspace/           # File operations
│   ├── inputs/
│   └── outputs/
├── memory/
│   ├── local_cache.json
│   └── chroma_db/      # Vector store
└── logs/
```

### 3.2 Memory Types

| Type | Storage | Purpose |
|------|---------|---------|
| **Short-term** | In-context | Current task chain |
| **Long-term** | Chroma/Pinecone | Semantic retrieval |
| **Workspace** | File system | Task artifacts |
| **Task History** | JSON/DB | Completed tasks |

### 3.3 Memory Pattern

```python
# AutoGPT memory interface
class Memory:
    def add(self, text: str, metadata: dict):
        """Add to vector store."""
        self.vector_store.add([text], [metadata])

    def get_relevant(self, query: str, k: int = 5):
        """Semantic retrieval."""
        return self.vector_store.similarity_search(query, k=k)

    def clear(self):
        """Reset memory."""
        self.vector_store.delete_all()
```

### 3.4 Key Insights

- **Vector-first**: Semantic search primary
- **Workspace = procedural memory**: File artifacts
- **Simple abstraction**: add/get_relevant/clear

---

## 4. CrewAI

### 4.1 Architecture

```
CrewAI
├── Agents (individual roles)
├── Tasks (assigned work)
├── Crew (agent orchestration)
└── Memory
    ├── Short-term (per-task)
    ├── Long-term (persistent)
    └── Entity (extracted facts)
```

### 4.2 Memory Configuration

```python
from crewai import Crew, Agent, Task

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    memory=True,  # Enable memory
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)

# Memory persists across crew runs
result = crew.kickoff()
```

### 4.3 Memory Types

| Type | Scope | Description |
|------|-------|-------------|
| **Short-term** | Task | Context within current execution |
| **Long-term** | Crew | Persists across kickoffs |
| **Entity** | Crew | Extracted entities (people, orgs) |
| **Shared** | All agents | Cross-agent knowledge |

### 4.4 Key Insights

- **Multi-agent aware**: Memory shared between agents
- **Entity extraction built-in**: People, orgs, concepts
- **Simple toggle**: `memory=True`

---

## 5. Microsoft AutoGen

### 5.1 Architecture

```
AutoGen
├── Agents
│   ├── AssistantAgent
│   ├── UserProxyAgent
│   └── Custom Agents
├── GroupChat (multi-agent)
└── Memory (via teachability)
```

### 5.2 Memory Patterns

**Conversation History:**
```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent("assistant", llm_config=config)
user = UserProxyAgent("user")

# Conversation history automatic
user.initiate_chat(assistant, message="Hello")
# History maintained in agent.chat_messages
```

**Teachability (Learning from Feedback):**
```python
from autogen.agentchat.contrib.capabilities.teachability import Teachability

teachability = Teachability(
    verbosity=0,
    reset_db=False,
    path_to_db_dir="./teachability_db"
)
teachability.add_to_agent(assistant)

# Agent now learns from corrections
user.initiate_chat(assistant, message="Remember: always use async")
# Stored in vector DB for future retrieval
```

### 5.3 Key Insights

- **Chat-centric**: Memory = message history
- **Teachability**: Learning from user feedback
- **Multi-agent**: Memory can be shared in GroupChat

---

## 6. Semantic Kernel (Microsoft)

### 6.1 Architecture

```
Semantic Kernel
├── Kernel (orchestrator)
├── Plugins (skills/tools)
├── Memory
│   ├── Volatile Memory
│   ├── Semantic Memory
│   └── Text Memory
└── Connectors
    ├── AI Services
    └── Memory Stores
```

### 6.2 Memory Interface

```python
import semantic_kernel as sk
from semantic_kernel.memory import SemanticTextMemory
from semantic_kernel.connectors.memory import ChromaMemoryStore

# Configure memory store
memory_store = ChromaMemoryStore(persist_directory="./memory")
memory = SemanticTextMemory(memory_store, embeddings_generator)

# Save memory
await memory.save_information(
    collection="user_facts",
    id="fact1",
    text="User prefers Python",
    description="Programming preference"
)

# Recall memory
results = await memory.search(
    collection="user_facts",
    query="What programming language?",
    limit=5
)
```

### 6.3 Memory Connectors

| Connector | Backend |
|-----------|---------|
| VolatileMemoryStore | In-memory dict |
| ChromaMemoryStore | Chroma DB |
| AzureCognitiveSearchMemoryStore | Azure Search |
| QdrantMemoryStore | Qdrant |
| PostgresMemoryStore | PostgreSQL |
| RedisMemoryStore | Redis |

### 6.4 Key Insights

- **Pluggable backends**: Connector pattern
- **Collection-based**: Organize by topic
- **Rich ecosystem**: Many connectors available

---

## 7. Comparison Matrix

| Framework | Memory Model | Persistence | Multi-agent | Semantic Search | Extensible |
|-----------|-------------|-------------|-------------|-----------------|------------|
| **Claude Code** | File-based | Yes | No | No | Limited |
| **OpenAI Assistants** | Platform-managed | Yes | Per-thread | File Search | No |
| **AutoGPT** | Vector + Workspace | Yes | No | Yes | Limited |
| **CrewAI** | 3-tier | Yes | Yes | Yes | Limited |
| **AutoGen** | Chat + Teachability | Optional | Yes | Via plugin | Yes |
| **Semantic Kernel** | Pluggable stores | Via connector | Via sharing | Yes | Yes |

---

## 8. Common Patterns Identified

### 8.1 Universal Patterns

1. **Conversation Memory**: All frameworks track messages
2. **Semantic Search**: Vector stores common
3. **Session Isolation**: thread_id or equivalent
4. **Persistence Toggle**: Optional persistence

### 8.2 Differentiated Patterns

| Pattern | Used By | Value |
|---------|---------|-------|
| **File-based memory** | Claude Code | Simple, human-readable |
| **Platform-managed** | OpenAI | Zero infrastructure |
| **Multi-agent sharing** | CrewAI, AutoGen | Collaboration |
| **Teachability** | AutoGen | Learning from feedback |
| **Pluggable connectors** | Semantic Kernel | Flexibility |
| **Entity extraction** | CrewAI | Structured facts |

### 8.3 Gaps Across All

1. **No unified interface**: Each framework is different
2. **Limited memory types**: Most have 2-3 types
3. **No lifecycle management**: No GC, consolidation
4. **No memory agents**: Manual management only
5. **Framework lock-in**: Memory tied to framework

---

## 9. Recommendations for memharness

### 9.1 Adopt These Patterns

| Pattern | From | Implementation |
|---------|------|----------------|
| Thread model | OpenAI | `thread_id` for conversation isolation |
| Pluggable connectors | Semantic Kernel | Backend abstraction layer |
| Multi-agent sharing | CrewAI | Namespace-based sharing |
| Teachability | AutoGen | Learning from corrections |
| File memory | Claude Code | Optional markdown export |
| Entity extraction | CrewAI | Built-in entity memory |

### 9.2 Fill These Gaps

| Gap | memharness Solution |
|-----|-------------------|
| No unified interface | Framework-agnostic API |
| Limited memory types | 10+ memory types |
| No lifecycle management | Built-in GC, consolidation |
| No memory agents | Summarizer, consolidator, etc. |
| Framework lock-in | Works with any framework |

### 9.3 Integration Strategy

```python
# memharness should provide adapters for each framework

# LangChain integration
from memharness.integrations.langchain import MemharnessMemory
memory = MemharnessMemory(backend="postgresql")
chain = ConversationChain(llm=llm, memory=memory)

# CrewAI integration
from memharness.integrations.crewai import MemharnessCrew
crew = MemharnessCrew(memory_backend="postgresql", ...)

# Semantic Kernel integration
from memharness.integrations.semantic_kernel import MemharnessConnector
kernel.register_memory_store(MemharnessConnector(...))

# Standalone (any framework)
from memharness import MemoryHarness
memory = MemoryHarness(backend="postgresql")
# Use directly with any agent
```

---

## Sources

- Claude Code documentation and behavior
- OpenAI Assistants API documentation
- AutoGPT repository (github.com/Significant-Gravitas/AutoGPT)
- CrewAI documentation
- Microsoft AutoGen documentation
- Semantic Kernel documentation

---

*Research completed: 2026-03-22*

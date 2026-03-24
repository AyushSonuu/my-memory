# LangChain & LangGraph Memory Systems

> Research Report for memharness project

---

## Executive Summary

LangChain and LangGraph provide the most mature memory abstractions in the Python agent ecosystem. LangGraph's recent memory overhaul (2024-2025) introduces a clean separation between short-term (thread-scoped) and long-term (namespace-scoped) memory, making it an excellent reference architecture for memharness.

---

## 1. LangChain Memory Types

### 1.1 Classic Memory Classes (Legacy)

| Memory Class | Description | Storage |
|-------------|-------------|---------|
| `ConversationBufferMemory` | Stores all messages verbatim | In-memory list |
| `ConversationBufferWindowMemory` | Last K messages only | In-memory list |
| `ConversationSummaryMemory` | LLM-generated summaries | In-memory string |
| `ConversationSummaryBufferMemory` | Hybrid: recent + summary | In-memory |
| `VectorStoreRetrieverMemory` | Semantic search over history | Vector store |
| `EntityMemory` | Extracts entities from conversations | In-memory dict |
| `ConversationKGMemory` | Knowledge graph of entities | NetworkX graph |

### 1.2 Integration Pattern

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)

# Memory auto-updates on each call
chain.run("Hello!")
chain.run("What did I just say?")  # Has context
```

### 1.3 Limitations of LangChain Memory

1. **Tightly coupled** to Chain/Agent classes
2. **No persistence by default** - memory lost on restart
3. **No multi-session support** - single conversation only
4. **No separation** between memory types
5. **Deprecated** in favor of LangGraph memory

---

## 2. LangGraph Memory Architecture

### 2.1 Two-Tier Memory Model

```
LangGraph Memory
├── Short-Term Memory (Thread-Scoped)
│   ├── Checkpointers (state persistence)
│   ├── Message history within session
│   └── Scoped to thread_id
│
└── Long-Term Memory (Namespace-Scoped)
    ├── Cross-session persistence
    ├── Hierarchical namespaces
    └── JSON document storage
```

### 2.2 Short-Term Memory: Checkpointers

Checkpointers persist graph state between invocations:

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.sqlite import SqliteSaver

# In-memory (testing)
checkpointer = MemorySaver()

# SQLite (local persistence)
checkpointer = SqliteSaver.from_conn_string("memory.db")

# PostgreSQL (production)
checkpointer = PostgresSaver.from_conn_string("postgresql://...")

# Use with graph
graph = builder.compile(checkpointer=checkpointer)

# Thread-scoped invocation
config = {"configurable": {"thread_id": "user-123-session-1"}}
graph.invoke({"messages": [...]}, config)
```

**Key Properties:**
- State persisted after each step
- Resume from any checkpoint
- Thread isolation via `thread_id`
- Supports branching (time travel)

### 2.3 Long-Term Memory: Stores

For cross-session memory, LangGraph uses **Stores**:

```python
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore

store = PostgresStore(conn_string="postgresql://...")

# Namespace = hierarchical organization (like folders)
# Key = document identifier (like filename)
namespace = ("users", "user-123", "preferences")
key = "dietary"

# Write
store.put(namespace, key, {"vegetarian": True, "allergies": ["nuts"]})

# Read
item = store.get(namespace, key)

# Search (semantic)
results = store.search(namespace, query="food preferences", limit=5)
```

### 2.4 Memory Types (Cognitive Model)

LangGraph maps to human cognition:

| Memory Type | Description | Implementation |
|-------------|-------------|----------------|
| **Semantic** | Facts about entities | Store with user namespace |
| **Episodic** | Past experiences/actions | Few-shot examples from history |
| **Procedural** | Instructions/rules | System prompt refinement |

### 2.5 Writing Strategies

| Strategy | Latency | Consistency | Use Case |
|----------|---------|-------------|----------|
| **Hot Path** | +High | Immediate | Critical facts |
| **Background** | None | Eventual | Bulk processing |

```python
# Hot path: write during graph execution
def memory_node(state):
    store.put(namespace, key, extracted_facts)
    return state

# Background: async after completion
async def background_memory_worker():
    while True:
        batch = await queue.get()
        await store.put_many(batch)
```

---

## 3. Key Patterns for memharness

### 3.1 What to Adopt

1. **Two-tier model**: Short-term (session) + Long-term (cross-session)
2. **Namespace hierarchy**: `(org, user, thread, memory_type)`
3. **Checkpointer interface**: Pluggable persistence backends
4. **Store interface**: JSON documents with semantic search

### 3.2 What to Improve

1. **More memory types**: LangGraph has 3, we want 10+
2. **Memory lifecycle**: No built-in consolidation/GC
3. **Memory agents**: No built-in summarization agents
4. **Framework agnostic**: LangGraph memory is LangGraph-only

### 3.3 Interface Inspiration

```python
# LangGraph-inspired interface for memharness
class MemoryStore(ABC):
    @abstractmethod
    def get(self, namespace: tuple, key: str) -> Optional[Item]: ...

    @abstractmethod
    def put(self, namespace: tuple, key: str, value: dict) -> None: ...

    @abstractmethod
    def search(self, namespace: tuple, query: str, limit: int) -> List[Item]: ...

    @abstractmethod
    def delete(self, namespace: tuple, key: str) -> None: ...
```

---

## 4. LangChain VectorStore Interface

For vector storage, LangChain defines a standard interface we should support:

```python
class VectorStore(ABC):
    @abstractmethod
    def add_texts(self, texts: List[str], metadatas: List[dict]) -> List[str]: ...

    @abstractmethod
    def similarity_search(self, query: str, k: int) -> List[Document]: ...

    @abstractmethod
    def similarity_search_with_score(self, query: str, k: int) -> List[Tuple[Document, float]]: ...

    @abstractmethod
    def delete(self, ids: List[str]) -> None: ...
```

**Implementations available:**
- Chroma, FAISS, Pinecone, Weaviate, Qdrant
- PostgreSQL (pgvector)
- SQLite (sqlite-vss)
- Redis (Redis Stack)

---

## 5. Recommendations for memharness

| Aspect | Recommendation |
|--------|----------------|
| **Memory Model** | Adopt LangGraph's 2-tier (short-term + long-term) |
| **Namespacing** | Use hierarchical namespaces for isolation |
| **Checkpointer** | Create similar interface for state persistence |
| **VectorStore** | Support LangChain VectorStore interface for compatibility |
| **Extensions** | Add memory types, lifecycle management, built-in agents |

---

## Sources

- LangGraph Memory Documentation (researched via WebFetch)
- LangChain Memory Concepts
- Personal knowledge of LangChain ecosystem

---

*Research completed: 2026-03-22*

# memharness — High-Level Design (HLD)

> Technical specification for the Agent Memory Harness package

---

## 1. Overview

### 1.1 Purpose

`memharness` is a **framework-agnostic Python package** that provides memory infrastructure for AI agents. It enables any agent framework (LangChain, LangGraph, CrewAI, Claude Code, custom) to have persistent, searchable, typed memory with built-in lifecycle management.

### 1.2 Design Principles

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | Memory infrastructure separate from agent logic |
| **Pluggable Backends** | Same API, multiple storage implementations |
| **Framework Agnostic** | Works with any agent framework |
| **Type Safety** | Structured memory types with schemas |
| **Lifecycle Aware** | Automated consolidation, summarization, GC |
| **Observable** | Logging, metrics, debugging support |

### 1.3 Key Patterns Adopted

| Pattern | Source | Application |
|---------|--------|-------------|
| 2-tier memory | LangGraph | Short-term + Long-term |
| Namespace hierarchy | LangGraph | `(org, user, thread)` isolation |
| Simple API | Mem0 | `add/search/update/delete` |
| Agent-controlled memory | MemGPT | Memory ops as tools |
| Pluggable backends | DeepAgents | Backend protocol + router |
| Composite routing | DeepAgents | Route by memory type |
| **VFS Tool Discovery** | **Tool Lens (SAP)** | **Progressive tool loading via virtual filesystem** |

---

## 2. Architecture

### 2.1 High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER APPLICATION                                │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  LangChain   │  │  LangGraph   │  │   CrewAI     │  │  Custom Agent    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    │                                      │
                    ▼                                      ▼
         ┌─────────────────────┐              ┌─────────────────────┐
         │ Framework Adapters  │              │    Direct API       │
         │ langchain, langgraph│              │    (any agent)      │
         └─────────────────────┘              └─────────────────────┘
                    │                                      │
                    └──────────────────┬───────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              memharness                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                            PUBLIC API                                   │ │
│  │                                                                         │ │
│  │  class MemoryHarness:                                                   │ │
│  │      # Simple API (App Developers)                                      │ │
│  │      add(content, memory_type, namespace, metadata) -> str             │ │
│  │      search(query, memory_type, namespace, k, filters) -> List[Memory] │ │
│  │      get(memory_id) -> Memory                                           │ │
│  │      update(memory_id, content, metadata) -> bool                       │ │
│  │      delete(memory_id) -> bool                                          │ │
│  │                                                                         │ │
│  │      # Advanced API (Framework Authors)                                 │ │
│  │      transaction() -> TransactionContext                                │ │
│  │      configure_lifecycle(policies) -> None                              │ │
│  │      register_memory_type(name, schema) -> None                         │ │
│  │      get_tools() -> List[Tool]                                          │ │
│  │                                                                         │ │
│  │      # Memory-Type-Specific Methods                                     │ │
│  │      read_conversational(thread_id, limit) -> str                       │ │
│  │      write_conversational(thread_id, role, content) -> str              │ │
│  │      search_knowledge_base(query, k, filters) -> str                    │ │
│  │      # ... (one pair per memory type)                                   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         MEMORY MANAGER                                  │ │
│  │                                                                         │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Memory Type Registry                                             │  │ │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐  │  │ │
│  │  │  │Conversational│ │KnowledgeBase│ │   Entity    │ │  Workflow  │  │  │ │
│  │  │  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘  │  │ │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐  │  │ │
│  │  │  │   Toolbox   │ │   Summary   │ │  Tool Log   │ │   Skills   │  │  │ │
│  │  │  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘  │  │ │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────────┐ │  │ │
│  │  │  │    File     │ │   Persona   │ │  Custom (User-Defined)      │ │  │ │
│  │  │  └─────────────┘ └─────────────┘ └─────────────────────────────┘ │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Lifecycle Engine                                                 │  │ │
│  │  │  • Policy Executor   • Scheduler   • Event Hooks                 │  │ │
│  │  │  • consolidate() • summarize() • expire() • gc()                 │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      BACKEND ROUTER (Composite)                        │ │
│  │                                                                         │ │
│  │  Routes memory operations to appropriate backend based on:             │ │
│  │  • Memory type (conversational → SQL, knowledge_base → Vector)        │ │
│  │  • Storage tier (hot → cache, warm → primary, cold → archive)         │ │
│  │  • Custom routing rules                                                 │ │
│  │                                                                         │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │ │
│  │  │  SQL Backend   │  │ Vector Backend │  │ Cache Backend  │           │ │
│  │  │  Protocol      │  │  Protocol      │  │  Protocol      │           │ │
│  │  └────────────────┘  └────────────────┘  └────────────────┘           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                      │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      STORAGE IMPLEMENTATIONS                           │ │
│  │                                                                         │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │ │
│  │  │  PostgreSQL    │  │    SQLite      │  │     Redis      │           │ │
│  │  │  + pgvector    │  │  + sqlite-vss  │  │  (cache layer) │           │ │
│  │  └────────────────┘  └────────────────┘  └────────────────┘           │ │
│  │  ┌────────────────┐  ┌────────────────┐                               │ │
│  │  │   In-Memory    │  │    Custom      │                               │ │
│  │  │   (testing)    │  │  (user impl)   │                               │ │
│  │  └────────────────┘  └────────────────┘                               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                       MEMORY AGENTS                                     │ │
│  │  (Built-in, run in isolated context, user provides LLM)               │ │
│  │                                                                         │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │ │
│  │  │  Summarizer  │ │ Consolidator │ │   GC Agent   │ │   Entity     │  │ │
│  │  │  Agent       │ │    Agent     │ │              │ │   Extractor  │  │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Interfaces

### 3.1 Memory Unit (Base Data Model)

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
import uuid

@dataclass
class MemoryUnit:
    """The atomic unit of stored information."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    namespace: tuple[str, ...] = ()  # e.g., ("org:acme", "user:alice", "thread:123")
    memory_type: str = ""  # e.g., "conversational", "knowledge_base"
    content: str = ""
    embedding: Optional[list[float]] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    score: Optional[float] = None  # Relevance score from search

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "namespace": self.namespace,
            "memory_type": self.memory_type,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
```

### 3.2 Backend Protocol

```python
from abc import ABC, abstractmethod
from typing import Optional, Protocol, runtime_checkable

@runtime_checkable
class BackendProtocol(Protocol):
    """Protocol for storage backends (inspired by DeepAgents)."""

    async def write(
        self,
        namespace: tuple[str, ...],
        key: str,
        value: dict,
        embedding: Optional[list[float]] = None,
    ) -> str:
        """Write a memory unit. Returns the ID."""
        ...

    async def read(
        self,
        namespace: tuple[str, ...],
        key: str,
    ) -> Optional[dict]:
        """Read a specific memory unit by key."""
        ...

    async def search(
        self,
        namespace: tuple[str, ...],
        query: str,
        embedding: Optional[list[float]] = None,
        k: int = 10,
        filters: Optional[dict] = None,
    ) -> list[dict]:
        """Semantic search within namespace."""
        ...

    async def list(
        self,
        namespace: tuple[str, ...],
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[dict]:
        """List all memories in namespace."""
        ...

    async def delete(
        self,
        namespace: tuple[str, ...],
        key: str,
    ) -> bool:
        """Delete a memory unit."""
        ...

    async def update(
        self,
        namespace: tuple[str, ...],
        key: str,
        value: dict,
        embedding: Optional[list[float]] = None,
    ) -> bool:
        """Update a memory unit."""
        ...
```

### 3.3 SQL Backend Protocol (Extension)

```python
class SQLBackendProtocol(BackendProtocol, Protocol):
    """Extended protocol for SQL-based backends."""

    async def execute(self, query: str, params: tuple = ()) -> list[dict]:
        """Execute raw SQL query."""
        ...

    async def list_ordered(
        self,
        namespace: tuple[str, ...],
        order_by: str = "created_at",
        order: str = "DESC",
        limit: int = 100,
    ) -> list[dict]:
        """List with ordering (for conversational memory)."""
        ...
```

### 3.4 Vector Backend Protocol (Extension)

```python
class VectorBackendProtocol(BackendProtocol, Protocol):
    """Extended protocol for vector-based backends."""

    async def similarity_search(
        self,
        namespace: tuple[str, ...],
        embedding: list[float],
        k: int = 10,
        threshold: Optional[float] = None,
    ) -> list[dict]:
        """Pure vector similarity search."""
        ...

    async def hybrid_search(
        self,
        namespace: tuple[str, ...],
        query: str,
        embedding: list[float],
        k: int = 10,
        filters: Optional[dict] = None,
        alpha: float = 0.5,  # Balance between keyword and semantic
    ) -> list[dict]:
        """Hybrid keyword + semantic search."""
        ...
```

### 3.5 Composite Backend (Router)

```python
from typing import Callable

class CompositeBackend:
    """Routes operations to different backends based on memory type or rules."""

    def __init__(
        self,
        default: BackendProtocol,
        routes: Optional[dict[str, BackendProtocol]] = None,
        router: Optional[Callable[[str, tuple], BackendProtocol]] = None,
    ):
        self.default = default
        self.routes = routes or {}
        self.router = router

    def _get_backend(self, memory_type: str, namespace: tuple) -> BackendProtocol:
        """Determine which backend to use."""
        if self.router:
            return self.router(memory_type, namespace)
        return self.routes.get(memory_type, self.default)

    async def write(self, namespace, key, value, embedding=None):
        memory_type = value.get("memory_type", "")
        backend = self._get_backend(memory_type, namespace)
        return await backend.write(namespace, key, value, embedding)

    # ... implement other methods similarly
```

---

## 4. Memory Types

### 4.1 Memory Type Registry

```python
from dataclasses import dataclass
from typing import Type, Callable, Optional

@dataclass
class MemoryTypeConfig:
    """Configuration for a memory type."""

    name: str
    storage: str  # "sql" | "vector" | "hybrid"
    schema: dict  # JSON Schema for validation
    index_type: Optional[str] = None  # "hnsw" | "ivfflat" | None
    default_k: int = 10
    supports_embedding: bool = True
    ordered: bool = False  # Time-ordered (conversational, tool_log)
    formatter: Optional[Callable[[dict], str]] = None  # Format for context

class MemoryTypeRegistry:
    """Registry of all memory types."""

    def __init__(self):
        self._types: dict[str, MemoryTypeConfig] = {}
        self._register_builtin_types()

    def _register_builtin_types(self):
        """Register the 10 built-in memory types."""
        self.register(MemoryTypeConfig(
            name="conversational",
            storage="sql",
            schema={
                "thread_id": "str",
                "role": "str",  # user | assistant | system
                "content": "str",
                "timestamp": "datetime",
                "summary_id": "str?",  # Link to summary if summarized
            },
            ordered=True,
            supports_embedding=False,
        ))

        self.register(MemoryTypeConfig(
            name="knowledge_base",
            storage="vector",
            schema={
                "content": "str",
                "source": "str?",
                "chunk_id": "str?",
            },
            index_type="hnsw",
        ))

        self.register(MemoryTypeConfig(
            name="entity",
            storage="vector",
            schema={
                "name": "str",
                "entity_type": "str",  # PERSON | ORG | PLACE | CONCEPT | SYSTEM
                "description": "str",
                "relationships": "list?",
            },
            index_type="hnsw",
        ))

        self.register(MemoryTypeConfig(
            name="workflow",
            storage="vector",
            schema={
                "task": "str",
                "steps": "list[str]",
                "outcome": "str",  # success | failed
                "result": "str?",
            },
            index_type="hnsw",
        ))

        self.register(MemoryTypeConfig(
            name="toolbox",
            storage="vector",
            schema={
                "server": "str",       # MCP server name (e.g., "github", "slack")
                "tool_name": "str",
                "description": "str",
                "parameters": "dict",
                "signature": "str?",
                "path": "str",         # VFS path: "/slack/send-message.json"
            },
            index_type="hnsw",
        ))

        self.register(MemoryTypeConfig(
            name="summary",
            storage="vector",
            schema={
                "summary": "str",
                "source_ids": "list[str]",  # IDs of summarized memories
                "thread_id": "str?",
                "expandable": "bool",       # Can expand to originals
                "source_type": "str",       # Type of source memories
            },
            index_type="hnsw",
        ))

        self.register(MemoryTypeConfig(
            name="tool_log",
            storage="sql",
            schema={
                "thread_id": "str",
                "tool_call_id": "str",
                "tool_name": "str",
                "tool_args": "dict",
                "result": "str",
                "status": "str",  # success | failed
                "error_message": "str?",
                "timestamp": "datetime",
            },
            ordered=True,
            supports_embedding=False,
        ))

        self.register(MemoryTypeConfig(
            name="skills",
            storage="vector",
            schema={
                "skill_name": "str",
                "description": "str",
                "examples": "list[str]?",
                "learned_from": "str?",
            },
            index_type="hnsw",
        ))

        self.register(MemoryTypeConfig(
            name="file",
            storage="hybrid",  # SQL metadata + vector content
            schema={
                "path": "str",
                "filename": "str",
                "content_summary": "str?",
                "mime_type": "str?",
                "size_bytes": "int?",
            },
            index_type="hnsw",
        ))

        self.register(MemoryTypeConfig(
            name="persona",
            storage="vector",
            schema={
                "block_name": "str",  # e.g., "identity", "preferences", "rules"
                "content": "str",
            },
            index_type="hnsw",
        ))

    def register(self, config: MemoryTypeConfig):
        """Register a memory type."""
        self._types[config.name] = config

    def get(self, name: str) -> MemoryTypeConfig:
        """Get memory type configuration."""
        if name not in self._types:
            raise ValueError(f"Unknown memory type: {name}")
        return self._types[name]

    def list_types(self) -> list[str]:
        """List all registered memory types."""
        return list(self._types.keys())
```

### 4.2 Storage Mapping

| Memory Type | Storage | Index | Access Pattern |
|-------------|---------|-------|----------------|
| conversational | SQL | B-tree (thread_id, timestamp) | Exact + ordered |
| knowledge_base | Vector | HNSW | Semantic search |
| entity | Vector | HNSW | Semantic + exact lookup |
| workflow | Vector | HNSW | Semantic search |
| toolbox | Vector | HNSW | Semantic search |
| summary | Vector | HNSW | Semantic + thread filter |
| tool_log | SQL | B-tree (thread_id, timestamp) | Exact + ordered |
| skills | Vector | HNSW | Semantic search |
| file | Hybrid | B-tree + HNSW | Path lookup + content search |
| persona | Vector | HNSW | Block lookup + semantic |

---

## 5. Main API (MemoryHarness)

### 5.1 Initialization

```python
from typing import Optional, Union, Callable
from memharness.backends import PostgresBackend, SqliteBackend, RedisBackend, InMemoryBackend
from memharness.embeddings import EmbeddingFunction

class MemoryHarness:
    """Main entry point for memharness."""

    def __init__(
        self,
        backend: Union[str, BackendProtocol] = "memory://",
        embedding_fn: Optional[EmbeddingFunction] = None,
        cache: Optional[str] = None,  # Redis URL for caching
        auto_embed: bool = True,
        namespace_prefix: Optional[tuple[str, ...]] = None,
    ):
        """
        Initialize MemoryHarness.

        Args:
            backend: Connection string or BackendProtocol instance
                - "postgresql://user:pass@host/db" → PostgresBackend
                - "sqlite:///path/to/db.sqlite" → SqliteBackend
                - "memory://" → InMemoryBackend
                - BackendProtocol instance → use directly
            embedding_fn: Function to generate embeddings (default: sentence-transformers)
            cache: Redis URL for caching layer (optional)
            auto_embed: Automatically embed content on write
            namespace_prefix: Default namespace prefix for all operations
        """
        self._backend = self._init_backend(backend)
        self._embedding_fn = embedding_fn or self._default_embedding_fn()
        self._cache = self._init_cache(cache) if cache else None
        self._auto_embed = auto_embed
        self._namespace_prefix = namespace_prefix or ()
        self._registry = MemoryTypeRegistry()
        self._lifecycle = LifecycleEngine(self)

    # ... implementation
```

### 5.2 Simple API

```python
class MemoryHarness:
    # ... (continued)

    async def add(
        self,
        content: str,
        memory_type: str,
        namespace: Optional[tuple[str, ...]] = None,
        metadata: Optional[dict] = None,
        key: Optional[str] = None,
    ) -> str:
        """
        Add a memory unit.

        Returns:
            str: The ID of the created memory

        Example:
            >>> memory_id = await memory.add(
            ...     content="User prefers Python",
            ...     memory_type="entity",
            ...     namespace=("user", "alice"),
            ...     metadata={"entity_type": "PREFERENCE"}
            ... )
        """
        ...

    async def search(
        self,
        query: str,
        memory_type: Optional[str] = None,
        namespace: Optional[tuple[str, ...]] = None,
        k: int = 10,
        filters: Optional[dict] = None,
    ) -> list[MemoryUnit]:
        """
        Search for relevant memories.

        Example:
            >>> results = await memory.search(
            ...     query="programming preferences",
            ...     memory_type="entity",
            ...     namespace=("user", "alice"),
            ...     k=5
            ... )
        """
        ...

    async def get(self, memory_id: str) -> Optional[MemoryUnit]:
        """Get a specific memory by ID."""
        ...

    async def update(
        self,
        memory_id: str,
        content: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> bool:
        """Update a memory unit."""
        ...

    async def delete(self, memory_id: str) -> bool:
        """Delete a memory unit."""
        ...
```

### 5.3 Memory-Type-Specific Methods

```python
class MemoryHarness:
    # ... (continued)

    # ===== CONVERSATIONAL MEMORY =====

    async def write_conversational(
        self,
        thread_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> str:
        """Write a conversation message."""
        ...

    async def read_conversational(
        self,
        thread_id: str,
        limit: int = 50,
        before: Optional[datetime] = None,
    ) -> str:
        """
        Read conversation history.

        Returns formatted string for LLM context:
        ## Conversation Memory
        [2026-03-22 10:00] user: Hello
        [2026-03-22 10:01] assistant: Hi there!
        """
        ...

    # ===== KNOWLEDGE BASE =====

    async def write_knowledge_base(
        self,
        content: str,
        source: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """Add to knowledge base."""
        ...

    async def search_knowledge_base(
        self,
        query: str,
        k: int = 5,
        filters: Optional[dict] = None,
    ) -> str:
        """
        Search knowledge base.

        Returns formatted string:
        ## Knowledge Base Memory
        Use these passages to ground your response:

        [1] (source: arxiv) Content here...
        [2] (source: docs) Content here...
        """
        ...

    # ===== ENTITY MEMORY =====

    async def write_entity(
        self,
        name: str,
        entity_type: str,
        description: str,
        relationships: Optional[list[dict]] = None,
    ) -> str:
        """Write an entity."""
        ...

    async def search_entity(
        self,
        query: str,
        entity_type: Optional[str] = None,
        k: int = 5,
    ) -> str:
        """Search entities."""
        ...

    # ===== WORKFLOW MEMORY =====

    async def write_workflow(
        self,
        task: str,
        steps: list[str],
        outcome: str,
        result: Optional[str] = None,
    ) -> str:
        """Record a workflow."""
        ...

    async def search_workflow(self, query: str, k: int = 3) -> str:
        """Find similar workflows."""
        ...

    # ===== TOOLBOX (VFS-based Discovery) =====

    async def register_tool_server(
        self,
        server_name: str,
        tools: list[dict],
    ) -> int:
        """Register an MCP server's tools into the toolbox."""
        ...

    async def write_toolbox(
        self,
        server: str,
        tool_name: str,
        description: str,
        parameters: dict,
        signature: Optional[str] = None,
    ) -> str:
        """Register a single tool."""
        ...

    # VFS Discovery Operations (Tool Lens pattern)

    async def toolbox_tree(self, path: str = "/") -> str:
        """
        Visualize tool hierarchy.

        Returns:
            /
            ├── github/ (12 tools)
            ├── slack/ (8 tools)
            └── sap/ (45 tools)
        """
        ...

    async def toolbox_ls(self, server: str) -> list[str]:
        """List tools in a server directory."""
        ...

    async def toolbox_grep(self, pattern: str, server: Optional[str] = None) -> list[dict]:
        """Search tools by pattern (semantic + keyword)."""
        ...

    async def toolbox_cat(self, tool_path: str) -> dict:
        """Get full tool schema by VFS path."""
        ...

    async def toolbox_glob(self, pattern: str) -> list[str]:
        """Pattern matching for tools (e.g., '*/send*')."""
        ...

    async def toolbox_select(self, tool_paths: list[str]) -> list[dict]:
        """Load selected tools into context (returns full schemas)."""
        ...

    def get_toolbox_discovery_tools(self) -> list["Tool"]:
        """
        Get VFS discovery tools for agent use.

        Returns tools: [tree, ls, grep, cat, glob, select]
        Agent can explore toolbox progressively (96% token savings).
        """
        ...

    # ===== SUMMARY (with Expansion) =====

    async def write_summary(
        self,
        summary: str,
        source_ids: list[str],
        thread_id: Optional[str] = None,
        keep_originals: bool = True,  # Archive originals, don't delete
    ) -> str:
        """
        Write a summary and optionally archive originals.

        Args:
            summary: The compressed summary text
            source_ids: IDs of memories being summarized
            thread_id: Thread ID if summarizing a conversation
            keep_originals: If True, archive originals (default). If False, delete.

        Returns:
            str: Summary ID
        """
        ...

    async def expand_summary(self, summary_id: str) -> list[MemoryUnit]:
        """
        Expand a summary to retrieve original memories (DETERMINISTIC).

        This is a deterministic operation — simply fetches by source_ids.

        Args:
            summary_id: The summary to expand

        Returns:
            list[MemoryUnit]: Original memories that were summarized

        Example:
            >>> summary = await memory.get_summary(thread_id="abc")
            >>> # summary.content = "User discussed AWS deployment with John..."
            >>>
            >>> originals = await memory.expand_summary(summary.id)
            >>> # Returns full original conversation messages
            >>> for msg in originals:
            ...     print(f"[{msg.metadata['role']}] {msg.content}")
        """
        ...

    async def get_context_with_expansion(
        self,
        thread_id: str,
        expand_if_needed: bool = True,
        detail_threshold: float = 0.8,  # Expand if query relevance > threshold
    ) -> str:
        """
        Get context, expanding summaries when more detail is needed.

        Args:
            thread_id: The conversation thread
            expand_if_needed: Auto-expand summaries when relevant
            detail_threshold: Relevance score above which to expand

        Returns:
            str: Formatted context (summaries or expanded originals)
        """
        ...

    # ===== TOOL LOG =====

    async def write_tool_log(
        self,
        thread_id: str,
        tool_call_id: str,
        tool_name: str,
        tool_args: dict,
        result: str,
        status: str,
        error_message: Optional[str] = None,
    ) -> str:
        """Log a tool execution."""
        ...

    async def read_tool_log(
        self,
        thread_id: str,
        limit: int = 20,
    ) -> str:
        """Read tool execution history."""
        ...

    # ===== SKILLS =====

    async def write_skill(
        self,
        skill_name: str,
        description: str,
        examples: Optional[list[str]] = None,
    ) -> str:
        """Register a learned skill."""
        ...

    async def search_skills(self, query: str, k: int = 3) -> str:
        """Find relevant skills."""
        ...

    # ===== FILE MEMORY =====

    async def write_file_reference(
        self,
        path: str,
        content_summary: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """Record a file reference."""
        ...

    async def search_files(self, query: str, k: int = 5) -> str:
        """Search file references."""
        ...

    # ===== PERSONA =====

    async def write_persona(
        self,
        block_name: str,
        content: str,
    ) -> str:
        """Write a persona block."""
        ...

    async def read_persona(self, block_name: Optional[str] = None) -> str:
        """Read persona (all blocks or specific)."""
        ...

    async def edit_persona(
        self,
        block_name: str,
        old_content: str,
        new_content: str,
    ) -> bool:
        """Edit a persona block (MemGPT-style)."""
        ...
```

### 5.4 Advanced API

```python
class MemoryHarness:
    # ... (continued)

    @asynccontextmanager
    async def transaction(self):
        """
        Transaction context for atomic operations.

        Example:
            async with memory.transaction() as txn:
                txn.write_conversational(...)
                txn.write_entity(...)
                # All succeed or all fail
        """
        ...

    def configure_lifecycle(self, policies: list["LifecyclePolicy"]):
        """Configure lifecycle policies."""
        self._lifecycle.configure(policies)

    def register_memory_type(
        self,
        name: str,
        schema: dict,
        storage: str = "vector",
        **kwargs,
    ):
        """Register a custom memory type."""
        config = MemoryTypeConfig(
            name=name,
            storage=storage,
            schema=schema,
            **kwargs,
        )
        self._registry.register(config)

    def get_tools(
        self,
        include: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
    ) -> list["Tool"]:
        """
        Get memory operations as tools for agent use.

        Example:
            tools = memory.get_tools(include=[
                "archival_memory_insert",
                "archival_memory_search",
                "core_memory_edit",
            ])
            agent = YourAgent(tools=tools)
        """
        ...

    async def assemble_context(
        self,
        query: str,
        thread_id: str,
        max_tokens: int = 4000,
        include_types: Optional[list[str]] = None,
    ) -> str:
        """
        Assemble optimal context from memory.

        Returns formatted context window:
        ## Conversation Memory
        ...

        ## Knowledge Base Memory
        ...

        ## Entity Memory
        ...
        """
        ...
```

---

## 6. Lifecycle Engine

### 6.1 Policy Definition

```python
from dataclasses import dataclass
from typing import Callable, Optional
from datetime import timedelta

@dataclass
class LifecyclePolicy:
    """Policy for automated memory lifecycle management."""

    name: str
    memory_type: str  # "*" for all types
    condition: Callable[[MemoryUnit], bool]
    action: str  # "summarize" | "archive" | "delete" | "consolidate"
    schedule: Optional[str] = None  # Cron expression
    enabled: bool = True

# Example policies
DEFAULT_POLICIES = [
    LifecyclePolicy(
        name="summarize_old_conversations",
        memory_type="conversational",
        condition=lambda m: (datetime.utcnow() - m.created_at) > timedelta(days=7),
        action="summarize",
        schedule="0 3 * * *",  # Daily at 3 AM
    ),
    LifecyclePolicy(
        name="cleanup_expired",
        memory_type="*",
        condition=lambda m: m.expires_at and m.expires_at < datetime.utcnow(),
        action="delete",
        schedule="0 * * * *",  # Hourly
    ),
    LifecyclePolicy(
        name="consolidate_entities",
        memory_type="entity",
        condition=lambda m: True,  # Consolidation checks similarity
        action="consolidate",
        schedule="0 4 * * 0",  # Weekly on Sunday
    ),
]
```

### 6.2 Lifecycle Engine

```python
class LifecycleEngine:
    """Manages memory lifecycle operations."""

    def __init__(self, harness: "MemoryHarness"):
        self._harness = harness
        self._policies: list[LifecyclePolicy] = []
        self._scheduler = None

    def configure(self, policies: list[LifecyclePolicy]):
        """Configure lifecycle policies."""
        self._policies = policies

    async def run_policy(self, policy: LifecyclePolicy):
        """Execute a single policy."""
        if not policy.enabled:
            return

        # Get memories matching condition
        memories = await self._harness._backend.list(
            namespace=(),  # All namespaces
            filters={"memory_type": policy.memory_type} if policy.memory_type != "*" else None,
        )

        for memory in memories:
            unit = MemoryUnit(**memory)
            if policy.condition(unit):
                await self._execute_action(unit, policy.action)

    async def _execute_action(self, memory: MemoryUnit, action: str):
        """Execute lifecycle action on memory."""
        if action == "summarize":
            await self._summarize(memory)
        elif action == "archive":
            await self._archive(memory)
        elif action == "delete":
            await self._harness.delete(memory.id)
        elif action == "consolidate":
            await self._consolidate(memory)

    async def _summarize(self, memory: MemoryUnit):
        """Summarize and compress memory."""
        # Uses memory agent (requires LLM)
        ...

    async def _consolidate(self, memory: MemoryUnit):
        """Find and merge similar memories."""
        # Find similar memories
        similar = await self._harness.search(
            query=memory.content,
            memory_type=memory.memory_type,
            k=5,
        )
        # Merge if similarity > threshold
        ...
```

---

## 7. Deterministic-First Design + Embedded AI Agents

> **Core Principle**: Simple operations are deterministic (no AI). AI agents handle only complex tasks that require intelligence.

### 7.1 Deterministic vs AI-Assisted Operations

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     DETERMINISTIC (No AI needed)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EXPLICIT WRITES — User specifies type, goes directly to store:        │
│                                                                         │
│    memory.add_conversational(msg)  →  Conversational Store (direct)    │
│    memory.add_entity(entity)       →  Entity Store (direct)            │
│    memory.add_knowledge(doc)       →  Knowledge Base (direct)          │
│    memory.add_workflow(wf)         →  Workflow Store (direct)          │
│                                                                         │
│  READS — Direct retrieval, no AI:                                       │
│                                                                         │
│    memory.get_conversational(thread_id, limit=50)                      │
│    memory.search_knowledge(query, k=5)                                  │
│    memory.get_entity(name)                                              │
│    memory.expand_summary(summary_id)  →  Returns original messages     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     AI-ASSISTED (Agents required)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  IMPLICIT WRITES — Type unknown, Router Agent decides:                  │
│                                                                         │
│    memory.add(content)  →  Router Agent → Correct Store                │
│                             (only if type not specified)               │
│                                                                         │
│  COMPLEX OPERATIONS — Require LLM intelligence:                        │
│                                                                         │
│    Entity Extraction     →  Extract people/orgs from text              │
│    Summarization         →  Compress conversations intelligently        │
│    Consolidation         →  Merge similar memories semantically         │
│    Context Assembly      →  Build optimal context for LLM               │
│    Tool Discovery        →  Progressive VFS exploration                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Operation Classification

| Operation | Deterministic | AI Agent | Notes |
|-----------|:-------------:|:--------:|-------|
| `add_conversational()` | ✅ | - | Direct to SQL store |
| `add_entity()` | ✅ | - | Direct to vector store |
| `add_knowledge()` | ✅ | - | Direct to vector store |
| `add_workflow()` | ✅ | - | Direct to vector store |
| `add_toolbox()` | ✅ | - | Direct to vector store |
| `get_*()` / `search_*()` | ✅ | - | Direct retrieval |
| `expand_summary()` | ✅ | - | Fetch by source_ids |
| `add()` (no type) | - | ✅ Router | Only when type unknown |
| Entity extraction | - | ✅ Extractor | Needs LLM understanding |
| Summarization | - | ✅ Summarizer | Needs LLM compression |
| Consolidation | - | ✅ Consolidator | Needs semantic merging |
| Context assembly | - | ✅ Assembler | Needs relevance scoring |
| Tool discovery | - | ✅ Discovery | Needs ReAct exploration |
| Index optimization | ✅ | - | Database operations |
| GC (basic) | ✅ | - | TTL-based deletion |

### 7.3 The 7 Specialized Agents (Only for Complex Tasks)

| Agent | Purpose | Trigger | When Used |
|-------|---------|---------|-----------|
| **🗂️ Router** | Route memories to correct type/storage | On `add()` without type | Only if type not specified |
| **🏷️ Entity Extractor** | Extract structured entities | Configurable | On write OR batch |
| **📋 Context Assembler** | Build optimal context windows | Before LLM call | When assembling context |
| **📝 Summarizer** | Compress old memories | Policy + threshold | When compression needed |
| **🔄 Consolidator** | Merge duplicates | Scheduled | Periodic cleanup |
| **🗑️ GC** | Remove stale memories | Scheduled | Periodic cleanup |
| **🔍 Tool Discovery** | VFS-based progressive tool finding | On demand | When discovering tools |

> **Note**: Index Optimizer removed from agents — it's a deterministic database operation.

### 7.2 Base Agent Interface

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional

class TriggerType(Enum):
    ON_WRITE = "on_write"          # Runs on every write
    ON_READ = "on_read"            # Runs on every read
    PRE_LLM = "pre_llm"            # Before LLM invocation
    POST_LLM = "post_llm"          # After LLM response
    SCHEDULED = "scheduled"         # Cron-based
    POLICY = "policy"               # Policy-triggered
    ON_DEMAND = "on_demand"         # Manual/agent-triggered

class EmbeddedAgent(ABC):
    """Base class for embedded memory management agents."""

    trigger: TriggerType
    schedule: Optional[str] = None  # Cron expression for SCHEDULED
    applies_to: list[str] = ["*"]   # Memory types this agent handles

    def __init__(
        self,
        memory: "MemoryHarness",
        llm: "LLMProvider",
    ):
        self.memory = memory
        self.llm = llm
        self.status = "idle"
        self.last_run = None
        self.runs_today = 0
        self.errors_today = 0

    @abstractmethod
    async def run(self, **kwargs) -> dict:
        """Execute the agent's task."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent name."""
        ...

    def log(self, message: str):
        """Log agent activity."""
        logger.info(f"[{self.name}] {message}")
```

### 7.3 Memory Router Agent

```python
class MemoryRouterAgent(EmbeddedAgent):
    """Routes memories to correct stores based on content analysis."""

    name = "router"
    trigger = TriggerType.ON_WRITE

    async def process(self, content: str, metadata: dict) -> RoutingDecision:
        """Analyze content and determine routing."""
        analysis = await self.llm.analyze(f"""
        Classify this content and determine memory routing:

        Content: {content}
        Metadata: {metadata}

        Memory Types: conversational, knowledge_base, entity, workflow,
                     toolbox, summary, tool_log, skills, file, persona

        Return JSON: {{
            "memory_type": "...",
            "storage_tier": "hot|warm|cold",
            "namespace_suggestion": [...],
            "confidence": 0.0-1.0
        }}
        """)
        return RoutingDecision(**analysis)
```

### 7.4 Entity Extraction Agent

```python
class EntityExtractionAgent(EmbeddedAgent):
    """Extracts structured entities from content."""

    name = "entity_extractor"
    trigger = TriggerType.ON_WRITE
    applies_to = ["conversational", "knowledge_base"]

    async def extract(self, content: str, namespace: tuple) -> list[Entity]:
        """Extract and store entities from content."""
        entities = await self.llm.analyze(f"""
        Extract all entities from this content:

        {content}

        For each entity, provide:
        - name: The entity name
        - type: PERSON | ORGANIZATION | PLACE | CONCEPT | SYSTEM
        - description: Brief description
        - relationships: Related entities

        Return as JSON array.
        """)

        for entity in entities:
            await self.memory.write_entity(**entity, namespace=namespace)

        return entities
```

### 7.5 Context Assembly Agent

```python
class ContextAssemblyAgent(EmbeddedAgent):
    """Assembles optimal context from memory."""

    name = "context_assembler"
    trigger = TriggerType.PRE_LLM

    async def assemble(
        self,
        query: str,
        thread_id: str,
        max_tokens: int = 4000,
    ) -> str:
        """Build optimal context window with priority-based allocation."""
        budget = TokenBudget(max_tokens)
        context_parts = []

        # Priority 1: Recent conversation (40%)
        conv = await self.memory.read_conversational(thread_id, limit=20)
        context_parts.append(("## Conversation Memory", conv))

        # Priority 2: Relevant knowledge (30%)
        kb = await self.memory.search_knowledge_base(query, k=5)
        context_parts.append(("## Knowledge Base Memory", kb))

        # Priority 3: Entities (15%)
        entities = await self.memory.search_entity(query, k=5)
        context_parts.append(("## Entity Memory", entities))

        # Priority 4: Workflows (10%)
        workflows = await self.memory.search_workflow(query, k=3)
        context_parts.append(("## Workflow Memory", workflows))

        # Priority 5: Summaries (5%)
        summaries = await self.memory.read_summary_context(query, thread_id)
        context_parts.append(("## Summary Memory", summaries))

        return self._format_context(context_parts)
```

### 7.6 Summarization Agent

```python
class SummarizationAgent(EmbeddedAgent):
    """Compresses old memories into summaries."""

    name = "summarizer"
    trigger = TriggerType.POLICY

    async def summarize_conversation(self, thread_id: str) -> str:
        """Summarize conversation and mark originals."""
        messages = await self.memory.read_conversational(thread_id, limit=100)

        summary = await self.llm.generate(f"""
        Summarize this conversation, preserving:
        - Key decisions made
        - Important facts mentioned
        - User preferences expressed
        - Action items

        Conversation:
        {messages}
        """)

        summary_id = await self.memory.write_summary(
            summary=summary,
            source_ids=[m.id for m in messages],
            thread_id=thread_id,
        )

        await self._mark_summarized(messages, summary_id)
        return summary_id
```

### 7.7 Consolidation Agent

```python
class ConsolidationAgent(EmbeddedAgent):
    """Merges duplicate/similar memories."""

    name = "consolidator"
    trigger = TriggerType.SCHEDULED
    schedule = "0 3 * * *"  # Daily at 3 AM

    async def run(self, memory_type: str = "*", threshold: float = 0.9) -> dict:
        """Find and merge similar memories."""
        clusters = await self._find_similar_clusters(memory_type, threshold)

        merged_count = 0
        for cluster in clusters:
            merged = await self._merge_memories(cluster.memories)
            await self.memory.add(**merged)
            await self.memory.delete_batch(cluster.memory_ids)
            merged_count += len(cluster.memories) - 1

        return {"merged_count": merged_count, "clusters": len(clusters)}

    async def _merge_memories(self, memories: list) -> dict:
        """Use LLM to intelligently merge memories."""
        merged_content = await self.llm.generate(f"""
        Merge these related memories into one comprehensive memory:
        {[m.content for m in memories]}

        Rules:
        - Preserve all unique information
        - Resolve contradictions (prefer most recent)
        - Create a coherent, deduplicated result
        """)
        return {"content": merged_content, ...}
```

### 7.8 GC Agent

```python
class GCAgent(EmbeddedAgent):
    """Garbage collection for stale memories."""

    name = "gc"
    trigger = TriggerType.SCHEDULED
    schedule = "0 4 * * 0"  # Weekly Sunday 4 AM

    async def run(self) -> dict:
        stats = {"deleted": 0, "archived": 0, "orphans_cleaned": 0}

        # 1. Delete expired memories
        expired = await self.memory.list(filters={"expires_at": {"$lt": now()}})
        for mem in expired:
            await self.memory.delete(mem.id)
            stats["deleted"] += 1

        # 2. Archive old memories
        old = await self.memory.list(filters={"created_at": {"$lt": days_ago(90)}})
        for mem in old:
            await self._archive(mem)
            stats["archived"] += 1

        # 3. Clean orphaned references
        orphans = await self._find_orphaned_references()
        for orphan in orphans:
            await self._clean_orphan(orphan)
            stats["orphans_cleaned"] += 1

        return stats
```

### 7.9 Tool Discovery Agent (VFS)

```python
class ToolDiscoveryAgent(EmbeddedAgent):
    """VFS-based progressive tool discovery."""

    name = "tool_discovery"
    trigger = TriggerType.ON_DEMAND

    async def discover(self, intent: str) -> list[dict]:
        """Discover tools using VFS exploration (ReAct pattern)."""
        messages = [
            {"role": "system", "content": TOOL_DISCOVERY_PROMPT},
            {"role": "user", "content": f"Find tools for: {intent}"},
        ]

        vfs_tools = [
            self.memory.toolbox_tree,
            self.memory.toolbox_ls,
            self.memory.toolbox_grep,
            self.memory.toolbox_cat,
            self.memory.toolbox_select,
        ]

        for _ in range(10):  # Max iterations
            response = await self.llm.generate(messages, tools=vfs_tools)

            if response.tool_calls:
                for tc in response.tool_calls:
                    result = await self._execute_vfs_op(tc)
                    messages.append({"role": "tool", "content": result})
            else:
                return self._parse_selected_tools(response.content)

        return []
```

### 7.10 Index Optimization Agent

```python
class IndexOptimizationAgent(EmbeddedAgent):
    """Maintains search index performance."""

    name = "index_optimizer"
    trigger = TriggerType.SCHEDULED
    schedule = "0 5 * * 0"  # Weekly Sunday 5 AM

    async def run(self) -> dict:
        stats = {}

        for memory_type in self.memory.list_types():
            config = self.memory.get_type_config(memory_type)

            if config.index_type == "hnsw":
                health = await self._check_hnsw_health(memory_type)
                if health.fragmentation > 0.3:
                    await self._rebuild_hnsw_index(memory_type)
                    stats[memory_type] = "rebuilt"
                else:
                    stats[memory_type] = "healthy"

        return stats
```

### 7.11 Agent Scheduler & Coordinator

```python
class AgentScheduler:
    """Coordinates all embedded agents."""

    def __init__(self, memory: "MemoryHarness", llm: "LLMProvider"):
        self.memory = memory
        self.llm = llm
        self.agents = {
            "router": MemoryRouterAgent(memory, llm),
            "entity_extractor": EntityExtractionAgent(memory, llm),
            "context_assembler": ContextAssemblyAgent(memory, llm),
            "summarizer": SummarizationAgent(memory, llm),
            "consolidator": ConsolidationAgent(memory, llm),
            "gc": GCAgent(memory, llm),
            "tool_discovery": ToolDiscoveryAgent(memory, llm),
            "index_optimizer": IndexOptimizationAgent(memory, llm),
        }
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """Start all scheduled agents."""
        for name, agent in self.agents.items():
            if agent.trigger == TriggerType.SCHEDULED:
                self.scheduler.add_job(
                    agent.run,
                    CronTrigger.from_crontab(agent.schedule),
                    id=name,
                )
        self.scheduler.start()

    async def on_write(self, content: str, metadata: dict, namespace: tuple):
        """Trigger ON_WRITE agents."""
        # Router always runs
        routing = await self.agents["router"].process(content, metadata)

        # Entity extraction runs for applicable types
        if routing.memory_type in ["conversational", "knowledge_base"]:
            await self.agents["entity_extractor"].extract(content, namespace)

    async def assemble_context(self, query: str, thread_id: str) -> str:
        """Trigger context assembly."""
        return await self.agents["context_assembler"].assemble(query, thread_id)

    async def discover_tools(self, intent: str) -> list[dict]:
        """Trigger tool discovery."""
        return await self.agents["tool_discovery"].discover(intent)
```

### 7.12 Deterministic Operation Matrix

| Agent | ON_WRITE | PRE_LLM | SCHEDULED | ON_DEMAND |
|-------|----------|---------|-----------|-----------|
| Router | ✅ (if no type) | - | - | - |
| Entity Extractor | ✅ (configurable) | - | ✅ (batch) | ✅ |
| Context Assembler | - | ✅ | - | ✅ |
| Summarizer | - | - | ✅ (policy) | ✅ |
| Consolidator | - | - | ✅ | ✅ |
| GC | - | - | ✅ | ✅ |
| Tool Discovery | - | - | - | ✅ |

---

## 8. Meta-Agent Layer (Plug-and-Play Memory-Aware Agents)

> **Concept**: A fleet of specialized "meta-agents" that sit above the memory layer and provide intelligent services to any agent using memharness. These agents are **memory-aware** — they know the memory topology, can route queries optimally, and provide the right context.

### 8.1 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          YOUR AGENT (LangChain, CrewAI, Custom)             │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          META-AGENT LAYER (Plug & Play)                     │
│                                                                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ 🧠 Context  │ │ 🔍 Query    │ │ 📊 Memory   │ │ 🎯 Intent   │           │
│  │   Curator   │ │  Optimizer  │ │   Analyst   │ │  Detector   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ 🔗 Relation │ │ 📝 Summary  │ │ 🛡️ Privacy │ │ 🎨 Format   │           │
│  │   Mapper    │ │  Explainer  │ │   Guard     │ │   Adapter   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                                              │
│  All meta-agents are MEMORY-AWARE and know the full memory topology        │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              memharness Core                                 │
│                    (Memory Types + Embedded Agents + Backends)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 The Meta-Agents Fleet

| Meta-Agent | Purpose | When to Use |
|------------|---------|-------------|
| **🧠 Context Curator** | Builds optimal context from ALL memory types intelligently | Before every LLM call |
| **🔍 Query Optimizer** | Rewrites queries for better retrieval across memory types | On search requests |
| **📊 Memory Analyst** | Provides insights about memory state, usage, gaps | On demand / monitoring |
| **🎯 Intent Detector** | Detects user intent to route to correct memory/workflow | On user input |
| **🔗 Relation Mapper** | Maps relationships between entities across memory | On entity operations |
| **📝 Summary Explainer** | Explains summaries, provides drill-down capability | When viewing summaries |
| **🛡️ Privacy Guard** | Filters sensitive info before returning to agent | On every read |
| **🎨 Format Adapter** | Formats memory for specific agent frameworks | On context assembly |

### 8.3 Context Curator (Core Meta-Agent)

```python
class ContextCurator(MetaAgent):
    """
    The brain that knows WHERE everything is and WHAT is relevant.

    Unlike basic context assembly, the Curator:
    - Understands memory topology (what's in each store)
    - Knows recency, relevance, and relationships
    - Adapts to the agent's current task
    - Manages token budget intelligently
    """

    async def curate(
        self,
        query: str,
        thread_id: str,
        task_type: str = "general",  # "coding" | "research" | "chat" | etc.
        max_tokens: int = 4000,
    ) -> CuratedContext:
        """
        Build perfectly curated context for the agent's task.

        Returns not just content, but metadata about what was included/excluded.
        """

        # 1. Analyze the query intent
        intent = await self.intent_detector.detect(query)

        # 2. Determine which memory types are relevant
        relevant_types = self._select_memory_types(intent, task_type)

        # 3. Build context with intelligent prioritization
        context = CuratedContext()

        for memory_type in relevant_types:
            # Get relevance-scored memories
            memories = await self._fetch_scored(memory_type, query, thread_id)

            # Add to context with budget management
            context.add(memory_type, memories, budget=self._allocate_budget(memory_type))

        # 4. Add relationship context if entities detected
        if intent.has_entities:
            relations = await self.relation_mapper.get_context(intent.entities)
            context.add("relationships", relations)

        # 5. Apply privacy filter
        context = await self.privacy_guard.filter(context)

        return context

    def _select_memory_types(self, intent: Intent, task_type: str) -> list[str]:
        """Intelligently select which memory types to query."""

        # Task-specific memory selection
        TASK_MEMORY_MAP = {
            "coding": ["workflow", "skills", "file", "tool_log"],
            "research": ["knowledge_base", "entity", "summary"],
            "chat": ["conversational", "entity", "persona"],
            "planning": ["workflow", "summary", "entity"],
        }

        base_types = TASK_MEMORY_MAP.get(task_type, ["conversational", "knowledge_base"])

        # Add intent-specific types
        if intent.mentions_tools:
            base_types.append("toolbox")
        if intent.asks_about_past:
            base_types.append("summary")

        return base_types
```

### 8.4 Query Optimizer

```python
class QueryOptimizer(MetaAgent):
    """
    Rewrites queries for optimal retrieval across memory types.

    Different memory types need different query formulations:
    - Entity: Extract entity names for exact match
    - Knowledge: Expand with synonyms for semantic search
    - Workflow: Extract action verbs and outcomes
    """

    async def optimize(self, query: str, memory_type: str) -> OptimizedQuery:
        """Rewrite query for specific memory type."""

        if memory_type == "entity":
            # Extract entity references
            return await self._entity_query(query)

        elif memory_type == "knowledge_base":
            # Expand with hypothetical document (HyDE)
            hypothetical = await self.llm.generate(
                f"Write a passage that would answer: {query}"
            )
            return OptimizedQuery(
                original=query,
                expanded=hypothetical,
                use_hybrid=True,
            )

        elif memory_type == "workflow":
            # Extract task structure
            return await self._workflow_query(query)

        return OptimizedQuery(original=query)
```

### 8.5 Memory Analyst

```python
class MemoryAnalyst(MetaAgent):
    """
    Provides insights about memory state — like a DBA for your agent's memory.

    Use for:
    - Monitoring memory health
    - Identifying gaps in knowledge
    - Suggesting consolidation opportunities
    - Reporting usage patterns
    """

    async def analyze(self, namespace: tuple = None) -> MemoryReport:
        """Generate comprehensive memory analysis."""

        report = MemoryReport()

        # Memory distribution
        report.distribution = await self._count_by_type(namespace)

        # Staleness analysis
        report.staleness = await self._analyze_staleness(namespace)

        # Consolidation opportunities
        report.duplicates = await self._find_near_duplicates(namespace)

        # Knowledge gaps
        report.gaps = await self._identify_gaps(namespace)

        # Usage patterns
        report.usage = await self._analyze_usage(namespace)

        return report

    async def suggest_actions(self) -> list[SuggestedAction]:
        """Suggest memory maintenance actions."""

        report = await self.analyze()
        suggestions = []

        if report.staleness.old_conversations > 10:
            suggestions.append(SuggestedAction(
                action="summarize",
                target="conversational",
                reason=f"{report.staleness.old_conversations} conversations older than threshold",
            ))

        if report.duplicates.count > 5:
            suggestions.append(SuggestedAction(
                action="consolidate",
                target="entity",
                reason=f"{report.duplicates.count} near-duplicate entities found",
            ))

        return suggestions
```

### 8.6 Privacy Guard

```python
class PrivacyGuard(MetaAgent):
    """
    Filters sensitive information before returning to agent.

    Configurable rules for:
    - PII detection and masking
    - Namespace-based access control
    - Content classification
    """

    def __init__(self, config: PrivacyConfig):
        self.config = config
        self.pii_detector = PIIDetector()

    async def filter(self, context: CuratedContext) -> CuratedContext:
        """Filter context based on privacy rules."""

        filtered = CuratedContext()

        for memory_type, memories in context.items():
            for memory in memories:
                # Check namespace access
                if not self._has_access(memory.namespace):
                    continue

                # Mask PII if configured
                if self.config.mask_pii:
                    memory.content = self.pii_detector.mask(memory.content)

                # Check content classification
                if self._is_allowed_classification(memory):
                    filtered.add(memory_type, memory)

        return filtered
```

### 8.7 Using Meta-Agents (Plug & Play)

```python
from memharness import MemoryHarness
from memharness.meta import MetaAgentLayer, ContextCurator, QueryOptimizer

# Initialize memory
memory = MemoryHarness(backend="postgresql://...")

# Add meta-agent layer (plug & play)
meta = MetaAgentLayer(
    memory=memory,
    llm=your_llm,
    agents=[
        ContextCurator(enabled=True),
        QueryOptimizer(enabled=True),
        PrivacyGuard(config=PrivacyConfig(mask_pii=True)),
        MemoryAnalyst(enabled=True),
    ],
)

# Use in your agent
async def agent_turn(user_input: str, thread_id: str):
    # Meta-agents automatically provide optimal context
    context = await meta.curate(
        query=user_input,
        thread_id=thread_id,
        task_type="coding",
    )

    # Context is already:
    # - Optimally selected from all memory types
    # - Relevance-scored and prioritized
    # - Privacy-filtered
    # - Token-budget managed

    response = await llm.generate(
        system=context.as_system_prompt(),
        user=user_input,
    )

    return response
```

### 8.8 Framework Adapters

```python
# LangChain integration
from memharness.meta.adapters import LangChainMetaAdapter

memory = MemoryHarness(...)
meta = MetaAgentLayer(memory, llm, agents=[...])

# Wrap as LangChain memory
langchain_memory = LangChainMetaAdapter(meta)

chain = ConversationChain(
    llm=llm,
    memory=langchain_memory,  # Meta-agents handle everything
)


# CrewAI integration
from memharness.meta.adapters import CrewAIMetaAdapter

crew_memory = CrewAIMetaAdapter(meta)

crew = Crew(
    agents=[...],
    memory=crew_memory,  # Shared memory-aware context
)
```

### 8.9 Meta-Agent Configuration

```yaml
# memharness.yaml
meta_agents:
  context_curator:
    enabled: true
    task_profiles:
      coding:
        priorities: [workflow, skills, file, tool_log]
        max_tokens: 6000
      research:
        priorities: [knowledge_base, entity, summary]
        max_tokens: 8000
      chat:
        priorities: [conversational, entity, persona]
        max_tokens: 4000

  query_optimizer:
    enabled: true
    use_hyde: true  # Hypothetical Document Embeddings
    expand_synonyms: true

  privacy_guard:
    enabled: true
    mask_pii: true
    pii_types: [email, phone, ssn, credit_card]
    namespace_acl:
      "org:*": [read, write]
      "org:other": []  # No access to other orgs

  memory_analyst:
    enabled: true
    report_schedule: "0 6 * * 1"  # Weekly Monday 6 AM
    alert_on_issues: true
```

> **See full details**: [12-ai-native-memory-agents.md](12-ai-native-memory-agents.md)

---

## 9. Framework Integrations

### 9.1 LangChain Adapter

```python
from langchain.memory import BaseMemory

class MemharnessLangChainMemory(BaseMemory):
    """LangChain-compatible memory using memharness."""

    def __init__(self, harness: MemoryHarness, thread_id: str):
        self._harness = harness
        self._thread_id = thread_id

    @property
    def memory_variables(self) -> list[str]:
        return ["history"]

    def load_memory_variables(self, inputs: dict) -> dict:
        history = asyncio.run(
            self._harness.read_conversational(self._thread_id)
        )
        return {"history": history}

    def save_context(self, inputs: dict, outputs: dict) -> None:
        asyncio.run(
            self._harness.write_conversational(
                self._thread_id, "user", inputs.get("input", "")
            )
        )
        asyncio.run(
            self._harness.write_conversational(
                self._thread_id, "assistant", outputs.get("output", "")
            )
        )
```

### 9.2 LangGraph Adapter

```python
from langgraph.checkpoint.base import BaseCheckpointSaver

class MemharnessCheckpointer(BaseCheckpointSaver):
    """LangGraph checkpointer using memharness."""

    def __init__(self, harness: MemoryHarness):
        self._harness = harness

    async def aget(self, config: dict) -> Optional[dict]:
        thread_id = config["configurable"]["thread_id"]
        return await self._harness.get(f"checkpoint:{thread_id}")

    async def aput(self, config: dict, checkpoint: dict) -> None:
        thread_id = config["configurable"]["thread_id"]
        await self._harness.add(
            content=json.dumps(checkpoint),
            memory_type="checkpoint",
            key=f"checkpoint:{thread_id}",
        )
```

---

## 10. Package Structure

```
memharness/
├── __init__.py              # Main exports
├── harness.py               # MemoryHarness class
├── config.py                # Configuration classes
├── types.py                 # MemoryUnit, MemoryTypeConfig
├── registry.py              # MemoryTypeRegistry
│
├── backends/
│   ├── __init__.py
│   ├── protocol.py          # BackendProtocol
│   ├── composite.py         # CompositeBackend
│   ├── postgres.py          # PostgresBackend
│   ├── sqlite.py            # SqliteBackend
│   ├── redis.py             # RedisBackend
│   └── memory.py            # InMemoryBackend
│
├── embeddings/
│   ├── __init__.py
│   ├── base.py              # EmbeddingFunction protocol
│   ├── sentence_transformers.py
│   └── openai.py
│
├── lifecycle/
│   ├── __init__.py
│   ├── engine.py            # LifecycleEngine
│   └── policies.py          # LifecyclePolicy, DEFAULT_POLICIES
│
├── agents/                  # Embedded AI Agents (for complex tasks)
│   ├── __init__.py
│   ├── base.py              # EmbeddedAgent ABC
│   ├── router.py            # MemoryRouterAgent
│   ├── summarizer.py        # SummarizationAgent
│   ├── consolidator.py      # ConsolidationAgent
│   ├── gc.py                # GCAgent
│   ├── entity_extractor.py  # EntityExtractionAgent
│   ├── context_assembler.py # ContextAssemblyAgent
│   ├── tool_discovery.py    # ToolDiscoveryAgent (VFS)
│   └── scheduler.py         # AgentScheduler
│
├── meta/                    # Meta-Agent Layer (Plug & Play)
│   ├── __init__.py
│   ├── base.py              # MetaAgent ABC
│   ├── layer.py             # MetaAgentLayer
│   ├── context_curator.py   # ContextCurator
│   ├── query_optimizer.py   # QueryOptimizer
│   ├── memory_analyst.py    # MemoryAnalyst
│   ├── privacy_guard.py     # PrivacyGuard
│   ├── relation_mapper.py   # RelationMapper
│   └── adapters/            # Framework adapters for meta layer
│       ├── __init__.py
│       ├── langchain.py
│       ├── crewai.py
│       └── langgraph.py
│
├── tools/
│   ├── __init__.py
│   └── memory_tools.py      # Tools for agent use
│
├── integrations/            # Basic framework integrations
│   ├── __init__.py
│   ├── langchain.py
│   ├── langgraph.py
│   └── crewai.py
│
└── server/                  # Optional REST API server
    ├── __init__.py
    ├── app.py
    └── routes.py
```

---

## 11. Configuration (Fully Configurable)

> **Principle**: All thresholds, schedules, TTLs, and policies are configurable. Nothing hardcoded.

### 10.1 Python Configuration API

```python
from memharness import MemoryHarness, Config
from memharness.config import (
    ConversationalConfig,
    SummarizationConfig,
    ConsolidationConfig,
    GCConfig,
    EntityExtractionConfig,
    ContextAssemblyConfig,
    ToolDiscoveryConfig,
    IndexConfig,
)

memory = MemoryHarness(
    backend="postgresql://...",
    config=Config(
        # ═══════════════════════════════════════════════════════════════
        # CONVERSATIONAL MEMORY
        # ═══════════════════════════════════════════════════════════════
        conversational=ConversationalConfig(
            max_messages_per_thread=1000,     # Before forced summarization
            default_ttl=None,                  # Never expire (or "90d", "1y")
            auto_summarize_threshold=50,       # Summarize after N messages
        ),

        # ═══════════════════════════════════════════════════════════════
        # SUMMARIZATION (AI Agent)
        # ═══════════════════════════════════════════════════════════════
        summarization=SummarizationConfig(
            enabled=True,
            triggers=[
                {"condition": "age > 7d", "memory_type": "conversational"},
                {"condition": "context_usage > 80%", "memory_type": "*"},
                {"condition": "message_count > 50", "memory_type": "conversational"},
            ],
            keep_originals=True,              # Archive, don't delete
            originals_ttl="365d",             # Keep originals for 1 year
            originals_storage="cold",         # Move to cold storage after summarization
        ),

        # ═══════════════════════════════════════════════════════════════
        # CONSOLIDATION (AI Agent)
        # ═══════════════════════════════════════════════════════════════
        consolidation=ConsolidationConfig(
            enabled=True,
            schedule="0 3 * * *",             # Cron: Daily at 3 AM
            similarity_threshold=0.9,         # Merge if > 90% similar
            min_cluster_size=2,               # Need at least 2 to merge
            memory_types=["entity", "knowledge_base"],  # Types to consolidate
        ),

        # ═══════════════════════════════════════════════════════════════
        # GARBAGE COLLECTION (Deterministic + AI)
        # ═══════════════════════════════════════════════════════════════
        gc=GCConfig(
            enabled=True,
            schedule="0 4 * * 0",             # Cron: Weekly Sunday 4 AM
            archive_after="90d",              # Move to cold storage after 90 days
            delete_archived_after="365d",     # Delete from cold after 1 year
            vacuum_after_delete=True,         # Reclaim storage space
            protect_referenced=True,          # Don't delete if referenced by summary
        ),

        # ═══════════════════════════════════════════════════════════════
        # ENTITY EXTRACTION (AI Agent)
        # ═══════════════════════════════════════════════════════════════
        entity_extraction=EntityExtractionConfig(
            enabled=True,
            mode="on_write",                  # "on_write" | "batch" | "disabled"
            batch_schedule="0 2 * * *",       # If mode="batch": Daily 2 AM
            types=["PERSON", "ORG", "PLACE", "CONCEPT", "PRODUCT", "SYSTEM"],
            min_confidence=0.7,               # Only store if confidence > 70%
            merge_existing=True,              # Merge with existing entities
        ),

        # ═══════════════════════════════════════════════════════════════
        # CONTEXT ASSEMBLY (AI Agent)
        # ═══════════════════════════════════════════════════════════════
        context_assembly=ContextAssemblyConfig(
            default_max_tokens=4000,
            priorities={                      # Token budget allocation
                "conversational": 0.40,       # 40% for recent conversation
                "knowledge_base": 0.30,       # 30% for relevant knowledge
                "entity": 0.15,               # 15% for entities
                "workflow": 0.10,             # 10% for workflows
                "summary": 0.05,              # 5% for summaries
            },
            expand_summaries=False,           # Use summaries by default
            auto_expand_threshold=0.8,        # Expand if relevance > 80%
        ),

        # ═══════════════════════════════════════════════════════════════
        # TOOL DISCOVERY (AI Agent - VFS)
        # ═══════════════════════════════════════════════════════════════
        tool_discovery=ToolDiscoveryConfig(
            enabled=True,
            max_iterations=10,                # Max ReAct iterations
            cache_ttl="1h",                   # Cache discovered tools
            prefer_recent=True,               # Prefer recently used tools
        ),

        # ═══════════════════════════════════════════════════════════════
        # INDEX OPTIMIZATION (Deterministic)
        # ═══════════════════════════════════════════════════════════════
        index_optimization=IndexConfig(
            enabled=True,
            schedule="0 5 * * 0",             # Weekly Sunday 5 AM
            rebuild_threshold=0.3,            # Rebuild if fragmentation > 30%
            auto_vacuum=True,                 # Auto vacuum after large deletes
        ),
    ),
)
```

### 10.2 Per-Namespace Overrides

```python
# Global default config (set above)
# ...

# Override for specific namespace (e.g., enterprise customer)
memory.configure_namespace(
    namespace=("org", "enterprise_customer"),
    config=Config(
        summarization=SummarizationConfig(
            triggers=[{"condition": "age > 30d"}],  # Keep longer for enterprise
        ),
        gc=GCConfig(
            delete_archived_after="7y",  # 7-year retention for compliance
        ),
    ),
)

# Override for specific user
memory.configure_namespace(
    namespace=("org", "acme", "user", "alice"),
    config=Config(
        context_assembly=ContextAssemblyConfig(
            default_max_tokens=8000,  # Alice needs more context
        ),
    ),
)
```

### 10.3 Configuration File (YAML)

```yaml
# memharness.yaml
backend: postgresql://user:pass@localhost/memharness

# ═══════════════════════════════════════════════════════════════
# CONVERSATIONAL
# ═══════════════════════════════════════════════════════════════
conversational:
  max_messages_per_thread: 1000
  default_ttl: null  # Never expire
  auto_summarize_threshold: 50

# ═══════════════════════════════════════════════════════════════
# SUMMARIZATION
# ═══════════════════════════════════════════════════════════════
summarization:
  enabled: true
  triggers:
    - condition: "age > 7d"
      memory_type: conversational
    - condition: "context_usage > 80%"
      memory_type: "*"
    - condition: "message_count > 50"
      memory_type: conversational
  keep_originals: true
  originals_ttl: 365d
  originals_storage: cold

# ═══════════════════════════════════════════════════════════════
# CONSOLIDATION
# ═══════════════════════════════════════════════════════════════
consolidation:
  enabled: true
  schedule: "0 3 * * *"
  similarity_threshold: 0.9
  min_cluster_size: 2
  memory_types:
    - entity
    - knowledge_base

# ═══════════════════════════════════════════════════════════════
# GARBAGE COLLECTION
# ═══════════════════════════════════════════════════════════════
gc:
  enabled: true
  schedule: "0 4 * * 0"
  archive_after: 90d
  delete_archived_after: 365d
  vacuum_after_delete: true
  protect_referenced: true

# ═══════════════════════════════════════════════════════════════
# ENTITY EXTRACTION
# ═══════════════════════════════════════════════════════════════
entity_extraction:
  enabled: true
  mode: on_write
  types:
    - PERSON
    - ORG
    - PLACE
    - CONCEPT
  min_confidence: 0.7

# ═══════════════════════════════════════════════════════════════
# CONTEXT ASSEMBLY
# ═══════════════════════════════════════════════════════════════
context_assembly:
  default_max_tokens: 4000
  priorities:
    conversational: 0.40
    knowledge_base: 0.30
    entity: 0.15
    workflow: 0.10
    summary: 0.05
  expand_summaries: false
  auto_expand_threshold: 0.8

# ═══════════════════════════════════════════════════════════════
# TOOL DISCOVERY
# ═══════════════════════════════════════════════════════════════
tool_discovery:
  enabled: true
  max_iterations: 10
  cache_ttl: 1h

# ═══════════════════════════════════════════════════════════════
# INDEX OPTIMIZATION
# ═══════════════════════════════════════════════════════════════
index_optimization:
  enabled: true
  schedule: "0 5 * * 0"
  rebuild_threshold: 0.3

# ═══════════════════════════════════════════════════════════════
# PER-NAMESPACE OVERRIDES
# ═══════════════════════════════════════════════════════════════
namespace_overrides:
  "org:enterprise":
    summarization:
      triggers:
        - condition: "age > 30d"
    gc:
      delete_archived_after: 7y

  "org:startup":
    gc:
      archive_after: 30d
      delete_archived_after: 90d
```

### 10.4 Loading Configuration

```python
# From file
memory = MemoryHarness.from_config("memharness.yaml")

# From environment
memory = MemoryHarness.from_env()  # Uses MEMHARNESS_* env vars

# Runtime updates (no restart needed)
await memory.update_config(
    summarization={"triggers": [{"condition": "age > 14d"}]}
)

# Enable/disable agents at runtime
await memory.disable_agent("consolidation")  # Temporarily disable
await memory.enable_agent("consolidation")   # Re-enable
```

### 10.5 Environment Variables

```bash
# Backend
MEMHARNESS_BACKEND=postgresql://user:pass@localhost/db
MEMHARNESS_CACHE=redis://localhost:6379

# Embeddings
MEMHARNESS_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MEMHARNESS_OPENAI_API_KEY=sk-...  # If using OpenAI embeddings

# LLM for agents
MEMHARNESS_LLM_PROVIDER=openai    # openai | anthropic | local
MEMHARNESS_LLM_MODEL=gpt-4o-mini
MEMHARNESS_ANTHROPIC_API_KEY=sk-ant-...

# Quick toggles
MEMHARNESS_SUMMARIZATION_ENABLED=true
MEMHARNESS_CONSOLIDATION_ENABLED=true
MEMHARNESS_GC_ENABLED=true
MEMHARNESS_ENTITY_EXTRACTION_ENABLED=true
```

### 11.6 Configuration Validation

```python
from memharness.config import validate_config, ConfigError

try:
    config = Config(
        summarization=SummarizationConfig(
            triggers=[{"condition": "invalid"}],  # Invalid condition
        ),
    )
    validate_config(config)
except ConfigError as e:
    print(f"Invalid config: {e}")
    # Invalid config: Unknown condition operator in 'invalid'
```

---

## 12. Next Steps

1. **Implement Phase 1**: Core memory types + PostgreSQL/SQLite backends
2. **Add tests**: Unit tests, integration tests
3. **Create documentation**: API docs, tutorials
4. **Publish to PyPI**: Initial release
5. **Implement Phase 2**: All backends, lifecycle, agents
6. **Framework integrations**: LangChain, LangGraph, CrewAI

---

*HLD Version: 1.0*
*Created: 2026-03-22*

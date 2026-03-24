# Infrastructure: Vector DBs, Caching & Storage

> Research Report for memharness project

---

## Executive Summary

memharness needs a flexible storage layer supporting SQL (exact queries), vectors (semantic search), and caching (performance). This report evaluates PostgreSQL+pgvector, SQLite, Redis, and other vector databases to inform our multi-backend architecture.

---

## 1. PostgreSQL + pgvector

### 1.1 Overview

pgvector is the **production-grade choice** for agent memory:
- ACID compliance
- Hybrid SQL + vector queries
- Mature ecosystem
- Horizontal scaling options

### 1.2 Indexing Methods

| Index | Build Speed | Query Speed | Memory | Best For |
|-------|-------------|-------------|--------|----------|
| **HNSW** | Slower | Faster | Higher | Production queries |
| **IVFFlat** | Faster | Slower | Lower | Large datasets, frequent updates |

**HNSW (Hierarchical Navigable Small World):**
```sql
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Query parameter
SET hnsw.ef_search = 40;
```

**IVFFlat (Inverted File):**
```sql
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Query parameter
SET ivfflat.probes = 10;
```

### 1.3 Distance Functions

| Operator | Distance | Use Case |
|----------|----------|----------|
| `<->` | L2 (Euclidean) | Default similarity |
| `<=>` | Cosine | Normalized embeddings |
| `<#>` | Inner Product | When vectors are normalized |
| `<+>` | L1 (Manhattan) | Sparse vectors |

### 1.4 Hybrid Search Pattern

```sql
-- Combine vector similarity with SQL filters
SELECT id, content, embedding <=> query_embedding AS distance
FROM memories
WHERE user_id = 'alice'
  AND memory_type = 'knowledge_base'
  AND created_at > NOW() - INTERVAL '7 days'
ORDER BY embedding <=> query_embedding
LIMIT 10;
```

### 1.5 Schema for memharness

```sql
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    namespace TEXT[] NOT NULL,  -- hierarchical: ['org', 'user', 'thread']
    key TEXT NOT NULL,
    memory_type TEXT NOT NULL,  -- conversation, knowledge_base, entity, etc.
    content TEXT NOT NULL,
    embedding vector(768),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,

    UNIQUE (namespace, key)
);

CREATE INDEX idx_memories_namespace ON memories USING GIN (namespace);
CREATE INDEX idx_memories_type ON memories (memory_type);
CREATE INDEX idx_memories_embedding ON memories USING hnsw (embedding vector_cosine_ops);
```

### 1.6 Recommendation

**Use PostgreSQL + pgvector for production.** Provides:
- Single database for SQL + vector
- ACID transactions
- Rich querying (JOIN, GROUP BY, etc.)
- Proven scalability

---

## 2. SQLite + Vector Extensions

### 2.1 Options

| Extension | Status | Features |
|-----------|--------|----------|
| **sqlite-vss** | Mature | FAISS-based, IVF index |
| **sqlite-vec** | Newer | Pure SQLite, simpler |
| **Chroma** | Embedded | SQLite backend |

### 2.2 sqlite-vss

```python
import sqlite3
import sqlite_vss

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vss.load(db)

# Create virtual table
db.execute("""
    CREATE VIRTUAL TABLE vss_memories USING vss0(
        embedding(768)
    )
""")

# Insert
db.execute("INSERT INTO vss_memories (rowid, embedding) VALUES (?, ?)",
           [1, embedding_bytes])

# Search
db.execute("""
    SELECT rowid, distance
    FROM vss_memories
    WHERE vss_search(embedding, ?)
    LIMIT 10
""", [query_embedding_bytes])
```

### 2.3 Use Case

**SQLite is ideal for:**
- Local-first applications
- Development/testing
- Single-user agents
- Edge deployment (no server needed)

### 2.4 Limitation

- No concurrent writes (file locking)
- Vector search less optimized than pgvector
- Limited scaling

---

## 3. Redis + Vector Search

### 3.1 Redis Stack

Redis Stack adds vector search to Redis:

```python
from redis import Redis
from redis.commands.search.field import VectorField, TextField, NumericField
from redis.commands.search.query import Query

r = Redis(host='localhost', port=6379)

# Create index
r.ft("memory_idx").create_index([
    TextField("content"),
    TextField("memory_type"),
    NumericField("created_at"),
    VectorField("embedding", "HNSW", {
        "TYPE": "FLOAT32",
        "DIM": 768,
        "DISTANCE_METRIC": "COSINE"
    })
])

# Add memory
r.hset("memory:1", mapping={
    "content": "User prefers Python",
    "memory_type": "entity",
    "embedding": embedding_bytes
})

# Vector search
query = Query("*=>[KNN 10 @embedding $vec AS score]")\
    .return_fields("content", "score")\
    .sort_by("score")\
    .dialect(2)

results = r.ft("memory_idx").search(query, {"vec": query_embedding_bytes})
```

### 3.2 Caching Patterns for Agent Memory

```python
# Pattern 1: Semantic Cache
# Cache LLM responses for similar queries
cache_key = f"semantic_cache:{hash(embedding)}"
cached = r.get(cache_key)
if not cached:
    response = llm.generate(query)
    r.setex(cache_key, 3600, response)  # TTL 1 hour

# Pattern 2: Hot Memory Cache
# Cache frequently accessed memories
hot_key = f"hot:{user_id}:{memory_type}"
r.zadd(hot_key, {memory_id: access_count})
# Get top-K hot memories
hot_memories = r.zrevrange(hot_key, 0, 9)

# Pattern 3: Pub/Sub for Memory Updates
# Real-time memory sync across agents
r.publish("memory_updates", json.dumps({
    "action": "write",
    "memory_id": "xxx",
    "user_id": "alice"
}))
```

### 3.3 Use Cases

| Pattern | Use Case |
|---------|----------|
| **Semantic Cache** | Avoid redundant LLM calls |
| **Hot Memory** | Frequently accessed entities |
| **Session Store** | Working memory (ephemeral) |
| **Pub/Sub** | Multi-agent memory sync |
| **Rate Limiting** | Memory write throttling |

### 3.4 Recommendation

**Use Redis as a caching layer**, not primary storage:
- Cache hot paths (frequent queries)
- Session/working memory
- Pub/sub for real-time sync
- Pair with PostgreSQL for persistence

---

## 4. Other Vector Databases

### 4.1 Comparison

| Database | Deployment | Best For | Limitations |
|----------|------------|----------|-------------|
| **Chroma** | Embedded/Server | Prototyping, small scale | No SQL, limited filtering |
| **Pinecone** | Managed | Production at scale | Vendor lock-in, cost |
| **Weaviate** | Self-host/Cloud | GraphQL API, modules | Complexity |
| **Qdrant** | Self-host/Cloud | Rust performance | Newer ecosystem |
| **Milvus** | Self-host | Massive scale | Operational overhead |

### 4.2 Chroma (Good for Development)

```python
import chromadb

client = chromadb.Client()  # In-memory
# or
client = chromadb.PersistentClient(path="./chroma_data")

collection = client.create_collection("memories")

# Add
collection.add(
    documents=["User likes Python"],
    metadatas=[{"user_id": "alice", "type": "entity"}],
    ids=["mem_1"]
)

# Query
results = collection.query(
    query_texts=["programming preferences"],
    n_results=5,
    where={"user_id": "alice"}
)
```

**Pros:** Simple API, embedded mode, good for testing
**Cons:** Limited SQL, no joins, less mature

---

## 5. Storage Architecture for memharness

### 5.1 Recommended Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    memharness API                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Storage Abstraction                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ SQL Store   │  │ Vector Store│  │ Cache Store         │ │
│  │ Interface   │  │ Interface   │  │ Interface           │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │                   │                    │
         ▼                   ▼                    ▼
┌─────────────┐     ┌─────────────┐      ┌─────────────┐
│ PostgreSQL  │     │ pgvector    │      │ Redis       │
│ SQLite      │     │ Chroma      │      │ In-memory   │
└─────────────┘     └─────────────┘      └─────────────┘
```

### 5.2 Backend Selection Matrix

| Use Case | Recommended Backend |
|----------|-------------------|
| Production | PostgreSQL + pgvector + Redis |
| Development | SQLite + Chroma + In-memory cache |
| Testing | All in-memory |
| Edge/Local | SQLite + sqlite-vss |
| Serverless | PostgreSQL (Neon/Supabase) |

### 5.3 Interface Design

```python
from abc import ABC, abstractmethod

class StorageBackend(ABC):
    """Base interface for all storage backends."""

    @abstractmethod
    async def write(self, namespace: tuple, key: str, value: dict) -> str:
        """Write a memory unit."""
        pass

    @abstractmethod
    async def read(self, namespace: tuple, key: str) -> Optional[dict]:
        """Read a specific memory unit."""
        pass

    @abstractmethod
    async def search(
        self,
        namespace: tuple,
        query: str,
        k: int = 10,
        filters: Optional[dict] = None
    ) -> List[dict]:
        """Semantic search within namespace."""
        pass

    @abstractmethod
    async def delete(self, namespace: tuple, key: str) -> bool:
        """Delete a memory unit."""
        pass

    @abstractmethod
    async def list(
        self,
        namespace: tuple,
        filters: Optional[dict] = None
    ) -> List[dict]:
        """List all memories in namespace."""
        pass
```

---

## 6. Key Recommendations

| Aspect | Recommendation |
|--------|----------------|
| **Primary Storage** | PostgreSQL + pgvector (production) |
| **Development** | SQLite + Chroma |
| **Caching** | Redis (hot paths, sessions) |
| **Index Type** | HNSW for queries, IVFFlat for write-heavy |
| **Hybrid Search** | Combine vector + SQL filters |
| **Abstraction** | Single interface, pluggable backends |

---

## Sources

- pgvector GitHub (github.com/pgvector/pgvector)
- Chroma Documentation (docs.trychroma.com)
- Redis Vector Search Documentation
- Personal knowledge of database systems

---

*Research completed: 2026-03-22*

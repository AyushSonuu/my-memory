# 🗺️ Everything I Know

> God-level map of all knowledge. Auto-maintained.

```mermaid
graph TB
    ROOT(("🧠 Everything"))
    
    subgraph TECH ["🔧 Tech (2 topics)"]
        AM["🧠 <b>Agent Memory</b><br/>7/7 ✅"]
        PY["🐍 <b>Python</b>"]
        PY --> AIO["⚡ <b>AsyncIO</b><br/>1/1 ✅"]
    end

    subgraph NT ["🌍 Non-Tech (0 topics)"]
        NTE["Coming soon..."]
    end

    ROOT --> TECH
    ROOT --> NT

    style ROOT fill:#37474f,color:#fff,stroke:#263238,stroke-width:2px
    style TECH fill:#e3f2fd,color:#333,stroke:#1565c0,stroke-width:2px
    style NT fill:#f5f5f5,color:#666,stroke:#bdbdbd,stroke-dasharray: 5 5
    style AM fill:#ff9800,color:#fff,stroke:#e65100
    style PY fill:#2196f3,color:#fff,stroke:#1565c0
    style AIO fill:#ff9800,color:#fff,stroke:#e65100
    style NTE fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
```

## 📊 Dashboard

| Status | Count | Topics |
|--------|-------|--------|
| 🟢 Solid | 0 | — |
| 🟡 Learning | 2 | Agent Memory, AsyncIO |
| 🔴 Weak/Todo | 0 | — |

## Key Connections

| Connection | How they relate |
|-----------|----------------|
| Agent Memory ↔ AsyncIO | Async for concurrent memory operations, tool execution, API calls |
| Agent Memory → RAG | Same pipeline, agent memory adds CRUD + write-back |
| Agent Memory → Vector DBs | OracleVS, COSINE, IVF indexes |
| Agent Memory → LangChain | Orchestration framework |
| AsyncIO → FastAPI | FastAPI is built on AsyncIO |

---

> 📂 Detailed views: [Tech Map](tech.md) · [Non-Tech Map](non-tech.md) · [Weak Spots](weak-spots.md) · [Connections](connections.md) · [Timeline](learning-journey.md)

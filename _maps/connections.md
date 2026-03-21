# 🔗 Cross-Topic Connections

> Rolling log of connections between topics. Max 30 entries.

```mermaid
graph LR
    AM["🧠 Agent Memory"]
    AIO["⚡ AsyncIO"]
    
    AM ---|"async for concurrent<br/>memory ops & tool execution"| AIO
    AM -.->|"future"| RAG["📖 RAG"]
    AM -.->|"future"| VDB["🗄️ Vector Databases"]
    AM -.->|"future"| LC["🔗 LangChain"]
    AIO -.->|"future"| FAPI["🚀 FastAPI"]

    style AM fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
    style AIO fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
    style RAG fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
    style VDB fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
    style LC fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
    style FAPI fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
```

## 🆕 Recently Discovered Connections

| Date | Connection | How I Found It |
|------|-----------|----------------|
| 2026-03-21 | Agent Memory ↔ AsyncIO | Async for concurrent memory ops, tool execution, API calls |
| 2026-03-21 | Agent Memory → RAG | Same pipeline, agent memory adds CRUD (L02) |
| 2026-03-21 | Agent Memory → Vector Databases | OracleVS, COSINE, IVF indexes (L03) |
| 2026-03-21 | Agent Memory → LangChain | Orchestration framework (L03-L06) |
| 2026-03-21 | AsyncIO → FastAPI | FastAPI is built on AsyncIO patterns |

> Connections will explode as more topics are added! 🔗

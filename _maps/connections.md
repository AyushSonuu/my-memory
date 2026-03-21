# 🔗 Cross-Topic Connections

> Rolling log of connections between topics. Max 30 entries.

```mermaid
graph LR
    AM["🧠 Agent Memory"]
    
    AM -.->|"future"| RAG["📖 RAG"]
    AM -.->|"future"| VDB["🗄️ Vector Databases"]
    AM -.->|"future"| LC["🔗 LangChain"]
    AM -.->|"future"| LLM["🤖 LLMs"]
    AM -.->|"future"| SD["🏗️ System Design"]

    style AM fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
    style RAG fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
    style VDB fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
    style LC fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
    style LLM fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
    style SD fill:#f5f5f5,color:#999,stroke-dasharray: 5 5
```

## 🆕 Recently Discovered Connections

| Date | Connection | How I Found It |
|------|-----------|----------------|
| 2026-03-21 | Agent Memory → RAG (same pipeline, agent memory adds CRUD) | L02: RAG vs Agent Memory comparison |
| 2026-03-21 | Agent Memory → Vector Databases (OracleVS, COSINE, IVF indexes) | L03: Memory Manager code lab |
| 2026-03-21 | Agent Memory → LangChain (orchestration, OracleVS integration) | L03-L06: all code labs |
| 2026-03-21 | Agent Memory → LLMs (extraction, summarization, augmentation, reasoning) | L04-L06: augmentation, context eng, agent loop |

> Only 1 topic so far. Connections will explode as you add more topics! 🔗

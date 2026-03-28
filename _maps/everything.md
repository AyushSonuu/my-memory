# 🗺️ Everything I Know

> God-level map of all knowledge.

```mermaid
graph TB
    ROOT(("🧠 Everything"))
    
    subgraph TECH ["🔧 Tech — 4 topics"]
        AG["🤖 Agentic AI — M1 ✅ M2 ✅ M3-M5 🚧"]
        AM["🧠 Agent Memory — 7/7 ✅"]
        PY["🐍 Python"]
        PY --> AIO["⚡ AsyncIO — 1/1 ✅"]
        PY --> THR["🧵 Threading — 1/1 ✅"]
        AG -.->|"builds on"| AM
        THR -.->|"vs"| AIO
    end

    subgraph NT ["🌍 Non-Tech — 0 topics"]
        NTE["Coming soon"]
    end

    ROOT --> TECH
    ROOT --> NT
```

## 📊 Dashboard

| Status | Count | Topics |
|--------|-------|--------|
| 🟢 Solid | 0 | — |
| 🟡 Learning | 3 | Agent Memory, AsyncIO, Threading |
| 🔴 Starting | 1 | Agentic AI (M1-M2 complete, M3-M5 pending) |

## Key Connections

| Connection | How they relate |
|-----------|----------------|
| Agentic AI ↔ Agent Memory | Agent memory = one of the capabilities agentic systems need |
| Agentic AI → Evals & Error Analysis | #1 predictor of building agents well; tracked in [vs.md](../tech/agentic-ai/vs.md) |
| Agentic AI → 4 Design Patterns | Reflection ✅, Tool Use, Planning, Multi-Agent |
| Reflection → External Feedback | Code execution, web search, regex, word count = breaks performance plateau |
| Threading ↔ AsyncIO | Both do I/O concurrency — threading uses OS threads, AsyncIO uses event loop |
| Agent Memory ↔ AsyncIO | Async for concurrent memory operations, tool execution, API calls |
| Agent Memory → RAG | Same pipeline, agent memory adds CRUD + write-back |
| Agent Memory → Vector DBs | OracleVS, COSINE, IVF indexes |
| AsyncIO → FastAPI | FastAPI is built on AsyncIO |

---

Detailed views: [Tech Map](tech.md) · [Non-Tech Map](non-tech.md) · [Weak Spots](weak-spots.md) · [Connections](connections.md) · [Timeline](learning-journey.md)

# 🗺️ Tech Knowledge Graph

> Deep view with sub-topics and lesson-level detail.

```mermaid
graph TB
    T(("🔧 Tech"))
    T --> AM["🧠 <b>Agent Memory</b>"]
    T --> PY["🐍 <b>Python</b>"]
    
    AM --> AML1["01 · Introduction"]
    AM --> AML2["02 · Why Memory"]
    AM --> AML3["03 · Memory Manager"]
    AM --> AML4["04 · Semantic Tool Memory"]
    AM --> AML5["05 · Memory Operations"]
    AM --> AML6["06 · Memory Aware Agent"]
    AM --> AML7["07 · Conclusion"]

    PY --> AIO["⚡ <b>AsyncIO</b>"]
    AIO --> AIOL1["01 · Complete Guide"]

    style T fill:#2196f3,color:#fff,stroke:#1565c0,stroke-width:2px
    style AM fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
    style PY fill:#2196f3,color:#fff,stroke:#1565c0
    style AIO fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
    style AML1 fill:#4caf50,color:#fff,stroke:#388e3c
    style AML2 fill:#4caf50,color:#fff,stroke:#388e3c
    style AML3 fill:#4caf50,color:#fff,stroke:#388e3c
    style AML4 fill:#4caf50,color:#fff,stroke:#388e3c
    style AML5 fill:#4caf50,color:#fff,stroke:#388e3c
    style AML6 fill:#4caf50,color:#fff,stroke:#388e3c
    style AML7 fill:#4caf50,color:#fff,stroke:#388e3c
    style AIOL1 fill:#4caf50,color:#fff,stroke:#388e3c
```

## Topics Detail

| Topic | Status | Lessons | Key Concepts |
|-------|--------|---------|-------------|
| 🧠 Agent Memory | 🟡 7/7 ✅ | 7 | Memory Manager, Toolbox Pattern, Summarization/Compaction, Agent Loop, Harness |
| ⚡ AsyncIO | 🟡 1/1 ✅ | 1 | Event Loop, Coroutines, Tasks, gather, TaskGroup, Threads, Processes, Semaphores |

---

> Detailed topic views → [Agent Memory](../tech/agent-memory/README.md) · [AsyncIO](../tech/python/asyncio/README.md)

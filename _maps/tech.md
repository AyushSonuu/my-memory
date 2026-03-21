# 🗺️ Tech Knowledge Graph

> Deep view with sub-topics and lesson-level detail.

```mermaid
graph TB
    T(("🔧 Tech"))
    T --> AM["🧠 Agent Memory"]
    T --> PY["🐍 Python"]
    
    AM --> L1["01 · Introduction"]
    AM --> L2["02 · Why Memory"]
    AM --> L3["03 · Memory Manager"]
    AM --> L4["04 · Semantic Tool Memory"]
    AM --> L5["05 · Memory Operations"]
    AM --> L6["06 · Memory Aware Agent"]
    AM --> L7["07 · Conclusion"]

    PY --> AIO["⚡ AsyncIO"]
    AIO --> AIOL1["01 · Complete Guide"]
```

## Topics Detail

| Topic | Status | Lessons | Key Concepts |
|-------|--------|---------|-------------|
| [🧠 Agent Memory](../tech/agent-memory/README.md) | 🟡 7/7 ✅ | 7 | Memory Manager, Toolbox Pattern, Summarization/Compaction, Agent Loop, Harness |
| [⚡ AsyncIO](../tech/python/asyncio/README.md) | 🟡 1/1 ✅ | 1 | Event Loop, Coroutines, Tasks, gather, TaskGroup, Threads, Processes, Semaphores |

---

Detailed topic views → [Agent Memory](../tech/agent-memory/README.md) · [AsyncIO](../tech/python/asyncio/README.md)

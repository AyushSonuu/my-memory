# 🗺️ Tech Knowledge Graph

> Deep view with sub-topics and lesson-level detail.

```mermaid
graph TB
    T(("🔧 Tech"))
    T --> AG["🤖 Agentic AI"]
    T --> AM["🧠 Agent Memory"]
    T --> PY["🐍 Python"]
    
    AG --> M1["Module 1 · Intro"]
    AG --> M2["Module 2 · Reflection"]
    AG --> M3["Module 3 · Tool Use"]
    AG --> M4["Module 4 · Practical Tips"]
    AG --> M5["Module 5 · Autonomous Agents"]

    AM --> L1["01 · Introduction"]
    AM --> L2["02 · Why Memory"]
    AM --> L3["03 · Memory Manager"]
    AM --> L4["04 · Semantic Tool Memory"]
    AM --> L5["05 · Memory Operations"]
    AM --> L6["06 · Memory Aware Agent"]
    AM --> L7["07 · Conclusion"]

    PY --> AIO["⚡ AsyncIO"]
    AIO --> AIOL1["01 · Complete Guide"]
    
    PY --> THR["🧵 Threading"]
    THR --> THRL1["01 · Complete Guide"]

    AG -.->|"builds on"| AM
    THR -.->|"vs"| AIO
```

## Topics Detail

| Topic | Status | Lessons | Key Concepts |
|-------|--------|---------|-------------|
| [🤖 Agentic AI](../tech/agentic-ai/README.md) | 🔴 0/5 modules | 30 videos | Reflection, Tool Use, Planning, Multi-Agent, Evals |
| [🧠 Agent Memory](../tech/agent-memory/README.md) | 🟡 7/7 ✅ | 7 | Memory Manager, Toolbox Pattern, Summarization/Compaction, Agent Loop, Harness |
| [⚡ AsyncIO](../tech/python/asyncio/README.md) | 🟡 1/1 ✅ | 1 | Event Loop, Coroutines, Tasks, gather, TaskGroup, Threads, Processes, Semaphores |
| [🧵 Threading](../tech/python/threading/README.md) | 🟡 1/1 ✅ | 1 | Manual Threads, ThreadPoolExecutor, submit vs map, I/O-bound vs CPU-bound |

---

Detailed topic views → [Agentic AI](../tech/agentic-ai/README.md) · [Agent Memory](../tech/agent-memory/README.md) · [AsyncIO](../tech/python/asyncio/README.md) · [Threading](../tech/python/threading/README.md)

# 🗺️ Tech Knowledge Graph

> Deep view with sub-topics and lesson-level detail.

```mermaid
graph TB
    T(("🔧 Tech"))
    T --> AG["🤖 Agentic AI"]
    T --> AM["🧠 Agent Memory"]
    T --> PY["🐍 Python"]
    
    AG --> M1["Module 1 · Intro ✅"]
    AG --> M2["Module 2 · Reflection ✅"]
    AG --> M3["Module 3 · Tool Use ✅"]
    AG --> M4["Module 4 · Practical Tips ✅"]
    AG --> M5["Module 5 · Autonomous Agents ✅"]

    AM --> AML["7 lessons ✅"]

    PY --> AIO["⚡ AsyncIO ✅"]
    PY --> THR["🧵 Threading ✅"]

    AG -.->|"builds on"| AM
    THR -.->|"vs"| AIO
```

## Topics Detail

| Topic | Status | Lessons | Key Concepts |
|-------|--------|---------|-------------|
| [🤖 Agentic AI](../tech/agentic-ai/README.md) | 🟡 All modules complete! | 30/30 | Task Decomposition, Evals (2×2 framework), Reflection (basic + multimodal + external feedback), Tool Use (aisuite, JSON schema, code execution, MCP), Error Analysis (traces, spreadsheets), Component Evals, LLM vs non-LLM fixes, Latency/Cost Optimization, Build↔Analyze cycle, Planning (JSON/code plans, step chaining), Multi-Agent (linear, hierarchical, deep hierarchy, all-to-all) |
| [🧠 Agent Memory](../tech/agent-memory/README.md) | 🟡 7/7 ✅ | 7 | Memory Manager, Toolbox Pattern, Summarization/Compaction, Agent Loop, Harness |
| [⚡ AsyncIO](../tech/python/asyncio/README.md) | 🟡 1/1 ✅ | 1 | Event Loop, Coroutines, Tasks, gather, TaskGroup, Threads, Processes, Semaphores |
| [🧵 Threading](../tech/python/threading/README.md) | 🟡 1/1 ✅ | 1 | Manual Threads, ThreadPoolExecutor, submit vs map, I/O-bound vs CPU-bound |

---

Detailed topic views → [Agentic AI](../tech/agentic-ai/README.md) · [Agent Memory](../tech/agent-memory/README.md) · [AsyncIO](../tech/python/asyncio/README.md) · [Threading](../tech/python/threading/README.md)

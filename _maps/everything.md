# 🗺️ Everything I Know

> God-level map of all knowledge.

```mermaid
graph TB
    ROOT(("🧠 Everything"))
    
    subgraph TECH ["🔧 Tech — 4 topics"]
        AG["🤖 Agentic AI — M1-M4 ✅ M5 🚧"]
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
| 🔴 Starting | 1 | Agentic AI (M1-M4 complete, M5 pending) |

**Total:** 4 topics · 25 lessons · 120+ flashcards · Last updated: 2026-03-31

## Key Connections

| Connection | How they relate |
|-----------|----------------|
| Agentic AI ↔ Agent Memory | Agent memory = one of the capabilities agentic systems need |
| Agentic AI → Evals & Error Analysis | #1 predictor of building agents well; M4 dedicated to this |
| Agentic AI → 4 Design Patterns | Reflection ✅, Tool Use ✅, Planning 🚧, Multi-Agent 🚧 |
| M4 Evals → M2 Evals | M2 introduced basic evals (objective + rubric). M4 goes deep: 2×2 framework, error analysis, component evals |
| Reflection → External Feedback | Code execution, web search, regex, word count = breaks performance plateau |
| Tool Use → Code Execution | THE meta-tool: LLM writes code, you execute it |
| Tool Use → MCP | M×N integrations → M+N via standard protocol |
| Code Execution → Reflection (M2) | Failed code → error → reflect → retry. Same external feedback pattern! |
| Threading ↔ AsyncIO | Both do I/O concurrency — threading uses OS threads, AsyncIO uses event loop |
| Agent Memory ↔ AsyncIO | Async for concurrent memory operations, tool execution, API calls |
| Agent Memory → RAG | Same pipeline, agent memory adds CRUD + write-back |

---

Detailed views: [Tech Map](tech.md) · [Non-Tech Map](non-tech.md) · [Weak Spots](weak-spots.md) · [Connections](connections.md) · [Timeline](learning-journey.md)

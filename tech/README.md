# 🗺️ Tech Knowledge Map

> All tech topics with confidence + progress.

```mermaid
graph TB
    T(("🔧 Tech"))
    T --> AG["🤖 <b>Agentic AI</b><br/>0/5 lessons"]
    T --> AM["🧠 <b>Agent Memory</b><br/>7/7 lessons ✅"]
    T --> PY["🐍 <b>Python</b>"]
    PY --> AIO["⚡ <b>AsyncIO</b><br/>1/1 ✅"]
    AG -.->|"builds on"| AM

    style T fill:#2196f3,color:#fff,stroke:#1565c0,stroke-width:2px
    style AG fill:#f44336,color:#fff,stroke:#c62828,stroke-width:2px
    style AM fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
    style PY fill:#2196f3,color:#fff,stroke:#1565c0
    style AIO fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
```

## 📊 Topics

| Topic | Confidence | Lessons | Flashcards | Last Updated |
|-------|-----------|---------|------------|-------------|
| [🤖 Agentic AI](agentic-ai/) | 🔴 Starting | 0/5 | — | 2026-03-24 |
| [🧠 Agent Memory](agent-memory/) | 🟡 Learning | 7/7 ✅ | 40+ | 2026-03-21 |
| [⚡ AsyncIO](python/asyncio/) | 🟡 Learning | 1/1 ✅ | 12 | 2026-03-21 |

## What's Covered

### Agentic AI (5 modules — in progress 🚧)
| # | Module | Topics |
|---|--------|--------|
| 01 | Intro to Agentic Workflows | What is it, Autonomy levels, Applications, Task Decomposition, Evals, Design Patterns |
| 02 | Reflection Design Pattern | Self-critique, Direct vs Iterative, Chart/SQL gen, External Feedback |
| 03 | Tool Use | Tools, Creating Tools, Syntax, Code Execution, MCP |
| 04 | Practical Tips | Evals, Error Analysis, Component Evals, Cost/Latency Optimization |
| 05 | Autonomous Agents | Planning, LLM Plans, Multi-Agent, Communication Patterns |

### Agent Memory (7 lessons)
| # | Topic |
|---|-------|
| 01 | Introduction — goldfish problem, evolution path |
| 02 | Why Agents Need Memory — 4 pillars, taxonomy, RAG vs Agent Memory |
| 03 | Memory Manager — agent stack, CRUD, deterministic vs agent-triggered, lifecycle |
| 04 | Semantic Tool Memory — toolbox pattern, augmentation, search-and-store |
| 05 | Memory Operations — summarization, compaction, workflow memory |
| 06 | Memory Aware Agent — agent loop, harness, full implementation |
| 07 | Conclusion — 5 building blocks of Memory Engineering |

### AsyncIO (1 lesson)
| # | Topic |
|---|-------|
| 01 | Complete Guide — event loop, coroutines, tasks, gather, TaskGroup, threads, processes, real-world example, profiling |

---

> 🌱 3 topics and growing!

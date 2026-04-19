# 🗺️ Tech Knowledge Map

> All tech topics with confidence + progress.

```mermaid
graph TB
    T(("🔧 Tech"))
    T --> AG["🤖 <b>Agentic AI</b><br/>M1-M5 ✅"]
    T --> AM["🧠 <b>Agent Memory</b><br/>7/7 lessons ✅"]
    T --> RAG["🔍 <b>RAG</b><br/>M1: 5/10 🔴"]
    T --> PY["🐍 <b>Python</b>"]
    PY --> AIO["⚡ <b>AsyncIO</b><br/>1/1 ✅"]
    PY --> THR["🧵 <b>Threading</b><br/>1/1 ✅"]
    PY --> MP["⚙️ <b>Multiprocessing</b><br/>1/1 ✅"]
    AG -.->|"builds on"| AM
    AM -.->|"retrieval"| RAG
    RAG -.->|"extends"| AG
    T --> SDD["📋 <b>Spec-Driven Dev</b><br/>1/16 🔴"]
    SDD -.->|"guides"| AG
    THR -.->|"vs"| AIO
    THR -.->|"vs"| MP
```

## 📊 Topics

| Topic | Confidence | Lessons | Flashcards | Last Updated |
|-------|-----------|---------|------------|-------------|
| [🤖 Agentic AI](agentic-ai/) | 🟡 Learning | 30/30 ✅ | 55+ | 2026-04-03 |
| [🧠 Agent Memory](agent-memory/) | 🟡 Learning | 7/7 ✅ | 40+ | 2026-03-21 |
| [🔍 RAG](rag/) | 🔴 Starting | 5/62 | 20+ | 2026-04-06 |
| [⚡ AsyncIO](python/asyncio/) | 🟡 Learning | 1/1 ✅ | 12 | 2026-03-21 |
| [🧵 Threading](python/threading/) | 🟡 Learning | 1/1 ✅ | 10 | 2026-03-24 |
| [⚙️ Multiprocessing](python/multiprocessing/) | 🟡 Learning | 1/1 ✅ | 10 | 2026-04-04 |
| [📋 Spec-Driven Dev](spec-driven-development/) | 🔴 Starting | 1/16 | 10 | 2026-04-20 |

---

> 🌱 7 topics and growing!

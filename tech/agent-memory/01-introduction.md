# 01 · Introduction 🎬


## 🎯 One Line
> Stateless agents = goldfish. Memory engineering gives them a diary that survives across sessions.

---

## ❌ The Problem → ✅ The Solution

| | Stateless Agent 🐟 | Memory-Aware Agent 🧠 |
|--|---|---|
| **Session 1** | Does great work | Does great work |
| **Session ends** | 💀 Everything gone | 💾 Memory persists |
| **Session 2** | Blank slate, starts over | Picks up where it left off |

> 💡 Stateless agent = voh friend jo har baar milne pe puchhta hai "tum karte kya ho?" 😂

---

## ⚡ The Evolution

```mermaid
graph LR
    PE["🔤 <b>Prompt Engineering</b><br/><i>How to ASK the model</i><br/>Ask good questions"]
    CE["📋 <b>Context Engineering</b><br/><i>What to SHOW the model</i><br/>Give the right textbook<br/>during the exam"]
    ME["🧠 <b>Memory Engineering</b><br/><i>What it REMEMBERS</i><br/>Actually remember stuff<br/>from last semester"]

    PE --> CE --> ME

    style PE fill:#2196f3,color:#fff,stroke:#1565c0,stroke-width:2px
    style CE fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:2px
    style ME fill:#4caf50,color:#fff,stroke:#388e3c,stroke-width:3px
```

**Key insight:** Memory is **infrastructure**, not a feature. External to the model, persistent, structured, queryable.

---

## 🗺️ Course Roadmap

| # | Lesson | Type | What you build |
|---|--------|------|----------------|
| 2 | Why Agents Need Memory | 📖 | Failure modes + memory-first architecture |
| 3 | Memory Manager | 💻 | Core store/retrieve system |
| 4 | Semantic Tool Memory | 💻 | Scale tool selection via search |
| 5 | Memory Operations | 💻 | Extraction + consolidation + self-update |
| 6 | Memory-Aware Agent | 💻 | Full stateful agent, end-to-end |

**Stack:** Oracle AI Database · LangChain · LLM pipelines

---

## 🧪 Quick Check

<details>
<summary>❓ Why do current agents struggle with long-horizon tasks?</summary>

They're stateless — session ends, context lost. Goldfish with amnesia. 🐟
</details>

<details>
<summary>❓ Context Engineering vs Memory Engineering?</summary>

**Context** = what's on the cheat sheet for THIS exam.
**Memory** = what you actually learned and remember across semesters. 📝→🧠
</details>

---

> **Next →** [Why AI Agents Need Memory](02-why-agents-need-memory.md)

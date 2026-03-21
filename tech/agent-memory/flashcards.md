# 🃏 Agent Memory Flashcards

> From: `agent-memory/` + related: _(first topic — cross-pulls coming soon)_
> Last updated: 2026-03-21

---

### 📌 Core Concepts

<details>
<summary>❓ Why do agents fail at long-horizon tasks?</summary>

**Stateless** — context lives in one session only. Session ends → 💀 everything gone.

> 🐟 Goldfish memory — great in the moment, total amnesia after!
</details>

<details>
<summary>❓ What is Memory Engineering?</summary>

Long-term memory as **first-class infrastructure** — external to the model, persistent, structured.

Not "save chat history" — it's extraction, consolidation, contradiction handling, write-back loops.
</details>

<details>
<summary>❓ Prompt Eng vs Context Eng vs Memory Eng?</summary>

| Level | What | Analogy |
|-------|------|---------|
| **Prompt** | How to *ask* | Asking good questions |
| **Context** | What to *show* (RAG, tools) | Cheat sheet during exam |
| **Memory** | What it *remembers* across sessions | Actually learned last semester |

Each level ↑ adds more persistence.
</details>

<details>
<summary>❓ 4 pillars of a memory-aware agent?</summary>

| # | Component | Job |
|---|-----------|-----|
| 1 | **Memory Manager** | Core store & retrieve |
| 2 | **Extraction Pipelines** | Pull key info from convos |
| 3 | **Contradiction Handling** | Resolve conflicts, keep fresh |
| 4 | **Semantic Tool Memory** | Scale tool selection via search |

All four combined → fully stateful agent 🤖
</details>

<details>
<summary>❓ Tech stack used?</summary>

| Tool | Role |
|------|------|
| **Oracle AI DB** | Vector + relational storage |
| **LangChain** | Agent orchestration |
| **LLM pipelines** | Extraction, consolidation, reasoning |
</details>

---

> 💡 *Bolke batao — padhke nahi, bolke yaad hota hai!* 🗣️

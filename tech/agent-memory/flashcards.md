# 🃏 Agent Memory Flashcards

> From: agent-memory/ + related: _(first topic — cross-pulls coming soon)_
> Last updated: 2026-03-21

---

### 📌 Core Agent Memory

<details>
<summary>❓ Why do current AI agents fail at long-horizon tasks?</summary>

They're **stateless** — everything lives in a single session's context window. When the session ends, all context is lost. Next session = blank slate.

🐟 Goldfish memory — great in the moment, forgets everything after!
</details>

<details>
<summary>❓ What is Memory Engineering?</summary>

Treating long-term memory as **first-class infrastructure** — external to the model, persistent across sessions, and structured.

Not just "save chat history." It's building a proper memory system: extraction, consolidation, contradiction handling, write-back loops.
</details>

<details>
<summary>❓ What's the evolution: Prompt Eng → Context Eng → Memory Eng?</summary>

| Level | Focus | Analogy |
|-------|-------|---------|
| Prompt Eng | How to ASK the model | Teaching someone to ask good questions |
| Context Eng | What to SHOW the model (RAG, tools) | Giving them a cheat sheet during the exam |
| Memory Eng | What the model REMEMBERS across sessions | Making sure they actually learned last semester's material |

Each level adds more persistence and structure.
</details>

<details>
<summary>❓ What 4 components make up a memory-aware agent (from this course)?</summary>

1. **Memory Manager** — core storage & retrieval system
2. **Extraction Pipelines** — pull important info from conversations
3. **Contradiction Handling + Self-Updating Memory** — resolve conflicts, keep memory fresh
4. **Semantic Tool Memory** — scale tool selection using memory

All combined = fully stateful memory-aware agent 🤖
</details>

<details>
<summary>❓ What tech stack does this course use?</summary>

| Tool | Role |
|------|------|
| Oracle AI Database | Persistent memory storage (vector + relational) |
| LangChain | Agent framework / orchestration |
| LLM-powered pipelines | Memory extraction, consolidation, reasoning |
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

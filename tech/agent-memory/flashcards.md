# 🃏 Agent Memory Flashcards

> From: `agent-memory/` + related: _(first topic — cross-pulls coming soon)_
> Last updated: 2026-03-21

---

### 📌 Core Concepts (Lesson 1)

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

---

### 🤔 Why Agents Need Memory (Lesson 2)

<details>
<summary>❓ What are the 4 pillars of an AI agent?</summary>

| Pillar | Role |
|--------|------|
| 👁️ **Perception** | Inputs (text, images, sensors) |
| 🧠 **Reasoning** | LLM thinks & plans |
| 🔧 **Action** | Tools (APIs, code) |
| 💾 **Memory** | Store, retrieve, apply |

Agent = autonomous + goal-bound + minimal human feedback.
</details>

<details>
<summary>❓ Stateless agent ka sabse bada problem kya hai? (Restaurant example)</summary>

User asks for recs (turn 1-2), then says "book the first one" (turn 3) → stateless agent: **"Which one??"** 🐟

Memory-augmented agent stores turns 1-2 in external DB → "first one" makes sense in turn 3. ✅
</details>

<details>
<summary>❓ Name the 5 types in the Memory Taxonomy</summary>

**Short-term:** Semantic Cache (cached responses) · Working Memory (context window + scratchpad)

**Long-term:** Procedural (workflows, toolbox) · Semantic (entities, knowledge base) · Episodic (persona, summaries, conversations)

> Short-term = RAM, Long-term = Hard Disk 💾
</details>

<details>
<summary>❓ How does Agent Memory differ from RAG?</summary>

Same pipeline (chunk → embed → DB → retrieve → rerank → LLM), BUT:
- RAG = **read-only** from static knowledge base
- Agent Memory = **read + write (CRUD)** to live tables
- Memory Manager abstracts CRUD operations
- Agent accesses Memory Manager through tools
</details>

<details>
<summary>❓ Why is the DATABASE the core of agent memory (not the LLM)?</summary>

- LLM = parametric memory, **frozen** after training, can't update
- Embedding model = important but just converts text → vectors
- **Database = ALL the data traffic** — storage, retrieval, optimization, scaling

> LLM soochta hai, DB yaad rakhta hai. Primary infrastructure = the DB! 🗄️
</details>

<details>
<summary>❓ Why isn't conversational memory enough?</summary>

4 gaps:
1. 📏 Context windows are finite, relationships aren't
2. 👤 Entities (people, places) aren't explicitly captured
3. 📦 Non-chat info (workflows, outcomes) is missed
4. 🔍 Not structured or queryable — just raw chat logs

> Sirf diary se kaam nahi chalta — contacts, to-do, KB bhi chahiye!
</details>

---

> 💡 *Bolke batao — padhke nahi, bolke yaad hota hai!* 🗣️

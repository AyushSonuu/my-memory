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
| 👁️ **Perception** | Inputs (text, audio, vision, structured data) |
| 🔧 **Action** | Tools (functions, REST APIs, scripts, skills, MCPs) |
| 🧠 **Reasoning** | LLM — thinks, plans, decides |
| 💾 **Memory** | Store, retrieve, apply knowledge across interactions |

Agent = autonomous + goal & objective bound + little to no human feedback.
</details>

<details>
<summary>❓ Stateless agent ka sabse bada problem kya hai? (Restaurant example)</summary>

Turn 1: user asks for recs → Turn 2: agent responds → Turn 3: user says "book the first one" → Turn 4: stateless agent **"I have no recollection, please specify"** 🐟

Memory-augmented agent stores turns 1-2 in external DB → resolves "first one" at turn 4. ✅
</details>

<details>
<summary>❓ Name the 5 types in the Memory Taxonomy</summary>

**Short-term:** Semantic Cache (vector search + cached LLM responses) · Working Memory (LLM context window + session based)

**Long-term:** Procedural (workflow + toolbox) · Semantic (entity memory + knowledge base) · Episodic (persona, summaries, conversational memory)

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

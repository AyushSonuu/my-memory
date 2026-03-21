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

### 🏗️ Constructing The Memory Manager (Lesson 3)

<details>
<summary>❓ What is the Agent Stack?</summary>

A **layered composition of tools and technologies** forming a system architecture for AI agents.

For this course, compressed to 3 layers: **Application** (UI) → **Memory** (Memory Core + Memory Manager) → **Infrastructure** (DB, compute).

The Data Layer becomes the **Memory Layer** when thinking from an agentic perspective.
</details>

<details>
<summary>❓ Memory Core vs Memory Manager — kya farak hai?</summary>

| | Memory Core | Memory Manager |
|--|---|---|
| **What** | Actual DB tables & vector stores | Control logic & CRUD methods |
| **Analogy** | Almaari (cupboard) 🗄️ | The person who organizes & retrieves from it |
| **Job** | Store data | Decide WHAT becomes memory, HOW it's structured, WHEN it's recalled |

Together they create memory-augmented agents.
</details>

<details>
<summary>❓ Why do conversational memories use SQL tables while KB uses vector stores?</summary>

**Conversational** → exact match by `thread_id` + chronological `timestamp` ordering. No semantic search needed → **SQL is faster and simpler**.

**Knowledge Base** → needs to find content *similar in meaning* to a query → requires **vector embeddings + cosine similarity search** → **Vector Store**.

> Different problems, different tools! 🔧
</details>

<details>
<summary>❓ Deterministic vs Agent-Triggered memory operations?</summary>

**Deterministic** = runs ALWAYS (alarm clock ⏰). Auto-save conversations, auto-load context every turn. Reliable, predictable, no gaps.

**Agent-Triggered** = agent DECIDES when (judgment call 🤔). Summarize, extract entities, deep retrieval. Higher signal, less noise.

Chicken-and-egg problem: agent can't decide to check memory it doesn't know exists → that's why deterministic retrieval at start of every turn!
</details>

<details>
<summary>❓ Define: Memory Unit</summary>

**Smallest atomic piece** of stored information with minimal attributes for capture, retrieval, and update.

Examples:
- **Conversational Unit** → `{content, role, timestamp}`
- **Workflow Unit** → `{content (CLOB), type (VARCHAR2), timestamp, vector (float[])}`
</details>

<details>
<summary>❓ Context Engineering vs Memory Engineering?</summary>

| | Context Engineering | Memory Engineering |
|--|---|---|
| **Goal** | Optimize what goes INTO context window | Design & maintain memory SYSTEMS |
| **Focus** | Signal-to-noise per token | Full lifecycle (store → retrieve → learn) |
| **Scope** | One LLM call | Entire agent lifespan |
| **Analogy** | Choose which cheat sheets for THIS exam | Build the entire library system |

Memory Eng = intersection of DB Eng + Agent Eng + ML Eng + Info Retrieval.
</details>

<details>
<summary>❓ What are the steps in the Memory Lifecycle?</summary>

1. **Ingest** (collect from sources)
2. **Enrich** (embeddings + metadata)
3. **Store** (short/medium/long-term)
4. **Organize** (indexing, relationship mapping)
5. **Retrieve** (text/vector/graph/hybrid)
6. → **LLM** processes it
7. **Serialize & Augment** output → back to Store → loop!

Key: LLM output feeds BACK as new memory → **continuous learning cycle** 🔄
</details>

<details>
<summary>❓ 4 steps: Memory Augmented → Memory Aware Agent</summary>

1. **System prompt awareness** — agent knows its memory stores exist
2. **Agent-triggered memory ops** — CRUD operations given as tools
3. **Memory lifecycle reasoning** — agent reasons THROUGH the lifecycle
4. **Context window segmentation** — partitions allocated per memory type

> Augmented = HAS memory. Aware = KNOWS it has memory + controls it! 🧠
</details>

<details>
<summary>❓ What tech was used in the L3 code lab?</summary>

| Component | Tool |
|-----------|------|
| Database | **Oracle AI Database 26ai** |
| Embedding | `sentence-transformers/paraphrase-mpnet-base-v2` (HuggingFace) |
| Vector Store | **OracleVS** (LangChain integration) |
| Distance | **COSINE** strategy |
| Index type | **IVF** (Inverted File) — 95% target accuracy |
| Abstraction | `StoreManager` (creates stores) + `MemoryManager` (unified CRUD) |
</details>

---

> 💡 *Bolke batao — padhke nahi, bolke yaad hota hai!* 🗣️

# 🧠 Agent Memory — Building Memory-Aware Agents

> Stateless agents = goldfish 🐟. Memory engineering = giving them a diary that actually sticks.

---

## 🧠 Brain — How This Connects

```mermaid
graph LR
    AM(("🧠 Agent Memory"))
    AM -->|"uses"| LLM["LLMs / Foundation Models"]
    AM -->|"powered by"| VDB["Vector Databases"]
    AM -->|"built with"| LC["LangChain"]
    AM -->|"stores in"| ODB["Oracle AI Database"]
    AM -->|"enables"| SA["Stateful Agents"]
    AM -.->|"evolution of"| PE["Prompt Engineering"]
    AM -.->|"evolution of"| CE["Context Engineering"]
    
    style AM fill:#ff9800,color:#fff,stroke:#e65100,stroke-width:3px
    style SA fill:#4caf50,color:#fff,stroke:#388e3c
    style PE fill:#90a4ae,color:#fff
    style CE fill:#90a4ae,color:#fff
    style LLM fill:#42a5f5,color:#fff
    style VDB fill:#42a5f5,color:#fff
    style LC fill:#42a5f5,color:#fff
    style ODB fill:#42a5f5,color:#fff
```

## 📊 Progress — 7/7 ✅ Complete!

| # | Lesson | Status |
|---|--------|--------|
| 01 | [Introduction](01-introduction.md) | ✅ Done |
| 02 | [Why Agents Need Memory](02-why-agents-need-memory.md) | ✅ Done |
| 03 | [Memory Manager](03-memory-manager.md) | ✅ Done |
| 04 | [Semantic Tool Memory](04-semantic-tool-memory.md) | ✅ Done |
| 05 | [Memory Operations](05-memory-operations.md) | ✅ Done |
| 06 | [Memory Aware Agent](06-memory-aware-agent.md) | ✅ Done |
| 07 | [Conclusion](07-conclusion.md) | ✅ Done |

**Overall confidence:** 🟡 Learning (just completed — first revision due 2026-03-24)

## 🧩 Memory Fragments
> Random "aha!" moments picked up along the way:
> 
> - 💡 **Evolution path:** Prompt Eng → Context Eng → Memory Eng. Each layer adds persistence.
> - 🐟 Stateless agents do great in one convo, then forget *everything*. Memory engineering fixes this.
> - 🏗️ Memory = **infrastructure**, not a feature — external to the model, persistent, structured.
> - 🤖 **4 pillars of an agent:** Perception · Reasoning · Action · Memory — remove any one and it's not a real agent.
> - 🗄️ **Database is the core** of agent memory — not the LLM (frozen), not the embedding model. DB sees all the data traffic.
> - 🔗 **Agent Memory = RAG + CRUD.** Same pipeline, but the agent can WRITE back, not just read.
> - 📖 Conversational memory alone = just a diary. You also need contacts, to-do lists, and a knowledge base.
> - 🏗️ **Memory Manager = abstraction on DB.** CRUD methods per memory type. SQL for exact-match, Vector for semantic search.
> - ⏰ **Deterministic ops = alarm clock** (always run). Agent-triggered = judgment call. Both are needed!
> - 🐔 **Chicken-and-egg problem:** Agent can't decide to check memory it doesn't know exists → deterministic retrieval at start.
> - 🔄 **Memory Lifecycle is a continuous loop** — LLM output feeds BACK as new memory. The agent literally learns!
> - 🧠 **Aware > Augmented:** Augmented = HAS memory. Aware = KNOWS it has memory + controls it via tools + reasons through lifecycle.
> - 🔧 **Toolbox Pattern:** Don't stuff 100 tools into context → store in vector DB, retrieve top-K via semantic search at runtime.
> - ✨ **Memory Unit Augmentation:** LLM enhances tool descriptions → better separability in embedding space → higher recall.
> - 🔄 **Search-and-store:** Tool results get persisted to KB memory — agent literally learns from searching.
> - 📉 **Context Window Reduction** has 2 techniques: Summarization (lossy) and Compaction (lossless via DB offload).
> - 🗄️ **Compaction > Summarization** when you might need details later — full content in DB, expand anytime.
> - ⚙️ **Workflow Memory** = reusable step-by-step playbooks. Do it once, follow the recipe forever.
> - 🔄 **Agent Loop** = cyclical: Assemble Context → Invoke LLM → Act. Repeats until stop condition.
> - 🏗️ **Agent Harness** = full scaffolding (before + during + after loop). Memory ops outside = deterministic. Inside = dynamic.
> - 📋 **Markdown headings** partition the context window per memory type — LLMs understand hierarchical structure from training.
> - 🧠 **System prompt** is what makes LLM memory-aware: tells it what memory exists, how context is partitioned, how to use each type.

---

## 🎬 Teach Mode — Lesson Flow

> Open in order = teach anyone Agent Memory

| # | Lesson | What You'll Get |
|---|--------|-----------------|
| 01 | [Introduction](01-introduction.md) | Why memory matters — the goldfish problem |
| 02 | [Why Agents Need Memory](02-why-agents-need-memory.md) | 4 pillars, memory taxonomy, RAG → Agent Memory |
| 03 | [Memory Manager](03-memory-manager.md) | Agent stack, CRUD per memory type, lifecycle, deterministic vs agent-triggered |
| 04 | [Semantic Tool Memory](04-semantic-tool-memory.md) | Toolbox pattern, augmentation, search-and-store |
| 05 | [Memory Operations](05-memory-operations.md) | Summarization, compaction, workflow memory, context monitor |
| 06 | [Memory Aware Agent](06-memory-aware-agent.md) | Agent loop, harness, full implementation + live demo |
| 07 | [Conclusion](07-conclusion.md) | 5 building blocks of Memory Engineering |

**Supporting:** [Flashcards](flashcards.md) — 40+ revision cards | [Cheatsheet](cheatsheet.md) — one-pager | [RAG vs Agent Memory](vs.md) — comparison

---

## 📚 Source
> 🎓 [Agent Memory: Building Memory-Aware Agents](https://www.deeplearning.ai/) — DeepLearning.AI × Oracle
> 🔗 [Oracle AI Developer Hub](https://github.com/oracle-devrel/oracle-ai-developer-hub) — extra resource

## 🔗 Connected Topics
> - **RAG** — same pipeline (chunk → embed → retrieve), but Agent Memory adds CRUD + write-back
> - **Vector Databases** — OracleVS, COSINE distance, IVF indexes power all semantic search
> - **LangChain** — orchestration framework, OracleVS integration, ArxivRetriever, text splitters
> - **LLMs** — reasoning engine + extraction + summarization + augmentation
> - **System Design** — memory as infrastructure, layered agent stack, context window management

## 30-Second Recall 🧠
> AI agents are **stateless goldfish** — brilliant per turn, blank slate next session. Memory engineering treats memory as **infrastructure**: external, persistent, structured. You build it in layers: **Memory Manager** (CRUD for 7 memory types) → **Toolbox Pattern** (semantic tool retrieval at scale) → **Context Engineering** (summarization + compaction) → **Agent Loop** (assemble → invoke → act cycle) → all wired into a **Memory Aware Agent** that loads prior context at startup, uses tools mid-execution, and persists everything for next time. The 5 building blocks: Memory Modeling, Semantic Retrieval, Extraction, Consolidation, Write-Back.

# 🃏 Agentic AI Flashcards

> From: agentic-ai/ + related: agent-memory/
> Last updated: 2026-03-25

---

### 📌 Core Agentic AI

<details>
<summary>❓ What makes AI "agentic"?</summary>

It doesn't just respond — it **acts**: plans, executes, reflects, iterates. Multi-step workflows with autonomy, not one-shot generation.
</details>

<details>
<summary>❓ Name the 4 agentic design patterns.</summary>

1. **Reflection** — self-critique loops
2. **Tool Use** — APIs, databases, code execution
3. **Planning** — break tasks into steps
4. **Multi-Agent** — specialized agents collaborating
</details>

<details>
<summary>❓ What's the key skill that determines your ability to build agents?</summary>

**Task Decomposition** — looking at complex tasks and breaking them into discrete steps where each step is implementable by an LLM or a tool. You keep asking: *"Can an LLM or tool do this step?"* If not, decompose further.
</details>

<details>
<summary>❓ What are the 6 building blocks for agentic workflows?</summary>

LLMs · Multimodal Models · Specialized AI Models · APIs/Tools · Retrieval (DB + RAG) · Code Execution
</details>

<details>
<summary>❓ What's the #1 differentiator between good and great agent builders?</summary>

**Disciplined dev process** — evals + error analysis. Not just building, but systematically measuring and improving. Build first → examine outputs → discover issues → create eval → fix → repeat.
</details>

<details>
<summary>❓ Rank the 4 design patterns from most to least developer control.</summary>

1. 🪞 Reflection (highest — you control the loop)
2. 🔧 Tool Use (you define the tools menu)
3. 📋 Planning (LLM picks the steps — experimental)
4. 👥 Multi-Agent (agents interact freely — hardest to control)
</details>

---

### 🪞 Module 2 — Reflection

_Coming after Module 2 notes._

---

### 🔧 Module 3 — Tool Use

_Coming after Module 3 notes._

---

### 🛠️ Module 4 — Practical Tips

_Coming after Module 4 notes._

---

### 🧠 Module 5 — Planning & Multi-Agent

_Coming after Module 5 notes._

---

### 🔗 From: Agent Memory

<details>
<summary>❓ How does Agent Memory connect to Agentic AI?</summary>

Agent Memory = the persistence layer. Without it, agents are goldfish. The 5 blocks (Modeling, Retrieval, Extraction, Consolidation, Write-Back) power the "remember and learn" capability that multi-step agentic workflows need.
</details>

<details>
<summary>❓ Memory vs Context Window — what's the difference?</summary>

**Context window** = exam ka cheat sheet (temporary, fits limited info).  
**Memory** = jo actually yaad hai (persistent, retrieved when needed via semantic search).  
Agents need both — context window for current task, memory for long-term knowledge.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

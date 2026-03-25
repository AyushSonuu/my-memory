# 🃏 Module 1 — Intro to Agentic Workflows Flashcards

> From: module-1-intro/ + related: agent-memory/
> Last updated: 2026-03-25

---

### 📌 Core Concepts

<details>
<summary>❓ What is "agentic AI" in one line?</summary>

AI systems that don't just respond — they **act**: plan, execute, reflect, and iterate over multi-step workflows with varying degrees of autonomy.
</details>

<details>
<summary>❓ What's the difference between non-agentic and agentic AI?</summary>

**Non-agentic** = one-shot generation (write essay with no backspace).  
**Agentic** = multi-step iterative workflow (outline → research → draft → revise). Like how a human actually works.
</details>

<details>
<summary>❓ Name the 4 agentic design patterns.</summary>

1. **Reflection** — self-critique loops
2. **Tool Use** — connect to APIs, databases, code execution
3. **Planning** — break tasks into steps
4. **Multi-Agent** — specialized agents collaborating
</details>

<details>
<summary>❓ What are the 3 factors that make an agentic task harder?</summary>

1. **Steps not known ahead of time** (must plan dynamically)
2. **No standard procedures** (solve as you go)
3. **Multimodal input** (vision, audio, not just text)
</details>

<details>
<summary>❓ What are the 5 degrees of autonomy?</summary>

Fully manual → Assistive → Semi-autonomous → Supervised autonomous → Fully autonomous.  
Most production systems today are **semi-autonomous** (human-in-the-loop).
</details>

---

### ✂️ Task Decomposition (Lesson 06)

<details>
<summary>❓ What's the ONE question to ask for every step in task decomposition?</summary>

**"Can this step be done by an LLM, a short piece of code, a function call, or a tool?"**

If yes → wire it in. If no → ask how a human would do it → decompose further.
</details>

<details>
<summary>❓ In the research agent example, why did V2 (3 steps) fail?</summary>

The essay was **disjointed** — the beginning, middle, and end didn't feel consistent. The "write essay" step was too big. Fix: decompose into **draft → critique → revise** (3 sub-steps instead of 1).
</details>

<details>
<summary>❓ What are the 6 building blocks for agentic workflows?</summary>

| Block | Purpose |
|-------|---------|
| 🧠 LLMs | Text gen, extraction, decisions |
| 🧠 Multimodal Models | Process images, audio, video |
| 🤖 Specialized AI Models | PDF→text, TTS, image analysis |
| 🔧 APIs / Tools | Web search, email, calendar |
| 🗄️ Retrieval | Database queries, RAG |
| 💻 Code Execution | LLM writes & runs code |
</details>

<details>
<summary>❓ Is task decomposition a one-time activity?</summary>

**No!** It's an iterative loop: build → test → find weak step → decompose further → test again. You rarely get it right the first time. Andrew Ng himself iterates multiple times.
</details>

<details>
<summary>❓ How did the research agent decomposition evolve?</summary>

- **V1** (1 step): Direct generation → shallow output
- **V2** (3 steps): Outline → search → write → better but disjointed  
- **V3** (5 steps): Outline → search → draft → critique → revise → deeper & coherent

Each version **further decomposes** the weakest step.
</details>

---

### 🔗 From: Agent Memory

<details>
<summary>❓ How does Agent Memory relate to Agentic AI?</summary>

Agent Memory provides the **persistence layer** for agentic workflows. Without it, agents are goldfish — they forget everything between calls. Memory enables multi-session context, learning from past interactions, and personalization. The 5 building blocks (Modeling, Retrieval, Extraction, Consolidation, Write-Back) power the "remember and learn" part of agents.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

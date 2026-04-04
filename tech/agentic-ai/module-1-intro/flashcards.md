# 🃏 Module 1 — Intro to Agentic Workflows Flashcards

> From: module-1-intro/ + related: agent-memory/
> Last updated: 2026-03-25

---

### 📌 Core Concepts

<details markdown="1">
<summary>❓ What is "agentic AI" in one line?</summary>

AI systems that don't just respond — they **act**: plan, execute, reflect, and iterate over multi-step workflows with varying degrees of autonomy.
</details>

<details markdown="1">
<summary>❓ What's the difference between non-agentic and agentic AI?</summary>

**Non-agentic** = one-shot generation (write essay with no backspace).  
**Agentic** = multi-step iterative workflow (outline → research → draft → revise). Like how a human actually works.
</details>

<details markdown="1">
<summary>❓ Name the 4 agentic design patterns.</summary>

1. **Reflection** — self-critique loops
2. **Tool Use** — connect to APIs, databases, code execution
3. **Planning** — break tasks into steps
4. **Multi-Agent** — specialized agents collaborating
</details>

<details markdown="1">
<summary>❓ What are the 3 factors that make an agentic task harder?</summary>

1. **Steps not known ahead of time** (must plan dynamically)
2. **No standard procedures** (solve as you go)
3. **Multimodal input** (vision, audio, not just text)
</details>

<details markdown="1">
<summary>❓ What are the 5 degrees of autonomy?</summary>

Fully manual → Assistive → Semi-autonomous → Supervised autonomous → Fully autonomous.  
Most production systems today are **semi-autonomous** (human-in-the-loop).
</details>

---

### ✂️ Task Decomposition (Lesson 06)

<details markdown="1">
<summary>❓ What's the ONE question to ask for every step in task decomposition?</summary>

**"Can this step be done by an LLM, a short piece of code, a function call, or a tool?"**

If yes → wire it in. If no → ask how a human would do it → decompose further.
</details>

<details markdown="1">
<summary>❓ In the research agent example, why did V2 (3 steps) fail?</summary>

The essay was **disjointed** — the beginning, middle, and end didn't feel consistent. The "write essay" step was too big. Fix: decompose into **draft → critique → revise** (3 sub-steps instead of 1).
</details>

<details markdown="1">
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

<details markdown="1">
<summary>❓ Is task decomposition a one-time activity?</summary>

**No!** It's an iterative loop: build → test → find weak step → decompose further → test again. You rarely get it right the first time. Andrew Ng himself iterates multiple times.
</details>

<details markdown="1">
<summary>❓ How did the research agent decomposition evolve?</summary>

- **V1** (1 step): Direct generation → shallow output
- **V2** (3 steps): Outline → search → write → better but disjointed  
- **V3** (5 steps): Outline → search → draft → critique → revise → deeper & coherent

Each version **further decomposes** the weakest step.
</details>

---

### 📏 Evals (Lesson 07)

<details markdown="1">
<summary>❓ Why shouldn't you try to build all evals before building the workflow?</summary>

Because problems are **very hard to predict** in advance. Build first → run on real inputs → examine outputs → discover issues → then create targeted evals. You'll always find unexpected failures (like competitor mentions) that you couldn't have anticipated.
</details>

<details markdown="1">
<summary>❓ What are the two types of eval metrics?</summary>

| Type | When | How |
|------|------|-----|
| **📐 Objective (code-based)** | Clear right/wrong | Write code to check (e.g., does output contain competitor name?) |
| **🧑‍⚖️ Subjective (LLM-as-Judge)** | Fuzzy quality | Prompt another LLM to score the output |

⚠️ LLMs aren't great at 1-5 scale ratings — it's a rough starting point only.
</details>

<details markdown="1">
<summary>❓ End-to-end vs component-level evals — what's the difference?</summary>

**End-to-end** = measures final output quality → tells you IF something is wrong.  
**Component-level** = measures each step's output → tells you WHERE it's wrong.  
You need both.
</details>

<details markdown="1">
<summary>❓ What is error analysis?</summary>

Manually reading through the **intermediate outputs (traces)** of each step to find where the agent falls short. Like reading the agent's diary page by page to spot the weak link. Automated evals can't fully replace this detective work.
</details>

---

### 🎨 Design Patterns (Lesson 08)

<details markdown="1">
<summary>❓ Name the 4 design patterns in order of decreasing developer control.</summary>

1. 🪞 **Reflection** (highest control) — LLM critiques its own output, developer controls the loop
2. 🔧 **Tool Use** — LLM calls functions from a developer-defined menu
3. 📋 **Planning** — LLM decides the steps at runtime (experimental)
4. 👥 **Multi-Agent** (lowest control) — multiple specialized LLM agents collaborate freely
</details>

<details markdown="1">
<summary>❓ What's the difference between self-reflection and a critique agent?</summary>

**Self-reflection** = same LLM critiques its own output (one model, two prompts).  
**Critique agent** = separate LLM prompted as "your role is to critique" — a preview of multi-agent!
</details>

<details markdown="1">
<summary>❓ How is the Planning pattern different from Task Decomposition?</summary>

**Task Decomposition** = developer hardcodes the steps.  
**Planning** = LLM decides the steps at runtime. More flexible but harder to control.
</details>

<details markdown="1">
<summary>❓ What is ChatDev and which pattern does it demonstrate?</summary>

**ChatDev** = a framework where multiple AI agents (CEO, Programmer, Tester, Designer) collaborate as a virtual software company. It's the **Multi-Agent** pattern in action. Created by Chen Qian et al.
</details>

<details markdown="1">
<summary>❓ Do design patterns work in isolation?</summary>

**No!** Real workflows often combine 2-3 patterns. Example: code generation uses Reflection (critique loop) + Tool Use (running code for error messages). They're building blocks you mix and match.
</details>

---

### 🔗 From: Agent Memory

<details markdown="1">
<summary>❓ How does Agent Memory relate to Agentic AI?</summary>

Agent Memory provides the **persistence layer** for agentic workflows. Without it, agents are goldfish — they forget everything between calls. Memory enables multi-session context, learning from past interactions, and personalization. The 5 building blocks (Modeling, Retrieval, Extraction, Consolidation, Write-Back) power the "remember and learn" part of agents.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

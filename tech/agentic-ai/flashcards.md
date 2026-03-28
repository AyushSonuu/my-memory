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

<details>
<summary>❓ What's the simplest way to implement the reflection pattern?</summary>

Two prompts, one loop: (1) Prompt LLM to generate v1, (2) Pass v1 back with a "critique and improve" prompt → get v2. **Surprisingly easy to implement** — Andrew Ng says so himself!
</details>

<details>
<summary>❓ Why use a DIFFERENT LLM for the critique step?</summary>

Different models have different strengths. **Reasoning models** (thinking models) are especially good at finding bugs. So: fast model for draft, reasoning model for critique. Jaise ek banda fast likhta hai, doosra carefully check karta hai! 🧐
</details>

<details>
<summary>❓ What makes reflection MUCH more powerful?</summary>

**External feedback** — new information from outside the LLM. Example: actually running the code and feeding error messages back. Without it, the LLM is guessing what *might* be wrong. With it, the LLM *knows* what went wrong.

Bina feedback = andhera mein teer 🏹. With feedback = spotlight ON 🔦
</details>

<details>
<summary>❓ Is reflection only useful for code generation?</summary>

No! Works for **any** output — emails, essays, charts, SQL, domain names. The pattern is universal: generate → critique → improve.
</details>

<details>
<summary>❓ Does reflection guarantee 100% correct output?</summary>

**No.** Andrew Ng is explicit: "Reflection is not magic." It gives a **modest performance bump** — not perfection. But for how easy it is to implement, the ROI is excellent.
</details>

<details>
<summary>❓ What is zero-shot vs one-shot vs few-shot prompting?</summary>

Number of **examples** in the prompt:
- **Zero-shot** = 0 examples (just instruction) — this is "direct generation"
- **One-shot** = 1 input→output example
- **Few-shot** = 2+ examples

More examples → LLM better understands your expected format.
</details>

<details>
<summary>❓ What research paper proved reflection outperforms direct generation?</summary>

**"Self-Refine"** by Madaan et al. (2023). Tested across 7 tasks (sentiment, code, math, etc.) — reflection won on ALL of them across multiple models (GPT-3.5, GPT-4).
</details>

<details>
<summary>❓ What are the two golden rules for writing reflection prompts?</summary>

1. **Clearly indicate the reflection action** — "Review...", "Check...", "Critique..."
2. **Specify criteria to check** — don't just say "improve it", say WHAT to look for (tone, facts, pronunciation, etc.)

Jitna specific criteria, utna focused feedback! 🎯
</details>

<details>
<summary>❓ What's special about chart generation reflection (multimodal reflection)?</summary>

The critic LLM doesn't just read code — it **looks at the generated chart image**. This catches visual issues (bad chart type, cramped labels, poor colors) that code review alone would miss. Code padh ke bugs milte hain, chart DEKH ke UX problems milte hain! 👁️
</details>

<details>
<summary>❓ Why might you use different LLMs for generation vs reflection?</summary>

Different models, different strengths. Fast general model (GPT-4o) for quick drafts. **Reasoning model** for thorough critique. Toggle combinations to find the best pairing for your task.
</details>

<details>
<summary>❓ What are the two types of evals for reflection workflows?</summary>

1. **Objective evals** — right answer exists → code compares output vs ground truth (e.g., SQL query returned 1,201? ✅/❌)
2. **Subjective evals** — quality is fuzzy → LLM-as-Judge with a binary rubric (e.g., chart has clear title? 0/1)

Objective = easier. Subjective = needs rubric tuning.
</details>

<details>
<summary>❓ Why is "which image is better?" (LLM pair comparison) unreliable?</summary>

Three issues: (1) answers don't match human judgment, (2) prompt-sensitive — rewording flips the "winner", (3) **position bias** — most LLMs always pick the first option. Jaise exam mein pehla option dekhke "yeh sahi hai" bol dena! 🍕
</details>

<details>
<summary>❓ Why use binary (0/1) rubric criteria instead of a 1-5 rating scale?</summary>

LLMs are poorly calibrated on scales — "3 vs 4" is vague. Binary is clear: title present? yes/no. Sum 5 binary scores → same 0-5 range, **way more consistent**. Decomposed scoring also shows WHERE it lost points.
</details>

<details>
<summary>❓ Once you build evals for reflection, what's the real unlock?</summary>

**Prompt engineering becomes data-driven.** Tweak the reflection/generation prompt → re-run eval → see if % correct goes up. No more vibes-based "this feels better." Numbers decide! 📈
</details>

<details>
<summary>❓ Why is reflection with external feedback more powerful than basic reflection?</summary>

Basic reflection = LLM re-examines the **same info** it already had. External feedback gives it **genuinely new facts** (error messages, web search, word counts, pattern matches). Apni copy khud check karna vs answer key mil jaana! 🔑
</details>

<details>
<summary>❓ Name three external feedback tools that boost reflection.</summary>

1. **Code execution** — run code, feed back errors/output
2. **Web search** — fact-check claims against real sources
3. **Pattern matching** (regex) — detect competitor names, banned words, etc.

Bonus: **Word count** — LLMs can't count words, but `len(text.split())` can!
</details>

<details>
<summary>❓ What are the 3 performance tiers, from worst to best?</summary>

1. ★ **Direct generation** — improves, then plateaus
2. ● **With reflection** — bumps above the plateau
3. ✦ **Reflection + external feedback** — highest trajectory, keeps climbing

If you're stuck at a plateau, don't grind — escalate to the next tier!
</details>

---

### 🔧 Module 3 — Tool Use

<details>
<summary>❓ What does "tool use" mean for LLMs?</summary>

Giving the LLM access to **functions** it can **request to call** when it needs real-time data, external info, or computation. Tools = regular code functions (web search, DB query, calculator). LLM bina tools ke = insaan bina haathon ke! 🖐️
</details>

<details>
<summary>❓ Does the LLM always call tools when they're available?</summary>

**No!** LLM decides based on the query. "What time is it?" → calls get_current_time(). "Caffeine in green tea?" → answers directly. Smart delegation — only uses tools when it actually needs them.
</details>

<details>
<summary>❓ Hard-coded tool calls vs LLM-chosen tool calls — what's the difference?</summary>

**Hard-coded:** Developer pre-programs "always search web at step 2" — runs every time.
**LLM-chosen:** Developer provides a tool menu, LLM decides at runtime which (if any) to call. More flexible, more intelligent.
</details>

<details>
<summary>❓ In the calendar assistant, 3 tools available — how many used?</summary>

**2 of 3.** check_calendar (find slots) → make_appointment (book 3 PM with Alice). Skipped delete_appointment — wasn't needed. LLM selects only what's relevant.
</details>

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

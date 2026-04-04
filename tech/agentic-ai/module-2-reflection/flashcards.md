# 🃏 Module 2 — Reflection Flashcards

> From: module-2-reflection/ lessons
> Last updated: 2026-03-28

---

### 🪞 Reflection Basics

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What's the simplest implementation of the reflection pattern?</summary>

Two prompts, one loop: (1) LLM generates v1, (2) Pass v1 back with a "critique and improve" prompt → get v2. Can use same or different LLM.
</details>


<details class="flashcard" markdown>
<summary>What makes reflection MUCH more powerful than basic self-critique?</summary>

**External feedback** — new information from outside the LLM. Code execution errors, web search results, regex pattern matches, word counts. Without it, LLM is guessing. With it, LLM KNOWS what went wrong.

Bina feedback = andhera mein teer 🏹. With feedback = spotlight ON 🔦
</details>


<details class="flashcard" markdown>
<summary>What are the 3 performance tiers (worst → best)?</summary>

1. ★ Direct generation — improves then plateaus
2. ● With reflection — bumps above plateau
3. ✦ Reflection + external feedback — highest trajectory
</details>


---


</div>

### 📝 Prompt Writing

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What are the two golden rules for reflection prompts?</summary>

1. **Clearly indicate the reflection action** — "Review...", "Check...", "Critique..."
2. **Specify criteria to check** — don't just say "improve it", say WHAT to look for

Jitna specific criteria, utna focused feedback! 🎯
</details>


<details class="flashcard" markdown>
<summary>What research paper proved reflection > direct generation?</summary>

**"Self-Refine"** by Madaan et al. (2023). Tested 7 tasks (sentiment, code, math...) — reflection won ALL of them across GPT-3.5 and GPT-4.
</details>


---


</div>

### 🎨 Multimodal Reflection

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What's special about chart generation reflection?</summary>

The critic LLM doesn't just read code — it **sees the actual chart image** (base64-encoded). Catches visual issues (bad chart type, cramped labels, poor colors) that code review alone misses.
</details>


<details class="flashcard" markdown>
<summary>Why use different LLMs for generation vs reflection?</summary>

Different strengths: fast model (GPT-4o-mini) for quick drafts, **reasoning model** (o4-mini) for thorough critique. The code uses `generation_model` and `evaluation_model` params — mix and match!
</details>


---


</div>

### 📏 Evaluating Reflection

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What are the two types of evals?</summary>

1. **Objective** — right answer exists → code compares vs ground truth (e.g., SQL returned 1,201? ✅/❌)
2. **Subjective** — quality is fuzzy → LLM-as-Judge with binary rubric
</details>


<details class="flashcard" markdown>
<summary>Why is LLM pair comparison ("which is better?") unreliable?</summary>

Three issues: (1) poor accuracy vs human judgment, (2) prompt-sensitive, (3) **position bias** — most LLMs always pick the first option. Like picking the first menu item without reading the rest! 🍕
</details>


<details class="flashcard" markdown>
<summary>Why binary rubric (0/1 criteria) beats 1-5 scale rating?</summary>

LLMs don't know the difference between a "3" and "4". Binary is clear: title present? yes/no. Sum 5 binary scores → 0-5 range, **way more consistent**. Plus you see WHERE it lost points.
</details>


<details class="flashcard" markdown>
<summary>How many ground truth examples do you need to start?</summary>

**10-15 is enough.** Don't let "not enough data" block you. Small dataset gives directional signal — add more later.
</details>


---


</div>

### 🔦 External Feedback

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>Name three external feedback tools from the course.</summary>

1. **Code execution** — run code, feed errors back
2. **Pattern matching** (regex) — detect competitor names
3. **Web search** — fact-check claims (Taj Mahal built in 1648?)

Bonus: **Word count** tool — LLMs can't count words, `len(text.split())` can!
</details>


<details class="flashcard" markdown>
<summary>When should you escalate from direct prompting → reflection → external feedback?</summary>

When prompt tuning shows **diminishing returns** (performance plateaus). Don't grind the plateau — escalate! Ask: "Can I add reflection? Can I inject external info?"
</details>


---


</div>

### 💻 Code Patterns

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What library does the course use for multi-provider LLM calls?</summary>

**aisuite** — unified client that works with OpenAI, Anthropic, and others. `client.chat.completions.create(model="openai:gpt-4.1", ...)` — provider prefix selects the backend.
</details>


<details class="flashcard" markdown>
<summary>How does the visualization notebook handle multimodal input?</summary>

`encode_image_b64(chart_path)` → converts image to base64 string → sends as part of the prompt alongside text to a multimodal LLM. Works with both OpenAI (vision) and Anthropic (Claude).
</details>


<details class="flashcard" markdown>
<summary>What's the code pattern for the SQL reflection workflow?</summary>

1. `generate_sql()` → LLM writes SQL from question + schema
2. `execute_sql()` → runs it, gets DataFrame
3. `evaluate_and_refine_sql()` → reflection LLM sees SQL + output + schema → returns JSON `{"feedback": "...", "refined_sql": "..."}`
4. Execute refined SQL → compare results
</details>


---

> 💡 **Revision tip:** Cover the answer, explain OUT LOUD, then reveal. Bolke yaad hota hai! 🗣️


</div>
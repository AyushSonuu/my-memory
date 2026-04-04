# 🃏 Module 4 — Practical Tips Flashcards

> From: module-4-practical-tips/ lessons 01-07
> Last updated: 2026-03-31

---

### 📊 Evals

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What is an eval?</summary>

An **automated test for your AI system** — feed it known inputs, check outputs against expected results, track whether changes make things better or worse. Like unit tests, but for AI quality.
</details>


<details class="flashcard" markdown>
<summary>What's the 2×2 eval framework?</summary>

Two axes:
- **How you evaluate:** Code-based (objective) vs LLM-as-a-judge (subjective)
- **Ground truth:** Per-example ground truth vs no per-example ground truth

| | Per-Example GT | No Per-Example GT |
|---|---|---|
| **Code** | Invoice date extraction | Marketing copy length |
| **LLM Judge** | Research talking points | Chart rubric grading |
</details>


<details class="flashcard" markdown>
<summary>When do you use LLM-as-a-judge instead of code-based eval?</summary>

When the output is **open-ended or creative** — there's no single "right answer" to match with code. Essays, explanations, charts — things where a rubric or judgment is needed, not pattern matching.
</details>


<details class="flashcard" markdown>
<summary>How many examples do you need to start an eval?</summary>

**10-20 is fine to start.** Don't get paralyzed thinking you need hundreds. Start small, grow the eval set as you discover edge cases. Andrew says many teams waste weeks overthinking this.
</details>


<details class="flashcard" markdown>
<summary>What are "end-to-end evals"?</summary>

Evals that test the **entire pipeline** — from user input (one end) to final output (the other end). They measure overall system performance, not individual components.
</details>


---


</div>

### 🔍 Error Analysis

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What's the difference between a "trace" and a "span"?</summary>

- **Trace** = full set of intermediate outputs from ALL steps of one agent run (the complete picture)
- **Span** = output of a SINGLE step within that trace (one piece)

Terms come from the computer observability literature.
</details>


<details class="flashcard" markdown>
<summary>What's the error analysis process?</summary>

1. Collect only **failing examples** (skip the good ones)
2. Read traces — look at each step's intermediate output
3. Ask: "Would a human expert do significantly better given the same input?"
4. Build a **spreadsheet** — mark errors per component per example
5. Count up error rates → fix the component with the highest rate (if you have ideas to fix it)
</details>


<details class="flashcard" markdown>
<summary>Why should you NOT go by gut feeling when deciding what to fix?</summary>

Andrew Ng says gut feeling "leads to months of work with very little progress." You might pick the wrong component and optimize it for weeks without improving overall performance. The spreadsheet approach gives you data-driven prioritization.
</details>


<details class="flashcard" markdown>
<summary>If a step's output is bad because its INPUT was garbage, who do you blame?</summary>

Blame the **upstream step** that produced the garbage input. If "Pick 5 Best Sources" selected bad articles, but the web search results were ALL low-quality blogs — fix the web search, not the source picker.
</details>


<details class="flashcard" markdown>
<summary>Can error percentages add up to more than 100%?</summary>

**Yes!** Errors are NOT mutually exclusive. A single failing example can have multiple broken components. Invoice 20 had both PDF-to-text errors AND LLM extraction errors. Count each component's failures independently.
</details>


<details class="flashcard" markdown>
<summary>In the invoice example, what was the surprising finding?</summary>

PDF-to-text had only **15%** errors, but LLM data extraction had **87%**. Most teams would instinctively fix the PDF parser first — but the real problem was the LLM picking the wrong date.
</details>


<details class="flashcard" markdown>
<summary>In the customer email example, what were the error rates?</summary>

| Component | Error Rate |
|---|---|
| LLM-drafted query | **75%** ← fix this first |
| Orders database | 4% |
| LLM-drafted email | 30% |
</details>


<details class="flashcard" markdown>
<summary>What's the prioritization formula?</summary>

`Priority = Error Rate × Fixability`. High error rate + actionable fix ideas = work on it now. High error rate + no fix ideas = skip for now, return later.
</details>


---


</div>

### 🔬 Component-Level Evals

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>Why not just use end-to-end evals for everything?</summary>

Two problems: (1) **Expensive** — every small tweak requires re-running the entire pipeline, (2) **Noisy** — randomness from other components can mask small improvements in the one you're tuning.
</details>


<details class="flashcard" markdown>
<summary>How do you build a component-level eval for web search?</summary>

1. Create a list of **gold standard web resources** for each query
2. Write code to measure overlap (e.g., **F1 score** from information retrieval)
3. Track as you vary hyperparameters: search engine, number of results, date range
4. Confirm with an end-to-end eval before declaring victory
</details>


---


</div>

### 🔧 Addressing Problems

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What are the two strategies for improving non-LLM components?</summary>

1. **Tune hyperparameters** — web search (results count, date range), RAG (similarity threshold, chunk size), ML models (detection threshold)
2. **Replace the component** — try a different search engine, RAG provider, etc.
</details>


<details class="flashcard" markdown>
<summary>What's the order of strategies for improving LLM components?</summary>

1. **Improve prompts** (explicit instructions, few-shot examples) — try first, cheapest
2. **Try a different model** — use evals to compare
3. **Split the step** — decompose into smaller sequential calls
4. **Fine-tune** — last resort, expensive in developer time, for mature applications at 90-95% needing to reach 99%
</details>


<details class="flashcard" markdown>
<summary>Llama 3.1 8B vs GPT-5 on PII redaction — what happened?</summary>

Llama 8B: didn't follow format (extra list), missed the name, didn't fully redact address. GPT-5: followed formatting exactly, found all PII, correctly redacted everything. **Larger frontier models are much better at following complex instructions.**
</details>


<details class="flashcard" markdown>
<summary>How do you develop intuition for model intelligence?</summary>

- Play with new models often (both proprietary and open-weight)
- Keep a personal eval set for calibration
- **Read other people's prompts** — published online, open-source packages, friends at companies
- Try different models in your workflows via aisuite
</details>


---


</div>

### ⚡💰 Latency & Cost

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What's the priority order: quality, latency, or cost?</summary>

**Quality first → Latency second → Cost third.** Getting high-quality outputs is the hardest part. Optimize speed and cost only after the system works well. Having high costs from high usage is "a good problem to have."
</details>


<details class="flashcard" markdown>
<summary>Three strategies for reducing latency?</summary>

1. **Parallelism** — run independent steps simultaneously (e.g., fetch 5 web pages at once)
2. **Smaller/faster model** — if the step doesn't need frontier intelligence
3. **Faster LLM provider** — some providers have specialized hardware for the same model
</details>


<details class="flashcard" markdown>
<summary>What are the three cost types in agentic workflows?</summary>

1. **LLM steps** — pay per token (input + output)
2. **API-calling tools** — pay per API call
3. **Compute steps** — based on server capacity/cost
</details>


---


</div>

### 🔄 Development Process

<div class="flashcard-deck" markdown>


<details class="flashcard" markdown>
<summary>What are the two major activities in building agentic AI?</summary>

**Building** (writing code, improving the system) and **Analyzing** (error analysis, building evals, reading traces). Less experienced teams over-index on building; the best teams balance both equally.
</details>


<details class="flashcard" markdown>
<summary>What's the maturity progression for analysis?</summary>

1. Manual output examination + reading traces
2. Small end-to-end evals (10-20 examples)
3. Systematic error analysis (spreadsheet counting)
4. Component-level evals for targeted improvement

Each level builds on the previous one.
</details>


---

> 💡 **Revision tip:** Cover the answer, explain out loud, then reveal.


</div>
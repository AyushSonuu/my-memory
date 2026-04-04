# 🃏 Module 5 — Autonomous Agents Flashcards

> From: module-5-autonomous-agents/ + related: module-3-tool-use/, module-2-reflection/
> Last updated: 2026-04-03

---

### 📌 Planning

<details markdown="1">
<summary>❓ What is the planning design pattern?</summary>

Instead of hard-coding "call tool A → B → C", you give the LLM a set of tools + a prompt: "return a step-by-step plan." The LLM generates its own plan, then executes it one step at a time, chaining each step's output as context to the next.

Hard-coded agent = train 🚂 (one track). Planning agent = taxi 🚕 (bolo kahaan, rasta khud nikalega)!
</details>

<details markdown="1">
<summary>❓ How does step chaining work in planning?</summary>

Step 1 text → LLM → executes → output. That output + Step 2 text → LLM → executes → output. That output + Step 3 text → LLM → and so on. Each step gets the **cumulative context** of all previous steps.
</details>

<details markdown="1">
<summary>❓ In the sunglasses example, the agent has 6 tools. How many does it use per query?</summary>

**Only 3!** And different queries use different subsets:
- "Round under $100?" → get_item_descriptions → check_inventory → get_item_price
- "Return gold frame" → check_past_transactions → get_item_descriptions → process_item_return

Same tools, completely different plans — that's the power of planning.
</details>

<details markdown="1">
<summary>❓ What's the biggest challenge with planning?</summary>

**Control and predictability.** You don't know what plan the LLM will generate at runtime. This makes the system harder to debug. That's why planning works great in agentic coding but is still growing in other domains.
</details>

---

### 📌 Plan Formats

<details markdown="1">
<summary>❓ Why format plans as JSON instead of plain text?</summary>

Code can't reliably parse plain text plans — "Find round sunglasses" doesn't tell code which tool or what args. JSON gives structured keys: `{"step": 1, "tool": "get_item_descriptions", "args": {"query": "round"}}` — just `json.loads()` and loop.
</details>

<details markdown="1">
<summary>❓ What 4 fields should each step in a JSON plan have?</summary>

1. **step** — number (ordering)
2. **description** — what this step does
3. **tool** — which tool to call
4. **args** — arguments to pass

These give your code everything it needs to execute programmatically.
</details>

<details markdown="1">
<summary>❓ Rank the plan formats by reliability.</summary>

| Rank | Format | Why |
|------|--------|-----|
| 🥇 | **Code** | Most precise — just execute it |
| 🥈 | **JSON** | Standard parsers, clear keys |
| 🥉 | **XML** | Good tags, slightly more verbose |
| 4th | **Markdown** | Needs custom parsing |
| 5th | **Plain text** | Regex/heuristics — least reliable |

Research (Wang et al. 2024): Code > JSON > Text across multiple models.
</details>

---

### 📌 Planning with Code

<details markdown="1">
<summary>❓ Why is tool-based planning bad for data analysis?</summary>

Three problems: **Brittle** (query doesn't fit your limited tools), **Inefficient** ("which month had highest hot chocolate sales" = 24+ steps with filter_rows × 12 months), **Edge case treadmill** (every new query type = create a new tool, forever).
</details>

<details markdown="1">
<summary>❓ How does "planning with code" solve the tool treadmill?</summary>

Prompt LLM: "Write Python code to solve this." Python + pandas = **thousands** of built-in functions the LLM already knows from training data. The code IS the plan — each step expressed as executable code. No new tools needed for new query types.

Tools = limited menu card. Code = poore kitchen ka access! 🍳
</details>

<details markdown="1">
<summary>❓ What's the security caveat with code execution?</summary>

LLM-generated code could be buggy or malicious — run it in a **sandbox** (Docker, VM, E2B). Many devs skip the sandbox (not best practice). Same concern as Module 3's code execution lesson.
</details>

<details markdown="1">
<summary>❓ When should you use tools vs code vs both?</summary>

| Scenario | Use |
|----------|-----|
| Data analysis, computation | 💻 Code execution |
| Proprietary APIs, internal systems | 🔧 Custom tools |
| Complex app with both | 🔀 Both! |
</details>

---

### 📌 Multi-Agent

<details markdown="1">
<summary>❓ Why use multiple agents instead of one?</summary>

Same reason you hire a **team** instead of one person: complex tasks decompose naturally into roles. Each agent gets a focused prompt + relevant tools. Easier to design, build, test, and **reuse**.

Also: like multiple processes on one CPU — decomposition makes the problem manageable.
</details>

<details markdown="1">
<summary>❓ How do you BUILD an individual agent?</summary>

Agent = **LLM prompted with a role** + given **specific tools**. Example:
- Researcher = LLM + "You are a research agent..." + web_search tool
- Designer = LLM + "You are a graphic designer..." + image_generation + code_execution
- Writer = LLM + "You are a writer..." + no extra tools (text gen is native)
</details>

<details markdown="1">
<summary>❓ What's the difference between planning with tools vs planning with agents?</summary>

Same mechanism, different building blocks:
- Tools: LLM sees `[get_price, check_inventory]` → plans which function to call
- Agents: LLM sees `[researcher, designer, writer]` → plans which agent to delegate to

Green boxes (tools) → Purple boxes (agents). The planning logic is identical.
</details>

<details markdown="1">
<summary>❓ In the manager-coordinated pattern, how many agents are there?</summary>

**Four!** The manager is the 4th agent — it plans, delegates to the 3 workers (researcher, designer, writer), collects results, and can reflect/improve the output. The manager is not just an orchestrator — it's an LLM-based agent too.
</details>

---

### 📌 Communication Patterns

<details markdown="1">
<summary>❓ What are the two most common communication patterns?</summary>

1. **Linear** — A → B → C (relay race, sequential)
2. **Hierarchical** — Manager coordinates team (hub-and-spoke)

These two cover the vast majority of real-world multi-agent systems today.
</details>

<details markdown="1">
<summary>❓ What's a deeper hierarchy look like?</summary>

Manager → Researcher, Designer, Writer. But:
- Researcher → Web Researcher + Fact Checker
- Writer → Style Writer + Citation Checker
- Designer works solo

Some agents have their own sub-agents — like departments in a company.
</details>

<details markdown="1">
<summary>❓ How does the all-to-all pattern work?</summary>

Every agent knows about all others. Any agent can message any other at any time. Messages get added to the receiver's context. They collaborate until everyone declares "done."

Results: **hard to predict.** Like a WhatsApp group — sometimes brilliant, sometimes pure chaos 😂
</details>

<details markdown="1">
<summary>❓ Rank the 4 communication patterns by control level.</summary>

| Pattern | Control | Usage |
|---------|---------|-------|
| Linear | 🟢 Highest | ⭐ Most common |
| Hierarchical | 🟢 High | ⭐ Most common |
| Deeper Hierarchy | 🟡 Moderate | Less common |
| All-to-All | 🔴 Lowest | Experimental |

More control = more predictable. Less control = more flexible but chaotic.
</details>

---

### 🔗 From: Module 3 — Tool Use

<details markdown="1">
<summary>❓ Planning with tools vs Tool Use module — what's the connection?</summary>

Module 3 = LLM **chooses** which tool to call at runtime (single-step decisions). Module 5 Planning = LLM writes a **multi-step plan** with tool sequences. Planning builds ON TOP of tool use — it's tool use with a plan layer.
</details>

---

### 🔗 From: Module 2 — Reflection

<details markdown="1">
<summary>❓ Where does reflection appear in multi-agent systems?</summary>

The **manager agent** can reflect on the final output! After the writer delivers the draft, the manager does a review/improvement step before producing the final result. Reflection is a design pattern that works inside multi-agent workflows too.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

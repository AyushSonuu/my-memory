# 🃏 Module 3 — Tool Use Flashcards

> From: module-3-tool-use/ lessons
> Last updated: 2026-03-28

---

### 🔧 Tool Basics

<details markdown="1">
<summary>❓ What does "tool use" mean for LLMs?</summary>

Giving the LLM access to **functions** it can **request to call** when it needs real-time data, external info, or computation. LLM bina tools ke = insaan bina haathon ke! 🖐️
</details>

<details markdown="1">
<summary>❓ Does the LLM always use available tools?</summary>

**No.** LLM decides based on the query. "What time?" → calls tool. "Caffeine in tea?" → answers directly. Smart delegation — only calls what's needed.
</details>

<details markdown="1">
<summary>❓ Hard-coded vs LLM-chosen tool calls?</summary>

**Hard-coded:** Developer pre-programs "always search web at step 2."
**LLM-chosen:** Developer provides a menu of tools, LLM picks at runtime.
This module = LLM-chosen approach.
</details>

---

### 🛠️ Creating Tools & Syntax

<details markdown="1">
<summary>❓ What is aisuite?</summary>

Open source library (co-created by Andrew Ng) — **unified interface** for multiple LLM providers. One `client.chat.completions.create()` call handles: schema generation, tool execution, result feed-back — all automatic.
</details>

<details markdown="1">
<summary>❓ How does aisuite auto-generate tool schemas?</summary>

Reads your function's: (1) **name** from `def`, (2) **description** from docstring, (3) **parameters** from signature. Builds JSON schema automatically. Docstring = tool ka resume! 📄
</details>

<details markdown="1">
<summary>❓ What's `max_turns` in aisuite?</summary>

Ceiling on consecutive tool calls to prevent infinite loops. Set to **5**, forget about it. Andrew Ng: "In practice, you almost never hit this limit."
</details>

<details markdown="1">
<summary>❓ What does the JSON schema for a tool with parameters look like?</summary>

```json
{"type": "function", "function": {
  "name": "get_current_time",
  "description": "Returns current time for the given time zone",
  "parameters": {"timezone": {"type": "string", "description": "IANA timezone"}}
}}
```
All auto-generated from your function + docstring!
</details>

---

### 💻 Code Execution

<details markdown="1">
<summary>❓ Why is code execution the ultimate meta-tool?</summary>

Instead of 50 individual tools (add, sqrt, log...), give the LLM ONE tool: write and execute Python. It can solve **anything expressible in code**. One tool to rule them all! 👑
</details>

<details markdown="1">
<summary>❓ What's the `<execute_python>` tag pattern?</summary>

1. System prompt: "wrap code in `<execute_python>` tags"
2. LLM writes code in tags
3. Regex extracts: `re.search(r"<execute_python>([\s\S]*?)</execute_python>", output)`
4. `exec()` or sandbox → feed result back
</details>

<details markdown="1">
<summary>❓ Why sandbox LLM-generated code?</summary>

Real horror story: Andrew Ng's team agent ran `rm *.py` — deleted files! Options: **Docker** (heavy, secure), **E2B** (lightweight), `exec()` (zero protection). Always sandbox in production.
</details>

---

### 🔌 MCP

<details markdown="1">
<summary>❓ What problem does MCP solve?</summary>

**M×N → M+N.** Without MCP, every app builds custom wrappers for each service. With MCP: clients connect to shared servers via standard protocol. 10 apps × 20 services = 200 wrappers → 30 connections! USB port for LLMs! 🔌
</details>

<details markdown="1">
<summary>❓ MCP Client vs Server?</summary>

**Client** = app that USES tools (Cursor, Claude Desktop, your app).
**Server** = service that PROVIDES tools (GitHub, Slack, PostgreSQL).
Protocol connects them all.
</details>

<details markdown="1">
<summary>❓ MCP Resources vs Tools?</summary>

**Resources** = fetch data (read README from GitHub). **Tools** = take actions (create PR, send message). MCP handles both.
</details>

---

### 💻 Code Lab Patterns

<details markdown="1">
<summary>❓ What are the three M3 labs about?</summary>

1. **UGL 1** — Turn functions into aisuite tools (get_current_time, file read/write, weather)
2. **UGL 2** — Email assistant: multi-tool agent (read/send/search emails via REST wrappers)
3. **Graded Lab** — Research agent: arxiv_search + tavily_search → reflection → HTML formatting
</details>

---

> 💡 **Revision tip:** Cover answers, explain OUT LOUD, then reveal. Bolke yaad hota hai! 🗣️

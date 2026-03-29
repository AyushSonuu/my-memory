# 📋 Agentic AI — Cheatsheet

> One-page reference. Covers M1-M3. Updated as modules complete.

---

## 🎯 What is Agentic AI?

> LLMs that don't just respond — they **act**: plan, execute, reflect, iterate.

```
Traditional AI:  Input → LLM → Output (one shot, done)
Agentic AI:      Input → LLM → Tool → LLM → Reflect → Tool → ... → Output (multi-step loop)
```

> 💡 "Chatbot = calculator. Agent = accountant who uses the calculator." 🧮

---

## 🧱 4 Design Patterns (Control ↓, Autonomy ↑)

| # | Pattern | What It Does | Control Level | Key Idea |
|---|---------|-------------|---------------|----------|
| 🪞 | **Reflection** | Self-critique loop — generate → critique → improve | 🟢 Highest | 2 prompts, 1 loop. Surprisingly easy! |
| 🔧 | **Tool Use** | LLM chooses which functions to call at runtime | 🟡 High | aisuite, docstrings, code execution, MCP |
| 📋 | **Planning** | LLM breaks task into sub-steps, executes each | 🟠 Medium | Experimental — can derail |
| 👥 | **Multi-Agent** | Specialized agents collaborating | 🔴 Lowest | Hardest to control |

---

## 🪞 Reflection — Quick Ref

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ 1. Generate  │ ──→ │ 2. Critique   │ ──→ │ 3. Improve   │ ──→ repeat?
│    (fast LLM)│     │ (reasoning    │     │ (apply fixes)│
│              │     │  model)       │     │              │
└─────────────┘     └──────────────┘     └─────────────┘
```

| Tier | Method | Performance |
|------|--------|-------------|
| ★ | Direct generation | Baseline → plateau |
| ●● | + Reflection | Bump above plateau |
| ✦✦✦ | + Reflection + External Feedback | Highest trajectory |

**External feedback sources:** code execution errors, web search, regex patterns, word count

---

## 🔧 Tool Use — Quick Ref

**aisuite flow:**
```python
# 1. Define function with good docstring
def get_weather(city: str) -> str:
    """Get current weather for a city. Args: city - city name."""
    ...

# 2. Pass to aisuite — auto JSON schema from docstring!
response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=messages,
    tools=[get_weather],  # aisuite reads name + docstring + params
    tool_choice="auto",
    max_turns=5           # ceiling on consecutive calls
)
```

| Concept | One-liner |
|---------|-----------|
| **Docstring** | Tool ka resume — LLM reads it to decide when/how to call 📄 |
| **max_turns** | Safety ceiling on consecutive tool calls (set to 5, forget about it) |
| **Code execution** | THE meta-tool. One `exec()` replaces 50 individual tools 👑 |
| **`<execute_python>` tags** | System prompt tells LLM to wrap code → regex extract → exec/sandbox |
| **Sandbox** | ALWAYS sandbox production code. `rm *.py` horror story 💀 |

---

## 🔌 MCP (Model Context Protocol)

```
WITHOUT MCP:                    WITH MCP:
App1 ──→ GitHub wrapper         App1 ──┐
App1 ──→ Slack wrapper          App2 ──┼──→ MCP ──→ GitHub server
App2 ──→ GitHub wrapper         App3 ──┘          → Slack server
App2 ──→ Slack wrapper                            → DB server
... M × N wrappers!             M + N connections!
```

| Term | Meaning |
|------|---------|
| **Client** | App that USES tools (Cursor, Claude Desktop) |
| **Server** | Service that PROVIDES tools (GitHub, Slack, Postgres) |
| **Resources** | Fetch data (read README) |
| **Tools** | Take actions (create PR, send message) |

> 💡 "MCP = USB port for LLMs. Plug any tool into any app!" 🔌

---

## 📐 Evals — Decision Tree

```
Right/wrong answer exists?
  ├─ YES → Objective eval (code compares output vs ground truth)
  └─ NO  → Subjective eval → USE BINARY RUBRIC (0/1 per criterion)
                              ❌ NOT 1-5 scale (poorly calibrated)
                              ❌ NOT pair comparison (position bias!)
```

| Eval Type | When | Reliability |
|-----------|------|-------------|
| **Objective (code-based)** | Clear right/wrong | ⭐⭐⭐⭐⭐ |
| **Binary rubric** | Fuzzy quality | ⭐⭐⭐⭐ |
| **1-5 scale** | Quick-and-dirty only | ⭐⭐ |
| **Pair comparison** | AVOID — position bias | ⭐ |

**Error Analysis** = read each step's output to find WHERE it breaks (stethoscope 🩺)

---

## 🔁 The Dev Process Loop

```
Build → Run → Examine outputs → Discover problems → Create eval → Fix → Verify → Repeat
```

> 💡 "Don't write all evals upfront. Build first → discover failures → create targeted evals."

---

## 6 Building Blocks for Agents

| Block | Examples |
|-------|---------|
| LLMs | GPT-4o, Claude, Gemini |
| Multimodal Models | Vision, audio |
| Specialized AI | Code models, math models |
| APIs / Tools | Web search, DB queries, file I/O |
| Retrieval | RAG, vector DBs |
| Code Execution | Python exec, sandboxed environments |

---

## 🧠 Key One-Liners

> 💡 "Agent = LLM + tools + loop. No loop = chatbot." 🔄
> 💡 "Reflection = apni copy khud check karna. + External feedback = answer key mil jaana!" 🔑
> 💡 "Docstring = tool ka resume. Bad resume = bad hire decisions." 📄
> 💡 "Code execution = one tool to rule them all." 👑
> 💡 "MCP = USB port for LLMs." 🔌
> 💡 "Eval = thermometer 🌡️. Error Analysis = stethoscope 🩺. Dono chahiye!"
> 💡 "Binary rubric > 1-5 scale. Jitna specific poochoge, utna reliable jawab." 🎯

---

> _M4 (Practical Tips) and M5 (Autonomous Agents) sections will be added when those modules are complete._

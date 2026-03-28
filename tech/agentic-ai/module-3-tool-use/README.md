# 🔧 Module 3 — Tool Use

> LLMs alone can only generate text — tools give them hands to interact with the real world.

---

## 📊 Progress

| # | Lesson | Confidence | Revised |
|---|--------|-----------|---------|
| 01 | [What Are Tools?](01-what-are-tools.md) | 🟡 | — |
| 02 | [Creating a Tool](02-creating-a-tool.md) | 🟡 | — |
| 03 | [Tool Syntax](03-tool-syntax.md) | 🟡 | — |
| 04 | [Code Execution](04-code-execution.md) | 🟡 | — |
| 05 | [MCP](05-mcp.md) | 🟡 | — |

---

## 📚 Sources
> - 🎓 [Agentic AI](https://learn.deeplearning.ai/courses/agentic-ai) — Module 3
> - 🔌 [MCP Docs](https://modelcontextprotocol.io/) — Anthropic's Model Context Protocol

## 30-Second Recall 🧠
> Tools = functions you give the LLM to **request to call** when it needs real-time data, external info, or computation. The LLM CHOOSES when to use them (not hard-coded). aisuite auto-generates JSON schemas from your function's name + docstring — one line to register a tool. **Code execution** is the ultimate meta-tool: instead of 50 individual tools, let the LLM write Python and execute it (but use a sandbox!). **MCP** standardizes tool sharing across the ecosystem: M×N custom wrappers → M+N shared connections. Clients (apps) connect to servers (tool providers) via a standard protocol.

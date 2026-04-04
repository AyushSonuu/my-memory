# 🎬 Episode 01 · What is LangChain? Complete Overview

> **Type:** Concept episode (show docs site + one code example)
> **Duration target:** 12-15 minutes
> **Thumbnail:** `LANGCHAIN` `OVERVIEW`
> **Docs:** https://docs.langchain.com/oss/python/langchain/overview

---

## 📝 SCRIPT

---

### 🎬 HOOK (0:00 - 0:30)

> *[Camera on you]*

"What if you could build an AI agent — one that can call APIs, search the web, remember conversations, and work with *any* language model — in under ten lines of code?

That's exactly what LangChain does. And in this episode, I'm going to show you what LangChain is, how it fits in the bigger ecosystem, its core benefits, and we'll write our first agent together. Let's get into it."

---

### 🦜 WHAT IS LANGCHAIN? (0:30 - 2:30)

> *[Screen share — show the docs site langchain.md page]*

"LangChain is an **open-source agent framework**. Let me break that down.

If you want to build anything powered by a large language model — a chatbot, a coding assistant, a RAG pipeline, a multi-agent system — you need to do a few things:

- Connect to a model (OpenAI? Anthropic? Google? Local?)
- Give it tools (web search? database queries? custom functions?)
- Manage conversation history
- Handle structured outputs
- And somehow make all of this reliable

LangChain does **all of this** with a standard interface. You write your code once, and you can swap the model provider without changing anything else.

But here's what makes LangChain special — it's not just a wrapper around API calls. It provides a **prebuilt agent architecture**. That means you get a fully functional agent loop — the model thinks, decides to use a tool, gets the result, thinks again — all handled for you.

> *[Show the architecture diagram on docs site]*

And under the hood? LangChain agents are built on top of **LangGraph** — the low-level runtime we covered in the last playlist. That means every LangChain agent automatically gets LangGraph's superpowers — durable execution, streaming, persistence, human-in-the-loop — without you having to configure any of it.

So to summarize: LangGraph is the engine. LangChain is the car built on that engine. You just get in and drive."

---

### 🔍 WHERE DOES IT FIT? (2:30 - 4:30)

> *[Screen share — show the stack diagram on docs home page]*

"Let me show you where LangChain sits in the ecosystem. We covered this in the intro video, but it's worth repeating:

```
🧠 Deep Agents  → The Harness    (built ON LangChain)
🦜 LangChain    → The Framework  (built ON LangGraph)  ← WE ARE HERE
🔷 LangGraph    → The Runtime    (the foundation)
```

Now the official docs actually give you a really clear recommendation on when to use what:

> *[Show the callout box from docs]*

| Use Case | Framework |
|----------|-----------|
| You want batteries-included — planning, subagents, file systems, sandboxes | **Deep Agents** |
| You want to quickly build agents with full control over tools, memory, prompts | **LangChain** ← most people start here |
| You need low-level control — custom state machines, deterministic + agentic workflows | **LangGraph** |

Here's the good news: **you don't need to know LangGraph to use LangChain.** LangChain handles that layer for you. Think of it like driving a car — you don't need to understand the engine to drive it. But if you watched our LangGraph playlist, you now understand what's happening under the hood. That gives you an edge when debugging or building advanced features."

---

### ⭐ FOUR CORE BENEFITS (4:30 - 8:00)

> *[Screen share — show the 4 benefit cards on docs page, go through each one]*

"The docs highlight four core benefits of LangChain. Let me walk through each one.

---

#### Benefit 1: Standard Model Interface

> *[Point to the first card]*

"Every LLM provider has a different API. OpenAI formats requests one way. Anthropic does it differently. Google has its own format. If you write code for one provider, switching to another means rewriting everything.

LangChain solves this. It gives you **one standard interface** for all of them. Same code, different provider. Want to switch from OpenAI to Anthropic? Change one string. Your agent code, your tools, your memory — everything else stays the same.

This isn't just convenient — it's **strategic**. It means no vendor lock-in. If a new model comes out tomorrow that's better and cheaper, you switch in ten seconds."

---

#### Benefit 2: Easy to Use, Highly Flexible Agent

> *[Point to the second card]*

"LangChain's agent abstraction is designed around a principle I really respect: **easy to start, flexible enough to scale.**

Getting started? You can build a functional agent in under ten lines of code. I'll show you that in a minute.

But when you need more control — custom context engineering, specialized middleware, multi-agent orchestration — LangChain gives you the hooks to customize everything. You're never locked into a simple pattern. You start simple, and you grow into complexity only when you need it."

---

#### Benefit 3: Built on Top of LangGraph

> *[Point to the third card]*

"This is the architectural decision that makes LangChain agents production-ready from day one.

Because LangChain agents run on LangGraph's runtime, they automatically get:
- **Durable execution** — your agent survives crashes and resumes where it left off
- **Streaming** — real-time token-by-token output
- **Human-in-the-loop** — pause the agent, let a human review, then continue
- **Persistence** — save and restore agent state across sessions

You get all of this without writing a single line of LangGraph code. It's just there."

---

#### Benefit 4: Debug with LangSmith

> *[Point to the fourth card]*

"When you're building agents, things go wrong. A lot. The model makes a weird tool call. The context gets too long. A tool returns unexpected data.

LangSmith is LangChain's observability platform. It gives you:
- Full **traces** of every step your agent takes
- Visualization of **execution paths** and **state transitions**
- Detailed **runtime metrics**

You set one environment variable — `LANGSMITH_TRACING=true` — and you can see exactly what your agent is doing at every step. We'll cover LangSmith in detail later in the series, but just know it exists and it's incredibly useful for debugging."

---

### 💻 YOUR FIRST AGENT — LIVE CODE (8:00 - 11:00)

> *[Screen share — open code editor, type the code]*

"Alright, enough talking. Let's build our first agent.

I'm going to show you the exact code from the official docs. Under ten lines. Here we go:

```python
# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

Let me walk through every line.

> *[Point to import]*

`create_agent` — this is the prebuilt agent architecture I was talking about. One function. That's all you need to create a full agent.

> *[Point to the function]*

`get_weather` — this is a **tool**. It's just a regular Python function with a docstring. LangChain reads the docstring to understand what the tool does. When the model decides it needs weather information, it will call this function automatically.

> *[Point to create_agent]*

`create_agent` — three things:
- `model` — which LLM to use. Notice the format: `anthropic:claude-sonnet-4-6`. Provider colon model. Want OpenAI? Just change it to `openai:gpt-4o`. Same code.
- `tools` — a list of functions the agent can use. We're giving it our weather function.
- `system_prompt` — instructions for how the agent should behave.

> *[Point to invoke]*

`agent.invoke` — this is where the magic happens. You send a message, and the agent:
1. Reads your message
2. Decides it needs weather data
3. Calls the `get_weather` tool
4. Gets the result
5. Generates a natural language response using that result

All of that happens in this one line.

> *[Run the code, show the output]*

And there it is. Our first agent. Under ten lines of code. It took a user's question, decided to use a tool, called it, and responded with the result."

---

### 🔄 RECAP (11:00 - 12:00)

> *[Camera on you]*

"Let's recap what we learned:

**LangChain is an agent framework** — it gives you a standard interface to any LLM, a prebuilt agent architecture, tools, memory, and structured outputs.

**It's built on LangGraph** — so you get durable execution, streaming, persistence, and human-in-the-loop for free.

**Four core benefits:** standard model interface, easy-but-flexible agents, LangGraph runtime under the hood, and LangSmith debugging.

**And you can build an agent in under ten lines of code** — we just did it.

In the **next video**, we'll set up our development environment properly — install LangChain, configure API keys, and make sure everything is ready for the rest of the series.

If you're following along, make sure to **subscribe** and I'll see you in the next one."

---

## 📝 YouTube Metadata

### Title
`What is LangChain? Complete Overview — Build AI Agents in 10 Lines of Code | Ep 01`

### Description
```
🦜 What is LangChain and why is it the most popular framework for building AI agents?

In this episode, you'll learn:
• What LangChain is and what problems it solves
• How it fits in the ecosystem (LangGraph → LangChain → Deep Agents)
• The 4 core benefits — standard interface, flexible agents, LangGraph runtime, LangSmith
• Build your FIRST agent in under 10 lines of code

📚 Official Docs: https://docs.langchain.com/oss/python/langchain/overview
💻 Code: https://github.com/AyushSonuu/langchain-ecosystem-tutorials/tree/main/langchain/ep01-overview

⏰ Timestamps:
00:00 — Hook
00:30 — What is LangChain?
02:30 — Where does it fit in the ecosystem?
04:30 — Four core benefits
08:00 — Your first agent (live code)
11:00 — Recap & next steps

🔗 Full Playlist: [link]
📖 Docs Site: https://ayushsonuu.github.io/langchain-ecosystem-tutorials

#langchain #aiagents #python #tutorial #langchain2026 #buildaiagents
```

### Tags
```
langchain, langchain overview, what is langchain, langchain tutorial, langchain python,
langchain agent, build ai agents, langchain 2026, langchain for beginners,
ai agents tutorial, langchain create agent, langchain quickstart,
langchain vs langgraph, langchain ecosystem, python ai agents
```

# ⚡ FastAPI

> Modern, fast Python web framework — declare once with types, get validation + docs + editor support for free.

---

## 🧠 Brain — How This Connects

```mermaid
graph LR
    FA(("⚡ FastAPI"))
    FA -->|"built on"| PY["🐍 Python Types<br/>& type hints"]
    FA -->|"validation via"| PD["🧱 Pydantic<br/>BaseModel"]
    FA -->|"async support"| AIO["⚡ AsyncIO<br/>coroutines"]
    FA -.->|"serves"| API["🌐 REST APIs<br/>OpenAPI"]
    FA -.->|"used in"| AG["🤖 Agentic AI<br/>tool endpoints"]

    style FA fill:#ff9800,color:#fff
```

## 📊 Progress
| # | Lesson | Confidence | Revised |
|---|--------|-----------|---------|
| 01 | [Python Types Intro](01-python-types-intro.md) | 🔴 | — |

## 🧩 Memory Fragments
> - FastAPI is ALL based on Python type hints — types aren't optional, they ARE the framework
> - Pydantic handles validation; Starlette handles the HTTP layer; FastAPI is the glue
> - `Annotated[str, Query(...)]` is how FastAPI gets rich metadata from type hints

---

## 🎬 Teach Mode — Lesson Flow

> Open these in order = you can teach anyone FastAPI

| # | Lesson | One-liner | Time |
|---|--------|-----------|------|
| 01 | [Python Types Intro](01-python-types-intro.md) | Type hints — the foundation everything else builds on | 8 min |

---

## 📚 Sources
> - 🌐 Docs: [FastAPI Official Documentation](https://fastapi.tiangolo.com/)

## 🔗 Connected Topics
> → [python/asyncio](../python/asyncio/) · [python/](../python/) · [agentic-ai](../agentic-ai/)

## 30-Second Recall 🧠
> FastAPI uses Python type hints to do everything: validate request data, convert types, generate error messages, and produce OpenAPI docs — all from a single annotation like `name: str`. Pydantic models are the data validation layer. `Annotated[type, metadata]` is how extra rules (like max length) get attached without extra code. Type hints themselves are passive — Python ignores them; FastAPI/Pydantic are the ones that act on them.

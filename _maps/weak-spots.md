# Where I'm Weak

> Ayush's knowledge gaps, revision debt, and incomplete topics — all in one place.
> Last updated: 2026-06-17

---

## 🔴 Critical Gaps (Start Here)

| Topic | Status | What's Missing | Next Action | Priority |
|-------|--------|---------------|-------------|----------|
| **FastAPI** | 🔴 Just started — 4/many lessons | Core routing, dependency injection, request/response models, middleware, auth, background tasks, testing | Continue lessons in order. Do NOT skip to advanced topics. | 🔴 P0 |

> 💡 FastAPI = ek naya bande ko poori company chalani hai — abhi toh wo sirf "Hello World" jaanta hai.

---

## 🟡 Needs Revision or Completion

### Revision Overdue

| Topic | Overdue Since | What to Revise | Next Action |
|-------|--------------|---------------|-------------|
| **Agentic AI** | Apr 2026 (~75 days overdue) | All 30 lessons — M1-M5. Memory types, tool use, ReAct, planning, multi-agent orchestration | Run full flashcard quiz M1→M5. Then re-read weak lessons. |
| **Agent Memory** | ~Mar 2026 | 7 lessons — memory types, episodic vs semantic, context compression | Flashcard quiz first. If score < 80%, re-read lessons. |

> ⚠️ Agentic AI has 30 lessons with ZERO revision since completion. This is your biggest revision debt. Every week you delay, forgetting compounds.

---

### Incomplete Topics

| Topic | Progress | What's Missing | Next Action | Priority |
|-------|----------|---------------|-------------|----------|
| **RAG** | ~20/62 lessons (~32%) | M3 remainder + M4 (LLMs & Text Generation) + M5-M6 (advanced retrieval, eval, production) | Pick up where M3 left off. Don't revise what you've done — just push forward. | 🟡 P1 |
| **GenAI with LLMs** | W1 done — W2/W3 not started | W2: Fine-tuning, RLHF, PEFT, LoRA. W3: Deployment, alignment, RLHF in practice | Start W2 L01 next. W1 knowledge is fresh — keep momentum. | 🟡 P1 |
| **Spec-Driven Development** | 13/16 lessons | L14-L16 — likely conclusion, wrap-up, and synthesis lessons | Finish final 3 lessons. Then close the topic. | 🟡 P2 |

---

### Python Concurrency (Cluster — all 🟡)

All three topics were learned around the same time. Treat as one revision block.

| Topic | Status | What's Missing | Next Action |
|-------|--------|---------------|-------------|
| **asyncio** | 🟡 Learned, no recent revision | Event loop internals, `async/await` patterns, `asyncio.gather`, task cancellation | Revise flashcards as a set with threading + multiprocessing |
| **threading** | 🟡 Learned, no recent revision | GIL limitations, thread safety, `Lock`/`RLock`, `ThreadPoolExecutor` | Same — revise as a cluster |
| **multiprocessing** | 🟡 Learned, no recent revision | `Process` vs `Pool`, `Queue`/`Pipe`, shared memory, `ProcessPoolExecutor` | Same — revise as a cluster |

> 💡 Ek saath padhna = ek saath yaad rehna. Concurrency cluster ko ek 45-min session mein revise karo — trio as one.

---

## Revision Overdue — Agentic AI (Special Note)

**Status:** 30/30 lessons complete. Zero revision since completion (~Apr 6, 2026).
**Days overdue:** ~75 days as of 2026-06-17.

**What you covered:**

| Module | Topics |
|--------|--------|
| M1 | Agent fundamentals, perception-action loop, stateless vs stateful |
| M2 | Tool use, function calling, LLM-as-orchestrator |
| M3 | ReAct pattern, chain-of-thought, scratchpad reasoning |
| M4 | Planning, multi-step task decomposition, self-reflection |
| M5 | Multi-agent systems, orchestration, agent communication |

**Why this matters:** Agentic AI is the core of your current track. RAG, Agent Memory, and FastAPI all connect here. Forgetting this = shaky foundations for everything else.

**Recommended revision session:**
1. Run flashcard quiz for M1 + M2 (20 min)
2. Run flashcard quiz for M3 + M4 + M5 (25 min)
3. Flag any cards you got wrong — re-read that lesson only
4. Do NOT re-read everything. Quiz first, targeted re-read only if needed.

---

## Priority Stack (What to Do Next)

```
1. 🔴 FastAPI       — active study, push lessons forward daily
2. 🟡 Agentic AI    — URGENT revision (75 days overdue)
3. 🟡 RAG           — continue lessons (32% done, long tail)
4. 🟡 GenAI w/ LLMs — start W2 while W1 is fresh
5. 🟡 Agent Memory  — revision (overdue ~Mar 2026)
6. 🟡 SDD           — just 3 lessons left, close it out
7. 🟡 Concurrency   — one cluster revision session (asyncio + threading + multiprocessing)
```

---

> This file is maintained manually after each vault sync. Update after every study session.
> Next rebuild due: when any topic status changes or new weak spots emerge.

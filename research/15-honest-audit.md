# memharness — Honest Audit (2026-03-23)

## HLD vs Reality

### ✅ Implemented & Working
| HLD Feature | Status | Quality |
|-------------|--------|---------|
| 10 Memory Types | ✅ All 10 | Good — each has its own module |
| Simple API (add/search/get/update/delete) | ✅ | Good |
| SQLite backend | ✅ | Working, tested |
| In-memory backend | ✅ | Working, 80% coverage |
| PostgreSQL backend | ✅ | Code exists, untested (no running PG) |
| Framework agnostic | ✅ | Works standalone |
| LangChain integration | ✅ | BaseTool, ChatHistory, Middleware |
| VFS Tool Discovery | ✅ | tree/ls/grep/cat |
| Config (YAML + code) | ✅ | Pydantic models |
| Async-first API | ✅ | Full async |
| Type safety | ✅ | Type hints, py.typed |
| CI/CD | ✅ | GitHub Actions, auto-deploy |
| PyPI published | ✅ | v0.4.2 |
| Docs (Docusaurus) | ✅ | Deployed, partially complete |

### ⚠️ Partially Done
| HLD Feature | Status | Gap |
|-------------|--------|-----|
| Memory lifecycle (summarize/consolidate/GC) | ⚠️ | Agents exist but are LLM-dependent, no auto-scheduling |
| Namespace hierarchy | ⚠️ | Basic — (type,) prefix, not full (org, user, thread) |
| Entity extraction | ⚠️ | Regex works, LLM path untested |
| LangGraph checkpointer | ⚠️ | Code exists, untested |
| Observability (logging/metrics) | ⚠️ | Basic logging, no metrics |

### ❌ Not Implemented
| HLD Feature | Status | Priority |
|-------------|--------|----------|
| Redis backend | ❌ | Low (not needed for v1) |
| Server mode (REST API) | ❌ | v2 feature |
| Multi-tenancy | ❌ | Design supports it, not implemented |
| Custom memory types | ❌ | Registry supports it, no user-facing API |
| Semantic cache | ❌ | v2 feature |
| Working memory (session scratchpad) | ❌ | v2 feature |
| Persona memory type (complete) | ⚠️ | Stub exists |

### 🗑️ Things to Remove/Clean
| Item | Issue | Action |
|------|-------|--------|
| Pydantic MemoryUnit in types.py | Unused — dataclass is canonical | Keep as SearchResult/Filter only |
| registry.py (565 lines) | Overly complex, formatter stubs | Simplify — remove unused formatters |
| agents/base.py | Old custom base class | Already simplified ✅ |
| tools/executor.py (752 lines) | Old executor, partially replaced by BaseTool | Audit — keep what tools use |

## What Went Wrong
1. **Started with too many features** — HLD was ambitious (Redis, server mode, etc.)
2. **Dual MemoryUnit** — types.py Pydantic vs harness.py dataclass caused confusion
3. **Agent stubs** — First Claude Code session wrote 2700 lines of agent stubs that didn't work
4. **postgres.py** — 1613 lines of inline SQL, now being split

## What Went Right
1. **Core API is solid** — add/search/get pattern works well
2. **Modular architecture** — split into memory_types/ was the right call
3. **LangChain middleware** — aligns with modern LangChain architecture
4. **CI/CD pipeline** — every PR goes through lint+test+docs
5. **Feature branch workflow** — clean history, squash merges

## Priority for Next Work
1. ~~Postgres modularization~~ → PR #11 (in progress)
2. Complete remaining 7 memory type docs
3. Clean up registry.py (simplify)
4. Add middleware docs page
5. Integration tests with real LLM (optional, behind flag)

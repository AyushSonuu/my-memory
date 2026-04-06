# LLM Wiki Pattern — Karpathy vs Our Vault

> 📰 Source: [Andrej Karpathy's "LLM Wiki" gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (April 2026)
> Filed: 2026-04-06 — first use of Query → Wiki Filing rule!

---

## 🎯 One Line
> We're running the same architecture Karpathy described — raw sources → LLM-maintained wiki → schema. Ours is specialized for learning + teaching with spaced repetition, visual notes, and dual ingest.

---

## 🖼️ The Three-Layer Architecture

```
┌───────────────────────────────────────────────────────┐
│  LAYER 1: RAW SOURCES (immutable)                      │
│                                                        │
│  Karpathy: articles, papers, images in raw/            │
│  Us: transcripts, PDFs in course_material/, code/      │
│      + articles, tweets, URLs (KB mode)                │
├───────────────────────────────────────────────────────┤
│  LAYER 2: THE WIKI (LLM-maintained)                    │
│                                                        │
│  Karpathy: entity pages, summaries, concept pages      │
│  Us: lesson notes, READMEs, flashcards, cheatsheets,  │
│      vs.md, _maps/ — all LLM-generated                │
├───────────────────────────────────────────────────────┤
│  LAYER 3: THE SCHEMA (conventions)                     │
│                                                        │
│  Karpathy: CLAUDE.md / AGENTS.md                       │
│  Us: AGENTS.md + SOUL.md + _templates/                 │
└───────────────────────────────────────────────────────┘
```

## ⚖️ Full Comparison

| Dimension | Karpathy's LLM Wiki | Our `my-memory` Vault |
|-----------|---------------------|----------------------|
| **Purpose** | General-purpose knowledge management | Learning + teaching + knowledge base |
| **Raw sources** | `raw/` folder — articles, papers, images | `course_material/`, `code/`, chat transcripts, articles, URLs |
| **Wiki layer** | Flat markdown pages — entities, summaries | Hierarchical — topic/module/lesson with READMEs at every level |
| **Schema** | `CLAUDE.md` | `AGENTS.md` + `SOUL.md` + `_templates/` |
| **Index** | Single `index.md` | 6 map files in `_maps/` (everything, tech, non-tech, weak-spots, connections, journey) |
| **Log** | Single `log.md` (append-only) | `memory/YYYY-MM-DD.md` (daily) + `MEMORY.md` (curated long-term) — two-layer system |
| **Reader/IDE** | Obsidian (graph view) | MkDocs Material → GitHub Pages |
| **Search** | `qmd` vector search at scale | Hierarchy + maps + grep (sufficient at current scale) |
| **Ingest** | Single mode (can batch) | **Dual mode** — Deep Ingest (courses) + KB Ingest (articles/TILs) |
| **Revision** | None | Spaced repetition: Day 1→3→7→14→30→90 + flashcards |
| **Active recall** | None | Flashcards at every level with cross-topic pulls |
| **Visual style** | Plain reference text | Mermaid + ASCII + tables + emoji + Hinglish hooks |
| **Teaching** | Not a goal | Core goal — numbered files = instant video scripts |
| **Confidence tracking** | What exists vs not | 🟢🟡🔴 per topic + weak-spots map |
| **Health audit** | Lint operation | Tier 3 Monthly Lint (adopted from Karpathy) |
| **Synthesis filing** | Query answers → wiki pages | Query → Wiki Filing rule (adopted from Karpathy) |
| **Contradiction tracking** | Flags when new contradicts old | ⚡ Contradiction Markers (adopted from Karpathy) |

## 💡 What We Adopted (V3.3)

| From Karpathy | Our Implementation |
|---------------|-------------------|
| Lint operation | Tier 3 Monthly Lint → `_maps/lint-report.md` |
| Query → wiki filing | 10+ line answers touching 2+ topics → offer to file |
| Contradiction awareness | ⚡ markers inline + log in connections.md |
| KB as primary use case | Dual ingest — vault is now learning + knowledge base |

## 💡 What We Already Had (Better)

| Our Feature | Why It's Better |
|-------------|----------------|
| Two-layer memory (daily + MEMORY.md) | Better than single append-only log — raw + curated |
| 6 map files | More navigable than single index.md |
| Hierarchical structure | IS the search — no need for vector search at this scale |
| Spaced repetition | Knowledge without recall is useless — Karpathy's wiki has no revision system |
| Flashcards with cross-pulls | Active recall across topics |
| Visual-first + Hinglish hooks | Knowledge that sticks, not just knowledge that exists |

---

> 🧠 **The core insight both systems share:** "The wiki is a persistent, compounding artifact. The knowledge is compiled once and then kept current, not re-derived on every query." — Karpathy

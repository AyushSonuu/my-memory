# MEMORY.md — Ayra's Long-Term Memory

## Who I Am
- **Name:** Ayra (formerly Vidya — विद्या = Knowledge in Sanskrit)
- **Purpose:** Transform raw learning material into structured, visual, revision-ready knowledge
- **Human:** Ayush Sonu (@AyushSonuu on GitHub)

## My Workspace
- **Repo:** `~/Desktop/my-memory/`
- **GitHub:** `https://github.com/AyushSonuu/my-memory`
- **Git config:** user `AyushSonuu`, email `sonuayush55@gmail.com`
- **Templates:** `_templates/` — always follow them
- **Docs site:** MkDocs Material → `docs/` folder → GitHub Pages

## Ayush's Learning Preferences
- Diagram-first — visuals before text, use RIGHT tool per diagram
- Concise: tables > paragraphs, bullets > walls of text
- English for concepts, Hinglish for humor and hooks (but don't flood — scarcity = impact)
- Zero hallucination tolerance
- Values spaced repetition — flashcards matter
- Wants notes good enough to teach from (YouTube content pipeline)
- **Pure concepts only** — no meta-commentary, no placeholders, no filler
- **Beginner-friendly** — even zero-background readers should understand
- **Define every term** when first introduced

## Design Decisions (V3.2)
- Topic-centric: one folder = one topic
- Brain mode + Teach mode in every README
- Numbered files = teaching order
- Auto-maintained `_maps/` directory = the crown jewel
- Flashcards pull from related topics too
- Sub-folders only when 3+ lessons deep, max 5 levels
- Tier 1 sync (every edit) + Tier 2 sync (end of session)

## Design Decisions (V3.3 — Karpathy Update, 2026-04-06)
- **LLM Wiki pattern validated** — Andrej Karpathy independently described the exact same architecture. We're a specialized variant optimized for learning + teaching.
- **Vault is now BOTH learning vault + knowledge base** — not just course notes. Accepts articles, tweets, TILs, opinions, papers, podcast notes, links.
- **Dual ingest modes:** Deep Ingest (courses, one-at-a-time, full treatment) + KB Ingest (articles/TILs, lighter, batchable)
- **Tier 3 Monthly Lint added** — contradiction scan, orphan check, stale claims, missing pages. Write to `_maps/lint-report.md`
- **Query → Wiki Filing rule** — if a chat answer is 10+ lines and touches 2+ topics, file it into the vault. Chat dies, vault lives.
- **Contradiction markers (⚡)** — when new info contradicts old, mark inline + log in connections.md. Don't silently overwrite.
- **Three "skip" re-evaluations:** Search tooling (our hierarchy IS our search at current scale), structured logs (daily+MEMORY.md is better than flat log.md), batch ingest (now supported as KB Ingest mode)

## Topics Covered

### Agentic AI (tech/agentic-ai/) — 🟡 Complete (revision overdue)
- **Source:** DeepLearning.AI course by Andrew Ng
- **Structure:** 5 modules → each module = sub-folder with individual video lesson files
- **Progress:** 30/30 lessons — COURSE COMPLETE ✅ (M1: ✅, M2: ✅, M3: ✅, M4: ✅, M5: ✅)
- **⚠️ Revision overdue since Apr 6** — 15 days behind!
- **Workflow (decided 2026-03-24):**
  1. Each module has: `course_material/` (PDF from Ayush) + `code/` (Ayush's practice code)
  2. Ayush watches videos → sends transcripts one by one
  3. Ayra builds notes from **transcript + module PDF** (PDF = slides/reference, transcript = narration)
  4. If a video has code → Ayush puts it in `code/` folder → Ayra references it in notes
  5. **PDF lives at:** `module-{n}-xxx/course_material/*.pdf`
  6. **Code lives at:** `module-{n}-xxx/code/` (Ayush-managed, any structure)
- **4 Design Patterns:** Reflection, Tool Use, Planning, Multi-Agent

### Agent Memory (tech/agent-memory/) — 🟡 Learning
- **Source:** DeepLearning.AI × Oracle course
- **Progress:** 7/7 lessons COMPLETE ✅
- **5 building blocks:** Memory Modeling, Semantic Retrieval, Extraction, Consolidation, Write-Back
- **Has:** cheatsheet.md ✅, vs.md (RAG vs Agent Memory) ✅

### AsyncIO (tech/python/asyncio/) — 🟡 Learning
- **Source:** Corey Schafer YouTube (1hr 42min)
- **Progress:** 1/1 lesson COMPLETE ✅
- **Key concepts:** Event Loop, Coroutines, Tasks, gather vs TaskGroup, to_thread, ProcessPoolExecutor, Semaphores
- **Has:** 7 code examples + terms.py, animations repo

### Spec-Driven Development (tech/spec-driven-development/) — 🟡 Nearly Complete
- **Source:** DeepLearning.AI × JetBrains course by Paul Everitt
- **Structure:** 16 video lessons (flat, no modules)
- **Progress:** 13/16 lessons done (L04/L05 = setup skipped, L16 = pending)
- **Key concept:** Write markdown specs → coding agent implements. Constitution + feature loops.
- **Connects to:** Agentic AI (guides coding agents), Tool Use, Planning patterns

### RAG (tech/rag/) — 🔴 In Progress
- **Source:** DeepLearning.AI course (5 modules, 62 lessons)
- **Progress:** M1: 7/10, M2: 1/12, M3-M5: not started (8/62 total)
- **M2 PDF:** 85 pages of course material ready
- **Key concepts so far:** RAG architecture, retriever + LLM + KB, applications, LLM foundations, IR basics
- **Workflow:** Same as Agentic AI (transcript + PDF cross-reference)

## Conventions & Decisions

### Code Folder (decided 2026-03-21)
- Each topic can have a `code/` folder — **Ayush manages it**, Ayra reads from it
- Structure: `code/L{n}/` per lesson → `L{n}.ipynb` or `L{n}.py` + supporting files
- Not every lesson has code — only when Ayush practices
- **When writing notes for a lesson, ALWAYS check `code/L{n}/` first**
- Code informs notes, not vice versa

### Visual Style (decided 2026-03-21)
- **Mermaid** → cycles, relationships, hierarchies, flows, convergence
- **ASCII** → simple stacks, context window layouts
- **Tables** → comparisons, features, cheat sheets
- **Don't force one tool** — use what fits THAT diagram best
- On global pages (README, maps): **don't use custom Mermaid fills** — let theme handle colors (works in both dark/light)
- In lesson notes: custom fills are fine (always dark-mode context)

### Docs Site (decided 2026-03-21)
- **MkDocs Material** — LangChain-style docs
- **Theme:** Green accent, Inter font, dark/light toggle
- **Build command:** `.venv/bin/python build_docs.py`
  - Auto-generates .py → rendered markdown wrappers
  - Renders .ipynb via mkdocs-jupyter
  - Builds full static site in `docs/`
  - Adds `.nojekyll`
- **Deploy:** GitHub Pages from `docs/` folder on main branch
- **Nav structure:** Tabs per major topic (Home, Agent Memory, Python)
- **When adding new topic:** update `mkdocs.yml` nav section
- **Venv:** `.venv/` with Python 3.12, mkdocs-material + mkdocs-jupyter

## Agent OS (V4.0 — 2026-04-07)
- **Brainchild from Ayush:** Self-extending agent architecture
- **`_tools/`** — self-created, tested, versioned executable tools
  - **Stack:** uv 0.11.3 + Python 3.13.12 + pyproject.toml + ruff + mypy + pytest
  - **Architecture:** uv workspace — root (ayra-tools) + lib (ayra-lib) + tools/* (each tool = workspace member)
  - **Shared lib (ayra-lib):** VaultConfig, Flashcard/QuizResult/ToolMeta types, VaultFlashcardParser, CardSource Protocol, registry ops
  - First tool: `flashcard-quiz` (v1.0.0, 27/27 tests, ruff clean, SOLID-compliant)
  - **SOLID enforced:** SRP per module, DI via Protocols, frozen dataclasses, composition root pattern
  - **Universal Tool Interface (BaseTool):** agent-agnostic execution protocol
    - `--schema` → JSON introspection (any agent can discover inputs/outputs)
    - `--input '{...}'` → programmatic mode (JSON in → ToolOutput JSON out, no terminal I/O)
    - `--topic foo` → interactive mode (pretty terminal for humans)
    - ToolOutput envelope: `{status, tool, version, data, message, errors, timestamp}`
    - Input validation + defaults + error handling built into base class
  - **Run:** `cd _tools && uv run flashcard-quiz --topic agent-memory`
- **`_agent/`** — AGENTS.md decomposed into kernel + 6 on-demand modules (Phase 2 DONE)
  - Kernel: 126 lines (identity, startup, tools, memory, golden rules summary, git, don'ts)
  - Modules: workflows, golden-rules, structure, sync-checklist, docs-site, planning
  - 22/22 key concepts verified — zero content dropped
  - Load only what's needed per task → massive context savings
- **`_db/`** — future brainchild: SQLite (chat history), ChromaDB (semantic search), GraphDB (relationships)
- **Memory restructured** — flat `memory/` → `memory/YYYY/MM/daily.md` + monthly README summaries + yearly README
- **Full plan:** `plans/agent-os.md`

## Lessons Learned
- 🎨 **Right visual for the job:** Mermaid for cycles/relationships, ASCII for stacks, tables for comparisons. Mix for variety.
- 📝 **Always wait for transcript/screenshots before finalizing** — initial drafts miss details
- 💻 **Check code folder before writing lesson notes** — code shows what was actually practiced
- 🚫 **No meta-commentary in lesson files** — no "Placeholder", "Direct from source", "Confidence: X" at top
- 🎯 **Define every term when first introduced** — never assume it's self-explanatory
- 😄 **Hinglish analogies only where needed** — scarcity = impact. If concept is already clear, don't force a joke.
- 🗣️ **Hinglish ONLY in `> 💡` blockquote hooks** — definitions, one-liners, table cells, and explanations must be clean English. Hinglish is reserved exclusively for the fun memory-anchor blockquotes.
- 🗺️ **Global Mermaid diagrams: no custom fills** — let theme handle colors for dark/light compatibility
- 🌐 **Always run `build_docs.py` after content changes** — single command handles everything
- 📄 **ALWAYS cross-reference module PDFs when writing notes** — PDFs have specific names (models, papers, systems), exact benchmark numbers, and slide diagrams that transcripts miss. Install: `pymupdf` (already in .venv). PDF path: `module-{n}-xxx/course_material/*.pdf`. Read EVERY page and patch missing details.
- 🔍 **Never trust maps alone for search** — maps are Tier 2 (can be stale). Always `grep` the filesystem when answering questions or checking if content exists. Maps = TOC, filesystem = Ctrl+F.
- 🖼️ **SVGs → ALWAYS standalone files in `assets/` folder, NEVER inline in markdown.** Inline `<svg>` blocks don't render in GitHub/MkDocs/most viewers. Save as `assets/{nn}-{slug}.svg`, reference with `![alt](assets/file.svg)`. Escape `&` → `&amp;` (it's XML). Learned the hard way on RAG module 2 lessons 04/05/07.
- ✂️ **Concise ≠ incomplete. Say everything ONCE, not three times.** Caught on RAG lesson 04. The sin was NOT "too much content" — it was the SAME content repeated in ASCII + table + prose + UX table (4 formats for 1 concept). **Rules: (1) Every concept MUST be present — drop nothing. (2) But say it ONCE with the RIGHT visual — if the diagram covers it, don't restate in prose. (3) Definitions stay as-is, exact. (4) Completeness + visual appeal + high recall = the goal. NOT fewer concepts.**

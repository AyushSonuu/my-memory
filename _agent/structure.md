# Repo Structure & Conventions

> Load this module when: creating new topics/files, finding where things go, understanding folder layout

## Repo Structure

```
my-memory/
├── README.md                              # 🏠 Portal + stats
├── AGENTS.md                              # Kernel (slim — references _agent/)
├── .gitignore
│
├── _agent/                                # 📦 Modular agent knowledge (on-demand)
│   ├── workflows.md                       # Ingest modes (Deep + KB)
│   ├── golden-rules.md                    # Content quality rules
│   ├── structure.md                       # This file — repo layout + conventions
│   ├── sync-checklist.md                  # Tier 1/2/3 sync procedures
│   └── docs-site.md                       # MkDocs build + nav rules
│
├── _tools/                                # 🔧 Self-created executable tools
│   ├── README.md                          # Discovery index
│   ├── registry.json                      # Machine-readable index
│   ├── lib/                               # Shared library (ayra-lib)
│   └── tools/                             # Individual tools
│
├── tech/                                  # All technical topics
│   ├── README.md                          # 🗺️ Tech mega-map (auto-maintained)
│   └── {topic}/                           # One folder per topic
│       ├── README.md                      # 🧠 Brain + 🎬 Teach
│       ├── 01-xxx.md                      # Numbered = teaching order
│       ├── flashcards.md                  # 🃏 Self + children + related
│       ├── vs.md                          # (optional) Comparisons
│       ├── cheatsheet.md                  # (optional) One-pager
│       ├── _assets/                       # (optional) Screenshots, slides
│       ├── code/                          # (optional) Ayush-managed practice code
│       ├── course_material/               # (optional) PDFs from courses
│       └── sub-topic/                     # (optional) 3+ lessons deep
│
├── non-tech/                              # All non-technical topics
│   ├── README.md                          # 🗺️ Non-tech mega-map
│   └── {topic}/
│
├── plans/                                 # 📋 Action plans & trackers (NOT notes!)
│   ├── README.md                          # Index of all active plans
│   ├── weekly/                            # 📅 Weekly planners
│   └── *.md                              # Individual plans/trackers
│
├── memory/                                # 📝 Session logs (hierarchical)
│   └── YYYY/MM/YYYY-MM-DD.md            # + monthly/yearly READMEs
│
├── _maps/                                 # 🗺️ AUTO-MAINTAINED (crown jewel!)
│   ├── everything.md                      # God map
│   ├── tech.md / non-tech.md             # Category graphs
│   ├── weak-spots.md                      # All 🔴
│   ├── connections.md                     # Cross-topic links (rolling last 30)
│   ├── learning-journey.md               # Gantt timeline
│   └── lint-report.md                    # Monthly health audit
│
├── _revision/                             # Spaced repetition
│   ├── tracker.json                       # Topic schedules
│   └── due-today.md                       # What needs revision today
│
├── _playlists/                            # YouTube content planning ONLY
├── _social/                               # LinkedIn, Twitter, blog posts
├── _templates/                            # Blueprints — READ before creating!
├── .venv/                                 # MkDocs env (separate from _tools/.venv)
├── mkdocs.yml                             # Docs site config
└── build_docs.py                          # Docs builder
```

## The `code/` Folder Convention

**Each topic can have a `code/` folder — managed by Ayush, referenced by Ayra.**

Ayush organizes code however he wants inside `code/`. There's no strict structure — he may use:
- `code/L3/L3.ipynb` (lesson-based folders)
- `code/example_1.py` (flat files)
- `code/terms.py` (standalone scripts)
- `code/some_folder/script.py` (custom grouping)
- Any mix of `.py`, `.ipynb`, `.js`, or other files

**Rules:**
1. **`code/` is Ayush-managed** — he creates folders, writes code, names files. Ayra does NOT write/edit code here.
2. **No fixed naming convention** — Ayush names things however makes sense to him.
3. **Not every topic has code** — only when Ayush actually practices.
4. **Ayra references code when writing notes** — when creating/updating a lesson's notes, check `code/` for that topic. Incorporate relevant code snippets, patterns, or observations into the notes.
5. **Code informs notes, not vice versa** — if the code shows something the transcript/slides don't cover, mention it.
6. **For docs site:** all `.py` files inside `code/` are auto-rendered by `build_docs.py`. `.ipynb` files need manual entry in `mkdocs.yml` nav.

## Key Structure Rules

**1. Topics go DIRECTLY under `tech/` or `non-tech/`**
- ✅ `tech/kafka/` `tech/docker/` `tech/redis/`
- ❌ `tech/messaging/kafka/` — NO grouping folders. Topics at root.

**2. Same pattern at EVERY level (fractal 🪆)**
```
{any-folder}/
├── README.md          # 🧠 Brain + 🎬 Teach
├── 01-xxx.md          # Numbered lessons (teaching order)
├── flashcards.md      # 🃏 Self + children + related pulls
├── vs.md              # (optional)
├── cheatsheet.md      # (optional)
├── _assets/           # (optional)
└── sub-topic/         # (optional) — same pattern repeats
```

**3. Sub-folders inside topics ONLY when:**
- An area needs **3+ dedicated lessons**

**4. Max depth: 5 levels**
```
tech / kafka / internals / kraft / ... STOP
  1      2        3         4      5 = max
```

**5. Every folder MUST have:**
- `README.md` — mandatory (brain + teach)
- `flashcards.md` — mandatory (revision is core)
- Numbered lessons — at least one

## README.md — Dual Purpose (Brain + Teach)

Every topic README has TWO halves:

**🧠 Brain Mode (top):**
- Mermaid connection graph → how this topic links to others
- Progress table → confidence per lesson (🟢🟡🔴)
- Memory fragments → random "aha!" moments accumulated over time
- Connected topics → links to related folders

**🎬 Teach Mode (bottom):**
- Numbered lesson flow table → open in order = teach anyone
- Sources → where the knowledge came from
- 30-second recall → quick revision paragraph

## Flashcards — Multi-Level Pull System

```
tech/kafka/flashcards.md
  ← pulls from: kafka's own lessons
  ← pulls from: kafka/internals/, kafka/ecosystem/ (children)
  ← pulls from: ../rabbitmq/, ../redis/ (related topics)

tech/kafka/internals/flashcards.md
  ← pulls from: internals lessons only (focused)
```

**Zoom levels for revision:**
- `kafka/flashcards.md` → broad Kafka quiz
- `kafka/internals/flashcards.md` → deep internals quiz
- Multiple topics' cards get cross-pulled for comparison

## Templates
Always read and follow `_templates/` blueprints before creating content. They are the law.

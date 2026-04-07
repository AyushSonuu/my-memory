# Repo Structure & Conventions

> Load this module when: creating new topics, finding files, understanding folder layout

## Repo Structure

```
my-memory/
├── README.md                              # 🏠 Portal + stats
├── AGENTS.md                              # Kernel (slim — refs _agent/)
├── _agent/                                # Modular agent knowledge (this folder)
├── _tools/                                # Self-created executable tools
├── .gitignore                             # Excludes OpenClaw workspace files
│
├── tech/                                  # All technical topics
│   ├── README.md                          # 🗺️ Tech mega-map (auto-maintained)
│   ├── kafka/                             # Topic: directly under tech/
│   │   ├── README.md                      # 🧠 Brain + 🎬 Teach
│   │   ├── 01-why-kafka.md                # Numbered = teaching order
│   │   ├── vs.md                          # Comparisons
│   │   ├── cheatsheet.md                  # One-pager
│   │   ├── flashcards.md                  # 🃏 Self + children + related
│   │   ├── _assets/                       # Screenshots, slide images
│   │   ├── internals/                     # Sub-topic (3+ lessons deep)
│   │   └── ecosystem/                     # Another sub-topic
│   └── ...
│
├── non-tech/                              # All non-technical topics
│   ├── README.md                          # 🗺️ Non-tech mega-map
│   └── ...
│
├── plans/                                 # 📋 Action plans & trackers (NOT notes!)
│   ├── README.md                          # Index of all active plans
│   ├── roadmap.md                         # Master roadmap 2026-27
│   ├── weekly/                            # 📅 Weekly planners (1 file per week)
│   └── ...
│
├── memory/                                # Session logs (year/month hierarchy)
│   └── YYYY/MM/YYYY-MM-DD.md
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
│
└── _templates/                            # Blueprints — READ before creating!
    ├── topic-readme.md
    ├── lesson.md
    ├── flashcards.md
    ├── cheatsheet.md
    └── vs.md
```

## The `code/` Folder Convention

**Each topic can have a `code/` folder — managed by Ayush, referenced by Ayra.**

Ayush organizes code however he wants inside `code/`. There's no strict structure — he may use:
- `code/L3/L3.ipynb` (lesson-based folders)
- `code/example_1.py` (flat files)
- `code/terms.py` (standalone scripts)
- Any mix of `.py`, `.ipynb`, `.js`, or other files

**Rules:**
1. **`code/` is Ayush-managed** — he creates folders, writes code, names files. Ayra does NOT write/edit code here.
2. **No fixed naming convention** — Ayush names things however makes sense to him.
3. **Not every topic has code** — only when Ayush actually practices.
4. **Ayra references code when writing notes** — check `code/` for that topic. Incorporate relevant code snippets, patterns, or observations into the notes.
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
├── vs.md              # (optional) comparisons
├── cheatsheet.md      # (optional) one-pager
├── _assets/           # (optional) images/screenshots
└── sub-topic/         # (optional) goes deeper — same pattern
```

**3. Sub-folders ONLY when:** An area needs **3+ dedicated lessons**

**4. Max depth: 5 levels**
```
tech / kafka / internals / kraft / ... STOP
  1      2        3         4      5 = max
```

**5. Every folder MUST have:** README.md + flashcards.md + numbered lessons

## README.md — Dual Purpose (Brain + Teach)

**🧠 Brain Mode (top):**
- Mermaid connection graph → how this topic links to others
- Progress table → confidence per lesson (🟢🟡🔴)
- Memory fragments → random "aha!" moments
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
```

**Zoom levels for revision:**
- `kafka/flashcards.md` → broad Kafka quiz
- `kafka/internals/flashcards.md` → deep internals quiz

## Templates
Always read and follow `_templates/` blueprints before creating content. They are the law.

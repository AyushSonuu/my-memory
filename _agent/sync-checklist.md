# Sync System — Tier 1/2/3 + Scaling + Search + Revision

> Load this module when: after creating/updating content, doing vault maintenance, or session end

## 🔄 AUTO-SYNC SYSTEM (THE GLUE THAT HOLDS EVERYTHING TOGETHER)

Every time you create or edit ANY content, the vault must stay in sync. But be SMART about it — sync in two tiers.

### ⚡ TIER 1: Always Sync (on EVERY edit)
These are local/cheap — always do them:

| What | Action |
|------|--------|
| **Topic README** | Update brain (connections, progress table, memory fragments) + teach (lesson flow) + sources + 30-sec recall |
| **Topic flashcards** | Add new Q&A + pull from children + pull from related topics |
| **Parent flashcards** | If nested, update parent's flashcards too |
| **`_revision/tracker.json`** | Add/update topic entry with dates + confidence |
| **Parent folder README** | Update the immediate parent's topic table |

### 🗺️ TIER 2: Batch Sync (after a session / when asked / periodically)
These touch global files — do them at END of a learning session, not after every tiny edit:

| What | Action |
|------|--------|
| **`_maps/everything.md`** | Rebuild god-level graph — categories + topics + connections + confidence colors |
| **`_maps/tech.md`** or **`non-tech.md`** | Rebuild category graph with topics + sub-topics |
| **`_maps/weak-spots.md`** | Rescan all 🔴 areas + suggestions |
| **`_maps/connections.md`** | Log new cross-topic connections (keep last 30 only) |
| **`_maps/learning-journey.md`** | Update gantt timeline |
| **`tech/README.md`** or **`non-tech/README.md`** | Update category overview map + table |
| **Root `README.md`** | Update stats (topic count, lessons, flashcards, last updated) |
| **`_revision/due-today.md`** | Regenerate from tracker.json |
| **`mkdocs.yml`** | Update `nav:` section when adding new topics/lessons. |
| **Docs rebuild** | Update nav → run `.venv/bin/python build_docs.py` → commit & push. See `_agent/docs-site.md` for nav patterns. |

**Why two tiers?** Rewriting 8 global files on every small edit wastes tokens and slows you down. Topic-level files = always. Global views + docs rebuild = batched.

### Quick Sync Checklist
```
EVERY edit (Tier 1):
  ☐ Topic README updated
  ☐ Topic flashcards updated  
  ☐ Parent flashcards updated (if nested)
  ☐ _revision/tracker.json updated

End of session / when asked (Tier 2):
  ☐ _maps/* rebuilt
  ☐ Category + Root READMEs updated
  ☐ _revision/due-today.md regenerated
  ☐ mkdocs.yml nav updated (if new pages added)
  ☐ Docs rebuilt (.venv/bin/python build_docs.py) & pushed
```

## 🚨 SCALING RULES (for when vault grows past ~25 topics)

**`_maps/everything.md` — Summary, NOT exhaustive:**
- Show CATEGORIES + topic count + top 5 strongest connections
- NOT every single topic as a node

**`tech/README.md` — Topics only, NOT sub-topics:**
- Show topic names + confidence + last updated
- Each topic's own README handles its internal depth

**`connections.md` — Rolling log, NOT infinite:**
- Keep only last 30 connections
- Older connections live in topic READMEs (source of truth)

**`learning-journey.md` — Current year only:**
- Archive older years into `_maps/archive/journey-2026.md`

**Mermaid confidence colors (always):**
- 🟢 `fill:#4caf50,color:#fff` — Solid understanding
- 🟡 `fill:#ff9800,color:#fff` — Learning / Okay
- 🔴 `fill:#f44336,color:#fff` — Weak / Todo

## Spaced Repetition

Update `_revision/tracker.json`:
```json
{
  "tech/kafka": {
    "firstLearned": "2026-03-20",
    "lastRevised": "2026-03-20",
    "nextRevision": "2026-03-23",
    "confidence": "yellow",
    "revisionCount": 0
  }
}
```
Schedule: Day 1 → Day 3 → Day 7 → Day 14 → Day 30 → Day 90

## 🔍 Search Strategy (How Ayra Finds Things)

| Layer | What It Is | When to Use | Staleness Risk |
|-------|-----------|-------------|----------------|
| **`_maps/` + READMEs** | Curated navigation | Session startup orientation | ⚠️ Can be stale |
| **Filesystem** (`grep`, `find`) | Raw search | Answering questions, finding content | ✅ Always accurate |

**Rules:**
1. **Answering a question?** → `grep -r "keyword" tech/ --include="*.md"` FIRST
2. **Starting a session?** → Read `_maps/` + READMEs for orientation
3. **Filing new content?** → Check filesystem for what already exists
4. **Never say "we don't have notes on X"** without a filesystem search

## 🧹 TIER 3: Monthly Lint (1st of month or on request)

```
Monthly Lint Checklist:
  ☐ Contradiction scan — do any topics explain the same concept differently?
  ☐ Orphan check — pages with no inbound links from READMEs or _maps
  ☐ Stale claims — topics with confidence 🟢 but lastRevised > 60 days ago
  ☐ Missing pages — concepts referenced in notes but lacking their own page
  ☐ Flashcard freshness — any flashcards referencing outdated content?
  ☐ Connection gaps — topics that SHOULD be linked but aren't
  ☐ Memory Fragment review — promote valuable fragments to full lessons if they've grown
  ☐ KB orphans — insights filed in fragments that deserve their own page now
  ☐ Map drift check — do _maps/ and READMEs match what actually exists on filesystem?
  ☐ Write findings to _maps/lint-report.md
```

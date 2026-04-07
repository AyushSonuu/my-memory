# 🔍 Tool Opportunity Audit — Ayra's Repeated Manual Workflows

> Audited: 2026-04-07
> Rule: If I do the same steps 3+ times manually, it becomes a tool.

## Hardcoded Workflows I Repeat Every Session

### 1. 🔄 Tier 1 Sync (EVERY edit — highest frequency)
**What I do manually every time:**
- Open topic README → find progress table → update row
- Open flashcards.md → add new Q&A blocks → check cross-topic pulls
- Open parent flashcards → add cross-pulls
- Open _revision/tracker.json → update dates/confidence

**Repetition:** Every single lesson. 30+ times so far.
**Automation value:** 🔴 HIGHEST — this is my #1 time sink.
**Tool:** `tier1-sync` — given a topic + lesson, auto-update README progress, flashcards count, tracker.json dates

---

### 2. 🗺️ Tier 2 Sync (end of session — medium frequency)
**What I do manually:**
- Rebuild all 6 `_maps/` files (everything, tech, weak-spots, connections, learning-journey, non-tech)
- Update tech/README.md stats
- Update root README.md stats
- Regenerate _revision/due-today.md
- Update mkdocs.yml nav
- Run build_docs.py
- Git commit + push

**Repetition:** Every session end. 10+ times so far.
**Automation value:** 🔴 HIGH — 7 files touched, same pattern every time.
**Tool:** `tier2-sync` — scan vault state, rebuild all global files, update docs nav

---

### 3. 📊 Revision Check (session startup)
**What I do manually:**
- Read _revision/tracker.json
- Calculate what's overdue vs due today
- Report to Ayush

**Repetition:** Every session startup.
**Automation value:** 🟡 MEDIUM — simple date math but I do it every time.
**Tool:** `revision-check` — read tracker.json, compute due/overdue, return structured report

---

### 4. 📈 Vault Stats (when asked or for README updates)
**What I do manually:**
- Count topics across tech/
- Count total lessons (numbered .md files)
- Count total flashcards (parse all flashcards.md)
- Count docs pages
- Compile into stats table

**Repetition:** Every Tier 2 sync + when Ayush asks.
**Automation value:** 🟡 MEDIUM — pure filesystem counting, perfect for automation.
**Tool:** `vault-stats` — scan vault, return counts for topics, lessons, flashcards, code files, docs pages

---

### 5. 🔗 Link Checker (should be part of Tier 3 lint)
**What I do manually:**
- Read READMEs, check if referenced files exist
- Check _maps/ entries against actual filesystem
- Find orphan pages with no inbound links

**Repetition:** Monthly lint + whenever something feels off.
**Automation value:** 🟡 MEDIUM
**Tool:** `vault-lint` — check broken links, orphan pages, stale claims, map drift

---

### 6. 📝 Memory Summary (month transitions)
**What I do manually:**
- Read all daily logs for the month
- Summarize into monthly README
- Update yearly README

**Repetition:** Monthly.
**Automation value:** 🟢 LOW (monthly, but still manual pattern).
**Tool:** Part of planning ritual — can wait.

---

## Priority Order (by automation value × frequency)

| # | Tool | Frequency | Value | Build When |
|---|------|-----------|-------|------------|
| 1 | `vault-stats` | Every Tier 2 + on-demand | 🟡 | NOW — simplest, enables others |
| 2 | `revision-check` | Every session | 🟡 | NOW — simple date math |
| 3 | `tier1-sync` | Every edit | 🔴 | NEXT — most impactful but complex |
| 4 | `tier2-sync` | Every session end | 🔴 | NEXT — depends on vault-stats |
| 5 | `vault-lint` | Monthly | 🟡 | LATER — Tier 3 monthly |

## Decision

**Ayra should build tools when she notices she's doing the same manual steps 3+ times.
This is not a future plan — it's a standing rule. See it, automate it.**

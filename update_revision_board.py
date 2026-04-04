#!/usr/bin/env python3
"""
update_revision_board.py — Auto-updates the revision board on README.md homepage.

Reads _revision/tracker.json, generates the "Upcoming Revisions" table,
updates README.md in-place, rebuilds docs, and pushes to GitHub.

Run manually:  .venv/bin/python update_revision_board.py
Cron (daily):  Configured via `crontab -e`

Schedule reference (spaced repetition):
  Day 1 → Day 3 → Day 7 → Day 14 → Day 30 → Day 90
"""

import json
import re
import subprocess
import sys
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).parent
TRACKER = ROOT / "_revision" / "tracker.json"
README = ROOT / "README.md"

# Topic display config: path → (emoji, short name, flashcard path)
TOPIC_META = {
    "tech/agent-memory":           ("🧠", "Agent Memory",     "tech/agent-memory/flashcards.md"),
    "tech/agentic-ai":             ("🤖", "Agentic AI",       "tech/agentic-ai/flashcards.md"),
    "tech/python/asyncio":         ("⚡", "AsyncIO",          "tech/python/asyncio/flashcards.md"),
    "tech/python/threading":       ("🧵", "Threading",        "tech/python/threading/flashcards.md"),
    "tech/python/multiprocessing": ("⚙️", "Multiprocessing",  "tech/python/multiprocessing/flashcards.md"),
    "tech/rag":                    ("🔍", "RAG",              "tech/rag/flashcards.md"),
}

REVISION_SCHEDULE = [3, 7, 14, 30, 90]  # Days between revisions

TODAY = date.today()


def get_round_label(revision_count: int, next_date: date) -> str:
    """Generate a human-readable round label."""
    if revision_count >= len(REVISION_SCHEDULE):
        day_gap = 90
    else:
        day_gap = REVISION_SCHEDULE[revision_count]

    round_num = revision_count + 1
    label = f"Round {round_num} — Day {day_gap}"

    if next_date < TODAY:
        label += " (overdue!)"

    return label


def get_status_icon(next_date: date) -> str:
    """Return status emoji based on urgency."""
    delta = (next_date - TODAY).days
    if delta < 0:
        return "🔴"       # overdue
    elif delta == 0:
        return "🟠"       # due today
    elif delta <= 3:
        return "🟡"       # due soon
    else:
        return "📅"       # upcoming


def generate_revision_table() -> str:
    """Read tracker.json and generate the markdown revision table."""
    with open(TRACKER) as f:
        tracker = json.load(f)

    rows = []
    for path, data in tracker.items():
        next_rev = data.get("nextRevision")
        if not next_rev:
            continue

        next_date = date.fromisoformat(next_rev)
        confidence = data.get("confidence", "red")
        revision_count = data.get("revisionCount", 0)
        lessons = data.get("lessonsCompleted", 0)

        # Skip topics with 0 lessons (nothing to revise yet)
        if lessons == 0:
            continue

        meta = TOPIC_META.get(path, ("📚", path.split("/")[-1].title(), f"{path}/flashcards.md"))
        emoji, name, flashcard_path = meta

        status = get_status_icon(next_date)
        round_label = get_round_label(revision_count, next_date)
        date_str = next_date.strftime("%b %d")

        rows.append((
            next_date,
            f"| {status} **{date_str}** | {emoji} {name} | {round_label} | [→ cards]({flashcard_path}) |"
        ))

    # Sort by date (soonest first)
    rows.sort(key=lambda x: x[0])

    if not rows:
        return "| — | No revisions scheduled | — | — |"

    return "\n".join(row[1] for row in rows)


def generate_stats() -> dict:
    """Calculate current vault stats from tracker."""
    with open(TRACKER) as f:
        tracker = json.load(f)

    total_topics = len(tracker)
    total_lessons = sum(d.get("lessonsCompleted", 0) for d in tracker.values())

    return {
        "topics": total_topics,
        "lessons": total_lessons,
        "date": TODAY.strftime("%Y-%m-%d"),
    }


def update_readme(revision_table: str, stats: dict):
    """Update README.md with new revision table and stats."""
    content = README.read_text()

    # Update revision table (between markers)
    revision_section = (
        "| Date | Topic | Round | Flashcards |\n"
        "|------|-------|-------|------------|\n"
        f"{revision_table}"
    )
    content = re.sub(
        r"\| Date \| Topic \| Round \| Flashcards \|.*?(?=\n---|\n\n## )",
        revision_section + "\n",
        content,
        flags=re.DOTALL,
    )

    # Update stats
    content = re.sub(
        r"\| \*\*Topics\*\* \| \d+ \|",
        f"| **Topics** | {stats['topics']} |",
        content,
    )
    content = re.sub(
        r"\| \*\*Lessons\*\* \| \d+ \|",
        f"| **Lessons** | {stats['lessons']} |",
        content,
    )
    content = re.sub(
        r"\| \*\*Last updated\*\* \| [\d-]+ \|",
        f"| **Last updated** | {stats['date']} |",
        content,
    )

    README.write_text(content)


def update_due_today():
    """Generate _revision/due-today.md."""
    with open(TRACKER) as f:
        tracker = json.load(f)

    due_path = ROOT / "_revision" / "due-today.md"
    lines = [
        f"# 📅 Revisions Due — {TODAY.strftime('%A, %B %d, %Y')}\n",
        "> Auto-generated by `update_revision_board.py`\n",
        "---\n",
    ]

    overdue = []
    due = []
    upcoming = []

    for path, data in tracker.items():
        next_rev = data.get("nextRevision")
        lessons = data.get("lessonsCompleted", 0)
        if not next_rev or lessons == 0:
            continue

        next_date = date.fromisoformat(next_rev)
        meta = TOPIC_META.get(path, ("📚", path.split("/")[-1].title(), f"{path}/flashcards.md"))
        emoji, name, fc = meta
        delta = (next_date - TODAY).days

        entry = f"- {emoji} **{name}** — [flashcards]({fc}) (next: {next_date.strftime('%b %d')})"

        if delta < 0:
            overdue.append(entry)
        elif delta == 0:
            due.append(entry)
        elif delta <= 3:
            upcoming.append(entry)

    if overdue:
        lines.append("## 🔴 Overdue\n")
        lines.extend(overdue)
        lines.append("")
    if due:
        lines.append("## 🟠 Due Today\n")
        lines.extend(due)
        lines.append("")
    if upcoming:
        lines.append("## 🟡 Due in 1-3 Days\n")
        lines.extend(upcoming)
        lines.append("")
    if not overdue and not due and not upcoming:
        lines.append("## ✅ All clear! Nothing due today or in the next 3 days.\n")

    due_path.write_text("\n".join(lines))


def build_and_push():
    """Rebuild docs and push to GitHub."""
    venv_python = ROOT / ".venv" / "bin" / "python"

    print("📦 Building docs...")
    subprocess.run([str(venv_python), "build_docs.py"], cwd=ROOT, check=True)

    print("📤 Committing and pushing...")
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)

    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=ROOT,
    )
    if result.returncode == 0:
        print("✅ No changes to commit.")
        return

    subprocess.run(
        ["git", "commit", "-m", f"🔄 revision: auto-update revision board ({TODAY})"],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, check=True)
    print("✅ Pushed!")


def main():
    print(f"📅 Updating revision board for {TODAY}...")

    revision_table = generate_revision_table()
    stats = generate_stats()

    update_readme(revision_table, stats)
    print("✅ README.md updated")

    update_due_today()
    print("✅ _revision/due-today.md updated")

    build_and_push()
    print("🎉 Done!")


if __name__ == "__main__":
    main()

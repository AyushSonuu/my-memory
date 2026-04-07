#!/usr/bin/env python3
"""
flashcard-quiz: Interactive CLI quiz from vault flashcards.

Parses the <details>/<summary> format used in the vault's flashcards.md files,
presents questions interactively, and tracks score.

Usage:
    python run.py --topic agent-memory
    python run.py --topic agent-memory --count 5
    python run.py --topic agent-memory --count 0 --mode sequential
    python run.py --topic python/asyncio --show-hint
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path

# Add _lib to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib" / "python"))


def find_flashcards_file(topic: str) -> Path | None:
    """Find flashcards.md for a given topic."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    tech_root = repo_root / "tech"

    # Try direct path: tech/{topic}/flashcards.md
    direct = tech_root / topic / "flashcards.md"
    if direct.exists():
        return direct

    # Try searching recursively
    for p in tech_root.rglob("flashcards.md"):
        if topic in str(p):
            return p

    return None


def parse_flashcards(file_path: Path) -> list[dict]:
    """
    Parse flashcards from the vault's <details>/<summary> format.
    
    Expected format:
        ### 📌 Section Name (Lesson X)
        
        <details markdown="1">
        <summary>❓ Question text</summary>
        
        Answer content (can be multi-line, include tables, code, etc.)
        </details>
    """
    content = file_path.read_text(encoding="utf-8")
    cards = []

    # Find all <details> blocks
    # Pattern: <details...> <summary>...question...</summary> ...answer... </details>
    pattern = re.compile(
        r'<details[^>]*>\s*<summary>\s*❓\s*(.*?)\s*</summary>\s*(.*?)\s*</details>',
        re.DOTALL
    )

    # Also track which section each card belongs to
    current_section = "General"
    lines = content.split('\n')
    section_map = {}  # line_number -> section_name

    for i, line in enumerate(lines):
        section_match = re.match(r'^###\s*📌\s*(.+?)(?:\s*\(.*?\))?\s*$', line)
        if section_match:
            current_section = section_match.group(1).strip()
        if '<details' in line:
            section_map[i] = current_section

    # Parse all flashcard blocks
    for match in pattern.finditer(content):
        question = match.group(1).strip()
        answer = match.group(2).strip()

        # Clean up answer: remove leading/trailing blank lines
        answer_lines = answer.split('\n')
        while answer_lines and not answer_lines[0].strip():
            answer_lines.pop(0)
        while answer_lines and not answer_lines[-1].strip():
            answer_lines.pop()
        answer = '\n'.join(answer_lines)

        # Find which section this card belongs to
        card_pos = content[:match.start()].count('\n')
        section = "General"
        for line_num in sorted(section_map.keys()):
            if line_num <= card_pos:
                section = section_map[line_num]

        cards.append({
            "question": question,
            "answer": answer,
            "section": section,
        })

    return cards


def strip_markdown(text: str) -> str:
    """Strip markdown formatting for cleaner terminal display."""
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'\033[3m\1\033[0m', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'\033[36m\1\033[0m', text)
    # Blockquote lines
    text = re.sub(r'^>\s*', '  │ ', text, flags=re.MULTILINE)
    # Header markers
    text = re.sub(r'^#{1,4}\s*', '', text, flags=re.MULTILINE)
    return text


def run_quiz(cards: list[dict], count: int, mode: str, show_hint: bool) -> dict:
    """Run the interactive quiz and return score."""
    if not cards:
        print("❌ No flashcards found!")
        return {"correct": 0, "total": 0, "percentage": 0.0, "missed": []}

    # Select cards based on mode
    if mode == "random":
        selected = random.sample(cards, min(count, len(cards))) if count > 0 else random.sample(cards, len(cards))
    elif mode == "sequential":
        selected = cards[:count] if count > 0 else cards
    elif mode == "reverse":
        selected = list(reversed(cards))[:count] if count > 0 else list(reversed(cards))
    else:
        selected = cards[:count] if count > 0 else cards

    total = len(selected)
    correct = 0
    missed = []

    print(f"\n{'='*60}")
    print(f"  🃏 FLASHCARD QUIZ — {total} questions")
    print(f"{'='*60}")
    print(f"  Press ENTER to reveal answer, then rate yourself:")
    print(f"  [y] Got it  [n] Missed  [q] Quit")
    print(f"{'='*60}\n")

    for i, card in enumerate(selected, 1):
        # Show question
        print(f"  ── Question {i}/{total} ──")
        if show_hint:
            print(f"  📂 {card['section']}")
        print(f"\n  ❓ {strip_markdown(card['question'])}\n")

        # Wait for enter
        try:
            input("  [Press ENTER to reveal answer] ")
        except (EOFError, KeyboardInterrupt):
            print("\n\n  👋 Quiz ended early!")
            break

        # Show answer
        print(f"\n  {'─'*50}")
        for line in card['answer'].split('\n'):
            print(f"  {strip_markdown(line)}")
        print(f"  {'─'*50}\n")

        # Get self-rating
        while True:
            try:
                rating = input("  Did you get it? [y/n/q]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                rating = 'q'

            if rating in ('y', 'yes'):
                correct += 1
                print("  ✅ Nice!\n")
                break
            elif rating in ('n', 'no'):
                missed.append(card['question'])
                print("  ❌ Review this one!\n")
                break
            elif rating in ('q', 'quit'):
                print("\n  👋 Quiz ended early!")
                total = i  # Adjust total to answered questions
                break
            else:
                print("  (y/n/q) ", end="")

        if rating in ('q', 'quit'):
            break

    # Results
    percentage = (correct / total * 100) if total > 0 else 0

    print(f"\n{'='*60}")
    print(f"  📊 RESULTS")
    print(f"{'='*60}")
    print(f"  Score: {correct}/{total} ({percentage:.0f}%)")

    if percentage == 100:
        print("  🏆 Perfect score! You're crushing it!")
    elif percentage >= 80:
        print("  🔥 Great job! Almost there!")
    elif percentage >= 60:
        print("  💪 Solid effort! Keep revising!")
    else:
        print("  📖 Time to review! Hit those notes again.")

    if missed:
        print(f"\n  ❌ Missed ({len(missed)}):")
        for q in missed:
            print(f"    • {q}")

    print(f"{'='*60}\n")

    return {
        "correct": correct,
        "total": total,
        "percentage": round(percentage, 1),
        "missed": missed,
    }


def main():
    parser = argparse.ArgumentParser(
        description="🃏 Flashcard Quiz — test yourself from vault flashcards"
    )
    parser.add_argument("--topic", required=True, help="Topic name (e.g., 'agent-memory')")
    parser.add_argument("--count", type=int, default=10, help="Number of questions (0=all)")
    parser.add_argument("--mode", choices=["random", "sequential", "reverse"], default="random")
    parser.add_argument("--show-hint", action="store_true", help="Show section as hint")
    parser.add_argument("--json", action="store_true", help="Output results as JSON (non-interactive)")
    parser.add_argument("--list", action="store_true", help="Just list available cards and exit")

    args = parser.parse_args()

    # Find flashcards file
    fc_path = find_flashcards_file(args.topic)
    if not fc_path:
        print(f"❌ No flashcards.md found for topic: {args.topic}")
        print(f"   Searched in: tech/{args.topic}/flashcards.md")
        sys.exit(1)

    # Parse cards
    cards = parse_flashcards(fc_path)
    if not cards:
        print(f"❌ No flashcards found in: {fc_path}")
        sys.exit(1)

    print(f"  📂 Found {len(cards)} flashcards in: {fc_path.relative_to(fc_path.parent.parent.parent)}")

    # List mode — just show cards and exit
    if args.list:
        for i, card in enumerate(cards, 1):
            print(f"  {i:3d}. [{card['section']}] {card['question']}")
        sys.exit(0)

    # Run quiz
    result = run_quiz(cards, args.count, args.mode, args.show_hint)

    # JSON output mode (for programmatic use)
    if args.json:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

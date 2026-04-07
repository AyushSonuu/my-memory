"""CLI entrypoint — wires together parser, quiz engine, and display.

This is the composition root: it creates concrete instances and connects
the modules. The only place that knows about all the pieces.

Dependency flow:
    CLI → creates VaultFlashcardParser (concrete)
    CLI → passes cards to quiz engine (select_cards, compute_result)
    CLI → passes results to display functions

    Parser, quiz engine, and display are decoupled from each other.
"""

from __future__ import annotations

import argparse
import json
import sys

from ayra_lib.config import VaultConfig
from ayra_lib.parsers import VaultFlashcardParser

from flashcard_quiz.display import (
    print_answer,
    print_card_list,
    print_correct,
    print_header,
    print_incorrect,
    print_question,
    print_quit,
    print_results,
)
from flashcard_quiz.quiz import SelectionStrategy, compute_result, select_cards


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="flashcard-quiz",
        description="🃏 Flashcard Quiz — test yourself from vault flashcards",
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Topic name (e.g., 'agent-memory', 'python/asyncio')",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of questions (0 = all). Default: 10",
    )
    parser.add_argument(
        "--mode",
        choices=[s.value for s in SelectionStrategy],
        default=SelectionStrategy.RANDOM.value,
        help="Question selection order. Default: random",
    )
    parser.add_argument(
        "--show-hint",
        action="store_true",
        help="Show section name as hint before answering",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON (non-interactive, for programmatic use)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_cards",
        help="List all available cards and exit",
    )
    return parser


def _prompt_rating() -> str | None:
    """Prompt user for self-rating. Returns 'y', 'n', or None for quit."""
    while True:
        try:
            response = input("  Did you get it? [y/n/q]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return None

        if response in ("y", "yes"):
            return "y"
        if response in ("n", "no"):
            return "n"
        if response in ("q", "quit"):
            return None


def _wait_for_reveal() -> bool:
    """Wait for user to press ENTER. Returns False if quit."""
    try:
        input("  [Press ENTER to reveal answer] ")
        return True
    except (EOFError, KeyboardInterrupt):
        return False


def _run_interactive_quiz(
    cards: list,  # list[Flashcard] — avoiding import cycle in annotation
    count: int,
    strategy: SelectionStrategy,
    *,
    show_hint: bool = False,
) -> dict:
    """Run an interactive quiz session.

    Args:
        cards: All parsed flashcards.
        count: Number of questions to ask.
        strategy: Card selection strategy.
        show_hint: Show section hints.

    Returns:
        Dict with correct, total, percentage, missed keys.
    """
    selected = select_cards(cards, count, strategy)
    total = len(selected)

    print_header(total)

    correct = 0
    missed: list[str] = []
    answered = 0

    for i, card in enumerate(selected, 1):
        print_question(i, total, card, show_hint=show_hint)

        if not _wait_for_reveal():
            print_quit()
            break

        print_answer(card)

        rating = _prompt_rating()
        if rating is None:
            print_quit()
            answered = i
            break

        answered = i
        if rating == "y":
            correct += 1
            print_correct()
        else:
            missed.append(card.question)
            print_incorrect()

    result = compute_result(correct, answered, missed)
    print_results(result)

    return {
        "correct": result.correct,
        "total": result.total,
        "percentage": result.percentage,
        "missed": list(result.missed),
    }


def main() -> None:
    """CLI entrypoint — composition root."""
    parser = _build_parser()
    args = parser.parse_args()

    # --- Resolve flashcards file ---
    config = VaultConfig()
    fc_path = config.find_flashcards(args.topic)

    if fc_path is None:
        print(f"❌ No flashcards.md found for topic: {args.topic}")
        print(f"   Searched in: tech/{args.topic}/flashcards.md")
        sys.exit(1)

    # --- Parse cards ---
    try:
        card_parser = VaultFlashcardParser(fc_path)
        cards = card_parser.load()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if not cards:
        print(f"❌ No flashcards found in: {fc_path}")
        sys.exit(1)

    rel_path = fc_path.relative_to(config.repo_root)
    print(f"  📂 Found {len(cards)} flashcards in: {rel_path}")

    # --- List mode ---
    if args.list_cards:
        print_card_list(cards)
        sys.exit(0)

    # --- Quiz mode ---
    strategy = SelectionStrategy(args.mode)
    result = _run_interactive_quiz(
        cards,
        args.count,
        strategy,
        show_hint=args.show_hint,
    )

    # --- JSON output ---
    if args.json_output:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

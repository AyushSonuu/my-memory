"""Terminal display and formatting for quiz output.

Single Responsibility: only concerned with how things look in the terminal.
Does NOT run quiz logic. Does NOT parse cards. Pure output formatting.

Dependency Inversion: depends on Flashcard and QuizResult abstractions,
not on parsers or quiz engine internals.
"""

from __future__ import annotations

import re

from ayra_lib.types import Flashcard, QuizResult

# --- ANSI helpers ---

BOLD = "\033[1m"
ITALIC = "\033[3m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


def strip_markdown(text: str) -> str:
    """Convert markdown formatting to ANSI terminal escapes.

    Args:
        text: Markdown-formatted string.

    Returns:
        String with ANSI escape codes for terminal display.
    """
    # Bold **text**
    text = re.sub(r"\*\*(.*?)\*\*", rf"{BOLD}\1{RESET}", text)
    # Italic *text*
    text = re.sub(r"\*(.*?)\*", rf"{ITALIC}\1{RESET}", text)
    # Inline code `text`
    text = re.sub(r"`([^`]+)`", rf"{CYAN}\1{RESET}", text)
    # Blockquotes > text
    text = re.sub(r"^>\s*", f"  {DIM}│{RESET} ", text, flags=re.MULTILINE)
    # Headers ### text
    text = re.sub(r"^#{1,4}\s*", "", text, flags=re.MULTILINE)
    return text


def print_header(total: int) -> None:
    """Print the quiz welcome banner.

    Args:
        total: Total number of questions in this quiz.
    """
    line = "═" * 60
    print(f"\n  {line}")
    print(f"  {BOLD}🃏 FLASHCARD QUIZ — {total} questions{RESET}")
    print(f"  {line}")
    print(f"  {DIM}Press ENTER to reveal answer, then rate yourself:")
    print(f"  [y] Got it  [n] Missed  [q] Quit{RESET}")
    print(f"  {line}\n")


def print_question(index: int, total: int, card: Flashcard, *, show_hint: bool = False) -> None:
    """Print a single question.

    Args:
        index: Current question number (1-based).
        total: Total questions in the quiz.
        card: The flashcard being shown.
        show_hint: Whether to show the section as a hint.
    """
    print(f"  {DIM}── Question {index}/{total} ──{RESET}")
    if show_hint:
        print(f"  {DIM}📂 {card.section}{RESET}")
    print(f"\n  {BOLD}❓ {strip_markdown(card.question)}{RESET}\n")


def print_answer(card: Flashcard) -> None:
    """Print the answer to a flashcard.

    Args:
        card: The flashcard whose answer to display.
    """
    separator = "─" * 50
    print(f"\n  {separator}")
    for raw_line in card.answer.split("\n"):
        print(f"  {strip_markdown(raw_line)}")
    print(f"  {separator}\n")


def print_correct() -> None:
    """Print correct answer feedback."""
    print(f"  {GREEN}✅ Nice!{RESET}\n")


def print_incorrect() -> None:
    """Print incorrect answer feedback."""
    print(f"  {RED}❌ Review this one!{RESET}\n")


def print_quit() -> None:
    """Print early quit message."""
    print(f"\n  {YELLOW}👋 Quiz ended early!{RESET}")


def print_results(result: QuizResult) -> None:
    """Print the final quiz results.

    Args:
        result: Computed quiz result.
    """
    line = "═" * 60
    print(f"\n  {line}")
    print(f"  {BOLD}📊 RESULTS{RESET}")
    print(f"  {line}")
    print(f"  Score: {result.correct}/{result.total} ({result.percentage}%) {result.grade}")

    if result.percentage == 100:
        print(f"  {GREEN}Perfect score! You're crushing it!{RESET}")
    elif result.percentage >= 80:
        print(f"  {GREEN}Great job! Almost there!{RESET}")
    elif result.percentage >= 60:
        print(f"  {YELLOW}Solid effort! Keep revising!{RESET}")
    else:
        print(f"  {RED}Time to review! Hit those notes again.{RESET}")

    if result.missed:
        print(f"\n  {RED}❌ Missed ({len(result.missed)}):{RESET}")
        for question in result.missed:
            print(f"    • {question}")

    print(f"  {line}\n")


def print_card_list(cards: list[Flashcard]) -> None:
    """Print all available cards as a numbered list.

    Args:
        cards: List of flashcards to display.
    """
    for i, card in enumerate(cards, 1):
        print(f"  {DIM}{i:3d}.{RESET} [{card.section}] {card.question}")

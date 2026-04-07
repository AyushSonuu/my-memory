"""Quiz engine — orchestrates question selection and scoring.

Single Responsibility: manages quiz flow and scoring.
Does NOT parse flashcards (parser does that).
Does NOT format output (display does that).

Open/Closed: new selection strategies added via QuizStrategy enum
without modifying existing logic.
"""

from __future__ import annotations

import random
from enum import StrEnum, auto

from ayra_lib.types import Flashcard, QuizResult


class SelectionStrategy(StrEnum):
    """How questions are selected from the card pool."""

    RANDOM = auto()
    SEQUENTIAL = auto()
    REVERSE = auto()


def select_cards(
    cards: list[Flashcard],
    count: int,
    strategy: SelectionStrategy = SelectionStrategy.RANDOM,
) -> list[Flashcard]:
    """Select cards from the pool using the given strategy.

    Args:
        cards: All available flashcards.
        count: Number to select (0 = all).
        strategy: Selection ordering.

    Returns:
        Selected subset of cards in the specified order.
    """
    if not cards:
        return []

    pool: list[Flashcard]

    match strategy:
        case SelectionStrategy.RANDOM:
            pool = random.sample(cards, len(cards))
        case SelectionStrategy.SEQUENTIAL:
            pool = list(cards)
        case SelectionStrategy.REVERSE:
            pool = list(reversed(cards))

    if count > 0:
        pool = pool[:count]

    return pool


def compute_result(
    correct: int,
    total: int,
    missed: list[str],
) -> QuizResult:
    """Build an immutable QuizResult from raw quiz data.

    Args:
        correct: Number of correct answers.
        total: Total questions answered.
        missed: List of missed question texts.

    Returns:
        Frozen QuizResult value object.
    """
    return QuizResult(
        correct=correct,
        total=total,
        missed=tuple(missed),
    )

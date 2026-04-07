"""Tests for quiz engine — selection strategies and result computation."""

from __future__ import annotations

import pytest
from ayra_lib.types import Flashcard
from flashcard_quiz.quiz import SelectionStrategy, compute_result, select_cards


def _make_cards(n: int) -> list[Flashcard]:
    """Factory: create n dummy flashcards for testing."""
    return [
        Flashcard(
            question=f"Question {i}?",
            answer=f"Answer {i}.",
            section=f"Section {i // 3}",
            card_index=i,
        )
        for i in range(n)
    ]


class TestSelectCards:
    """Test card selection strategies."""

    def test_sequential_order(self) -> None:
        """Sequential should preserve original order."""
        cards = _make_cards(5)
        selected = select_cards(cards, 3, SelectionStrategy.SEQUENTIAL)
        assert len(selected) == 3
        assert [c.card_index for c in selected] == [0, 1, 2]

    def test_reverse_order(self) -> None:
        """Reverse should flip the order."""
        cards = _make_cards(5)
        selected = select_cards(cards, 3, SelectionStrategy.REVERSE)
        assert len(selected) == 3
        assert [c.card_index for c in selected] == [4, 3, 2]

    def test_random_returns_correct_count(self) -> None:
        """Random should return the requested count."""
        cards = _make_cards(10)
        selected = select_cards(cards, 5, SelectionStrategy.RANDOM)
        assert len(selected) == 5

    def test_random_no_duplicates(self) -> None:
        """Random selection should not have duplicates."""
        cards = _make_cards(10)
        selected = select_cards(cards, 10, SelectionStrategy.RANDOM)
        indices = [c.card_index for c in selected]
        assert len(set(indices)) == 10

    def test_count_zero_returns_all(self) -> None:
        """Count=0 should return all cards."""
        cards = _make_cards(7)
        selected = select_cards(cards, 0, SelectionStrategy.SEQUENTIAL)
        assert len(selected) == 7

    def test_count_exceeds_pool(self) -> None:
        """If count > available cards, return all cards."""
        cards = _make_cards(3)
        selected = select_cards(cards, 10, SelectionStrategy.SEQUENTIAL)
        assert len(selected) == 3

    def test_empty_cards(self) -> None:
        """Empty card list should return empty."""
        selected = select_cards([], 5, SelectionStrategy.RANDOM)
        assert selected == []


class TestComputeResult:
    """Test quiz result computation."""

    def test_perfect_score(self) -> None:
        result = compute_result(10, 10, [])
        assert result.correct == 10
        assert result.total == 10
        assert result.percentage == 100.0
        assert result.grade == "🏆"
        assert result.missed == ()

    def test_partial_score(self) -> None:
        result = compute_result(7, 10, ["Q1", "Q2", "Q3"])
        assert result.percentage == 70.0
        assert result.grade == "💪"
        assert len(result.missed) == 3

    def test_failing_score(self) -> None:
        result = compute_result(2, 10, ["Q" + str(i) for i in range(8)])
        assert result.percentage == 20.0
        assert result.grade == "📖"

    def test_zero_total(self) -> None:
        result = compute_result(0, 0, [])
        assert result.percentage == 0.0

    def test_result_immutable(self) -> None:
        result = compute_result(5, 10, ["Q1"])
        with pytest.raises(AttributeError):
            result.correct = 6  # type: ignore[misc]

    def test_great_score(self) -> None:
        result = compute_result(8, 10, ["Q1", "Q2"])
        assert result.percentage == 80.0
        assert result.grade == "🔥"

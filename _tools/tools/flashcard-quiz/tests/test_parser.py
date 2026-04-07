"""Tests for flashcard parsing — VaultFlashcardParser."""

from __future__ import annotations

from pathlib import Path

import pytest
from ayra_lib.parsers import VaultFlashcardParser


class TestVaultFlashcardParser:
    """Test suite for VaultFlashcardParser (SRP: only tests parsing)."""

    def test_parse_correct_count(self, sample_flashcards_file: Path) -> None:
        """Should parse all 4 cards from sample file."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        assert len(cards) == 4

    def test_parse_question_text(self, sample_flashcards_file: Path) -> None:
        """Should extract clean question text without ❓ prefix."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        assert cards[0].question == "What is an agent?"
        assert cards[2].question == "How does RAG work?"

    def test_parse_answer_content(self, sample_flashcards_file: Path) -> None:
        """Should preserve answer content including markdown."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        assert "LLM-powered" in cards[0].answer
        assert "💡" in cards[0].answer

    def test_parse_table_in_answer(self, sample_flashcards_file: Path) -> None:
        """Should preserve markdown tables in answers."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        assert "Reflection" in cards[1].answer
        assert "Multi-Agent" in cards[1].answer

    def test_parse_numbered_list_in_answer(self, sample_flashcards_file: Path) -> None:
        """Should preserve numbered lists in answers."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        assert "1. Query" in cards[2].answer
        assert "5. Return to user" in cards[2].answer

    def test_section_assignment(self, sample_flashcards_file: Path) -> None:
        """Should assign correct sections to cards."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        assert cards[0].section == "Core Concepts"
        assert cards[1].section == "Core Concepts"
        assert cards[2].section == "Advanced Topics"
        assert cards[3].section == "Advanced Topics"

    def test_no_section_defaults_to_general(self, minimal_card_file: Path) -> None:
        """Cards without a preceding section header should be 'General'."""
        parser = VaultFlashcardParser(minimal_card_file)
        cards = parser.load()
        assert len(cards) == 1
        assert cards[0].section == "General"

    def test_empty_file_returns_empty_list(self, empty_flashcards_file: Path) -> None:
        """Should return empty list for files with no card blocks."""
        parser = VaultFlashcardParser(empty_flashcards_file)
        cards = parser.load()
        assert cards == []

    def test_card_index_sequential(self, sample_flashcards_file: Path) -> None:
        """Card indices should be 0-based and sequential."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        indices = [c.card_index for c in cards]
        assert indices == [0, 1, 2, 3]

    def test_source_file_tracked(self, sample_flashcards_file: Path) -> None:
        """Each card should record its source filename."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        assert all(c.source_file == "flashcards.md" for c in cards)

    def test_answer_whitespace_cleaned(self, sample_flashcards_file: Path) -> None:
        """Answers should not have leading/trailing blank lines."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        for card in cards:
            assert not card.answer.startswith("\n")
            assert not card.answer.endswith("\n")

    def test_file_not_found_raises(self, tmp_path: Path) -> None:
        """Should raise FileNotFoundError for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            VaultFlashcardParser(tmp_path / "nonexistent.md")

    def test_immutability(self, sample_flashcards_file: Path) -> None:
        """Flashcard objects should be immutable (frozen dataclass)."""
        parser = VaultFlashcardParser(sample_flashcards_file)
        cards = parser.load()
        with pytest.raises(AttributeError):
            cards[0].question = "mutated"  # type: ignore[misc]


class TestParserWithRealVault:
    """Integration tests against actual vault data (skipped if vault absent)."""

    def test_parse_agent_memory(self) -> None:
        """Should parse real agent-memory flashcards if vault exists."""
        from ayra_lib.config import VaultConfig

        config = VaultConfig()
        fc_path = config.find_flashcards("agent-memory")

        if fc_path is None:
            pytest.skip("Vault not found — running outside repo")

        parser = VaultFlashcardParser(fc_path)
        cards = parser.load()
        assert len(cards) > 0, "agent-memory should have flashcards"
        assert all(c.question for c in cards), "Every card must have a question"

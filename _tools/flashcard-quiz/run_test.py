"""Tests for flashcard-quiz tool."""

import sys
from pathlib import Path

# Add tool dir and _lib to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib" / "python"))

from run import parse_flashcards, find_flashcards_file


class TestParseFlashcards:
    """Test flashcard parsing from vault format."""

    def _write_temp_flashcards(self, tmp_path: Path, content: str) -> Path:
        fc = tmp_path / "flashcards.md"
        fc.write_text(content)
        return fc

    def test_parse_single_card(self, tmp_path):
        content = """# 🃏 Test Flashcards

### 📌 Core Concepts (Lesson 1)

<details markdown="1">
<summary>❓ What is an agent?</summary>

An LLM-powered system that can take actions autonomously.
</details>
"""
        fc = self._write_temp_flashcards(tmp_path, content)
        cards = parse_flashcards(fc)
        assert len(cards) == 1
        assert cards[0]["question"] == "What is an agent?"
        assert "LLM-powered" in cards[0]["answer"]
        assert cards[0]["section"] == "Core Concepts"

    def test_parse_multiple_cards(self, tmp_path):
        content = """# 🃏 Test Flashcards

### 📌 Section A

<details markdown="1">
<summary>❓ Question 1?</summary>

Answer 1.
</details>

<details markdown="1">
<summary>❓ Question 2?</summary>

Answer 2.
</details>

### 📌 Section B

<details markdown="1">
<summary>❓ Question 3?</summary>

Answer 3.
</details>
"""
        fc = self._write_temp_flashcards(tmp_path, content)
        cards = parse_flashcards(fc)
        assert len(cards) == 3
        assert cards[0]["section"] == "Section A"
        assert cards[1]["section"] == "Section A"
        assert cards[2]["section"] == "Section B"

    def test_parse_multiline_answer(self, tmp_path):
        content = """### 📌 Test

<details markdown="1">
<summary>❓ What are the 3 steps?</summary>

1. First step
2. Second step
3. Third step

> 💡 Remember: one, two, three!
</details>
"""
        fc = self._write_temp_flashcards(tmp_path, content)
        cards = parse_flashcards(fc)
        assert len(cards) == 1
        assert "First step" in cards[0]["answer"]
        assert "Third step" in cards[0]["answer"]
        assert "💡" in cards[0]["answer"]

    def test_parse_table_in_answer(self, tmp_path):
        content = """### 📌 Comparisons

<details markdown="1">
<summary>❓ RAG vs Agent Memory?</summary>

| Feature | RAG | Agent Memory |
|---------|-----|-------------|
| Scope | Session | Cross-session |
| Source | External docs | Agent's own history |
</details>
"""
        fc = self._write_temp_flashcards(tmp_path, content)
        cards = parse_flashcards(fc)
        assert len(cards) == 1
        assert "RAG" in cards[0]["answer"]
        assert "Cross-session" in cards[0]["answer"]

    def test_parse_empty_file(self, tmp_path):
        fc = self._write_temp_flashcards(tmp_path, "# Empty flashcards\n\nNo cards here.")
        cards = parse_flashcards(fc)
        assert len(cards) == 0

    def test_no_section_header(self, tmp_path):
        content = """<details markdown="1">
<summary>❓ Orphan question?</summary>

Orphan answer.
</details>
"""
        fc = self._write_temp_flashcards(tmp_path, content)
        cards = parse_flashcards(fc)
        assert len(cards) == 1
        assert cards[0]["section"] == "General"


class TestFindFlashcards:
    """Test flashcard file discovery."""

    def test_find_agent_memory(self):
        """Should find agent-memory flashcards in the real vault."""
        fc = find_flashcards_file("agent-memory")
        if fc:  # Only assert if vault exists (CI-safe)
            assert fc.name == "flashcards.md"
            assert "agent-memory" in str(fc)

    def test_find_nonexistent(self):
        """Should return None for nonexistent topic."""
        fc = find_flashcards_file("nonexistent-topic-xyz")
        assert fc is None

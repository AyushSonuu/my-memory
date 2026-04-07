"""Reusable parsers for vault content formats."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Protocol

from ayra_lib.types import Flashcard

# --- Protocol (Interface Segregation + Dependency Inversion) ---


class CardSource(Protocol):
    """Protocol for anything that can produce flashcards.

    Any class implementing this protocol can be used as a card source
    for the quiz engine — vault files, databases, APIs, etc.
    """

    def load(self) -> list[Flashcard]:
        """Load and return all available flashcards."""
        ...


# --- Concrete Implementation ---


class VaultFlashcardParser:
    """Parses flashcards from the vault's <details>/<summary> markdown format.

    Single Responsibility: only concerned with parsing vault markdown → Flashcard objects.
    Does NOT know about quizzes, display, or file discovery.

    Expected input format:
        ### 📌 Section Name (Lesson X)

        <details markdown="1">
        <summary>❓ Question text</summary>

        Answer content (multi-line, tables, code blocks, etc.)
        </details>
    """

    # Regex: match <details> blocks with ❓ questions
    _CARD_PATTERN = re.compile(
        r"<details[^>]*>\s*<summary>\s*❓\s*(.*?)\s*</summary>\s*(.*?)\s*</details>",
        re.DOTALL,
    )

    # Regex: match section headers like ### 📌 Core Concepts (Lesson 1)
    _SECTION_PATTERN = re.compile(
        r"^###\s*📌\s*(.+?)(?:\s*\(.*?\))?\s*$",
        re.MULTILINE,
    )

    def __init__(self, file_path: Path) -> None:
        """Initialize with the path to a flashcards.md file.

        Args:
            file_path: Absolute or relative path to the flashcards markdown file.

        Raises:
            FileNotFoundError: If the file doesn't exist.
        """
        self._file_path = Path(file_path)
        if not self._file_path.exists():
            msg = f"Flashcard file not found: {self._file_path}"
            raise FileNotFoundError(msg)

    @property
    def file_path(self) -> Path:
        """The file being parsed (read-only)."""
        return self._file_path

    def load(self) -> list[Flashcard]:
        """Parse all flashcards from the file.

        Returns:
            List of Flashcard objects in document order.
        """
        content = self._file_path.read_text(encoding="utf-8")
        section_map = self._build_section_map(content)
        return self._extract_cards(content, section_map)

    def _build_section_map(self, content: str) -> list[tuple[int, str]]:
        """Build a mapping of character positions to section names.

        Returns:
            Sorted list of (char_position, section_name) tuples.
        """
        sections: list[tuple[int, str]] = []
        for match in self._SECTION_PATTERN.finditer(content):
            section_name = match.group(1).strip()
            sections.append((match.start(), section_name))
        return sorted(sections, key=lambda x: x[0])

    def _resolve_section(
        self, char_pos: int, section_map: list[tuple[int, str]]
    ) -> str:
        """Determine which section a card belongs to based on position.

        Args:
            char_pos: Character offset of the card in the document.
            section_map: Sorted section position map.

        Returns:
            Section name, or 'General' if no section header precedes the card.
        """
        current = "General"
        for pos, name in section_map:
            if pos <= char_pos:
                current = name
            else:
                break
        return current

    @staticmethod
    def _clean_answer(raw: str) -> str:
        """Strip leading/trailing blank lines from answer text.

        Args:
            raw: Raw answer text from regex match.

        Returns:
            Cleaned answer with consistent whitespace.
        """
        lines = raw.split("\n")

        # Strip leading blank lines
        while lines and not lines[0].strip():
            lines.pop(0)

        # Strip trailing blank lines
        while lines and not lines[-1].strip():
            lines.pop()

        return "\n".join(lines)

    def _extract_cards(
        self, content: str, section_map: list[tuple[int, str]]
    ) -> list[Flashcard]:
        """Extract all flashcard blocks from content.

        Args:
            content: Full file content.
            section_map: Section position map from _build_section_map.

        Returns:
            List of parsed Flashcard objects.
        """
        cards: list[Flashcard] = []

        for idx, match in enumerate(self._CARD_PATTERN.finditer(content)):
            question = match.group(1).strip()
            answer = self._clean_answer(match.group(2))
            section = self._resolve_section(match.start(), section_map)

            cards.append(
                Flashcard(
                    question=question,
                    answer=answer,
                    section=section,
                    source_file=str(self._file_path.name),
                    card_index=idx,
                )
            )

        return cards

"""Shared data models — immutable, type-safe, serializable."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Flashcard:
    """A single flashcard parsed from the vault format.

    Immutable value object — once parsed, a flashcard never changes.
    """

    question: str
    answer: str
    section: str = "General"
    source_file: str = ""
    card_index: int = 0

    def __str__(self) -> str:
        return f"[{self.section}] {self.question}"


@dataclass(frozen=True, slots=True)
class QuizResult:
    """Outcome of a quiz session.

    Immutable — produced once after the quiz completes.
    """

    correct: int
    total: int
    missed: tuple[str, ...] = ()

    @property
    def percentage(self) -> float:
        """Score as a percentage (0.0-100.0)."""
        if self.total == 0:
            return 0.0
        return round(self.correct / self.total * 100, 1)

    @property
    def grade(self) -> str:
        """Human-readable grade emoji."""
        pct = self.percentage
        if pct == 100:
            return "🏆"
        if pct >= 80:
            return "🔥"
        if pct >= 60:
            return "💪"
        return "📖"


@dataclass(frozen=True, slots=True)
class ToolMeta:
    """Metadata for a registered tool (from registry.json).

    Maps 1:1 to a registry entry. Immutable.
    """

    name: str
    path: str
    version: str
    runtime: str
    description: str
    tags: tuple[str, ...] = ()
    status: str = "stable"
    created: str = ""
    tests: str = ""


@dataclass(frozen=True, slots=True)
class ToolRegistry:
    """The complete tool registry. Immutable snapshot."""

    version: str
    description: str
    tools: tuple[ToolMeta, ...] = ()
    last_updated: str = ""

    def find_tool(self, name: str) -> ToolMeta | None:
        """Look up a tool by name."""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None

    def list_by_tag(self, tag: str) -> tuple[ToolMeta, ...]:
        """Filter tools by tag."""
        return tuple(t for t in self.tools if tag in t.tags)

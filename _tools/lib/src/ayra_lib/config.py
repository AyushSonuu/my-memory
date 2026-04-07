"""Vault configuration — paths, constants, environment detection."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta, timezone
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30))

# Detect repo root: walk up from this file until we find AGENTS.md
_SEARCH = Path(__file__).resolve().parent
_REPO_ROOT: Path | None = None
for _p in [_SEARCH, *_SEARCH.parents]:
    if (_p / "AGENTS.md").exists():
        _REPO_ROOT = _p
        break


@dataclass(frozen=True, slots=True)
class VaultConfig:
    """Immutable configuration for the vault filesystem layout.

    Single source of truth for all paths. Passed as dependency
    (Dependency Inversion) rather than imported as global.
    """

    repo_root: Path = field(default_factory=lambda: _REPO_ROOT or Path.cwd())

    # --- Derived paths (computed, not stored) ---

    @property
    def tech_dir(self) -> Path:
        return self.repo_root / "tech"

    @property
    def tools_dir(self) -> Path:
        return self.repo_root / "_tools"

    @property
    def registry_path(self) -> Path:
        return self.tools_dir / "registry.json"

    @property
    def memory_dir(self) -> Path:
        return self.repo_root / "memory"

    @property
    def maps_dir(self) -> Path:
        return self.repo_root / "_maps"

    @property
    def templates_dir(self) -> Path:
        return self.repo_root / "_templates"

    @property
    def revision_dir(self) -> Path:
        return self.repo_root / "_revision"

    def find_topic(self, name: str) -> Path | None:
        """Locate a topic directory by name under tech/.

        Supports both direct (e.g., 'agent-memory') and nested
        (e.g., 'python/asyncio') topic paths.

        Returns:
            Path to the topic directory, or None if not found.
        """
        # Direct match first (fast path)
        direct = self.tech_dir / name
        if direct.is_dir():
            return direct

        # Recursive search (handles nested topics)
        for candidate in self.tech_dir.rglob("*"):
            if candidate.is_dir() and candidate.name == name:
                return candidate

        return None

    def find_flashcards(self, topic: str) -> Path | None:
        """Locate flashcards.md for a given topic.

        Returns:
            Path to flashcards.md, or None if not found.
        """
        topic_dir = self.find_topic(topic)
        if topic_dir is None:
            return None

        flashcards = topic_dir / "flashcards.md"
        return flashcards if flashcards.exists() else None

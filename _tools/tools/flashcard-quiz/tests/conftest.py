"""Shared test fixtures for flashcard-quiz tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def sample_flashcards_file(tmp_path: Path) -> Path:
    """Create a sample flashcards.md file matching vault format."""
    content = """\
# 🃏 Test Topic Flashcards

> From: `test-topic/` | Last updated: 2026-04-07

---

### 📌 Core Concepts (Lesson 1)

<details markdown="1">
<summary>❓ What is an agent?</summary>

An **LLM-powered** system that can take actions autonomously.

> 💡 Agent = waiter jo khud decide kare kya karna hai!
</details>

<details markdown="1">
<summary>❓ What are the 4 design patterns?</summary>

| Pattern | Control |
|---------|---------|
| Reflection | High |
| Tool Use | Medium |
| Planning | Low |
| Multi-Agent | Lowest |
</details>

### 📌 Advanced Topics (Lesson 2)

<details markdown="1">
<summary>❓ How does RAG work?</summary>

1. Query
2. Retrieve relevant docs
3. Augment prompt with context
4. Generate answer
5. Return to user
</details>

<details markdown="1">
<summary>❓ Vector DB vs SQL DB?</summary>

- **Vector DB**: semantic similarity search, embeddings
- **SQL DB**: structured queries, exact match, relationships

> 💡 Vector = meaning se dhundo. SQL = column se dhundo.
</details>
"""
    fc = tmp_path / "flashcards.md"
    fc.write_text(content)
    return fc


@pytest.fixture
def empty_flashcards_file(tmp_path: Path) -> Path:
    """Create an empty flashcards.md file."""
    fc = tmp_path / "flashcards.md"
    fc.write_text("# 🃏 Empty Flashcards\n\nNo cards here.\n")
    return fc


@pytest.fixture
def minimal_card_file(tmp_path: Path) -> Path:
    """Create a file with a single card and no section header."""
    content = """\
<details markdown="1">
<summary>❓ Orphan question?</summary>

Orphan answer content.
</details>
"""
    fc = tmp_path / "flashcards.md"
    fc.write_text(content)
    return fc

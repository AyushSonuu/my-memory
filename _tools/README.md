# 🔧 Ayra Tools

> Self-created, tested, versioned, SOLID-compliant executable tools for the learning vault.

## Architecture

```
_tools/                          # Workspace root (uv manages)
├── pyproject.toml               # Workspace config + shared deps + linting + testing
├── uv.lock                      # Lockfile (deterministic, cross-platform)
├── registry.json                # Tool discovery index (auto-maintained)
├── README.md                    # This file
│
├── lib/                         # Shared library (workspace member)
│   ├── pyproject.toml
│   └── src/ayra_lib/            # Importable as `ayra_lib`
│       ├── __init__.py
│       ├── config.py            # Paths, constants, vault config
│       ├── parsers.py           # Reusable parsers (flashcards, markdown, etc.)
│       ├── registry.py          # Registry read/write operations
│       └── types.py             # Shared data models (dataclasses)
│
└── tools/                       # Individual tools (each = workspace member)
    └── flashcard-quiz/
        ├── pyproject.toml       # Tool metadata + deps (depends on ayra-lib)
        ├── src/flashcard_quiz/
        │   ├── __init__.py
        │   ├── cli.py           # CLI entrypoint (argparse)
        │   ├── parser.py        # Flashcard parsing (SRP)
        │   ├── quiz.py          # Quiz engine (SRP)
        │   └── display.py       # Terminal display/formatting (SRP)
        └── tests/
            ├── __init__.py
            ├── test_parser.py
            ├── test_quiz.py
            └── conftest.py      # Shared fixtures
```

## Design Principles

### SOLID Compliance

| Principle | How We Apply It |
|-----------|----------------|
| **S**ingle Responsibility | Each module does ONE thing: `parser.py` parses, `quiz.py` runs quiz logic, `display.py` formats output |
| **O**pen/Closed | New quiz modes (e.g., timed, spaced-repetition weighted) added by extending, not modifying existing classes |
| **L**iskov Substitution | All parsers implement a common protocol — swap flashcard parser for any other card source |
| **I**nterface Segregation | CLI depends on small interfaces, not fat classes. Quiz engine doesn't know about display. |
| **D**ependency Inversion | High-level modules depend on abstractions (protocols), not concrete implementations |

### Other Practices

- **Type hints everywhere** — `mypy --strict` clean
- **Dataclasses for data** — no dicts floating around
- **Protocols for contracts** — duck typing with safety
- **uv for dependency management** — fast, deterministic, lockfile-based
- **ruff for linting** — fast, opinionated, consistent
- **pytest for testing** — fixtures, parametrize, clean assertions
- **Semantic versioning** — every tool is semver'd
- **One command to run** — `uv run flashcard-quiz --topic agent-memory`

## Quick Reference

```bash
# Install/sync all dependencies
cd _tools && uv sync

# Run a tool
uv run flashcard-quiz --topic agent-memory --count 5

# Run all tests
uv run pytest

# Run tests for one tool
uv run pytest tools/flashcard-quiz/tests/ -v

# Lint
uv run ruff check .

# Type check
uv run mypy lib/ tools/
```

## Adding a New Tool

1. Create `tools/new-tool/` with `pyproject.toml` + `src/` + `tests/`
2. Add `ayra-lib` as workspace dependency
3. Register console script entrypoint in pyproject.toml
4. Write tests — must pass before registering
5. Add to `registry.json`
6. `uv sync` to wire everything up

## Registry

`registry.json` is the discovery layer. I (Ayra) auto-maintain it. Check it to see what's available.

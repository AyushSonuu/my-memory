# 🔧 Ayra Tools — Self-Created Executable Tools

> Agent-agnostic. Filesystem-discoverable. JSON in, JSON out.

## Discovery (for any agent)

**You are an agent and just landed in this repo. Here's how to find and use tools:**

### Step 1: Read this file
You're doing it. Below is the tool index with descriptions.

### Step 2: Find the right tool
Scan the index below. Each tool has a `TOOL.md` with full documentation.

### Step 3: Read the tool's TOOL.md
```
_tools/tools/{tool-name}/TOOL.md
```
Contains: when to use, when NOT to use, inputs, outputs, examples, error handling.

### Step 4: Get the schema (optional, for structured input building)
```bash
cd _tools && uv run {tool-name} --schema
```
Returns machine-readable JSON: inputs, types, required, defaults, enums, examples.

### Step 5: Execute
```bash
# Programmatic (agent mode) — JSON in → JSON out
cd _tools && uv run {tool-name} --input '{"key": "value"}'

# Interactive (human mode) — pretty terminal UI
cd _tools && uv run {tool-name} --topic foo --count 5
```

### Step 6: Parse the response
Every tool returns a standard `ToolOutput` envelope:
```json
{
  "status": "success | error | partial",
  "tool": "tool-name",
  "version": "1.0.0",
  "data": { ... },
  "message": "Human-readable summary",
  "errors": [],
  "timestamp": "ISO-8601"
}
```

---

## Tool Index

<!-- TOOL_INDEX_START — auto-updated, do not edit manually -->

| Tool | Description | Version | Status |
|------|-------------|---------|--------|
| [flashcard-quiz](tools/flashcard-quiz/TOOL.md) | Interactive quiz from vault flashcards. Revision, recall testing, structured Q&A data. | 1.1.0 | ✅ stable |

<!-- TOOL_INDEX_END -->

---

## Universal Interface Protocol

Every tool in this workspace implements the same contract:

```
┌────────────────────────────────────────────────┐
│           TOOL EXECUTION PROTOCOL               │
│                                                  │
│  --schema       → ToolSchema JSON               │
│                   (introspection for agents)     │
│                                                  │
│  --input '{}'   → ToolOutput JSON               │
│                   (programmatic execution)       │
│                                                  │
│  --flag args    → Pretty terminal output        │
│                   (interactive for humans)       │
│                                                  │
│  ALWAYS:                                         │
│  • JSON parseable output (in agent mode)        │
│  • Standard ToolOutput envelope                  │
│  • Input validation with clear error messages   │
│  • No ANSI/color codes in agent mode            │
└────────────────────────────────────────────────┘
```

## File System Layout

```
_tools/
├── README.md                       ← You are here (discovery index)
├── pyproject.toml                  ← uv workspace root
├── uv.lock                         ← Deterministic lockfile
├── registry.json                   ← Machine-readable tool index
│
├── lib/                            ← Shared library (ayra-lib)
│   └── src/ayra_lib/
│       ├── config.py               ← Vault paths + topic discovery
│       ├── types.py                ← Shared data models (frozen)
│       ├── parsers.py              ← Content parsers + CardSource protocol
│       ├── registry.py             ← Registry read/write ops
│       └── tool_interface.py       ← BaseTool + ToolOutput + ToolSchema
│
└── tools/                          ← Individual tools
    └── {tool-name}/
        ├── TOOL.md                 ← Human + agent documentation
        ├── pyproject.toml          ← Tool metadata + deps
        ├── src/{tool_name}/
        │   ├── cli.py              ← Composition root entrypoint
        │   ├── tool.py             ← BaseTool implementation
        │   └── ...                 ← Tool-specific modules (SRP)
        └── tests/
            └── test_*.py           ← pytest test suite
```

## Building a New Tool

1. Create `tools/new-tool/` with: `TOOL.md`, `pyproject.toml`, `src/`, `tests/`
2. Implement `BaseTool` → `schema()` + `execute()` + optionally `run_interactive()`
3. Wire entrypoint in `pyproject.toml` → `[project.scripts]`
4. Write tests — must pass before registering
5. Add `TOOL.md` with full documentation
6. Update the tool index table in this README
7. Update `registry.json`
8. `uv sync` to wire everything up

## Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.13 | Runtime |
| uv | 0.11+ | Package management, workspace, lockfile |
| ruff | 0.15+ | Linting (isort, pycodestyle, bugbear, simplify) |
| mypy | 1.20+ | Type checking (strict mode) |
| pytest | 9.0+ | Testing framework |
| hatchling | — | Build backend |

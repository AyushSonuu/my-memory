# 🔧 _tools/ — Self-Created Executable Tools

> Ayra creates, tests, versions, and uses these tools. The repo's self-extending capability layer.

## How It Works

```
NEED → CREATE → TEST → REGISTER → USE → ITERATE
```

1. **Need:** I identify a task that should be a reusable tool (not a one-off script)
2. **Create:** Write `tool.yaml` (metadata) + `run.py`/`run.js` (executable) + tests
3. **Test:** Run tests — must pass before registering
4. **Register:** Add to `registry.json`
5. **Use:** Execute via standard interface
6. **Iterate:** Bug or enhancement → fix → bump version → update CHANGELOG.md

## Tool Standard

Every tool is a folder with:

```
tool-name/
├── tool.yaml          # Metadata: name, version, inputs, outputs, runtime, deps
├── run.py             # Main executable (or run.js for Node.js)
├── run_test.py        # Tests (or run.test.js)
└── CHANGELOG.md       # Version history
```

### tool.yaml Schema

```yaml
name: tool-name                    # kebab-case, unique
version: 1.0.0                    # semver
description: What this tool does   # one-liner
runtime: python                    # python | node
entrypoint: run.py                 # main file to execute
python_version: ">=3.10"           # if runtime=python
node_version: ">=18"               # if runtime=node

inputs:                            # CLI arguments
  - name: arg_name
    type: string                   # string | integer | float | boolean | path
    required: true
    description: What this arg does
    default: null                  # optional default
    enum: [opt1, opt2]             # optional allowed values

outputs:
  - name: result
    type: object
    description: What the tool returns

dependencies: []                   # pip packages (python) or npm packages (node)
tags: []                           # for discovery
created: 2026-04-07
updated: 2026-04-07
author: ayra                       # ayra | ayush
status: stable                     # dev | stable | deprecated
```

## Running a Tool

```bash
# Python tool
_tools/.venv/bin/python _tools/tool-name/run.py --arg1 value1 --arg2 value2

# Node.js tool
node _tools/tool-name/run.js --arg1 value1 --arg2 value2

# Running tests
_tools/.venv/bin/python -m pytest _tools/tool-name/run_test.py -v
```

## Registry

`registry.json` is the master index — auto-maintained by Ayra. Check it to discover available tools.

## Runtimes

| Runtime | When to Use | Env |
|---------|------------|-----|
| **Python** | Data processing, DB ops, ML/embeddings, PDF/image work, analysis. **Default choice.** | `_tools/.venv/` |
| **Node.js** | JSON/API-heavy ops, stream processing, fast CLI tools, when npm packages are best option | `_tools/node_modules/` |

## Shared Code

`_lib/python/` and `_lib/node/` contain shared utilities used across multiple tools. Import from here to avoid duplication.

## Rules

1. **No tool without tests** — tests must pass before registering
2. **Semver versioning** — bump version on every change
3. **One tool, one purpose** — keep tools focused
4. **Dependencies in tool.yaml** — auto-installed into _tools/.venv or node_modules
5. **Git-tracked** — every tool is version controlled
6. **Self-documenting** — tool.yaml IS the documentation

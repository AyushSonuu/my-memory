# 🤖 Minion — Unattended Coding Agents Platform

> **Status:** Product Planning
> **Created:** 2026-04-07
> **Inspiration:** Stripe Minions (1,300 PRs/week, zero human code)
> **Core Agent:** Deep Agents CLI (LangChain, open source, MIT, any LLM)

---

## Vision

A **configurable SaaS platform** where users connect their GitHub repos, create tickets (from our frontend or GitHub Issues), and autonomous coding agents (Minions) pick up tasks, understand the codebase, write production-ready code following the project's conventions, run validation, raise PRs, and even review each other's work — all without human intervention until final review.

```
USER (frontend or GitHub)          MINION PLATFORM                     GITHUB
                                                                        
Create ticket ──────────────► Queue ───► Assign Minion           ┌─── Repo
"Fix login validation"              │                             │
                                    ▼                             │
                              ┌──────────┐                       │
                              │ MINION 1 │  clone/worktree ──────┘
                              │ (Coder)  │  read conventions
                              │          │  plan → implement
                              │          │  lint → test → fix
                              │          │  commit → push
                              │          │  open PR ──────────────► PR #N
                              └──────────┘
                                    │
                              ┌──────────┐
                              │ MINION 2 │  review PR #N ─────────► Review
                              │(Reviewer)│  check quality           comments
                              └──────────┘
                                    │
                              Human does final review + merge
```

---

## Core Components

### 1. Deep Agents CLI — The Coding Engine

**What it is:** LangChain's open-source terminal coding agent. MIT licensed. Provider-agnostic (OpenAI, Anthropic, Google, Ollama, etc.).

**Why this:**
- Built on LangGraph — production runtime with streaming, persistence, checkpointing
- Has everything we need built-in: file ops, shell exec, web search, task planning, memory, sub-agents
- **Headless mode** — `deepagents -n` for non-interactive execution (perfect for unattended)
- **Shell allow-list** — `-S "pytest,git,make,npm"` — controlled shell access
- **Auto-approve** — `-y` — no human-in-the-loop for unattended runs
- **Skills** — custom expertise files the agent loads (like our AGENTS.md pattern!)
- **MCP tools** — extensible via Model Context Protocol
- **LangSmith tracing** — built-in observability
- **Any LLM** — `--model anthropic:claude-sonnet-4-5` or `--model ollama:codellama`
- **Sub-agents** — `task` tool for delegating parallel work

**How we use it:**
```bash
# Non-interactive, auto-approve, shell allow-list, specific model
deepagents -n -y -S "recommended" --model anthropic:claude-sonnet-4-5 \
  "Fix issue #42: Login validation allows empty passwords. 
   Read AGENTS.md for conventions. Run tests after fixing."
```

**Key: We don't build a coding agent. We orchestrate one.**

### 2. Blueprint Engine — The Orchestrator

The thing Stripe custom-built. Deterministic steps + agentic steps in a configurable pipeline.

```yaml
# blueprints/fix-issue.yaml
name: fix-issue
description: Fix a GitHub issue end-to-end

env:
  max_ci_retries: 2
  model: anthropic:claude-sonnet-4-5
  shell_allow: "recommended"

steps:
  - name: setup
    type: deterministic
    actions:
      - git_worktree_create: "/tmp/minion-{{run_id}}"
      - detect_stack          # auto-detect lang, PM, lint, test commands
      - install_deps          # run detected install command

  - name: gather-context
    type: deterministic
    actions:
      - read_repo_rules       # AGENTS.md, .cursor/rules, .deepagents/, README
      - fetch_issue: "{{issue_url}}"  # title, body, comments, labels
      - pre_hydrate_links     # fetch any URLs in issue body (like Stripe does)

  - name: plan-and-implement
    type: agentic
    agent: deepagents
    mode: headless
    prompt_template: |
      ## Task
      {{issue_title}}
      {{issue_body}}
      
      ## Repo Conventions
      {{repo_rules}}
      
      ## Instructions
      1. Explore the codebase to understand the relevant code
      2. Plan your approach
      3. Implement the fix/feature
      4. Make sure your code follows the project's existing patterns
      5. Don't over-engineer — solve exactly what's asked, nothing more
    tools:
      - read_file, write_file, edit_file, ls, glob, grep
      - execute (shell_allow: {{shell_allow}})
      - web_search (if needed)

  - name: validate
    type: deterministic
    actions:
      - run_lint: "{{detected_lint_cmd}}"
      - run_tests: "{{detected_test_cmd}}"
      - run_typecheck: "{{detected_typecheck_cmd}}"  # if available
    on_failure: fix-errors

  - name: fix-errors
    type: agentic
    agent: deepagents
    mode: headless
    max_retries: "{{max_ci_retries}}"
    prompt_template: |
      Validation failed with these errors:
      {{validation_stderr}}
      
      Fix only the failing issues. Don't change unrelated code.
    on_max_retries: ship  # ship even if partial — still useful

  - name: ship
    type: deterministic
    actions:
      - git_add_commit: "fix: resolve #{{issue_id}} — {{issue_title}}"
      - git_push: "fix/{{issue_id}}"
      - gh_pr_create:
          title: "fix: {{issue_title}}"
          body: "Closes #{{issue_id}}\n\n{{pr_description}}"
          labels: ["minion-generated"]
      - cleanup_worktree

  - name: review  # OPTIONAL — another minion reviews the PR
    type: agentic
    agent: deepagents
    mode: headless
    condition: "{{enable_review}}"
    prompt_template: |
      Review PR #{{pr_number}} for:
      1. Code quality and readability
      2. Does it actually fix #{{issue_id}}?
      3. Any edge cases missed?
      4. Over-engineering? Unnecessary changes?
      Post review comments via gh CLI.
```

### 3. Stack Detector — Works On Any Repo

Auto-detect language, package manager, lint/test/typecheck commands by scanning repo files:

```
Detect → (pyproject.toml + uv.lock) → Python + uv
       → lint: ruff check . OR flake8
       → test: pytest OR python -m unittest
       → typecheck: mypy (if configured)

Detect → (package.json + yarn.lock) → Node + yarn  
       → lint: yarn lint OR npx eslint .
       → test: yarn test OR npx jest
       → typecheck: npx tsc --noEmit (if tsconfig.json exists)

Detect → (go.mod) → Go
       → lint: golangci-lint run
       → test: go test ./...

Detect → (Cargo.toml) → Rust
       → lint: cargo clippy
       → test: cargo test
```

Falls back to reading `package.json` scripts, `Makefile` targets, `pyproject.toml [tool.pytest]`, etc.

### 4. Frontend — Ticket Management + Dashboard

**Phase 1 (MVP):** CLI only — no frontend needed yet.

**Phase 2+:** Web dashboard where users can:
- Connect GitHub repos (OAuth)
- Create tickets (synced as GitHub Issues with labels)
- View minion run status (running, completed, failed, partial)
- See agent decision logs (what files it read, what it planned, what it changed)
- Configure: which blueprints to use, which model, retry limits, auto-assign rules
- Review PRs inline (or link to GitHub PR)

```
┌─────────────────────────────────────────────┐
│  MINION DASHBOARD                            │
│                                              │
│  Connected Repos: 3                          │
│  ┌────────────────────────────────────────┐ │
│  │ user/frontend-app    12 PRs this week  │ │
│  │ user/api-server       8 PRs this week  │ │
│  │ user/shared-lib       3 PRs this week  │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  [+ Create Ticket]                           │
│                                              │
│  Recent Runs:                                │
│  ✅ #42 Fix login validation    → PR #87    │
│  ✅ #43 Add dark mode toggle    → PR #88    │
│  ⚠️  #44 Refactor auth module   → Partial   │
│  🔄 #45 Add rate limiting       → Running   │
│  ❌ #46 Migrate to PostgreSQL   → Failed    │
└─────────────────────────────────────────────┘
```

### 5. Multi-Minion Patterns

```
PATTERN 1: Coder + Reviewer (default)
  Minion A writes code → PR
  Minion B reviews PR → comments/approve

PATTERN 2: Parallel Coders
  5 issues assigned → 5 minions spin up simultaneously
  Each works in isolated worktree
  5 PRs created in parallel

PATTERN 3: Coder + Validator
  Minion A writes code → PR
  Minion B pulls the branch, runs extended tests,
  checks for edge cases, security issues

PATTERN 4: Planner + Coder(s)
  Minion A reads complex issue, breaks into sub-tasks
  Sub-tasks created as sub-issues
  Multiple minions pick up sub-tasks in parallel
```

---

## Design Principles (Non-Negotiable)

| Principle | What It Means |
|-----------|--------------|
| **Production-ready code** | Agent writes code that passes lint, tests, type checks. Not "vibe code". |
| **Don't over-engineer** | Solve exactly what's asked. No refactoring the world. No adding features not requested. |
| **Respect repo conventions** | Read AGENTS.md, .cursor/rules, README. Follow existing patterns. |
| **Know when to stop** | Max 2 CI retries. Diminishing returns. Partial is still valuable. |
| **Human review always** | Minions write. Humans review. Never auto-merge. |
| **Configurable, not opinionated** | Any GitHub repo. Any language. Any LLM. Any blueprint. |
| **Observable** | Every run logged. What was read, planned, changed, tested. Traceable. |
| **Isolated** | Each minion in its own worktree/container. Can't affect other work. |
| **Secure** | Shell allow-lists. No arbitrary network access. No secret exposure. |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    MINION PLATFORM                             │
│                                                                │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  Frontend    │  │  CLI        │  │  GitHub Webhooks     │ │
│  │  (Next.js)   │  │  (Python)   │  │  (issue.created)     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬───────────┘ │
│         └────────────────┼─────────────────────┘              │
│                          ▼                                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                    TASK QUEUE                           │   │
│  │  (Redis / PostgreSQL / simple file queue for MVP)      │   │
│  └───────────────────────┬───────────────────────────────┘   │
│                          ▼                                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │              BLUEPRINT ENGINE (Orchestrator)            │   │
│  │                                                         │   │
│  │  Reads: blueprint YAML                                  │   │
│  │  For each step:                                         │   │
│  │    deterministic → run Python/shell                     │   │
│  │    agentic → invoke Deep Agents CLI (headless)          │   │
│  │  Handles: retries, failure routing, timeouts            │   │
│  └──────────┬────────────────────────┬───────────────────┘   │
│             ▼                        ▼                        │
│  ┌──────────────────┐  ┌──────────────────────────┐         │
│  │  ENVIRONMENT MGR  │  │  CONTEXT LOADER           │         │
│  │  git worktrees    │  │  repo rules, issue data,  │         │
│  │  Docker (prod)    │  │  stack detection           │         │
│  │  cleanup          │  │  link pre-hydration        │         │
│  └──────────────────┘  └──────────────────────────┘         │
│             ▼                        ▼                        │
│  ┌───────────────────────────────────────────────────────┐   │
│  │              DEEP AGENTS CLI (headless)                 │   │
│  │  deepagents -n -y -S "recommended" --model X          │   │
│  │  File ops + shell + web search + sub-agents            │   │
│  │  LangSmith tracing for observability                   │   │
│  └───────────────────────────────────────────────────────┘   │
│                          ▼                                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │              FEEDBACK LOOP                              │   │
│  │  lint → test → typecheck → agent retry (max 2)        │   │
│  └───────────────────────────────────────────────────────┘   │
│                          ▼                                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │              SHIP                                       │   │
│  │  git commit → push → gh pr create → label              │   │
│  │  Optional: another minion reviews the PR               │   │
│  └───────────────────────────────────────────────────────┘   │
│                          ▼                                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │              RUN LOG (Observability)                     │   │
│  │  What was read, planned, changed, tested, shipped      │   │
│  │  Stored in DB + optionally LangSmith                   │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Coding Agent** | Deep Agents CLI (headless mode) | Open source, any LLM, LangGraph runtime, sub-agents, MCP |
| **Orchestrator** | Python (our own Blueprint Engine) | We know Python, uv, SOLID patterns |
| **Environment** | Git worktrees (dev) → Docker (prod) | Free, instant, isolated |
| **Stack Detection** | Python (file-based heuristics) | Scan repo files to detect lang/PM/lint/test |
| **Queue** | SQLite (MVP) → Redis/PostgreSQL (scale) | Start simple |
| **Backend API** | FastAPI | Async, fast, Python, OpenAPI docs |
| **Frontend** | Next.js + shadcn/ui | Modern, fast, GitHub OAuth |
| **Database** | PostgreSQL (prod) / SQLite (dev) | Run history, repo configs, user data |
| **Auth** | GitHub OAuth | Users already have GitHub accounts |
| **Observability** | LangSmith (built into Deep Agents) + structured logs | Free tier available |
| **CI/CD** | GitHub Actions | Deploy the platform itself |
| **Hosting** | Vercel (frontend) + Railway/Fly.io (backend) | Cheap, auto-scale |

---

## Build Phases

| Phase | What | Deliverable | Effort |
|-------|------|-------------|--------|
| **0** | ✅ Research + Plan | This document | Done |
| **1** | **MVP CLI** — `minion --issue URL` — single blueprint, Deep Agents headless, worktree, lint+test, PR | Working CLI that one-shots an issue into a PR | 1 week |
| **2** | **Blueprint YAML engine** — parse blueprints, execute deterministic/agentic nodes, retry logic | Configurable pipelines | 1 week |
| **3** | **Stack detection + feedback loop** — auto-detect lang/PM/lint/test, run validation, feed errors back | Works on any repo | 3-4 days |
| **4** | **Multi-minion** — parallel execution, reviewer minion, worktree management | Multiple issues simultaneously | 1 week |
| **5** | **Backend API** — FastAPI, task queue, run history, GitHub webhooks | API that frontend can call | 1 week |
| **6** | **Frontend** — Next.js dashboard, GitHub OAuth, ticket creation, run viewer | Web UI | 1-2 weeks |
| **7** | **Polish + Deploy** — hosting, docs, README, demo video | Public launch | 1 week |

### Total: ~6-8 weeks for full platform

### MVP (Phase 1) — What We Build First

```bash
# Install
uv tool install minion

# One-shot an issue into a PR
minion --issue https://github.com/user/repo/issues/42

# Or describe a task directly
minion --repo user/repo --task "Add input validation to signup form"

# With options
minion --issue URL --model anthropic:claude-sonnet-4-5 --max-retries 2
```

---

## Repo Structure

```
github.com/AyushSonuu/minion
├── pyproject.toml                  # uv, Python 3.13
├── README.md                       # Product description + demo GIF
├── LICENSE                         # MIT
│
├── src/minion/
│   ├── __init__.py
│   ├── cli.py                      # CLI entrypoint (click/typer)
│   ├── orchestrator.py             # Blueprint engine
│   ├── blueprint.py                # YAML parser + step executor
│   ├── environment.py              # Worktree/Docker management
│   ├── context.py                  # Repo rules loader + issue fetcher
│   ├── stack_detector.py           # Language/PM/lint/test detection
│   ├── agent_runner.py             # Deep Agents CLI adapter (headless)
│   ├── feedback.py                 # Lint + test runner + error parser
│   ├── shipper.py                  # Git commit + push + PR creation
│   └── models.py                   # Data models (frozen dataclasses)
│
├── blueprints/
│   ├── fix-issue.yaml              # Default: fix a GitHub issue
│   ├── add-feature.yaml            # Add a feature from description
│   ├── review-pr.yaml              # Review an existing PR
│   └── fix-flaky-test.yaml         # Fix a flaky test (like Stripe)
│
├── tests/
│   ├── test_blueprint.py
│   ├── test_stack_detector.py
│   ├── test_environment.py
│   └── test_feedback.py
│
├── api/                            # Phase 5: FastAPI backend
│   ├── main.py
│   ├── routes/
│   └── models/
│
└── frontend/                       # Phase 6: Next.js dashboard
    ├── package.json
    └── src/
```

---

## Competitive Landscape

| Product | Model | Strength | Our Differentiation |
|---------|-------|----------|-------------------|
| **Stripe Minions** | Internal, closed | 1,300 PRs/week at scale | We're **open source**, any repo |
| **GitHub Copilot Workspace** | Attended, GitHub-only | Deep GitHub integration | We're **unattended**, any LLM |
| **Devin** | SaaS, expensive | Full agent with browser | We're **lightweight**, CLI-first |
| **Sweep AI** | SaaS | Issue → PR flow | We're **self-hostable**, open blueprints |
| **CodeRabbit** | SaaS | PR review only | We do **code + review** |
| **OpenHands** | Open source | Browser-based agent | We're **terminal-native**, Deep Agents |

**Our niche: Open-source, self-hostable, configurable blueprints, any LLM, any GitHub repo.**

---

## YouTube Angle (Deep Agents Playlist)

| Episode | Title |
|---------|-------|
| 1 | How Stripe Ships 1,300 PRs/Week with Zero Human Code |
| 2 | Building the Blueprint Engine — Hybrid Deterministic + Agentic Pipelines |
| 3 | Deep Agents CLI — The Open Source Claude Code Alternative |
| 4 | Stack Detection — Making Minions Work on Any Repo |
| 5 | Live Build — Issue to PR in Under 5 Minutes |
| 6 | Multi-Minion — Coder + Reviewer Working Together |
| 7 | Building the Dashboard — Next.js + FastAPI + GitHub OAuth |

---

## Open Decisions (To Resolve Before Building)

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Product name | Minion / Forge / Codelet / AutoPR | Need to brainstorm — "Minion" is Stripe's brand |
| 2 | Primary LLM | Claude Sonnet / GPT-4o / Codestral | Default Claude Sonnet, configurable |
| 3 | Blueprint format | YAML / TOML / Python DSL | YAML — human-readable, versionable |
| 4 | Environment | Worktrees only / Docker / both | Worktrees for MVP, Docker option for prod |
| 5 | Hosting model | SaaS only / self-host only / both | Both — CLI self-host, hosted dashboard option |
| 6 | Pricing (if SaaS) | Free tier + paid / open core | Open core — CLI free, dashboard paid |

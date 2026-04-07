# 🔬 Deep Research: How Unattended Coding Agent Platforms Work

> **Purpose:** Understand the detailed mechanics before building. No code until we understand the system.
> **Date:** 2026-04-07
> **Sources:** Stripe Minions (Part 1 + ByteByteGo), OpenHands, Sweep AI, Qodo PR-Agent, Goose, GitHub Apps/API docs, Deep Agents CLI docs

---

## 1. How Does an Agent Actually Raise a PR?

This is the critical path. Every system does it slightly differently.

### Method A: `gh` CLI (Simplest — what Sweep, local tools use)

```bash
# Agent writes code in a branch, then:
git checkout -b fix/issue-42
git add -A
git commit -m "fix: resolve login validation — closes #42"
git push origin fix/issue-42

# Create PR via gh CLI (uses user's GitHub token)
gh pr create \
  --title "fix: Login validation allows empty passwords" \
  --body "Closes #42\n\nChanges:\n- Added validation..." \
  --base main \
  --head fix/issue-42 \
  --label "minion-generated"
```

**Pros:** Simple, uses existing auth (`gh auth login`), works locally.
**Cons:** Uses the user's identity. PR shows as authored by the human, not the bot.
**When:** CLI tools, local execution, personal use.

### Method B: GitHub App (What Stripe, OpenHands Cloud, Sweep SaaS use)

A **GitHub App** is a first-class GitHub integration that:
- Installs on a repo/org with specific permissions
- Gets its own identity (PRs show as "authored by bot")
- Receives **webhooks** (issue.created, push, PR events)
- Uses **installation access tokens** (server-to-server, no user needed)

```
1. User installs your GitHub App on their repo
   → App gets permissions: read code, write PRs, read issues, write comments
   → App subscribes to webhooks: issues.opened, issue_comment.created

2. User creates an issue labeled "minion"
   → GitHub sends webhook to your server: POST /webhooks
   → { action: "labeled", issue: { number: 42, title: "Fix login", body: "..." } }

3. Your server:
   → Clones repo (using installation token)
   → Runs agent in isolated environment
   → Agent writes code, runs tests
   → Pushes branch using installation token
   → Creates PR via GitHub REST API (as the app, not as a user)

4. PR appears as "authored by YourAppName[bot]"
   → Human reviews + merges
```

**GitHub App Permissions needed:**
| Permission | Access | Why |
|-----------|--------|-----|
| `contents` | read + write | Clone repo, push branches |
| `pull_requests` | read + write | Create PRs, add comments |
| `issues` | read + write | Read issue details, add labels, comment |
| `checks` | read | See CI status |
| `metadata` | read | Repo info |

**How the token flow works:**
```
GitHub App (registered) → has App ID + Private Key
                       → generates JWT
                       → exchanges JWT for Installation Token (per-repo)
                       → uses Installation Token for API calls
                       → token expires after 1 hour, auto-refresh
```

### Method C: GitHub Actions (What PR-Agent uses)

A GitHub Action that triggers on issue/PR events:

```yaml
# .github/workflows/minion.yml
name: Minion
on:
  issues:
    types: [labeled]
  
jobs:
  run-minion:
    if: contains(github.event.label.name, 'minion')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run coding agent
        uses: your-org/minion-action@v1
        with:
          issue_number: ${{ github.event.issue.number }}
          model: "anthropic:claude-sonnet-4-5"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Pros:** Runs in GitHub's infra, free for public repos, no server needed.
**Cons:** Limited to Actions runtime (6hrs max), needs secrets configured per-repo.
**When:** Open-source distribution. Users add one workflow file = done.

### Our Decision

**Phase 1 (CLI/MVP):** Method A — `gh` CLI. Simplest. Proves the concept.
**Phase 2 (Platform):** Method B — GitHub App. Proper identity, webhooks, multi-user.
**Phase 3 (Distribution):** Method C — GitHub Action. Easy adoption for open-source users.

---

## 2. Open Source Landscape — Who's Built What?

### OpenHands (formerly OpenDevin)

| Aspect | Detail |
|--------|--------|
| **What** | AI-driven development platform — SDK + CLI + GUI + Cloud |
| **Architecture** | SDK (Python) → CLI → Local GUI → Cloud (hosted) → Enterprise |
| **Agent** | Custom CodeAct agent on top of their SDK |
| **Execution** | Docker sandbox (isolated containers) |
| **GitHub** | Cloud has Slack, Jira, Linear integrations. Issue → PR flow. |
| **License** | MIT (core), proprietary (enterprise features) |
| **Scale** | GitHub star: 50k+, very active |
| **Lesson for us** | Multi-layer product: SDK → CLI → GUI → Cloud → Enterprise. Start with SDK/CLI, expand. |

### Sweep AI

| Aspect | Detail |
|--------|--------|
| **What** | GitHub bot: Issue → PR. Originally the OG of this space. |
| **Architecture** | GitHub App + webhook handler + agent pipeline |
| **Trigger** | Label an issue "sweep" → bot picks it up |
| **How** | Reads repo, plans changes, writes code, creates PR |
| **Config** | `sweep.yaml` in repo root (rules, branch, ignored dirs) |
| **Status** | Pivoted to JetBrains plugin. Original GitHub bot less active. |
| **License** | Open source (Python) |
| **Lesson for us** | `sweep.yaml` config per-repo is smart. Webhook-triggered GitHub App is the proven pattern. |

### Qodo PR-Agent (formerly CodiumAI)

| Aspect | Detail |
|--------|--------|
| **What** | AI-powered PR review tool (describe, review, improve, ask) |
| **Architecture** | CLI + GitHub Action + GitHub App + Webhook |
| **Scope** | Reviews PRs, doesn't write code from scratch |
| **Distribution** | Multiple install methods: CLI (`pip install`), GitHub Action, Docker, webhook |
| **Platforms** | GitHub, GitLab, Bitbucket, Azure DevOps, Gitea |
| **License** | Open source (core), commercial (Qodo Merge) |
| **Lesson for us** | Review-only agent = simpler but very useful. We should have reviewer minions too. Multi-platform is a differentiator. |

### Goose (AAIF, formerly Block)

| Aspect | Detail |
|--------|--------|
| **What** | General-purpose AI agent. Desktop app, CLI, API. |
| **Architecture** | Rust-based. 15+ LLM providers. 70+ MCP extensions. |
| **Connection to Stripe** | Stripe forked Goose early on as the base for Minions |
| **Execution** | Local machine, MCP for external tools |
| **License** | Apache 2.0 |
| **Lesson for us** | Goose is too general. Stripe had to customize heavily. We need opinionated orchestration, not a general agent. |

### Stripe Minions (Closed, but Documented)

| Aspect | Detail |
|--------|--------|
| **Base** | Forked Goose, heavily customized |
| **Key innovation** | Blueprints (hybrid deterministic + agentic pipelines) |
| **Environment** | Pre-warmed cloud devboxes (10s spin-up), isolated from prod |
| **Context** | Scoped rules per subdirectory + MCP Toolshed (400+ tools) |
| **Context pre-hydration** | Deterministically fetch links in issue body BEFORE agent starts |
| **Feedback** | Local lint (<5s daemon) → selective CI (from 3M tests) → max 2 retries |
| **Trigger** | Slack (primary), CLI, web UI, internal app integrations, flaky test auto-tickets |
| **Output** | PR following company template, labeled, ready for review |
| **Scale** | 1,300+ PRs merged/week |

---

## 3. Detailed Architecture Decisions

### Environment Isolation

| Option | Speed | Isolation | Cost | When |
|--------|-------|-----------|------|------|
| **Git worktrees** | Instant | Branch-level (same machine) | Free | MVP, local CLI |
| **Docker containers** | ~10-30s | Full (filesystem + network) | Low | Production, multi-user |
| **Cloud VMs (like Stripe)** | 10s (with warm pool) | Complete | High | Enterprise scale |
| **GitHub Codespaces** | ~60s | Complete | Medium | Hosted option |

**Our path:** Worktrees (Phase 1) → Docker (Phase 2) → Cloud option (Phase 3+)

### Context Strategy (Critical — What Stripe Got Right)

**The Problem:** Agent has limited context window. Can't dump entire codebase.

**Stripe's Approach:**
1. **Conditional rules** — rules scoped to subdirectories, loaded as agent navigates
2. **MCP tools** — agent calls tools to fetch specific context (docs, tickets, search)
3. **Pre-hydration** — before agent starts, deterministically fetch all links in the issue body
4. **Curated tool subsets** — not all 400 tools. Agent gets a small relevant set.

**Our Approach:**
1. **Read repo rules first** — AGENTS.md, .cursor/rules, .deepagents/skills/, README.md, CONTRIBUTING.md
2. **Issue context** — title, body, comments, linked issues, mentioned files
3. **Pre-hydrate** — if issue body has URLs, fetch them before agent starts
4. **Deep Agents skills** — custom per-repo skills loaded automatically
5. **Stack-aware context** — based on detected stack, load relevant conventions

### Feedback Loop Design

```
AGENT WRITES CODE
       │
       ▼
┌──────────────────┐
│ LOCAL VALIDATION  │ ← Fast, <10 seconds
│ • Lint (ruff/eslint/clippy)
│ • Format check (prettier/black)
│ • Type check (mypy/tsc)
└──────┬───────────┘
       │ Pass? ──→ CI
       │ Fail? ──→ Feed errors back to agent (retry 1)
       ▼
┌──────────────────┐
│ CI VALIDATION     │ ← Slower, selective tests
│ • Run tests
│ • Integration checks
└──────┬───────────┘
       │ Pass? ──→ Ship PR
       │ Fail? ──→ Feed errors back to agent (retry 2)
       │           If still fails → Ship partial PR with note
       ▼
┌──────────────────┐
│ SHIP              │ ← Deterministic, always runs
│ • git commit
│ • git push
│ • gh pr create
│ • Label: minion-generated
│ • Comment: run summary
└──────────────────┘
```

**Hard cap: 2 CI retries maximum.** Stripe validated this — diminishing returns after 2.

### Multi-Minion Coordination

```
ISSUE TYPES → MINION PATTERNS

Simple bug fix      → 1 Coder minion + 1 Reviewer minion (optional)
Feature request     → 1 Planner minion → N Coder minions (parallel) → 1 Reviewer
Flaky test          → 1 Coder minion (specialized blueprint)
Refactoring         → 1 Planner → N Coders (split by file/module) → 1 Reviewer
Multiple issues     → N independent Coders (parallel worktrees)
```

**Reviewer minion:** Separate agent that:
- Reads the PR diff
- Checks against repo conventions
- Looks for edge cases, over-engineering, unnecessary changes
- Posts review comments via GitHub API
- Approves or requests changes

---

## 4. How to Make PRs Actually Good (Not Over-Engineered)

This is the hardest part. An agent that writes code is easy. An agent that writes **good** code is hard.

### System Prompt Design (Critical)

```
You are a coding agent fixing issue #{{issue_id}} in {{repo_name}}.

RULES:
1. FIX EXACTLY WHAT'S ASKED. Nothing more.
2. Follow the repo's existing patterns and conventions.
3. Don't refactor code unrelated to the issue.
4. Don't add features not requested.
5. Don't change code style unless that's the task.
6. If unsure about a convention, look at surrounding code and match it.
7. Keep changes minimal. Smallest diff that solves the problem.
8. Add/update tests for your changes if the repo has tests.
9. If you can't fully solve it, solve what you can and document what's left.

REPO CONVENTIONS:
{{repo_rules}}
```

### Quality Guardrails (Deterministic)

| Check | How | When |
|-------|-----|------|
| **Diff size** | Count changed lines. Flag if >500 lines for a "small fix" | Before shipping |
| **Unrelated changes** | Compare changed files vs files mentioned in issue | Before shipping |
| **New dependencies** | Flag if agent adds new packages not in the issue scope | Before shipping |
| **Test coverage** | Check if changed files have corresponding test changes | Before shipping |
| **Convention compliance** | Run repo's lint/format | During feedback loop |

---

## 5. Product Configuration (Per-Repo)

Users configure per-repo via a config file (like `sweep.yaml`):

```yaml
# .minion.yaml (in repo root)
model: anthropic:claude-sonnet-4-5    # default LLM
max_retries: 2                         # CI retry cap
auto_assign: true                      # auto-pick up labeled issues
labels:
  trigger: "minion"                    # which label triggers a run
  generated: "minion-generated"        # label added to PRs
branch_prefix: "minion/"               # branch naming
rules:                                 # additional context files
  - AGENTS.md
  - CONTRIBUTING.md
  - .cursor/rules
ignore:                                # don't touch these
  - "*.lock"
  - "dist/"
  - "node_modules/"
review:
  enabled: true                        # auto-review PRs
  model: anthropic:claude-sonnet-4-5   # can use different model for review
blueprints:
  bug: fix-issue                       # label "bug" → fix-issue blueprint
  feature: add-feature                 # label "feature" → add-feature blueprint
  test: fix-flaky-test                 # label "test" → fix-flaky-test blueprint
```

---

## 6. Summary: What We Build (In Order)

| # | What | How | Key Question Answered |
|---|------|-----|----------------------|
| 1 | **CLI MVP** | Python + Deep Agents (headless) + `gh` CLI | "Can an agent fix an issue and raise a PR?" |
| 2 | **Blueprint Engine** | YAML parser + step executor | "Can we orchestrate deterministic + agentic?" |
| 3 | **Stack Detector** | File-based heuristics | "Can it work on any repo?" |
| 4 | **GitHub App** | Webhooks + installation tokens | "Can it trigger automatically from issues?" |
| 5 | **Reviewer Minion** | Second agent reads PR diff | "Can agents review each other?" |
| 6 | **Parallel Execution** | Worktree pool + concurrent agents | "Can it handle multiple issues at once?" |
| 7 | **Frontend** | Next.js dashboard | "Can non-CLI users manage this?" |

---

## 7. Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Agent writes bad code | PR rejected, wasted time | Strong system prompt + lint + tests + reviewer minion + diff guards |
| Agent hallucinates fixes | Wrong changes merged | Human review always required. Never auto-merge. |
| Agent loops forever | Cost explosion | Hard retry cap (2). Timeout per step. Budget per run. |
| Agent modifies wrong files | Unrelated changes | Diff guard: flag files not mentioned in issue |
| Context window overflow | Agent loses context | Pre-hydrate only relevant context. Use Deep Agents compaction. |
| API rate limits | Runs stall | Exponential backoff. Queue with rate limiting. |
| Security: agent executes malicious code | Data leak, damage | Sandboxed environment. Shell allow-list. No prod access. |
| Cost per run | Expensive at scale | Track tokens/run. Configurable model (cheaper for simple tasks). |

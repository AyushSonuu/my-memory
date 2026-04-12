# EGDR Evaluation Framework — Working Folder

> **Project:** Build a comprehensive, user-centric evaluation framework for Experience Generation Deep Research
> **Owner:** Ayush Sonu (I772464)
> **Started:** 2026-04-12
> **Status:** 🟡 Design Complete → Implementation Phase

## Purpose

This folder is Ayra's **persistent working memory** for the EGDR eval project. Everything discovered, designed, and decided lives here — no context lost between sessions.

## Folder Structure

```
egdr-evals/
├── README.md                  ← You are here (project overview + status)
├── STATUS.md                  ← Current progress, blockers, next actions
├── research/                  ← Web research, paper summaries, technique notes
│   ├── white-paper-summary.md    ← Brad's eval-framework.md distilled
│   ├── andrew-ng-evals.md        ← Module 4 concepts mapped to EGDR
│   ├── anthropic-eval-guide.md   ← Anthropic's "Demystifying Evals" key points
│   └── deepeval-langfuse.md      ← How DeepEval + Langfuse work together
├── codebase-audit/            ← What exists in the repo today
│   ├── component-inventory.md    ← Every evaluable component catalogued
│   ├── existing-evals.md         ← What's already built + status
│   └── file-map.md               ← Key file paths reference
├── design/                    ← Architecture docs (HLD, LLD, decisions)
│   ├── eval-framework-design.md  ← The full HLD+LLD (master doc)
│   ├── decisions.md              ← Architecture Decision Records (ADRs)
│   └── user-centric-evals.md     ← Product vision for user-facing evals
├── eval-sets/                 ← Eval set development workspace
│   └── (future: case templates, gold set drafts)
└── sessions/                  ← Session logs (what was done each session)
    └── 2026-04-12.md             ← Today's session
```

## Quick Links

| What | Where |
|------|-------|
| Full design doc (HLD+LLD) | [`design/eval-framework-design.md`](design/eval-framework-design.md) |
| Current status + next steps | [`STATUS.md`](STATUS.md) |
| Component inventory | [`codebase-audit/component-inventory.md`](codebase-audit/component-inventory.md) |
| Existing eval infra audit | [`codebase-audit/existing-evals.md`](codebase-audit/existing-evals.md) |

## Key Context

- **Repo:** `experience-generation-server` on SAP GitHub
- **Stack:** Python, LangGraph, LangChain, Langfuse, DeepEval (dep broken)
- **Brad Powley** wrote the eval framework white paper — we align with his 8-milestone roadmap
- **User-centric evals** = the cross-app product vision from team discussion
- **Andrew Ng Module 4** = our methodology foundation (error analysis, 2×2 grid, component evals)

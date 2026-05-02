# Spec-Driven Development (SDD) Skill

> **Stop vibe-coding. Write the spec, let the agent code. You think, it types.**

A comprehensive skill for guiding users through the complete Spec-Driven Development workflow—a structured approach to AI-assisted software development from the DeepLearning.AI × JetBrains course.

## What This Skill Does

This skill helps users:

1. **Create Project Constitutions** — Document mission, tech stack, and roadmap
2. **Write Feature Specifications** — Plan, requirements, and validation before coding
3. **Guide Implementation** — Supervise agent-driven development
4. **Review and Validate** — High-level code review preventing drift
5. **Facilitate Replanning** — Continuous improvement between features
6. **Build Automation** — Create agent skills for repeated workflows
7. **Support Brownfield Projects** — Reverse-engineer specs from existing code

## Why SDD Matters

| Problem | SDD Solution |
|---------|-------------|
| **Context Decay** | Specs persist across sessions and agents |
| **Downstream Amplification** | One spec sentence → cascading code changes |
| **Intent Drift** | You define problem, agent elaborates aligned plan |
| **Team Chaos** | Constitution provides single source of truth |
| **Cognitive Debt** | Manageable feature loops + high-level reviews |

## The SDD Workflow

```
Constitution → Feature Loop → Replan → Repeat
             (Plan → Implement → Validate)
```

**Key Insight:** Specs decouple *what/why* (you) from *how* (agent).

## Skill Structure

```
spec-driven-development/
├── SKILL.md                      # Main skill instructions
├── README.md                     # This file
└── references/
    ├── 01-constitution.md                # Creating mission, tech stack, roadmap
    ├── 02-feature-specification.md       # Writing plan, requirements, validation
    ├── 03-implementation-validation.md   # Implementation & code review
    ├── 04-replanning-advanced.md         # Replanning & advanced patterns
    └── 05-quick-reference.md             # Cheatsheet & flashcards
```

## When to Use This Skill

Invoke when user wants to:

- **Start a new project** systematically with AI
- **Add SDD to existing codebase** (brownfield)
- **Write a project constitution**
- **Plan a feature** before coding
- **Review their workflow** and improve it
- **Build agent skills** for automation
- **Transition from vibe coding** to structured development

## Quick Start

### For Greenfield Projects

```markdown
User: "I want to build [PROJECT] with SDD"

You:
1. Interview about mission, tech stack, roadmap
2. Create constitution (3 files in specs/)
3. Review and iterate
4. Start feature loop
```

### For Brownfield Projects

```markdown
User: "I have an existing codebase, want to use SDD"

You:
1. Read code, README, commits, TODOs
2. Reverse-engineer constitution
3. Present findings for confirmation
4. Start feature loop
```

## Core Principles

1. **Never edit specs manually** — ask agent (keeps consistency)
2. **/clear before major phases** — fresh context
3. **Small roadmap steps** — manageable features
4. **Control process, not minutiae** — architecture, not variable names
5. **Fix spec AND code** — when bugs flow from spec gaps
6. **Replanning is mandatory** — prevents compounding errors

## Reference Materials

Each reference file provides deep-dive guidance:

| File | Content |
|------|---------|
| `01-constitution.md` | Constitution creation (greenfield + brownfield) |
| `02-feature-specification.md` | Writing plan, requirements, validation |
| `03-implementation-validation.md` | Implementation process & code review |
| `04-replanning-advanced.md` | Replanning, agent skills, research backlog |
| `05-quick-reference.md` | Cheatsheet, prompts, flashcards |

Direct users to read specific references when deep details are needed.

## Example Invocations

```markdown
"Help me set up spec-driven development for my project"
"I want to write a constitution"
"Let's plan this feature properly before coding"
"I'm tired of vibe coding, how do I structure this?"
"Can you help me transition this codebase to SDD?"
```

## Success Metrics

User has successfully adopted SDD when:

1. ✅ Constitution exists and is committed
2. ✅ Features developed on separate branches with specs
3. ✅ Using `/clear` before major phases
4. ✅ Replanning happens between features
5. ✅ Specs updated via agent (not manual)
6. ✅ User reports improved workflow

## Course Source

Based on: **"Spec-Driven Development with Coding Agents"**
- **Platform**: DeepLearning.AI × JetBrains
- **Instructor**: Paul Everitt (Developer Advocate, JetBrains)
- **Intro by**: Andrew Ng

## Related Standards & Tools

- **MCP** (Model Context Protocol) — External tools
- **ACP** (Agent Client Protocol) — Agent-client connections
- **Agent Skills** — Repeatable workflows
- **Frameworks**: GitHub Spec Kit, OpenSpec (Fission AI)

## The Golden Rule

> **You are the architect. The agent is the builder. Provide the blueprint (spec), supervise the construction (review), but don't micromanage the tools (variable names).**

---

**Version**: 1.0.0  
**Created**: 2026-04-24  
**License**: Based on DeepLearning.AI course materials

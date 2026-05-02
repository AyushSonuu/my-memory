# SDD Quick Reference — Cheatsheet

## The SDD Workflow (One Page)

```
┌─────────────────────────────────────────────┐
│ 1. CONSTITUTION (once, then evolves)        │
│    Mission + Tech Stack + Roadmap            │
│    Greenfield: converse with agent          │
│    Brownfield: reverse-engineer from code   │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│ 2. FEATURE LOOP (repeat per feature)        │
│    ┌────────────────────────────────────┐   │
│    │ a. Plan (fresh branch, /clear)     │   │
│    │    - plan.md, requirements.md,     │   │
│    │      validation.md                 │   │
│    └────────────────────────────────────┘   │
│    ┌────────────────────────────────────┐   │
│    │ b. Implement (/clear again)        │   │
│    │    - Agent builds from spec        │   │
│    └────────────────────────────────────┘   │
│    ┌────────────────────────────────────┐   │
│    │ c. Validate (high-level review)    │   │
│    │    - Fix spec AND code if gaps     │   │
│    └────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│ 3. REPLAN (between features, mandatory!)    │
│    - Update constitution                    │
│    - Revise roadmap                         │
│    - Improve workflow (build skills)        │
└─────────────────────────────────────────────┘
```

---

## Core Principles

| Principle | Why |
|-----------|-----|
| **Never edit specs manually** | Causes drift (docs out of sync) |
| **/clear before major phases** | Fresh context, constitution as source |
| **Small roadmap steps** | Manageable features, less AI fatigue |
| **Control process, not minutiae** | Decide architecture, not variable names |
| **Fix spec AND code** | When bugs flow from spec gaps |
| **Replanning is mandatory** | Prevents compounding errors |

---

## File Structure

```
project/
├── specs/
│   ├── mission.md           # Vision, audience, scope
│   ├── tech-stack.md        # Architecture, DB schema, API
│   ├── roadmap.md           # Sequence of phases
│   └── features/
│       └── feature-name/
│           ├── plan.md           # Task groups
│           ├── requirements.md   # Technical needs
│           └── validation.md     # Success criteria
├── backlog/                 # Research findings
│   └── research-topic.md
└── [your code]
```

---

## Constitution Checklist

**mission.md:**
- [ ] Vision and goals clear
- [ ] Target audience defined
- [ ] Scope and constraints specified
- [ ] Problems to solve listed

**tech-stack.md:**
- [ ] Framework versions pinned
- [ ] Database schema defined
- [ ] API contracts documented
- [ ] Architecture patterns specified
- [ ] Smoke tests listed

**roadmap.md:**
- [ ] Phases small and manageable
- [ ] Sequence logical
- [ ] Dependencies clear
- [ ] Each phase described

---

## Feature Spec Checklist

**plan.md:**
- [ ] Approach clear
- [ ] Task groups defined
- [ ] Sequence logical
- [ ] Dependencies identified

**requirements.md:**
- [ ] Technical needs captured
- [ ] Constraints specified
- [ ] Versions pinned (if needed)
- [ ] No minutiae (variable names, etc.)

**validation.md:**
- [ ] Success criteria measurable
- [ ] Automated tests specified
- [ ] Manual steps documented
- [ ] Balance of both achieved

---

## Common Prompts

### Start Constitution (Greenfield)

```
I'm building [PROJECT] with [TECH]. Target audience: [AUDIENCE].

Can you help create a constitution (mission, tech stack, roadmap)?
Use AskUserQuestion for clarifications.
```

### Reverse-Engineer Constitution (Brownfield)

```
I have an existing [LANGUAGE] project. Can you reverse-engineer
a constitution from the codebase?

Code: [PATH], README: [PATH], recent commits and TODOs for roadmap.
```

### Start Feature Spec

```
Ready to implement [FEATURE] from roadmap.

Can you write the feature spec (plan, requirements, validation)?
Constitution: specs/
```

### Implement Feature

```
Implement all task groups from:
- Plan: specs/features/[name]/plan.md
- Requirements: specs/features/[name]/requirements.md
- Validation: specs/features/[name]/validation.md

Constitution: specs/
```

### Fix Spec Gap

```
Bug found: [ISSUE]. This is a spec gap.

Update:
1. requirements.md to add [REQUIREMENT]
2. Code to implement it
3. validation.md to test it
```

### Replan After Feature

```
Let's replan after [FEATURE]:
1. Constitution gaps discovered?
2. Roadmap phases still right?
3. Repeated workflows to automate (skills)?
```

### Research Backlog

```
Research [TOPIC], don't change anything yet.
Write findings to: backlog/research-[topic].md
Include: pros/cons, trade-offs, next steps.
```

### Create Agent Skill

```
I keep repeating [WORKFLOW]. Can we automate with a skill?
Use your skill-creator to build it.
```

---

## Validation Review Levels

### ✅ High-Level (FOCUS HERE)

- Feature works as spec'd?
- Conventions followed?
- Structure correct?
- Aligns with constitution?
- Tests passing?

### ❌ Low-Level (DON'T NITPICK)

- Variable names
- CSS classes
- Minor formatting

---

## When to Use What

| Situation | Action |
|-----------|--------|
| Starting new project | Create constitution (greenfield) |
| Existing codebase | Reverse-engineer constitution (brownfield) |
| Planning feature | Write feature spec (plan, requirements, validation) |
| Before coding | `/clear` for fresh context |
| After feature | Replan (update constitution, roadmap, workflow) |
| Repeated workflow | Build agent skill |
| Mid-feature idea | Research backlog pattern |
| Spec mistake found | Fix spec AND code (ask agent) |

---

## Key Terms Flashcard Style

**SDD** = Write markdown spec → agent implements → engineered code

**Constitution** = Project-level specs (mission + tech stack + roadmap)

**Feature Spec** = Plan + requirements + validation for one feature

**Vibe Coding** = Freestyle prompting without specs → disposable code

**Context Decay** = Loss of project context across agent sessions

**Downstream Amplification** = Small spec changes → large code changes

**Drift** = Specs and code out of sync

**Cognitive Debt** = Mental load of tracking fast-generated code

**Replanning** = Update constitution/roadmap/workflow between features

**Agent Skills** = Automation for repeated workflows

**Research Backlog** = File away ideas for later without stopping work

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Editing specs manually | Ask agent to edit (keeps consistency) |
| Skipping /clear | Context contamination → stale specs |
| Roadmap phases too big | Split into smaller steps |
| Nitpicking low-level details | Focus on high-level review |
| Skipping replanning | Mandatory between features |
| Not defining DB schema upfront | Hard to change later |
| Treating specs as "write once" | They're living, will evolve |

---

## Success Metrics

User has successfully adopted SDD when:

1. ✅ Constitution exists and committed
2. ✅ Features on separate branches with specs
3. ✅ Using /clear before major phases
4. ✅ Replanning between features
5. ✅ Specs updated via agent (not manual)
6. ✅ User reports improved workflow

---

## Resources

- **Course**: DeepLearning.AI × JetBrains — "Spec-Driven Development with Coding Agents"
- **Frameworks**: GitHub Spec Kit, OpenSpec (Fission AI)
- **Standards**: MCP, ACP, Agent Skills

---

## The Golden Rule

> **You are the architect. The agent is the builder. Provide the blueprint (spec), supervise the construction (review), but don't micromanage the tools (variable names).**

---

## Next-Level Patterns

- **Skill chains**: One skill calls another
- **Spec version control**: Tag constitution versions
- **Automated health checks**: Periodic constitution reviews
- **Sub-agent validation**: Independent deep reviews
- **Validation automation**: Turn manual steps into scripts

---

**📖 Full Guides:**
- `01-constitution.md` — Constitution creation
- `02-feature-specification.md` — Writing feature specs
- `03-implementation-validation.md` — Implementation & validation
- `04-replanning-advanced.md` — Replanning & advanced patterns

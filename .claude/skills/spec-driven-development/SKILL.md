---
name: spec-driven-development
description: Guide users through the complete Spec-Driven Development workflow for AI-assisted coding. Use this skill when users want to build software systematically with coding agents (like Claude Code, GitHub Copilot, Cursor, etc.), transition from "vibe coding" to structured development, create project specifications (Constitution: mission + tech stack + roadmap), implement features through spec-first planning, work with existing codebases (brownfield projects), or build automated workflows with agent skills. This skill implements the DeepLearning.AI course methodology for professional AI-assisted development.
compatibility:
  tools: [Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion]
---

# Spec-Driven Development (SDD)

> **Stop vibe-coding. Write the spec, let the agent code. You think, it types.**

This skill guides users through the complete Spec-Driven Development workflow—a structured approach to AI-assisted software development that treats specifications as first-class artifacts and agents as highly capable builders.

## What Is Spec-Driven Development?

SDD decouples **specification** (what + why) from **implementation** (how):

- **You write**: Clear markdown specs defining goals, constraints, and success criteria
- **Agent implements**: Generates code from your specifications
- **Result**: Engineered, maintainable code instead of disposable "vibe code"

### Why SDD Matters

| Problem | SDD Solution |
|---------|-------------|
| **Context Decay** — Agents are stateless, lose project context | Specs persist across sessions and agents |
| **Downstream Amplification** — Small changes require rewriting hundreds of lines | One spec sentence → cascading code changes |
| **Intent Drift** — Agent guesses at requirements | You define problem, agent elaborates aligned plan |
| **Team Chaos** — Multiple agents build contradictory features | Constitution provides single source of truth |

## The SDD Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. CONSTITUTION (One-time, then evolving)              │
│    Mission + Tech Stack + Roadmap                       │
│    [Read: references/01-constitution.md]                │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 2. FEATURE LOOP (Repeat for each feature)              │
│    ┌───────────────────────────────────────────────┐   │
│    │ a. Plan → Feature Spec (Plan + Requirements + │   │
│    │    Validation)                                 │   │
│    │    [Read: references/02-feature-specification.md]│
│    └───────────────────────────────────────────────┘   │
│    ┌───────────────────────────────────────────────┐   │
│    │ b. Implement → Agent builds from spec         │   │
│    │    [Read: references/03-implementation.md]     │   │
│    └───────────────────────────────────────────────┘   │
│    ┌───────────────────────────────────────────────┐   │
│    │ c. Validate → Review & verify                 │   │
│    │    [Read: references/04-validation.md]         │   │
│    └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 3. REPLAN (Between features)                            │
│    Update constitution, revise roadmap, improve process │
│    [Read: references/05-replanning.md]                  │
└─────────────────────────────────────────────────────────┘
```

## When to Use This Skill

Invoke this skill when the user wants to:

- **Start a new project** with AI assistance (greenfield)
- **Add SDD to existing project** (brownfield)
- **Write a constitution** for a project
- **Plan a feature** before implementation
- **Review their SDD workflow** and improve it
- **Build agent skills** to automate repeated tasks
- **Transition from vibe coding** to structured development

## How to Guide Users Through SDD

### Phase 1: Assess Starting Point

First, determine where the user is:

```markdown
Ask:
1. "Are you starting a new project (greenfield) or working with existing code (brownfield)?"
2. "Do you have a constitution already, or should we create one?"
3. "What's your goal right now—starting fresh, planning a feature, or improving your workflow?"
```

Based on their answer, guide them to the appropriate phase.

---

### Phase 2: Constitution Creation

**For Greenfield Projects:**

1. **Interview the User** (conversational approach)
   - What problem are you solving?
   - Who is your target audience?
   - What's your scope and constraints?
   - What's your tech stack preference (or should I suggest)?
   - How granular should the roadmap be?

2. **Draft the Constitution**
   Create three files in `specs/`:
   
   ```
   specs/
   ├── mission.md       # Vision, audience, scope, constraints
   ├── tech-stack.md    # Architecture, DB schema, API design, smoke tests
   └── roadmap.md       # Sequence of feature phases (keep small!)
   ```

3. **Review as Spec Reviewer**
   After drafting, review for:
   - Inconsistencies between documents
   - Missing technical details (DB schema, API contracts)
   - Ambiguous requirements
   - Alignment between mission and tech choices

4. **Iterate via Conversation**
   - Never edit specs manually
   - User asks for changes → you update ALL related documents
   - Keep artifacts consistent

**For Brownfield Projects:**

1. **Reverse-Engineer Constitution**
   - Read existing code structure
   - Review README, TODO, commits
   - Extract: mission (from docs), tech stack (from code), roadmap (from issues/TODOs)

2. **Present Findings & Confirm**
   - "Based on your codebase, here's what I extracted..."
   - User confirms/corrects your understanding

3. **Create Constitution Files**
   - Same 3-file structure as greenfield
   - Expect to replan heavily after first feature (tune initial gaps)

**📖 Deep Dive:** `references/01-constitution.md`

---

### Phase 3: Feature Development Loop

For each feature on the roadmap:

#### Step 3a: Feature Specification

**Setup:**
```
1. Create feature branch: `git checkout -b feature/feature-name`
2. Clear agent context: /clear (fresh slate, constitution as source of truth)
```

**Write Feature Spec** (interview style):

Create three documents in `specs/features/`:

```
specs/features/feature-name/
├── plan.md          # Approach, task sequence (task groups)
├── requirements.md  # Technical needs, constraints, pinned versions
└── validation.md    # Scorecard—how to verify success
```

**Interview Questions:**
- What's the feature goal?
- What task sequence makes sense?
- Any specific constraints (libraries, versions, patterns)?
- How will we know it works? (validation criteria)

**The Right Level of Control:**
- ✅ Control: scope, pinned versions, validation method, architectural approach
- ❌ Don't oversteer: variable names, minor implementation details

**Review Before Proceeding:**
- Is the plan clear and logical?
- Are requirements complete but not cluttered?
- Can the validation be executed?
- Do all three docs align?

**📖 Deep Dive:** `references/02-feature-specification.md`

#### Step 3b: Implementation

**Setup:**
```
1. /clear again (avoid stale context contaminating build)
2. Review feature spec one more time
```

**Prompt Structure:**
```
"Implement all task groups from the feature spec:
- Plan: [specs/features/feature-name/plan.md]
- Requirements: [specs/features/feature-name/requirements.md]
- Validation: [specs/features/feature-name/validation.md]

Constitution:
- Mission: [specs/mission.md]
- Tech Stack: [specs/tech-stack.md]
"
```

**Your Role During Implementation:**
- Supervisor/architect (not coder)
- Watch progress in real-time
- Review changes in commit window
- Run the app to see pixels on screen

**Strategy Choice:**
- **All task groups at once**: Standard features, confident in spec
- **One task group at a time**: Security, database, sensitive areas (smaller commits = easier review)

**📖 Deep Dive:** `references/03-implementation.md`

#### Step 3c: Validation

**Two-Level Review:**

1. **High-Level Review** (focus here!)
   - Does the feature work as spec'd?
   - Are project conventions followed?
   - Is component structure correct?
   - Does it align with constitution?

2. **Low-Level Review** (DON'T nitpick)
   - Variable names, CSS classes → not worth the cognitive debt

**When Issues Flow from Spec Mistakes:**
- Fix BOTH spec and code
- Ask agent to update spec → keeps consistency
- Manual edits cause "drift" (docs out of sync)

**Code Review Checklist:**
```markdown
- [ ] Feature works as specified
- [ ] Follows tech stack conventions
- [ ] Components properly structured
- [ ] Tests passing (if applicable)
- [ ] No manual spec edits (used agent)
- [ ] Both spec and code updated if spec had gaps
```

**Sub-Agent Deep Review** (optional):
- Spawn sub-agent for deep review
- Preserves main agent's context window
- Agent finds issues on second look

**📖 Deep Dive:** `references/04-validation.md`

---

### Phase 4: Replanning

**When:** Between feature implementations

**Three Levels:**

1. **Feature-Level Replanning**
   - Update recent feature specs/code (e.g., add testing)
   - Small improvements

2. **Project-Level Replanning**
   - Revise constitution based on learnings
   - Update roadmap (re-prioritize, consolidate phases)
   - Add new requirements

3. **Workflow-Level Replanning**
   - Improve SDD process itself
   - Build agent skills to automate repeated workflows
   - Update validation checklists

**Decision Matrix:**

| Change Size | Action |
|-------------|--------|
| Small, early in dev | Implement directly during replanning |
| Big change | Schedule as new feature phase on roadmap |

**Replanning Prompt:**
```
"Let's replan after completing [feature]:
1. Review recent feature—any gaps in specs?
2. Update constitution if needed
3. Review roadmap—still make sense?
4. Identify repeated workflows → automate with skills?"
```

**Why "Run Slow to Run Fast":**
- Replanning prevents compounding mistakes
- Constitution quality = downstream success
- Time here = massive savings later

**📖 Deep Dive:** `references/05-replanning.md`

---

## Advanced Patterns

### Agent Skills (Automate Your Workflow)

When users repeat the same prompts, build a skill:

**Creating Skills:**
1. Tell user: "You're repeating this workflow—let's automate it with a skill"
2. Use skill-creator: "Use your skill creator to talk through this"
3. Agent interviews user, writes skill
4. Test and iterate

**Skill Scope:**
- **Per-project**: Project-specific conventions
- **Global**: Applies across all projects

**Invoking Skills:**
- Name it in prompt: "Using the feature-spec skill..."
- Progressive disclosure (agent auto-decides, but not always reliable)

**Examples:**
- Constitution checker
- Feature spec template generator
- Validation report generator
- Changelog updater on merge

**📖 Deep Dive:** `references/06-agent-skills.md`

### Research Backlog Pattern

When user has idea mid-feature:

1. Research with agent (don't stop branch work)
2. Tell agent: "Write report to `backlog/research-topic.md`"
3. Later: Schedule on roadmap with link to backlog
4. As backlog grows: Automate with research skill

---

### Brownfield Constitution Generation

**Artifacts to Read:**
- Code structure (directories, file patterns)
- README, CONTRIBUTING, docs
- Git history (recent commits)
- TODO, FIXME comments
- Package manifests (package.json, requirements.txt)
- CI/CD configs

**Extraction Steps:**
1. Mission: Extract from README, docs
2. Tech Stack: Detect from code (frameworks, versions, architecture)
3. Roadmap: Extract from TODOs, issues, commit patterns

**Expect Heavy Replanning:**
- Initial constitution has gaps
- First feature reveals missing context
- Give extra time to tune

**📖 Deep Dive:** `references/07-brownfield.md`

---

## Best Practices & Principles

### Core Rules

1. **Never edit specs manually** — always ask agent (keeps consistency)
2. **Clear agent context (/clear) before major phases** — fresh slate, constitution as source
3. **Small roadmap steps** — manageable features, less AI fatigue
4. **Control process, don't oversteer** — decide architecture, not variable names
5. **Fix spec AND code** — when code bugs flow from spec gaps
6. **Git commit constitution** — it's living, versioned
7. **Replanning is mandatory** — not optional, prevents compounding errors

### The Right Level of Detail

```
┌────────────────────────────────────────────┐
│ YOU PROVIDE (HIGH LEVEL)                   │
│ • Goals, mission, target audience          │
│ • Architectural decisions                  │
│ • Constraints, success criteria            │
│ • Trade-off choices                        │
├────────────────────────────────────────────┤
│ AGENT FIGURES OUT (LOW LEVEL)             │
│ • Variable names                           │
│ • Function signatures                      │
│ • Implementation details                   │
│ • Boilerplate                              │
└────────────────────────────────────────────┘
```

**Architect Analogy:**
- You = architect (design, supervise, review)
- Agent = builder (constructs from your drawings)
- Focus on **context the builder doesn't know**

### Cognitive Debt Management

**What is Cognitive Debt?**
Mental load of tracking what code does and how it evolved. Agents write fast → you can't keep up.

**How SDD Reduces It:**
- Small feature loops (manageable changes)
- Specs as review checklists
- High-level reviews (not nitpicking)
- Clean breaks between features (/clear)

### Validation Tips

**High-Level Focus:**
- Does feature work?
- Matches spec?
- Conventions followed?
- Structure correct?

**Don't Sweat Low-Level:**
- CSS class names
- Variable naming
- Minor formatting

**When to Use Sub-Agents:**
- Deep review (preserves context)
- Security-sensitive code
- Complex logic validation

---

## Greenfield vs Brownfield Summary

| Aspect | Greenfield 🌱 | Brownfield 🏭 |
|--------|--------------|---------------|
| **Starting Point** | From scratch | Existing codebase |
| **Constitution Creation** | Converse with agent | Reverse-engineer from code |
| **Conversation Richness** | User provides all context | Agent reads code/docs (richer) |
| **Then What?** | Feature loops | Same feature loops |
| **Replanning Emphasis** | Standard | Expect heavy tuning |

Both converge on the same workflow after constitution exists.

---

## Communication Style

### With the User

- **Explain the why**: Why specs matter, why /clear, why replan
- **Interview style**: Ask clarifying questions (use AskUserQuestion when choices exist)
- **Phase confirmations**: "Constitution ready. Shall we start first feature?"
- **Transparent reviews**: "I found 3 inconsistencies in the spec..."
- **No jargon overload**: Explain "context decay," "downstream amplification" simply

### Skill Invocation Phrases

Users might say:
- "Help me set up spec-driven development"
- "I want to write a constitution for my project"
- "Let's plan this feature properly before coding"
- "I'm tired of vibe coding, how do I structure this?"
- "Can you help me transition this codebase to SDD?"
- "How do I do feature specs?"

---

## Reference Materials

This skill includes detailed reference documents:

1. **references/01-constitution.md** — Creating mission, tech stack, roadmap
2. **references/02-feature-specification.md** — Writing plan, requirements, validation
3. **references/03-implementation.md** — Agent implementation process
4. **references/04-validation.md** — Code review, drift prevention
5. **references/05-replanning.md** — Three levels of replanning
6. **references/06-agent-skills.md** — Building automation workflows
7. **references/07-brownfield.md** — Working with existing codebases
8. **references/08-quick-reference.md** — Cheatsheet, flashcard-style review

When deep details needed, guide user to read the relevant reference file.

---

## Example Session Flow

### Greenfield: New Project

```
User: "I want to build a task management API with SDD"

You:
1. "Great! Let's start with the constitution. I'll interview you:
   - Who's your target audience?
   - What problem does this solve?
   - Any tech stack preferences?"
   
2. [After interview] "Based on our conversation, I'll draft:
   - Mission (vision, audience, scope)
   - Tech Stack (Node.js + Express + PostgreSQL + Prisma)
   - Roadmap (5 phases, starting small)
   
   Review these and let me know if anything needs adjustment."

3. [User approves] "Constitution committed! Roadmap phase 1: 'Basic task CRUD.'
   Shall we write the feature spec for it?"

4. [Feature spec interview] → creates plan.md, requirements.md, validation.md

5. "Feature spec ready. Shall I implement it, or would you like to review first?"

6. [Implementation] "All tasks complete! Running validation checklist now..."

7. "Feature done! Let's replan before phase 2:
   - Should we add testing to the constitution?
   - Roadmap phases still make sense?
   - Any repeated workflows to automate?"
```

### Brownfield: Existing Codebase

```
User: "I have a Django app, want to introduce SDD"

You:
1. "Perfect! I'll reverse-engineer a constitution from your codebase.
   Can you point me to:
   - Main code directory
   - README or docs
   - Any TODOs or issue tracker?"

2. [Reads code/docs] "Here's what I extracted:
   - Mission: [from README]
   - Tech Stack: Django 4.2, PostgreSQL, Celery for async
   - Roadmap: [from TODOs] 3 pending features
   
   Does this match your understanding?"

3. [User confirms + corrects] "Constitution created! Since this is brownfield,
   expect to replan heavily after first feature (we'll tune gaps).
   
   Which roadmap item should we tackle first?"

4. [Proceeds to feature loop as usual]
```

---

## Success Metrics

A user has successfully adopted SDD when:

1. ✅ Constitution exists and is committed
2. ✅ Features developed on separate branches with specs
3. ✅ User uses /clear before major phases
4. ✅ Replanning happens between features
5. ✅ Specs updated (via agent) when gaps found
6. ✅ User explains specs improved their workflow

---

## Key Terminology

- **Constitution**: Project-level specs (mission + tech stack + roadmap)
- **Feature Spec**: Plan + requirements + validation for one feature
- **Vibe Coding**: Freestyle prompting without specs (produces disposable code)
- **Context Decay**: Loss of project context across agent sessions
- **Downstream Amplification**: Small spec changes → large code changes
- **Drift**: When specs and code go out of sync
- **Cognitive Debt**: Mental load of tracking fast-generated code
- **Replanning**: Updating constitution, roadmap, or process between features

---

## Remember

> **You are a guide, not a dictator. Interview the user, propose solutions, but they decide. Control the process, don't oversteer the agent. Specs are contracts—keep them consistent. Replanning isn't optional—it prevents disaster.**

---

## Additional Resources

- **Course Source**: DeepLearning.AI × JetBrains — "Spec-Driven Development with Coding Agents"
- **Instructor**: Paul Everitt (Developer Advocate, JetBrains)
- **Open-Source Frameworks**: GitHub Spec Kit, OpenSpec (Fission AI)
- **Related Standards**: MCP (Model Context Protocol), ACP (Agent Client Protocol), Agent Skills

---

**This skill embodies professional AI-assisted development. Use it to help users move from chaos to engineering.**

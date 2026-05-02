# Constitution Creation — Deep Dive

> The constitution is your project's DNA. It captures **immutable decisions** that guide all downstream work.

## What Is a Constitution?

A constitution consists of three pillars:

1. **Mission** (`specs/mission.md`) — The "why"
   - Vision and goals
   - Target audience
   - Scope and constraints
   - Problems you're solving

2. **Tech Stack** (`specs/tech-stack.md`) — The "how"
   - Development technologies (frameworks, languages)
   - Deployment technologies
   - Architecture decisions
   - Database schema
   - API contracts
   - Smoke tests

3. **Roadmap** (`specs/roadmap.md`) — The "when"
   - Sequence of feature phases
   - Each phase = future feature spec
   - **Living document** (evolves with replanning)

## Why Write Constitution WITH the Agent?

The agent asks **surprisingly good questions** you might not consider:

- Architecture patterns you hadn't thought of
- External packages that already solve your problem
- Trade-offs (speed vs data fidelity, security vs convenience)
- Consistency checks between documents

**Your business context + Agent's technical knowledge = Better specs than either alone**

## Greenfield: Building from Scratch

### Step-by-Step Process

**1. Prepare Your Context**

Gather:
- Project description (what you're building, why)
- Stakeholder input (README, vision docs)
- Any existing requirements or constraints

**2. Initial Prompt to Agent**

```markdown
I'm starting a new project called [PROJECT NAME]. Here's what it does:
[Brief description]

I want to use Spec-Driven Development. Can you help me create a constitution?
The constitution should include:
- Mission (vision, audience, scope)
- Tech Stack (architecture, frameworks, database)
- Roadmap (organized in small, manageable steps)

[Optional: Point to any existing docs]
```

**3. Agent Interview Phase**

The agent will ask clarifying questions. Common topics:

| Question Area | Example |
|---------------|---------|
| **Tone** | Should mission.md be formal, playful, technical? |
| **Backend Language** | TypeScript, Python, Go, Rust? Why? |
| **Frontend Framework** | React, Vue, Svelte, or server-rendered? |
| **Database** | PostgreSQL, MongoDB, SQLite? Schema early or iterative? |
| **API Style** | REST, GraphQL, tRPC? Why? |
| **Granularity** | How small should roadmap phases be? |
| **Testing** | Test-driven, or add later? Framework? |
| **Deployment** | Vercel, AWS, Docker, serverless? |

**Your Job:** Make the key architectural decisions. Use YOUR knowledge of trade-offs.

**4. Agent Drafts Constitution**

The agent writes three files:

```
specs/
├── mission.md       # Business context (agent can't know this)
├── tech-stack.md    # Engineering decisions
└── roadmap.md       # Phase sequence
```

**5. Review as Spec Reviewer**

Check for:

✅ **Consistency**
- Do mission.md and tech-stack.md align?
- Does roadmap reference the right tech?
- Are environment variables named consistently?

✅ **Completeness**
- Is DB schema defined? (Headache to change later!)
- Are API contracts clear?
- Are smoke tests specified?
- Is data flow documented?

✅ **Ambiguity**
- Any thresholds mentioned without values?
- Any "we'll decide later" that should be decided now?
- Any terms used inconsistently?

**6. Iterate via Agent**

Found an issue? **DON'T edit manually.**

Tell the agent:
```markdown
"I noticed [issue]. Can you update the specs to [fix]?
Make sure all related documents stay consistent."
```

The agent updates ALL affected files.

**7. Commit the Constitution**

```bash
git add specs/
git commit -m "Add project constitution (mission, tech stack, roadmap)"
```

### Example: AgentClinic Constitution

**Project:** A parody clinic where AI agents get relief from their humans

**mission.md** (excerpt):
```markdown
# AgentClinic Mission

## Vision
A playful API + dashboard for tracking AI agent "ailments" and "treatments"

## Target Audience
Developers working with AI agents (internal tool, lighthearted)

## Problems We Solve
- Agents suffer from hallucinations, context rot, memory issues
- Need to track treatment effectiveness over time
- Want visibility into common agent problems

## Scope
- REST API for agent check-ins
- Dashboard to view ailments and treatments
- Treatment effectiveness tracking
```

**tech-stack.md** (excerpt):
```markdown
# AgentClinic Tech Stack

## Architecture
- Backend: Next.js API routes (TypeScript)
- Frontend: React (Next.js App Router)
- Database: PostgreSQL (Prisma ORM)
- Deployment: Vercel

## Database Schema

### Agents
- id, name, created_at

### Ailments
- id, code (e.g., "HALLUCINATION"), severity (1-5), description

### Visits
- id, agent_id, ailment_id, status (TRIAGE, ACTIVE, FOLLOW_UP), created_at

### Treatments
- id, visit_id, treatment_type, effectiveness_score

## API Contracts

POST /api/visits
- Validates agent exists
- Searches previous visits for chronic issues
- Returns visit_id + recommended treatment

## Smoke Tests
- Chronic ailments detected (>3 visits for same ailment)
- Treatment effectiveness calculated correctly
```

**roadmap.md** (excerpt):
```markdown
# AgentClinic Roadmap

## Phase 1: Nano Foundation
- Basic Next.js setup
- Prisma schema + migrations
- Empty homepage placeholder

## Phase 2: Agent Check-In
- POST /api/visits endpoint
- Ailment catalog
- Treatment mapping

## Phase 3: Dashboard
- List all agents
- View visit history
- Treatment effectiveness chart
```

---

## Brownfield: Reverse-Engineering from Existing Code

### Artifacts to Read

1. **Code Structure**
   - Directory layout
   - File naming patterns
   - Module organization

2. **Documentation**
   - README.md
   - CONTRIBUTING.md
   - ADRs (Architecture Decision Records)
   - Comments

3. **Configuration**
   - package.json, requirements.txt, Gemfile
   - Database migrations
   - CI/CD configs

4. **Project History**
   - Recent commits (git log)
   - TODO comments
   - Issue tracker
   - Roadmap files

### Extraction Process

**1. Read the Codebase**

Use Glob and Grep to understand:

```bash
# Directory structure
ls -R

# Dependencies
cat package.json  # or requirements.txt, etc.

# Recent activity
git log --oneline -20

# TODOs and plans
grep -r "TODO\|FIXME\|HACK" .
```

**2. Draft Constitution**

Based on findings:

**mission.md** — Extract from:
- README "About" section
- Documentation
- Commit messages (the "why" behind changes)

**tech-stack.md** — Detect from:
- Framework imports
- Database connection code
- API route patterns
- Testing setup

**roadmap.md** — Extract from:
- TODO comments
- GitHub Issues
- Project board
- Unreleased branches

**3. Present to User for Confirmation**

```markdown
"Based on your codebase, here's the constitution I extracted:

**Mission** (from README):
[Summary]

**Tech Stack** (detected):
- Backend: Django 4.2
- Database: PostgreSQL
- Async: Celery + Redis
- Testing: pytest

**Roadmap** (from TODOs and issues):
1. Add user authentication
2. Refactor report generation
3. Add PDF export

Does this match your understanding? Anything to correct or add?"
```

**4. Iterate and Commit**

Refine based on user feedback, then commit.

---

## Agent as Spec Reviewer

The agent reviews your constitution for:

### Inconsistencies

| What It Finds | Example |
|---------------|---------|
| **Threshold mismatches** | Mission says "low confidence = 0.3", tech-stack says "0.4" |
| **Naming conflicts** | Mission calls it "effectiveness score", tech-stack calls it "treatment rating" |
| **Alignment gaps** | Mission mentions LLM provider, tech-stack doesn't specify which one |

### Missing Decisions

| Question | Why It Matters |
|----------|----------------|
| **Schema version in payloads?** | Lightweight change now, big payoff when APIs evolve |
| **Soft-delete or hard-delete?** | Affects data recovery, audit trails |
| **Authentication method?** | Need to know before building endpoints |
| **Error handling strategy?** | Consistent across all endpoints |

### Trade-Off Clarifications

| Trade-Off | Example |
|-----------|---------|
| **Speed vs accuracy** | "Use approximate search or exact match?" |
| **Security vs convenience** | "Dashboard protected or open (private deploy)?" |
| **Flexibility vs simplicity** | "Configurable LLM provider or hardcode OpenAI?" |

---

## Best Practices

### DO ✅

- **Write WITH the agent** (collaborative, not solo)
- **Define DB schema upfront** (hard to change later)
- **Ask agent to edit specs** (keeps consistency)
- **Commit the constitution** (it's living, version it)
- **Expect long, detailed specs** (normal! pays off downstream)
- **Create two versions if needed** (detailed + pared-down)

### DON'T ❌

- **Edit specs manually** (causes drift)
- **Skip the DB schema** (nightmare to refactor)
- **Leave thresholds undefined** (agent will guess)
- **Treat as "write once"** (it's living, will evolve)
- **Worry about length** (long specs = clear specs)

---

## Constitution vs agents.md

| | `agents.md` | Constitution |
|---|---|---|
| **Scope** | Agent-specific instructions | Project-level decisions |
| **Audience** | One specific tool | Agent-agnostic (any agent) |
| **Structure** | Varies by agent | Standardized (3 pillars) |
| **Agreement** | Human → agent | Human ↔ agent AND human ↔ human |

The constitution is a **contract between humans** (team alignment) AND between **human and agent** (implementation guide).

---

## Example Prompts

### Starting Constitution (Greenfield)

```markdown
I'm building a task management API with Next.js. Target audience is small teams
who want a lightweight alternative to Jira.

Can you help me create a constitution? I want:
- Mission: vision, audience, scope
- Tech Stack: Next.js + PostgreSQL + Prisma
- Roadmap: Small phases (5-7), starting with basic CRUD

Use AskUserQuestion for any clarifications.
```

### Reverse-Engineer Constitution (Brownfield)

```markdown
I have an existing Django app (e-commerce platform). Can you reverse-engineer
a constitution from the codebase?

Code is in /src, README at /README.md.
Check recent commits and TODOs for roadmap.
```

### Review Constitution

```markdown
I've drafted a constitution (specs/ directory). Can you review it for:
- Inconsistencies between mission/tech-stack/roadmap
- Missing technical details (DB schema, API contracts)
- Ambiguous requirements or thresholds
```

---

## Next Steps

After constitution is committed:
1. Choose first roadmap item
2. Write feature spec (plan + requirements + validation)
3. Start the feature development loop

**📖 Continue to:** `02-feature-specification.md`

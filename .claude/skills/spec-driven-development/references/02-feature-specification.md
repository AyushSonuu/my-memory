# Feature Specification — Deep Dive

> Before coding, discuss the spec with the agent: a plan for tasks, requirements, and a validation scorecard.

## What Is a Feature Spec?

A feature spec consists of three documents:

1. **Plan** (`specs/features/[feature-name]/plan.md`)
   - Approach and strategy
   - Task groups (sequence of work)
   - How the feature will be built step-by-step

2. **Requirements** (`specs/features/[feature-name]/requirements.md`)
   - Technical needs
   - Constraints
   - Pinned versions
   - Important details (NOT minutiae like variable names)

3. **Validation** (`specs/features/[feature-name]/validation.md`)
   - Scorecard—how to verify success
   - Agent needs to know how to check it got things right
   - Manual steps, automated tests, or both

**All three stay in sync** — when you change one via agent, it updates the others.

---

## The Feature Spec Process

### Setup

**1. Create Feature Branch**

```bash
git checkout -b feature/[feature-name]
```

Work on separate branch = clean slate between features.

**2. Clear Agent Context**

```
/clear
```

**Why:** Agent gets what it needs from the constitution (official source), not stale memory. Fresh context = specs capture **intent**, not artifacts of previous work.

---

### Writing the Spec (Interview Style)

**Initial Prompt:**

```markdown
I want to implement [FEATURE NAME] from the roadmap.

Can you help me write the feature spec? I need:
1. Plan — approach and task groups
2. Requirements — technical needs and constraints
3. Validation scorecard — how to verify it works

Constitution:
- Mission: specs/mission.md
- Tech Stack: specs/tech-stack.md

Use AskUserQuestion for clarifications.
```

**Agent Interview Questions:**

The agent will ask about:

| Area | Example Questions |
|------|------------------|
| **Scope** | What's included in this phase? What's deferred? |
| **Approach** | Should we build API first or UI first? |
| **Task Sequence** | Does task A need to complete before task B? |
| **Constraints** | Any specific libraries or patterns to use/avoid? |
| **Versions** | Should we pin framework versions? |
| **Validation** | How will we test this—manual, automated, or both? |

**Your Job: Make Key Decisions**

✅ Control:
- Phase scope (what's in, what's out)
- Pinned versions (e.g., "use Hono 3.x")
- Strict enforcement (e.g., "TypeScript strict mode")
- Validation method (e.g., "manual curl commands")
- Architectural choices (e.g., "use repository pattern")

❌ Don't Oversteer:
- Variable names
- Minor implementation details
- Internal function structure

**Architect Analogy:** You provide the blueprint, the agent figures out how to construct it.

---

### The Three Documents

#### 1. Plan (`plan.md`)

**What It Contains:**
- High-level approach
- Task groups (not individual tasks—groups!)
- Sequence of work

**Example: Agent Check-In Feature**

```markdown
# Plan: Agent Check-In API

## Approach
Build POST /api/visits endpoint that accepts agent check-ins, searches for
chronic ailments, and returns visit ID + recommended treatment.

## Task Groups

### Task Group 1: Database Setup
- Create Visits table schema
- Add indexes for agent_id queries
- Set up Prisma migrations

### Task Group 2: Ailment Catalog
- Create Ailments table
- Seed with initial ailment codes (HALLUCINATION, CONTEXT_ROT, etc.)
- Add severity levels (1-5)

### Task Group 3: Visit Endpoint
- Implement POST /api/visits
- Validate request payload
- Search previous visits for chronic issues
- Return visit_id + treatment recommendation

### Task Group 4: Testing
- Write integration tests for endpoint
- Test chronic ailment detection
- Test error handling
```

**Why Task Groups, Not Individual Tasks?**
- Gives agent flexibility in implementation order within a group
- Reduces micromanagement
- Agent can parallelize when appropriate

---

#### 2. Requirements (`requirements.md`)

**What It Contains:**
- Technical needs
- Constraints
- Pinned versions
- Architecture rules

**Example: Agent Check-In Feature**

```markdown
# Requirements: Agent Check-In API

## Technical Stack
- Framework: Hono 3.x (pinned)
- Database: PostgreSQL with Prisma
- TypeScript: strict mode enabled

## API Contract

POST /api/visits
Request:
{
  "agent_id": "string (UUID)",
  "ailment_code": "string (from catalog)",
  "symptoms": "string (description)"
}

Response (200):
{
  "visit_id": "UUID",
  "status": "TRIAGE | ACTIVE | FOLLOW_UP",
  "recommended_treatment": "string"
}

Response (400):
{
  "error": "Invalid agent_id | Unknown ailment_code"
}

## Chronic Ailment Detection
- Chronic = agent has >3 previous visits for same ailment_code
- Search visits from last 90 days

## Treatment Mapping
- HALLUCINATION → Temperature reduction
- CONTEXT_ROT → Context infusion
- MEMORY_ISSUES → Working memory expansion

## Constraints
- All timestamps in UTC
- Use repository pattern for data access
- No raw SQL—use Prisma queries only
```

---

#### 3. Validation (`validation.md`)

**What It Contains:**
- How to verify the feature works
- Manual steps, automated tests, or both
- Success criteria

**Example: Agent Check-In Feature**

```markdown
# Validation: Agent Check-In API

## Automated Tests

### Integration Tests
- [ ] POST /api/visits creates new visit record
- [ ] Response includes visit_id and recommended_treatment
- [ ] Invalid agent_id returns 400 error
- [ ] Unknown ailment_code returns 400 error

### Chronic Detection Tests
- [ ] Agent with 4+ visits flagged as chronic
- [ ] Agent with <4 visits NOT flagged as chronic
- [ ] Only visits from last 90 days counted

## Manual Validation

### Happy Path
1. Start dev server: `npm run dev`
2. Create test agent (seed script or manual DB insert)
3. POST to /api/visits with valid payload
4. Verify response has visit_id and treatment
5. Check database—visit record exists

### Error Cases
1. POST with invalid agent_id → 400 error
2. POST with unknown ailment_code → 400 error
3. POST with malformed JSON → 400 error

### Chronic Ailment Detection
1. Create agent with 4 previous HALLUCINATION visits
2. POST new HALLUCINATION visit
3. Verify response flags as chronic
4. Check database—chronic flag set

## Success Criteria
- All automated tests passing
- Manual validation steps completed
- No TypeScript errors
- Endpoint returns in <500ms
```

---

## The Right Level of Control

```
┌────────────────────────────────────┐
│  ✅ CONTROL                        │
│  • Phase scope decisions           │
│  • Pinned versions                 │
│  • Architecture patterns           │
│  • Validation method               │
│  • API contracts                   │
│  • Error handling strategy         │
├────────────────────────────────────┤
│  ❌ DON'T OVERSTEER                │
│  • Variable names                  │
│  • Function names                  │
│  • Code formatting                 │
│  • Internal implementation         │
└────────────────────────────────────┘
```

**Golden Rule:** Control the **process**, not the **minutiae**.

---

## Review Before Implementation

### Plan Review

✅ Check:
- Is the approach right?
- Task sequence logical?
- Any dependencies between groups?
- Scope clear (what's in, what's out)?

**Get this right early** — it keeps the agent on track.

### Requirements Review

✅ Check:
- Technical needs captured?
- Constraints clear and reasonable?
- API contracts well-defined?
- No minor details cluttering it?

### Validation Review

✅ Check:
- Can the agent actually verify success?
- Realistic checks?
- Balance of automated + manual?
- Success criteria measurable?

---

## When You Find Issues

**DON'T edit manually** → Ask the agent to fix.

Example:
```markdown
"I want to add a 'nice placeholder homepage' to this phase.
Can you update the plan, requirements, and validation to include it?"
```

Agent updates **all three docs** to stay in sync.

---

## Common Pitfalls

### ❌ Pitfall 1: Too Much Detail

**Bad:**
```markdown
Requirements:
- Variable name for visit count: visitCount
- Function name for chronic detection: detectChronicAilment
- Use camelCase for all variables
```

**Good:**
```markdown
Requirements:
- Use repository pattern for data access
- Chronic detection: >3 visits in last 90 days
- Follow TypeScript naming conventions (camelCase)
```

### ❌ Pitfall 2: Vague Validation

**Bad:**
```markdown
Validation:
- Test the endpoint
- Make sure it works
```

**Good:**
```markdown
Validation:
- POST with valid payload → 200 response with visit_id
- POST with invalid agent_id → 400 error
- Chronic agent (4+ visits) → response flags as chronic
```

### ❌ Pitfall 3: Skipping /clear

**Problem:** Agent carries over context from previous features → spec captures old artifacts, not fresh intent.

**Solution:** Always `/clear` before writing feature spec.

---

## Flow State Checklist

Before writing feature spec:

- [ ] Unfinished work cleared?
- [ ] Last feature branch merged to main?
- [ ] Next roadmap item still correct?
- [ ] Agent context `/clear`'d?

**Fresh slate = clean spec.**

---

## Example Prompts

### Start Feature Spec

```markdown
I'm ready to implement Phase 2 from the roadmap: "Agent Check-In API"

Can you help write the feature spec (plan, requirements, validation)?

Constitution:
- Mission: specs/mission.md
- Tech Stack: specs/tech-stack.md
- Roadmap: specs/roadmap.md (Phase 2 is the target)

Key decisions:
- Use Hono 3.x (pinned)
- Repository pattern for data access
- Integration tests required

Use AskUserQuestion for any clarifications.
```

### Update Existing Spec

```markdown
I want to add "email notification on check-in" to the current feature spec.

Can you update:
1. Plan (add task group for email)
2. Requirements (define email contract)
3. Validation (add email tests)

Keep all three docs in sync.
```

### Review Spec Before Implementation

```markdown
I've written the feature spec (specs/features/agent-checkin/).

Can you review it for:
- Is the task sequence logical?
- Are requirements complete but not cluttered?
- Is validation realistic and executable?
- Any conflicts with the constitution?
```

---

## Next Steps

After feature spec is complete and reviewed:
1. Commit the spec (small commit)
2. `/clear` again (fresh context for implementation)
3. Implement the feature (next guide)

**📖 Continue to:** `03-implementation.md`

# Replanning & Advanced Patterns

## Replanning: The Secret Weapon

**When:** Between feature implementations (mandatory, not optional)

**Why:** Prevents compounding mistakes. Constitution quality = downstream success. "Run slow to run fast."

---

## Three Levels of Replanning

### 1. Feature-Level Replanning

**Scope:** Update recent feature specs/code

**Examples:**
- Add testing to recent feature
- Improve error handling
- Add missing validation

**Prompt:**
```markdown
Let's improve the [feature] we just completed:
- Add unit tests (we skipped them initially)
- Update feature spec to document testing policy
- Ensure validation.md includes test coverage
```

---

### 2. Project-Level Replanning

**Scope:** Revise constitution, update roadmap

**Examples:**
- Consolidate roadmap phases
- Add new requirements discovered
- Update tech stack decisions
- Re-prioritize features

**Prompt:**
```markdown
Time to replan after completing [features]. Can you help me:
1. Review constitution—any learnings to capture?
2. Update roadmap—phases still make sense?
3. Any new requirements discovered?

Let's update specs to reflect current understanding.
```

**Decision Matrix:**

| Change Size | Action |
|-------------|--------|
| Small, early in dev | Implement directly during replanning |
| Big change | Schedule as new feature phase on roadmap |

---

### 3. Workflow-Level Replanning

**Scope:** Improve the SDD process itself

**Examples:**
- Build agent skills for repeated workflows
- Automate validation checklists
- Create spec templates
- Streamline branching strategy

**Prompt:**
```markdown
I keep repeating [workflow]. Can we automate this with an agent skill?

Example workflow:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Use your skill-creator to build this.
```

---

## Agent Skills (Workflow Automation)

### What Are Agent Skills?

Packages of instructions + resources that give agents new capabilities.

**Use for:**
- Definable, repeatable workflows
- Project/org-specific context
- Reducing repeated prompts

**Examples:**
- Constitution checker (reviews for consistency)
- Feature spec template generator
- Validation report generator
- Changelog updater on merge
- Database migration helper

---

### Creating Skills

**Process:**
1. Identify repeated workflow
2. Tell user: "Let's automate this with a skill"
3. Use skill-creator: `"Use your skill creator to talk through this"`
4. Agent interviews user, writes skill
5. Test and iterate

**Skill Scope:**
- **Per-project**: Project-specific conventions
- **Global**: Applies across all projects

---

### Invoking Skills

| Method | How | Reliability |
|--------|-----|------------|
| **Name in prompt** | "Using the feature-spec skill..." | ✅ Reliable |
| **Skill-from-skill** | One skill calls another | ✅ Reliable |
| **Progressive disclosure** | Agent auto-decides | ⚠️ Not always reliable (esp. large context) |

**Tip:** When you know you want a skill, **name it explicitly**. Saves thinking tokens.

---

## Research Backlog Pattern

### The Problem

You have an idea mid-feature, but:
- Don't want to stop current work
- Not ready to commit to it yet
- Don't want to lose the idea

### The Solution

**Step-by-Step:**

1. **Research with agent** (don't stop branch work)
   ```markdown
   "I'm curious about [topic]. Can you research it?
   Don't stop current feature work—just investigate."
   ```

2. **Write report to backlog**
   ```markdown
   "Great research! Can you write a report to:
   backlog/research-[topic].md
   
   Include: findings, recommendations, trade-offs, next steps."
   ```

3. **Schedule on roadmap later**
   ```markdown
   "Add to roadmap.md as future phase:
   - Phase N: [Topic]
   - Link to backlog file for details"
   ```

4. **Scale with skill** (as backlog grows)
   ```markdown
   "I keep doing research and filing to backlog.
   Can we automate this with a 'research-backlog' skill?"
   ```

---

## Brownfield-Specific Patterns

### Initial Constitution Tuning

**Expect Heavy Replanning:**
- First feature reveals missing context
- Constitution gaps become obvious
- Roadmap may need reorganization

**First Replanning Session (Extra Time):**
```markdown
After completing first feature with new SDD workflow, let's heavily replan:

1. Constitution gaps discovered?
   - Mission unclear in any areas?
   - Tech stack missing decisions?
   
2. Roadmap realistic?
   - Phases too big/small?
   - Dependencies clarified?
   
3. Feature spec template working?
   - What to add/remove for next features?

Update constitution to reflect learnings.
```

---

### Legacy Debt Management

**Pattern:** Interleave new features with legacy cleanup

**Roadmap Strategy:**
```markdown
Phase 1: New feature (SDD workflow)
Phase 2: Refactor legacy area touched by Phase 1
Phase 3: New feature
Phase 4: Refactor legacy area touched by Phase 3
...
```

**Why:** Gradual migration, not big-bang rewrite.

---

## Advanced Validation Patterns

### Sub-Agent Deep Review

**When:**
- Security-sensitive code
- Complex business logic
- Independent verification needed

**How:**
```markdown
Spawn a sub-agent to review [feature] implementation.

Focus areas:
- [Area 1]
- [Area 2]
- [Area 3]

Report findings: what passed, what needs attention.
```

**Benefits:**
- Preserves main agent's context window
- Agent finds issues on second look
- No bias from implementation knowledge

---

### Validation Script Automation

**Pattern:** Turn manual validation into scripts

**Example:**
```markdown
# Before (validation.md)
Manual Steps:
1. Start server
2. POST to /api/visits with test data
3. Check response has visit_id
4. Query database to verify record

# After (automated)
npm run validate-checkin-api

Script does:
- Starts test server
- Runs test requests
- Queries test database
- Reports pass/fail
```

**Implementation:**
```markdown
"Can you create a validation script for this feature?
Script should automate the manual steps in validation.md.

Add to package.json: 'validate-[feature]': 'node scripts/validate-[feature].js'"
```

---

## Common Replanning Triggers

| Trigger | Replanning Action |
|---------|------------------|
| **Feature took way longer than expected** | Roadmap phases too big—split them |
| **Repeated spec mistakes** | Add to spec template/checklist |
| **Validation keeps missing bugs** | Improve validation.md requirements |
| **Agent keeps misunderstanding** | Constitution needs clearer language |
| **Tech stack choice regretted** | Acknowledge, plan migration phase |
| **New requirement discovered** | Update mission.md, roadmap.md |
| **Team member keeps asking same questions** | Document in constitution |

---

## The MVP Moment

### When Everything Comes Together

**What is the MVP moment?**
Attempting to implement multiple remaining roadmap phases in one go.

**Why risky?**
- Tests constitution quality under stress
- Large diff = hard to review
- Agent can drift if specs have gaps

**When safe?**
Only when:
1. Constitution quality is HIGH
2. Previous feature specs solid
3. You can handle reviewing big diff
4. Confident in context quality

### If MVP Doesn't Match Vision

**Problem:** Spec gaps → agent filled with assumptions

**Solution: Responsible Replanning**
```markdown
MVP result doesn't match my vision in these areas:
[List specific gaps]

Let's do responsible replanning:
1. What spec gaps led to these issues?
2. Update constitution to close gaps
3. Update remaining roadmap phases to reflect lessons
4. Consider re-implementing affected areas
```

---

## MCP → CLI + Skills Trend

**What's happening:**
- MCP Servers (Model Context Protocol) → more setup, more context
- CLI + Skills → less setup, less context
- Trend accelerating toward CLI + Skills

**Example: Context7**
- Old: Context7 MCP server
- New: Context7 CLI + Skill
- Purpose: Keep agent updated with latest package docs

**Why it matters for SDD:**
Your automated workflows should favor CLI + Skills over MCP when possible.

---

## Open-Source SDD Frameworks

### GitHub Spec Kit

**Commands:**
- `/constitution` — Create/update constitution
- `/plan` — Write feature plan
- `/tasks` — Break into tasks
- `/implement` — Execute implementation

**Features:**
- Branch management
- Verification scripts
- Opinionated spec formats

---

### OpenSpec (Fission AI)

**Workflow:**
```
propose → explore → apply → archive
```

**Maps to SDD:**
- propose = Constitution
- explore = Feature spec planning
- apply = Implementation
- archive = Replanning

---

## Next-Level Patterns

### Skill Chains

One skill calls another skill:

```markdown
# Skill: full-feature-cycle
1. Call: feature-spec skill
2. Wait for user approval
3. Call: implement-feature skill
4. Call: validate-feature skill
5. Call: replan skill
```

### Spec Version Control

Tag constitution versions:

```bash
git tag constitution-v1.0 -m "Initial constitution"
git tag constitution-v2.0 -m "Added testing policy, updated roadmap"
```

**Why:** Track constitution evolution over time.

### Automated Spec Health Checks

Build a skill that reviews constitution for:
- Internal consistency
- Outdated decisions
- Missing sections
- Drift from actual code

Run periodically (e.g., before each new feature).

---

## Example Prompts

### Feature-Level Replanning

```markdown
Let's improve the recent [feature]:
- Add unit tests
- Update feature spec to document testing approach
- Ensure validation covers new tests

Keep specs and code in sync.
```

### Project-Level Replanning

```markdown
After completing 3 features, time to replan:

1. Constitution review:
   - Tech stack decisions still right?
   - Mission scope evolved?
   
2. Roadmap update:
   - Consolidate phases 4-6 into 2 larger phases?
   - New requirements to add?
   
3. Process improvements:
   - Feature spec template working?
   - Validation checklist sufficient?
```

### Workflow-Level Replanning

```markdown
I keep writing feature specs with the same structure.
Can we automate this with a skill?

Use your skill-creator. The workflow is:
1. Interview me about feature
2. Generate plan.md, requirements.md, validation.md
3. Review and iterate
```

### Research Backlog

```markdown
I'm curious about switching from PostgreSQL to MongoDB.
Can you research trade-offs? Don't change anything yet.

Write findings to: backlog/research-mongodb.md

Include: pros/cons, migration effort, performance implications.
```

---

**📖 Related:**
- `01-constitution.md` — Constitution creation
- `02-feature-specification.md` — Feature specs
- `03-implementation-validation.md` — Implementation & validation
- `06-quick-reference.md` — Cheatsheet

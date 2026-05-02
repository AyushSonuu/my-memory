# Implementation & Validation — Quick Reference

## Implementation Process

### Setup
```bash
# 1. Clear agent context (avoid stale context)
/clear

# 2. Review feature spec one more time
cat specs/features/[feature-name]/plan.md
cat specs/features/[feature-name]/requirements.md
cat specs/features/[feature-name]/validation.md
```

### Implementation Prompt

```markdown
Implement all task groups from the feature spec:
- Plan: specs/features/[feature-name]/plan.md
- Requirements: specs/features/[feature-name]/requirements.md
- Validation: specs/features/[feature-name]/validation.md

Constitution:
- Mission: specs/mission.md
- Tech Stack: specs/tech-stack.md
```

### Your Role: Supervisor
- Watch progress in real-time (console output)
- Review changes in commit window
- Run the app to verify pixels on screen
- Don't code—supervise and review

### Strategy Choice

| Strategy | When to Use |
|----------|------------|
| **All task groups at once** | Standard features, confident in spec |
| **One task group at a time** | Security, database, sensitive areas (smaller commits) |

---

## Validation Process

### Two-Level Review

**1. High-Level Review (FOCUS HERE)**

✅ Check:
- Does the feature work as spec'd?
- Project conventions followed?
- Component structure correct?
- Aligns with constitution?
- Tests passing (if applicable)?

**2. Low-Level Review (DON'T NITPICK)**

❌ Skip:
- Variable names
- CSS class names
- Minor formatting
- Trivial refactors

**Why?** Low-level nitpicking = cognitive debt. Focus on what matters.

---

### When Bugs Flow from Spec Mistakes

**Fix BOTH spec and code:**

```markdown
"I found a bug—[describe]. This is because the spec was missing [requirement].

Can you:
1. Update the requirements doc to add [requirement]
2. Fix the code to implement it
3. Update validation to test for it

Keep all docs in sync."
```

**Never edit specs manually** — causes drift (docs out of sync).

---

### Code Review Checklist

```markdown
- [ ] Feature works as specified
- [ ] Follows tech stack conventions
- [ ] Components properly structured
- [ ] Tests passing (if applicable)
- [ ] No manual spec edits (used agent to update)
- [ ] Both spec and code updated if spec had gaps
- [ ] No security issues
- [ ] Error handling appropriate
```

---

### Sub-Agent Deep Review (Optional)

When to use:
- Security-sensitive code
- Complex logic
- Want second opinion

Benefits:
- Preserves main agent's context window
- Agent finds issues on second look
- Independent verification

```markdown
"Can you spawn a sub-agent to do a deep security review of this implementation?
Focus on: input validation, SQL injection, authentication checks."
```

---

### What Is "Drift"?

**Drift** = when artifacts (specs, code, docs) go out of sync.

**Causes:**
- Manual edits to specs
- Forgetting to update related documents
- Changes in code not reflected in spec

**Prevention:**
- Always ask agent to make changes
- Agent updates ALL related files
- Commit specs + code together

---

### Cognitive Debt Management

**What is Cognitive Debt?**
Mental load of tracking what code does and how it evolved. Agents write fast → you can't keep up.

**How SDD Reduces It:**
- Small feature loops (manageable changes)
- Specs as review checklists
- High-level reviews (not nitpicking)
- Clean breaks between features (/clear)

---

### Validation Completion

After validation passes:

```bash
# 1. Commit the feature
git add .
git commit -m "Implement [feature-name] (closes #N)"

# 2. Merge to main (or open PR)
git checkout main
git merge feature/[feature-name]

# 3. Clean up
git branch -d feature/[feature-name]
```

**Next:** Replanning phase

---

## Common Issues

### Issue: Agent Didn't Follow Spec

**Diagnosis:**
- Stale context contaminated build?
- Spec too vague?
- Agent misunderstood requirement?

**Fix:**
1. Identify what went wrong
2. Update spec if it was unclear
3. Re-run implementation (or just fix the issue)

---

### Issue: Tests Failing

**Diagnosis:**
- Implementation bug?
- Validation spec wrong?
- Environment issue?

**Fix:**
1. Read test output
2. If validation was wrong, update validation.md
3. Fix code to pass validation
4. Re-run tests

---

### Issue: Feature Works But Doesn't Match Vision

**Problem:** Spec didn't capture your intent.

**Fix:**
1. Update requirements to clarify intent
2. Update implementation to match
3. Learn for next feature: be more explicit in spec

---

## Example Prompts

### Implement All Task Groups

```markdown
Ready to implement! Here's the spec:
- Plan: specs/features/agent-checkin/plan.md
- Requirements: specs/features/agent-checkin/requirements.md
- Validation: specs/features/agent-checkin/validation.md

Constitution: specs/ (mission, tech-stack, roadmap)

Implement all task groups. Show me progress as you work.
```

### Implement One Task Group

```markdown
Let's implement just Task Group 1 (Database Setup) first.

Plan: specs/features/agent-checkin/plan.md (see Task Group 1)
Requirements: specs/features/agent-checkin/requirements.md
Constitution: specs/

After this group is done, I'll review before we continue.
```

### Fix Bug from Spec Gap

```markdown
Found a bug: the endpoint doesn't validate that ailment_code exists in the catalog.

This is a spec gap. Can you:
1. Update requirements.md to require ailment_code validation
2. Fix the code to implement it
3. Update validation.md to test for it
```

### Sub-Agent Review

```markdown
Spawn a sub-agent to review this implementation for:
- SQL injection vulnerabilities
- Missing input validation
- Authentication/authorization gaps
- Error handling completeness

Report findings back to me.
```

---

**📖 Related:**
- `01-constitution.md` — Constitution creation
- `02-feature-specification.md` — Writing feature specs
- `05-replanning.md` — What to do after validation

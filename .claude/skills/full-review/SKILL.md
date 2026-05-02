---
name: full-review
description: Launch all code review agents in parallel to comprehensively analyze changed files in the current branch
---

You are executing the **full-review** skill, which launches all specialized code review agents in parallel to provide fast, comprehensive analysis.

## Step 1: Identify Changed Files

First, determine what files have changed in the current branch compared to the base branch.

Run these commands to gather context:

```bash
# Get current branch name
git branch --show-current

# Identify base branch (usually 'dev' or 'main')
git rev-parse --verify dev >/dev/null 2>&1 && echo "dev" || echo "main"

# Get list of changed files
git diff dev...HEAD --name-only

# Get summary statistics
git diff dev...HEAD --stat
```

## Step 2: Prepare Context for Agents

Create a shared context summary that includes:
- Current branch name
- Base branch being compared against
- List of changed files (categorized: Python files, test files, config files)
- Brief summary of the scope of changes

## Step 3: Launch All Review Agents in Parallel

**CRITICAL**: Launch ALL agents in a SINGLE message with multiple Agent tool calls. This ensures they run in parallel.

Use the Agent tool to launch these 9 agents simultaneously:

### 1. branch-code-reviewer
**Prompt template**:
```
Review all code changes in the current branch compared to the dev branch.

Changed files:
{list_of_changed_files}

Provide:
1. Summary of changes and their purpose
2. Potential bugs with severity levels
3. Missing test suggestions
4. Code quality observations
5. Recommendations for improvement

Focus only on the changed files listed above. Do not review unchanged code.
```

### 2. logic-correctness-reviewer
**Prompt template**:
```
Review the following changed files for logic errors, off-by-one bugs, edge case handling, and conditional correctness:

{list_of_python_files_changed}

Check specifically for:
- Off-by-one errors in loops and counters
- Missing edge case handling (empty lists, None, zero values)
- Incorrect conditional logic
- Boundary condition issues
- Counter arithmetic bugs

Provide specific file:line references for all issues found.
```

### 3. performance-reviewer
**Prompt template**:
```
Analyze the following changed files for performance issues:

{list_of_python_files_changed}

Look for:
- N+1 database query patterns
- Sequential async operations that should be parallel
- Redundant computations or function calls
- Single operations in loops that should be batched
- Blocking I/O in async functions
- Inefficient data structures

Focus on performance bottlenecks that could impact production.
```

### 4. security-reviewer
**Prompt template**:
```
Perform a security review of the following changed files:

{list_of_python_files_changed}

Check for:
- SQL injection vulnerabilities (string interpolation in queries)
- Command injection (shell command construction)
- Path traversal (unchecked file paths)
- Unescaped glob/regex patterns
- Missing input validation
- Information disclosure in error messages
- Hardcoded secrets or credentials

Flag only confirmed vulnerabilities with ≥70% confidence.
```

### 5. db-ops-reviewer
**Prompt template**:
```
Review database operations in the following changed files:

{list_of_files_with_db_operations}

Analyze:
- Missing synchronize_session=False on bulk operations
- Fetch-then-delete antipatterns
- Missing expire_all() after bulk updates
- N+1 query patterns in ORM code
- Transaction management issues
- Inefficient query patterns

This project uses PostgreSQL (SQLAlchemy/psycopg2) and Cassandra (CQLEngine).
Provide specific fixes with code examples.
```

### 6. resource-leak-detector
**Prompt template**:
```
Scan the following changed files for resource management issues:

{list_of_python_files_changed}

Look for:
- Files opened without context managers
- Database connections not properly closed
- Missing finally blocks for cleanup
- Unawaited async background tasks
- Memory leaks in long-lived state
- Network sockets not closed

Provide specific file:line references and corrected code examples.
```

### 7. test-quality-reviewer
**Prompt template**:
```
Review test quality in the following changed test files:

{list_of_test_files_changed}

Check for:
- Incorrect mock patch targets (patched at definition vs usage)
- Missing or ineffective assertions
- Misleading test names
- Race conditions in async tests
- Tests that don't properly isolate
- Mock leakage between tests

If no test files changed, note: "No test files modified in this PR."
```

### 8. pr-comprehensive-reviewer
**Prompt template**:
```
Provide a comprehensive code review of the current branch ({branch_name}) compared to {base_branch} branch.

Context:
- {file_count} files changed (+{additions}, -{deletions} lines)
- {summary_of_changes}

Focus on:
1. Overall architecture and design patterns
2. Code organization and modularity
3. Error handling completeness
4. Integration between components
5. Potential breaking changes
6. Documentation needs
7. Production readiness

Provide holistic assessment of the changes.
```

### 9. general-purpose (with /review command)
**Prompt template**:
```
Execute the built-in /review command to analyze the changed files in branch {branch_name} compared to {base_branch}.

Changed files:
{list_of_changed_files}

After running the review, provide:
1. Summary of what /review identified
2. Key recommendations from the built-in review
3. Any additional insights not covered by other specialized agents

Run: /review
```

## Step 4: Compile Results

After all agents complete, compile their findings into a unified report:

```markdown
# Full Code Review Results

**Branch**: {branch_name}
**Base**: {base_branch}
**Files Changed**: {count}

## Summary

| Agent | Critical | Errors | Warnings | Info |
|-------|----------|--------|----------|------|
| Branch Review | X | X | X | X |
| Logic Correctness | X | X | X | X |
| Performance | X | X | X | X |
| Security | X | X | X | X |
| Database Ops | X | X | X | X |
| Resource Leaks | X | X | X | X |
| Test Quality | X | X | X | X |
| PR Review | X | X | X | X |
| Built-in Review | X | X | X | X |

**Total**: X critical, X errors, X warnings

## Critical Issues (Must Fix Before Merge)

{Compile all CRITICAL issues from all agents}

## Errors (Should Fix Before Merge)

{Compile all ERROR-level issues from all agents}

## Warnings (Consider Fixing)

{Compile all WARNING-level issues from all agents}

## Positive Observations

{Compile positive feedback from all agents}

## Overall Assessment

{2-3 sentence summary of code quality and merge recommendation}
```

## Step 5: Present to User

Provide the compiled report to the user in a clear, actionable format. Include:
- Total issue counts by severity
- Grouping by file when multiple agents flag the same file
- Clear action items for the developer
- Estimated time to fix critical issues

## Important Notes

- **Scope**: Only review files that changed in current branch vs base branch
- **Parallel execution**: Launch ALL agents in one message for speed
- **Context sharing**: All agents should receive the same list of changed files
- **No entire codebase review**: Focus only on new/modified code
- **Git required**: This skill requires a git repository

## Error Handling

If git commands fail:
- Check if directory is a git repository
- Verify base branch exists (try 'dev', then 'main')
- If no changes detected, inform user and exit gracefully

## Example Execution

```
user: "/full-review"

A: "I'll launch all review agents in parallel to analyze your branch changes."

[Identifies 12 changed files]
[Launches 9 agents simultaneously]
[Agents run in parallel, ~2-3 min total]
[Compiles results]

A: "Full review complete! Found 2 critical issues, 5 errors, and 8 warnings across 12 files."
```

---

## Implementation

When this skill is invoked:

1. Run git commands to identify changed files
2. Categorize files (Python, tests, config, etc.)
3. Launch ALL 9 agents using Agent tool in parallel
4. Wait for all agents to complete
5. Compile and present unified results
6. Provide actionable next steps

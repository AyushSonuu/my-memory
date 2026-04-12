# Anthropic — Demystifying Evals for AI Agents

> **Source:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
> **Distilled:** 2026-04-12

## Key Definitions (Anthropic's Terminology)

| Term | Definition | EGDR Equivalent |
|------|-----------|-----------------|
| **Task** | Single test with defined inputs + success criteria | One eval case in our eval set |
| **Trial** | One attempt at a task (multiple trials per task for consistency) | One run of a report for a given query |
| **Grader** | Logic that scores some aspect of agent performance | Our BaseGrader instances |
| **Transcript/Trace** | Complete record of a trial (outputs, tool calls, reasoning) | Langfuse trace |
| **Outcome** | Final state in environment (not just what agent said) | The stored artifact + eval scores |
| **Evaluation harness** | Infrastructure that runs evals E2E | Our eval runner + pipeline |
| **Agent harness** | System enabling model to act as agent | LangGraph workflows |
| **Evaluation suite** | Collection of tasks for specific capabilities | Our eval set organized by capability |

## Why Evals Break Down Without Structure

Teams can get surprisingly far with manual testing + dogfooding. The **breaking point** comes when:
- Users report the agent "feels worse" after changes
- Team is "flying blind" — no way to verify except guess-and-check
- Debugging is reactive: wait for complaints → reproduce → fix → hope nothing regressed
- Can't distinguish real regressions from noise

## Key Insights for EGDR

### 1. Frontier Models Find Creative Solutions
> Opus 4.5 solved a flight-booking problem by discovering a policy loophole. It "failed" the eval but actually came up with a better solution.

**Implication for EGDR:** Our evals must account for valid alternative approaches. A report that organizes information differently than the gold standard isn't necessarily wrong.

### 2. Multiple Trials for Consistency
Because model outputs vary between runs, Anthropic runs **multiple trials** to produce consistent results.

**Implication for EGDR:** Run eval cases 3-5 times, track pass@k AND pass^k (from Brad's paper):
- pass@k = at least one of k runs succeeds (peak capability)
- pass^k = ALL k runs succeed (consistency/reliability)

### 3. Evals at Any Stage
- **Bolt:** Built evals AFTER they already had a widely-used agent. In 3 months built a full eval system.
- **Descript:** Evolved from manual grading → LLM graders with periodic human calibration.
- **Claude Code:** Started with fast iteration from feedback, later added evals for narrow areas, then complex behaviors.

**Implication for EGDR:** We're in the "Claude Code early stage" — we have fast iteration from feedback. Now it's time to add structured evals, starting narrow (report quality) and expanding (component-level, user-centric).

### 4. Grader Types Match Our Design

Anthropic recommends the same layered approach:
- Code-based graders as automated gates
- LLM judges for quality scoring
- Human review of sampled results

This exactly matches our GraderRegistry design with `GraderType.CODE`, `GraderType.LLM_JUDGE`, `GraderType.HUMAN`.

## Applicability to EGDR Design

| Anthropic Recommendation | Our Implementation |
|--------------------------|-------------------|
| Start with 20-50 tasks from real failures | Pull from Langfuse traces + user feedback |
| Build simple graders first | Code-based: citation check, latency, source diversity |
| Run multiple trials | Track pass@k and pass^k per eval case |
| Grade outcomes, not just transcripts | Check stored artifact quality, not just what agent "said" |
| Use eval suites per capability | Organize by: report quality, research quality, efficiency |
| Calibrate LLM judges against humans | Monthly human review sample → compare to LLM scores |

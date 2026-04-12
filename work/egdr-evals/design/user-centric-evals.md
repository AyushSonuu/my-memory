# User-Centric Eval System — Product Vision

> **Origin:** Team conversation about cross-app evaluation product
> **Core Insight:** Users care about evaluations. Build for ourselves first (guinea pig), then offer to customers.

## The Conversation (Paraphrased)

- User research team discovered users **care a lot** about evaluations
- Discussion about a **cross-app evaluation product**
- Idea: build this for our own internal evaluations first (prove value)
- Then extend to customers who want to set up their own eval criteria
- Users might have **specific requirements/metrics** beyond our defaults
- This gives us **useful evaluation data** for improving our system

## Product Vision

### For Users
- Setup custom eval configurations via UI
- Define what "good" means for THEIR use case
- Run evals on demand on any report
- See scores over time, compare report versions
- Use different prompts and see how they affect quality
- Export eval results for compliance/audit

### For Us (EGDR Team)
- Learn what users actually care about (from their custom criteria)
- Get labeled preference data (thumbs up/down + custom scores)
- Calibrate our LLM judges against real user satisfaction
- Populate eval set automatically from user feedback
- Understand which metrics correlate with retention/satisfaction

## Three-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 3: USER-DEFINED                       │
│  "Score my reports on SAP product knowledge" │
│  Threshold: 4.0, Weight: high                │
│  → User creates, user controls               │
├─────────────────────────────────────────────┤
│  Layer 2: ORGANIZATION DEFAULTS              │
│  "All reports must cite 3+ sources"          │
│  "Neutrality check must pass"                │
│  → Admin sets, applies to all org users      │
├─────────────────────────────────────────────┤
│  Layer 1: SYSTEM (non-negotiable)            │
│  Completeness, Structure, Relevance,         │
│  Overall Quality, Neutrality                 │
│  → We control, always runs                   │
└─────────────────────────────────────────────┘
```

## Key Features to Build

### Phase 1: Eval Configuration API
- `createEvaluation(name, metrics[], thresholds, target_type)`
- `runEvaluation(evaluation_id, artifact_id)`
- `listEvaluationRuns(filters)`
- GraphQL mutations extending existing eval resolvers

### Phase 2: Eval Templates
Pre-built configurations for common use cases:
- "CFO Financial Report" (financial accuracy weighted 2×)
- "Market Analysis" (competitive landscape coverage)
- "Account Plan" (stakeholder coverage, action items)
- "Technical Assessment" (depth, accuracy, source quality)

### Phase 3: Eval Dashboard
- Score trends over time per user/org
- Metric breakdown (which dimensions score lowest?)
- Report comparison (version A vs version B)
- Prompt impact analysis (same query, different prompts → score delta)

## Data Flywheel

```
User creates custom eval
    → Tells us what they care about (free insight!)
    
User rates reports (thumbs up/down)
    → Positively rated + high eval score = gold set candidate
    → Negatively rated = regression test case
    
User's custom criteria
    → Reveals gaps in our default metrics
    → Inspires new system-level metrics
    
Aggregate user evals
    → Correlate with retention/engagement
    → Validate our LLM judges against real user preferences
```

## Implementation Notes

### Leverages Existing Infrastructure
- `EvaluationEntityHandler` already supports STANDARD + CUSTOM evaluations
- `EvaluationRunEntityHandler` stores run results in Cassandra
- Score writing to Langfuse already works
- User feedback → Langfuse already works
- GraderRegistry pattern (new) plugs in cleanly

### What's Needed
- `EvalConfiguration` model (new — user-configurable metric selection)
- `geval_custom` grader (new — user natural language → LLM judge criteria)
- UI for eval creation/viewing (frontend work)
- Eval template library (curation work)
- Dashboard components (frontend work)

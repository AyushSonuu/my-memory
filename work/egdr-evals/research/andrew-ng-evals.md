# Andrew Ng Module 4 — Evals & Error Analysis Applied to EGDR

> **Source:** `tech/agentic-ai/module-4-practical-tips/` (lessons 01-07)
> **Applied to:** EGDR evaluation framework design
> **Distilled:** 2026-04-12

## Core Methodology

### The Development Loop (Lesson 01)
```
Build quick → Look at outputs → Spot failures → Build eval → Tweak → Run eval → Ship/iterate
```
- Start with 10-20 examples, not 1000
- Plan to iterate on evals too (they mature with the system)
- Blend metrics + human eye (early: more human, later: more automated)

### The 2×2 Eval Framework (Lesson 01)

```
                  │ Per-Example Ground Truth │ Universal Rule/Rubric
──────────────────┼─────────────────────────┼──────────────────────
Code-Based        │ Invoice date extraction  │ Word count check
(Objective)       │ (extracted == actual)    │ (len <= 10)
──────────────────┼─────────────────────────┼──────────────────────
LLM-as-Judge      │ Research coverage        │ Chart quality rubric
(Subjective)      │ (gold points in essay?)  │ (clear axes?)
```

### EGDR Mapping of 2×2

| Quadrant | EGDR Example |
|----------|-------------|
| Code + Ground Truth | Citation URLs match source list, topic coverage F1 |
| Code + Universal | Report length in bounds, section count ≥ 3, latency < 120s |
| LLM Judge + Ground Truth | Factual accuracy vs gold answer, synthesis vs source content |
| LLM Judge + Universal | Coherence rubric, neutrality 9-param audit, structure check |

## Error Analysis (Lessons 02-03)

### The Process
1. Collect **only failing** examples (skip the good ones)
2. Read traces span by span
3. Compare each step to "would a human expert do better?"
4. Build spreadsheet: example × component → mark failures
5. Count error rates per component
6. **Priority = Error Rate × Fixability**

### Key Insight: Cascading Errors
> If step 3 got garbage input from step 2, fix step 2. Don't blame downstream for upstream failures.

### EGDR Error Analysis Template

| Report ID | Outline (C2) | Research Agent (C3) | Search Results (C4) | Synthesis (C10) | Section Writing (C11) | Assembly (C12) |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| R-001 | | ❌ | | | | |
| R-002 | ❌ | | ❌ | | ❌ | |
| ... | | | | | | |
| **Error Rate** | ?% | ?% | ?% 🎯? | ?% | ?% | ?% |

**Percentages are NOT mutually exclusive** — one report can have multiple component failures.

### Cascading Error Check for EGDR
```
Bad outline → sections miss topics → NOT section writer's fault
Bad search  → bad synthesis → NOT synthesis agent's fault
Bad tools   → bad research → NOT research agent's fault
```
Always trace upstream before blaming the component.

## Component-Level Evals (Lesson 04)

### Why Not Just E2E?
- **Expensive:** Full pipeline = all LLM calls + tool calls for every small tweak
- **Noisy:** Other components introduce randomness that masks improvements

### EGDR Component Eval Designs

| Component | Isolated Eval | Gold Standard | Metric |
|-----------|---------------|---------------|--------|
| Web Search | Query → results | Expert URL lists | F1 (gold URLs ∈ results) |
| Research Agent | Brief → tool sequence | Expert trace | Tool selection accuracy |
| Synthesis | Raw sources → summary | Expert synthesis | Fidelity (LLM judge) |
| Section Writer | Brief + research → section | Expert section | Quality rubric |
| Outline | Query → outline | Expert outline | Coverage, section match |

### Workflow
```
Error Analysis → identifies bottleneck
     ↓
Component Eval → fast, focused iteration
     ↓
E2E Eval → confirm overall improvement
```

## Addressing Problems (Lesson 05)

### Non-LLM Components (search, tools, DB)
1. Tune hyperparameters (search engine, result count, date range)
2. Replace provider (different search engine, different API)

### LLM Components (agents, evaluators)
1. **Improve prompts** — add explicit instructions, few-shot examples (CHEAPEST)
2. **Try different model** — swap via aisuite, compare with evals
3. **Split the step** — decompose one complex call into 2-3 simpler ones
4. **Fine-tune** — LAST RESORT (expensive in dev time)

### EGDR-Specific Fix Map

| Component | Type | First Try | Second Try |
|-----------|------|-----------|------------|
| Web Search (C4) | Non-LLM Tool | Tune: result count, date range | Replace: different search engine/API |
| Research Agent (C3) | LLM | Improve research prompt | Try different model, split reasoning |
| Synthesis (C10) | LLM | Improve synthesis prompt | Split into extract → organize → write |
| Section Writer (C11) | LLM | Improve writing prompt + brief format | Try stronger model for writing |
| Outline (C2) | LLM | Add few-shot outline examples | Split into brainstorm → structure |

## Latency & Cost (Lesson 06)

### Priority Order: Quality → Latency → Cost

### EGDR Latency Optimization Targets
- **Parallelism:** Sections already run in parallel (up to 10 concurrent via semaphore ✅)
- **Smaller models:** Research query generation doesn't need frontier model
- **Faster providers:** SAP AI Core may have different serving speeds per model

### Cost Benchmarking
Benchmark each step's token + API cost individually. Don't guess — measure.

## The Build ↔ Analyze Cycle (Lesson 07)

| Stage | Build | Analyze |
|:-----:|-------|---------|
| Start | Quick prototype | Manual output review |
| Early | Tune based on traces | Small eval sets (10-20) |
| Growing | Focused component fixes | Error analysis spreadsheets |
| Mature | Targeted improvements | Component-level evals + E2E confirmation |

### Andrew Ng Quote
> "If you implement even a fraction of this module, you'll be ahead of the vast majority of developers. Not because others can't code — they just don't do the analysis."

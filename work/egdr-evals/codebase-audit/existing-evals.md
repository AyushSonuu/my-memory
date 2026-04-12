# Existing Eval Infrastructure — What's Already Built

> **Audited:** 2026-04-12
> **Verdict:** More exists than expected. Langfuse is fully operational. LLM-as-judge evals are running in production. DeepEval code exists but is blocked by dep conflict.

## ✅ Fully Operational

### 1. Langfuse Observability (Milestone 1 — DONE)
- **Init:** `langfuse_support.py` → `init_langfuse()` populates env vars at startup
- **Callbacks:** `CustomLangfuseHandler` wraps standard Langfuse handler + injects SAP AI Core cost
- **Traces:** Every LLM call, tool invocation, agent handoff captured as hierarchical traces
- **Naming:** Standardized contract: `workflow:slug`, `agent:slug`, `tool:slug`, `subworkflow:slug:qualifier`
- **Context propagation:** `propagate_langfuse_context()` ensures child workflows inherit trace
- **Env detection:** Works across local, dev, staging, production environments

### 2. Online LLM-as-Judge Evaluation (Milestone 3 — Partial)
- **evaluation_workflow.py:** LangGraph workflow running 4 evaluators sequentially:
  1. Completeness (report vs outline vs user question) → 1-5
  2. Structure (format, flow, headers) → 1-5
  3. Relevance (section-level relevance to query) → 1-5
  4. Overall Quality → 6 sub-scores (research depth, source quality, analytical rigor, practical value, balance, writing quality) → 1-5 each
- **evaluation_runner.py:** Runs asynchronously after report generation
  - Creates Langfuse observation span for eval
  - Writes scores to Langfuse via `write_trace_scores`
  - Writes results to Cassandra via `EvaluationRunEntityHandler`
  - Handles errors gracefully, marks failed runs

### 3. Langfuse Score Pipeline
- **Score schema:** Canonical names defined (`report.completeness`, `report.structure`, etc.)
- **Score writing:** `write_trace_scores()` with retry logic (3 attempts, exponential backoff)
- **Score config:** Environment-based config IDs for standardization
- **Association:** Scores linked to traces by `trace_id` (preferred) → `observation_id` → `session_id`

### 4. User Feedback → Langfuse
- **chat_feedback_resolvers.py:** Handles thumbs up/down, star ratings, free-text
- **_push_langfuse_score():** Pushes feedback as Langfuse score with trace correlation
- **update_langfuse_synced():** Tracks sync status per feedback item

### 5. Evaluation Registry + Storage
- **Registry:** 3 standard types (Comprehensive Report Assessment, Text Coherence, Financial Performance)
- **Entity handler:** STANDARD (code-defined) + CUSTOM (DB-stored) evaluations
- **Run storage:** Cassandra for metadata, blob storage for detailed results
- **Run lifecycle:** PENDING → RUNNING → COMPLETED/FAILED with duration tracking

### 6. Neutrality Evaluator (Ethics)
- 9-parameter structured evaluation (framing language, selective omission, assertion upgrade, etc.)
- Pass/Fail verdict with High/Medium/Low severity
- Compares synthesized research against raw tool outputs
- Full structured JSON output

### 7. Evaluation Prompts
All prompts defined in `evaluation_prompts.py`:
- COMPLETENESS_PROMPT
- STRUCTURE_PROMPT
- RELEVANCE_PROMPT
- OVERALL_QUALITY_PROMPT
- CORRECTNESS_PROMPT (needs gold answer)
- GROUNDEDNESS_PROMPT (needs retrieval context)
- NEUTRALITY_PROMPT (9-param ethics)

## ⚠️ Exists But Blocked

### DeepEval Integration
- **evaluation_model.py:** `EvaluationModel(DeepEvalBaseLLM)` — wraps SAP AI Core models
- **metrics.py:** `MetricsManager` — 3 GEval metrics with rubrics (0-10 scale)
- **report_evaluator.py:** `ReportEvaluator` — creates `LLMTestCase`, calls `deepeval.evaluate()`
- **evaluation_nodes.py:** Integration point in evaluation pipeline (uses metrics_manager)
- **BLOCKED:** `deepeval ^2.9.4` conflicts with `sap-ai-sdk-core` on `click` package version

## ❌ Not Built Yet

| What | White Paper Section | Notes |
|------|-------------------|-------|
| Code-based graders (CI gates) | §3.2, Milestone 2 | Citation validity, latency, source diversity |
| Offline eval set | §3.2, §6, Milestone 5 | Need to curate from Langfuse production data |
| Baseline metrics | §8, Milestone 7 | Need eval set first |
| Ship/no-ship thresholds | §8, Milestone 8 | Need baseline first |
| Component-level evals | §3.1 | Need error analysis first |
| Intermediate step evals | §3.1 | Orchestration, plan, source, synthesis evals |
| Efficiency monitoring/alerting | §3.1 | Langfuse has cost data but no alert thresholds |
| User-defined eval configurations | Conversation | The cross-app product vision |

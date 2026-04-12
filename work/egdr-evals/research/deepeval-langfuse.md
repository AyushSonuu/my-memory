# DeepEval + Langfuse — Integration Architecture

> **Sources:** DeepEval docs, Langfuse docs, EGDR codebase
> **Distilled:** 2026-04-12

## What Each Tool Does

### DeepEval
- Open-source LLM evaluation framework
- Unit-test style (`deepeval test run`)
- 50+ built-in metrics (GEval, faithfulness, answer relevancy, etc.)
- Key metric for us: **GEval** — customizable LLM-as-judge with criteria + rubric
- Supports multi-turn, RAG, agent evaluation
- Has cloud platform (Confident AI) but we use Langfuse instead

### Langfuse
- Open-source LLM observability platform
- Traces every LLM call, tool invocation, agent handoff
- Built on OpenTelemetry
- **Scores system:** attach numeric/categorical/boolean scores to traces
- Score configs for standardized metric names
- Dashboards, filtering, analytics on scores over time
- Native LangChain/LangGraph callback handler

## How They're Used in EGDR Today

### Langfuse (Fully Operational)
```
Server Process
    │
    ├── CustomLangfuseHandler (callback on every LLM call)
    │   └── Injects SAP AI Core cost data into observations
    │
    ├── Trace context propagation
    │   └── propagate_langfuse_context() → child workflows inherit trace
    │
    ├── Score writing
    │   └── write_trace_scores() → eval results → Langfuse scores
    │   └── Score names: report.completeness, report.structure, etc.
    │
    ├── User feedback → Langfuse scores
    │   └── _push_langfuse_score() in chat_feedback_resolvers.py
    │
    └── Naming contract
        └── workflow:report-generation-workflow (abc123)
        └── subworkflow:research-workflow:market-overview
```

### DeepEval (Code Exists, Dep Blocked)

```python
# In evaluations/metrics.py (EXISTS but can't run):
MetricsManager creates 3 GEval metrics:
  - KPIs and Success Metrics (rubric: 0-3, 4-7, 8-10)
  - Competitive Positioning (rubric: 0-3, 4-7, 8-10)
  - Market Analysis Depth (rubric: 0-3, 4-7, 8-10)

# In evaluations/evaluation_model.py (EXISTS):
EvaluationModel extends DeepEvalBaseLLM
  - Wraps ModelProvider for SAP AI Core models
  - Implements generate() and a_generate()

# In evaluations/report_evaluator.py (EXISTS):
ReportEvaluator.evaluate_report()
  - Creates LLMTestCase(input, actual_output, expected_output, retrieval_context)
  - Calls deepeval.evaluate(test_cases, metrics)

# BLOCKER in pyproject.toml:
# deepeval = "^2.9.4"  # conflicts with sap-ai-sdk-core click requirement
```

## Resolution Strategy: Hybrid A+B

### Online Evals (in server process) → Direct LLM-as-Judge

Already working via `evaluation_workflow.py`:
- Completeness evaluator (LLM judge, 1-5 scale)
- Structure evaluator (LLM judge, 1-5 scale)
- Relevance evaluator (LLM judge, 1-5 scale)
- Overall quality evaluator (6 sub-dimensions, 1-5 each)
- Neutrality evaluator (9 parameters, Pass/Fail)

These use direct LLM calls with structured output — NO DeepEval dependency needed.

Results flow to:
1. Langfuse scores (via `write_trace_scores`)
2. Cassandra evaluation_runs (via `EvaluationRunEntityHandler`)

### Offline Evals (separate process) → DeepEval in Isolated Venv

```bash
# Setup
python -m venv eval_venv
source eval_venv/bin/activate
pip install deepeval langfuse

# Run offline eval set
python run_offline_eval.py --eval-set eval_sets/v0.1/ --config production
# → Reads eval cases
# → Runs DeepEval GEval metrics
# → Pushes scores to Langfuse via API
# → Compares vs baseline
# → Outputs ship/no-ship report
```

## Score Schema (Already Defined)

From `langfuse_score_schema.py`:

```python
REPORT_SCORE_NAME_MAPPING = {
    "completeness": "report.completeness",
    "structure": "report.structure",
    "relevance": "report.relevance",
    "overall_quality_research_depth": "report.overall_quality.research_depth",
    "overall_quality_source_quality": "report.overall_quality.source_quality",
    "overall_quality_analytical_rigor": "report.overall_quality.analytical_rigor",
    "overall_quality_practical_value": "report.overall_quality.practical_value",
    "overall_quality_balance_and_objectivity": "report.overall_quality.balance_and_objectivity",
    "overall_quality_writing_quality": "report.overall_quality.writing_quality",
    "overall": "report.overall",  # Average of all above
}
```

## Key File Paths

| Component | Path |
|-----------|------|
| Langfuse init + callbacks | `core/common/telemetry/langfuse_support.py` |
| Custom handler (SAP cost) | `core/common/telemetry/custom_langfuse_handler.py` |
| Score writing | `core/common/telemetry/langfuse_scores.py` |
| Score schema | `core/common/telemetry/langfuse_score_schema.py` |
| Eval workflow (LangGraph) | `orchestration/workflows/evaluation_workflow.py` |
| Eval runner (async post-gen) | `orchestration/evaluation/evaluation_runner.py` |
| Eval prompts | `orchestration/resources/evaluation_prompts.py` |
| Eval types/models | `orchestration/resources/evaluation_types.py` |
| DeepEval metrics | `evaluations/metrics.py` |
| DeepEval model wrapper | `evaluations/evaluation_model.py` |
| DeepEval report evaluator | `evaluations/report_evaluator.py` |
| Eval registry | `evaluations/evaluation_registry.py` |
| Eval entity handler | `data_access/entities/evaluation_entity_handler.py` |
| Eval run handler | `data_access/entities/evaluation_run_entity_handler.py` |
| User feedback → Langfuse | `apis/gql/resolvers/chat_feedback_resolvers.py` |

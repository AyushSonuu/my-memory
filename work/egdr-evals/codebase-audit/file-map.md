# Key File Paths — EGDR Codebase Reference

> **Repo:** `experience-generation-server`
> **Base:** `/Users/I772464/Library/CloudStorage/OneDrive-SAPSE/Desktop/experience-generation/experience-generation-server`

## Telemetry / Langfuse

| File | What |
|------|------|
| `core/common/telemetry/langfuse_support.py` | Init, callbacks, context propagation, naming |
| `core/common/telemetry/custom_langfuse_handler.py` | LangChain callback + SAP cost injection |
| `core/common/telemetry/langfuse_scores.py` | Score writing with retries |
| `core/common/telemetry/langfuse_score_schema.py` | Canonical score names |
| `core/common/telemetry/model_pricing.py` | SAP AI Core cost calculation |

## Evaluation (Backend)

| File | What |
|------|------|
| `evaluations/evaluation_registry.py` | EvaluationType enum + EVALUATION_DEFINITIONS_REGISTRY |
| `evaluations/evaluation_model.py` | DeepEvalBaseLLM wrapper for SAP AI Core |
| `evaluations/metrics.py` | MetricsManager (3 GEval metrics) |
| `evaluations/report_evaluator.py` | ReportEvaluator (deepeval.evaluate wrapper) |
| `evaluations/evaluation_nodes.py` | evaluate_report() integration point |
| `evaluations/README.md` | How to add standard evaluations |

## Evaluation (Orchestration)

| File | What |
|------|------|
| `orchestration/workflows/evaluation_workflow.py` | LangGraph: completeness → structure → relevance → quality |
| `orchestration/evaluation/evaluation_runner.py` | Async post-generation eval runner |
| `orchestration/resources/evaluation_prompts.py` | All eval prompts (completeness, structure, relevance, quality, correctness, groundedness, neutrality) |
| `orchestration/resources/evaluation_types.py` | Pydantic models for eval I/O |
| `orchestration/resources/evaluation_states.py` | LangGraph state for eval workflow |

## Evaluator Agents

| File | What |
|------|------|
| `orchestration/agents/evaluators/completeness_evaluator.py` | Report vs outline vs query |
| `orchestration/agents/evaluators/structure_evaluator.py` | Format, flow, headers |
| `orchestration/agents/evaluators/relevance_evaluator.py` | Section relevance |
| `orchestration/agents/evaluators/overall_quality_evaluator.py` | 6 sub-dimensions |
| `orchestration/agents/evaluators/groundedness_evaluator.py` | Claims vs context |
| `orchestration/agents/evaluators/correctness_evaluator.py` | Report vs gold answer |
| `orchestration/agents/evaluators/neutrality_evaluator.py` | 9-param ethics audit |

## Workflows

| File | What |
|------|------|
| `orchestration/workflows/report_generation_workflow.py` | Main pipeline: intake → outline → sections → report → store → eval |
| `orchestration/workflows/research_workflow.py` | Per-section: researcher → tools → charts → synthesize |
| `orchestration/workflows/edit_workflow.py` | Report editing pipeline |
| `orchestration/workflows/assistant_workflow.py` | General assistant |
| `orchestration/workflows/react_agentic_workflow.py` | Generic ReAct |
| `orchestration/workflows/scenario_analysis_workflow.py` | Scenario planning |

## Agents (Non-Evaluator)

| File | What |
|------|------|
| `orchestration/agents/report_intake_agent.py` | Decides execute vs ask questions |
| `orchestration/agents/generate_outline_agent.py` | Creates report outline |
| `orchestration/agents/generic_research_agent.py` | ReAct research loop |
| `orchestration/agents/synthesize_research_agent.py` | Condenses raw research |
| `orchestration/agents/write_section_agent.py` | Writes report sections |
| `orchestration/agents/chart_config_agent.py` | Generates chart configs |
| `orchestration/agents/report_summary_agent.py` | Generates summary message |

## Tools

| File | What |
|------|------|
| `orchestration/tools/search_web_tool.py` | Web search |
| `orchestration/tools/research_company_tool.py` | Company research |
| `orchestration/tools/query_sap_tool.py` | SAP data |
| `orchestration/tools/query_cx_data_tool.py` | CX/CRM data |
| `orchestration/tools/search_stakeholder_tool.py` | People search |
| `orchestration/tools/search_resources_tool.py` | User-uploaded resources |
| `orchestration/tools/store_artifact_tool.py` | Artifact storage |
| `orchestration/tools/think_tool.py` | Internal reasoning |
| `orchestration/tools/mcp_tools/` | MCP connectors |
| `orchestration/tools/tool_registry.py` | Tool registration |

## Data Access

| File | What |
|------|------|
| `data_access/entities/evaluation_entity_handler.py` | STANDARD + CUSTOM eval CRUD |
| `data_access/entities/evaluation_run_entity_handler.py` | Eval run lifecycle (Cassandra) |
| `data_access/postgres/store/evaluation_store.py` | PostgreSQL eval storage |
| `data_access/cassandra/store/evaluation_run_store.py` | Cassandra eval run storage |

## API Layer

| File | What |
|------|------|
| `apis/gql/resolvers/chat_feedback_resolvers.py` | User feedback → Langfuse scores |
| `apis/gql/resolvers/subscription_resolvers.py` | Workflow execution + Langfuse trace setup |
| `apis/gql/resolvers/execution/context.py` | Execution context + Langfuse metadata |
| `apis/gql/resolvers/execution/workflow_runner.py` | Workflow runner + Langfuse integration |
| `apis/api_server.py` | Server startup (calls init_langfuse) |

## Config

| File | What |
|------|------|
| `pyproject.toml` | Dependencies (langfuse ^3.14.1, deepeval commented out) |
| `core/config/configuration.py` | DEFAULT_MODEL_NAME, ModelConfig |
| `environments/env_config.py` | Environment variable loading |

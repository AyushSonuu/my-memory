# EGDR Component Inventory — Every Evaluable Piece

> **Source:** Codebase audit of `experience-generation-server`
> **Audited:** 2026-04-12

## Pipeline Architecture

```
User Query → Intake → Outline → [N×(Research → Synthesis → Write Section)] → Assemble Report → Store → Eval
```

## Component Catalog

### LLM Agents

| ID | Agent | File | Role | Eval Exists? |
|----|-------|------|------|:---:|
| C1 | `report_intake_agent` | `orchestration/agents/report_intake_agent.py` | Decides: execute or ask clarifying questions | ❌ |
| C2 | `generate_report_outline` | `orchestration/agents/generate_outline_agent.py` | Creates section structure + objective | ❌ |
| C3 | `generic_research_agent` | `orchestration/agents/generic_research_agent.py` | ReAct loop: reasons about what to search, picks tools | ❌ |
| C10 | `synthesize_research_agent` | `orchestration/agents/synthesize_research_agent.py` | Condenses raw tool outputs into coherent research | ❌ |
| C11 | `write_section_agent` | `orchestration/agents/write_section_agent.py` | Writes one report section from brief + research | ❌ |
| C15 | `chart_config_agent` | `orchestration/agents/chart_config_agent.py` | Generates chart configs from data | ❌ |
| C17 | `report_summary_agent` | `orchestration/agents/report_summary_agent.py` | Generates summary message for UI | ❌ |
| C18 | `intent_router_agent` | `orchestration/agents/intent_router_agent.py` | Routes user intent to correct workflow | ❌ |

### Tools (Non-LLM)

| ID | Tool | File | Role | Eval Exists? |
|----|------|------|------|:---:|
| C4 | `search_web_tool` | `orchestration/tools/search_web_tool.py` | Web search API | ❌ |
| C5 | `research_company_tool` | `orchestration/tools/research_company_tool.py` | Company-specific research | ❌ |
| C6 | `query_sap_tool` | `orchestration/tools/query_sap_tool.py` | SAP internal data query | ❌ |
| C7 | `query_cx_data_tool` | `orchestration/tools/query_cx_data_tool.py` | CX/CRM data query | ❌ |
| C8 | `search_stakeholder_tool` | `orchestration/tools/search_stakeholder_tool.py` | Stakeholder/people search | ❌ |
| C9 | MCP tools | `orchestration/tools/mcp_tools/` | Various MCP connectors | ❌ |
| C19 | `search_resources_tool` | `orchestration/tools/search_resources_tool.py` | Search user-uploaded resources | ❌ |
| C20 | `store_artifact_tool` | `orchestration/tools/store_artifact_tool.py` | Store report as artifact | ❌ |
| C21 | `query_datasource_tool` | `orchestration/tools/query_datasource_tool.py` | Generic datasource query | ❌ |
| C22 | `think_tool` | `orchestration/tools/think_tool.py` | Internal reasoning step | N/A |

### Workflows (Orchestration)

| ID | Workflow | File | Components Orchestrated |
|----|----------|------|------------------------|
| W1 | `report_generation_workflow` | `orchestration/workflows/report_generation_workflow.py` | C1 → C2 → [C3..C11] → store → eval |
| W2 | `research_workflow` | `orchestration/workflows/research_workflow.py` | C3 ↔ tools → charts → C10 |
| W3 | `evaluation_workflow` | `orchestration/workflows/evaluation_workflow.py` | Completeness → Structure → Relevance → Quality |
| W4 | `edit_workflow` | `orchestration/workflows/edit_workflow.py` | Edit request → identify → generate → apply |
| W5 | `assistant_workflow` | `orchestration/workflows/assistant_workflow.py` | General assistant interactions |
| W6 | `react_agentic_workflow` | `orchestration/workflows/react_agentic_workflow.py` | Generic ReAct pattern |
| W7 | `scenario_analysis_workflow` | `orchestration/workflows/scenario_analysis_workflow.py` | Scenario planning |
| W8 | `chart_generation_workflow` | `orchestration/workflows/chart_generation_workflow.py` | Data → chart config |

### Evaluators (Already Exist)

| ID | Evaluator | File | What It Measures | Scale |
|----|-----------|------|-----------------|-------|
| E1 | `completeness_evaluator` | `orchestration/agents/evaluators/completeness_evaluator.py` | Report covers all outline points | 1-5 |
| E2 | `structure_evaluator` | `orchestration/agents/evaluators/structure_evaluator.py` | Logical flow, correct format | 1-5 |
| E3 | `relevance_evaluator` | `orchestration/agents/evaluators/relevance_evaluator.py` | Section-level relevance to query | 1-5 |
| E4 | `overall_quality_evaluator` | `orchestration/agents/evaluators/overall_quality_evaluator.py` | 6 sub-dimensions | 1-5 each |
| E5 | `groundedness_evaluator` | `orchestration/agents/evaluators/groundedness_evaluator.py` | Claims supported by sources | Per-claim bool |
| E6 | `correctness_evaluator` | `orchestration/agents/evaluators/correctness_evaluator.py` | Mirrors independent authority answer | 1-5 |
| E7 | `neutrality_evaluator` | `orchestration/agents/evaluators/neutrality_evaluator.py` | 9-parameter ethics audit | Pass/Fail + Severity |

## Architecture Notes

### Key Design Patterns
- **Registry pattern:** `@workflow(id=...)`, `@agent(id=...)` decorators register components
- **BaseWorkflow / BaseAgent:** All inherit from these, ensuring consistent config handling
- **LangGraph state machines:** Workflows are compiled LangGraph graphs with typed state
- **Async evaluation:** `evaluation_runner.py` schedules eval as background `asyncio.Task`
- **Semaphore concurrency:** Up to 10 parallel section research+write pipelines

### Config Propagation
- `Configuration.from_runnable_config(config)` → extracts org_id, user_id, thread_id, etc.
- Langfuse context propagated via `propagate_langfuse_context()` to child workflows
- Run names follow contract: `workflow:report-generation-workflow (abc123)`

### Data Flow
```
Report generated
    → store_artifact_tool (stores in blob)
    → evaluation_runner.run_report_evaluation_job (async)
        → evaluation_workflow (LangGraph: completeness → structure → relevance → quality)
        → write_trace_scores (Langfuse)
        → EvaluationRunEntityHandler (Cassandra)
```

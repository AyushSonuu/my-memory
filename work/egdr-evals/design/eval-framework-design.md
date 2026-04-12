# EGDR Evaluation Framework — Comprehensive System Design

> **Author:** Ayush Sonu + Ayra | **Date:** 2026-04-12
> **System:** Experience Generation Deep Research (EGDR) @ SAP
> **Purpose:** HLD + LLD for a user-centric, extensible evaluation framework
> **Sources:** Brad Powley's white paper, Andrew Ng Module 4 (Agentic AI), Anthropic's eval guide, codebase audit

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Landscape — What We're Evaluating](#2-system-landscape)
3. [Architecture: High-Level Design (HLD)](#3-hld)
4. [Architecture: Low-Level Design (LLD)](#4-lld)
5. [The 4×4 Eval Matrix — Applying Andrew Ng's Framework](#5-the-4x4-eval-matrix)
6. [Component Decomposition + Error Analysis Map](#6-component-decomposition)
7. [User-Centric Eval System (The Product Vision)](#7-user-centric-evals)
8. [Metric Catalog — Complete Reference](#8-metric-catalog)
9. [Grader Architecture](#9-grader-architecture)
10. [Eval Set Management](#10-eval-set-management)
11. [Langfuse + DeepEval Integration Architecture](#11-langfuse-deepeval)
12. [Continuous Improvement Loop](#12-continuous-improvement)
13. [Roadmap & Prioritization](#13-roadmap)

---

## 1. Executive Summary

EGDR is a multi-agent research platform that compresses days of analyst work into minutes. But speed without reliability is dangerous — a fluent report that's factually wrong is worse than no report.

This document designs a **comprehensive, extensible, user-centric evaluation framework** that:

1. **Measures quality** at end-to-end AND component level
2. **Enables users** to define their own eval criteria (the cross-app eval product vision)
3. **Applies Andrew Ng's error analysis** methodology to our specific pipeline
4. **Integrates with existing Langfuse + DeepEval** infrastructure
5. **Feeds a continuous improvement loop** from production → eval set → tuning → ship

### Design Principles

| Principle | What It Means |
|-----------|---------------|
| **User-centric** | Users define what "good" means for THEM. Our system evals + user evals coexist |
| **Extensible** | New metrics, new evaluators, new grading methods — all pluggable via registry |
| **Observable** | Every eval decision is traceable back to the exact trace/span |
| **Evidence-based** | Ship/no-ship decisions backed by data, not gut feeling |
| **Proportional** | Eval effort matches blast radius of change |

---

## 2. System Landscape — What We're Evaluating {#2-system-landscape}

### EGDR Pipeline Architecture (from codebase)

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  REPORT GENERATION WORKFLOW (LangGraph)                            │
│                                                                     │
│  ┌─────────────┐   ┌──────────────────┐   ┌─────────────────────┐ │
│  │ 1. INTAKE    │──▶│ 2. OUTLINE       │──▶│ 3. SECTIONS (||)    │ │
│  │ report_intake│   │ generate_outline  │   │ [N sections in      │ │
│  │ _agent      │   │ _agent           │   │  parallel]           │ │
│  └─────────────┘   └──────────────────┘   └──────────┬──────────┘ │
│                                                       │             │
│        Each section runs a RESEARCH WORKFLOW:          │             │
│        ┌──────────────────────────────────────┐       │             │
│        │  RESEARCH WORKFLOW (per section)      │       │             │
│        │                                       │       │             │
│        │  ┌────────────┐  ┌───────────────┐   │       │             │
│        │  │ RESEARCHER │──│ TOOLS         │   │       │             │
│        │  │ (ReAct loop│  │ • search_web  │   │       │             │
│        │  │  generic_  │  │ • research_co │   │       │             │
│        │  │  research) │  │ • query_sap   │   │       │             │
│        │  └────────────┘  │ • query_cx    │   │       │             │
│        │       │          │ • search_     │   │       │             │
│        │       ▼          │   stakeholder │   │       │             │
│        │  ┌────────────┐  │ • MCP tools   │   │       │             │
│        │  │ SYNTHESIZE │  │ • think_tool  │   │       │             │
│        │  │ _RESEARCH  │  └───────────────┘   │       │             │
│        │  └────────────┘                       │       │             │
│        └──────────────────────────────────────┘       │             │
│                                                       │             │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────▼──────────┐  │
│  │ 4. GENERATE      │──│ 5. STORE     │──│ 6. EVAL (async)     │  │
│  │ _REPORT (merge   │  │ _ARTIFACT    │  │ evaluation_workflow  │  │
│  │  all sections)   │  │              │  │ + evaluation_runner  │  │
│  └──────────────────┘  └──────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Evaluable Components Inventory

| ID | Component | Type | Agent/Tool | Current Eval? |
|----|-----------|------|------------|:-------------:|
| C1 | **Report Intake** | LLM Agent | `report_intake_agent` | ❌ |
| C2 | **Outline Generation** | LLM Agent | `generate_report_outline` | ❌ |
| C3 | **Research (ReAct)** | LLM Agent | `generic_research_agent` | ❌ |
| C4 | **Web Search** | Tool | `search_web_tool` | ❌ |
| C5 | **Company Research** | Tool | `research_company_tool` | ❌ |
| C6 | **SAP Data Query** | Tool | `query_sap_tool` | ❌ |
| C7 | **CX Data Query** | Tool | `query_cx_data_tool` | ❌ |
| C8 | **Stakeholder Search** | Tool | `search_stakeholder_tool` | ❌ |
| C9 | **MCP Tools** | Tool | Various MCP connectors | ❌ |
| C10 | **Research Synthesis** | LLM Agent | `synthesize_research_agent` | ❌ |
| C11 | **Section Writing** | LLM Agent | `write_section_agent` | ❌ |
| C12 | **Report Assembly** | Code | merge sections | ❌ |
| C13 | **End-to-End Report** | Pipeline | full report_generation_workflow | ✅ Partial |
| C14 | **Edit Workflow** | Pipeline | edit_workflow | ❌ |
| C15 | **Chart Generation** | LLM Agent | `chart_config_agent` | ❌ |
| C16 | **Neutrality** | LLM Judge | `neutrality_evaluator` | ✅ Exists |

### Existing Eval Infrastructure (from codebase audit)

| What | Status | Files |
|------|--------|-------|
| **Langfuse tracing** | ✅ Full | `langfuse_support.py`, `custom_langfuse_handler.py` |
| **Langfuse score writing** | ✅ Full | `langfuse_scores.py`, `langfuse_score_schema.py` |
| **Evaluation Workflow (LangGraph)** | ✅ Working | `evaluation_workflow.py` (completeness, structure, relevance, overall quality) |
| **Evaluation Runner (async)** | ✅ Working | `evaluation_runner.py` (post-generation, writes to Langfuse + Cassandra) |
| **Evaluation Registry** | ✅ Working | `evaluation_registry.py` (STANDARD + CUSTOM types) |
| **DeepEval metrics** | ⚠️ Code exists, dep broken | `metrics.py`, `report_evaluator.py` (click conflict) |
| **Neutrality evaluator** | ✅ Full | 9-parameter ethics check with structured output |
| **User feedback → Langfuse** | ✅ Working | `chat_feedback_resolvers.py` → `_push_langfuse_score()` |
| **Evaluation Run storage** | ✅ Cassandra + Blob | `evaluation_run_entity_handler.py` |

---

## 3. Architecture: High-Level Design (HLD) {#3-hld}

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         EGDR EVAL FRAMEWORK (HLD)                          │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    EVALUATION PLANE                                  │   │
│  │                                                                     │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────┐   │   │
│  │  │ OFFLINE EVAL  │  │ ONLINE EVAL   │  │ USER-DEFINED EVAL     │   │   │
│  │  │ ENGINE        │  │ ENGINE        │  │ ENGINE                │   │   │
│  │  │               │  │               │  │                       │   │   │
│  │  │ • Eval sets   │  │ • Runtime     │  │ • Custom metrics      │   │   │
│  │  │ • CI gates    │  │   evaluators  │  │ • Custom rubrics      │   │   │
│  │  │ • Baseline    │  │ • Feedback    │  │ • Threshold config    │   │   │
│  │  │   comparison  │  │   collection  │  │ • Eval templates      │   │   │
│  │  │ • A/B testing │  │ • Anomaly     │  │ • Eval runs on demand │   │   │
│  │  │               │  │   detection   │  │                       │   │   │
│  │  └──────┬────────┘  └──────┬────────┘  └──────────┬────────────┘   │   │
│  │         │                  │                       │                │   │
│  │         └──────────────────┼───────────────────────┘                │   │
│  │                            ▼                                        │   │
│  │              ┌──────────────────────────┐                           │   │
│  │              │    GRADER FRAMEWORK      │                           │   │
│  │              │                          │                           │   │
│  │              │  ┌────────┐ ┌─────────┐  │                           │   │
│  │              │  │ Code   │ │ LLM-as- │  │                           │   │
│  │              │  │ Grader │ │ Judge   │  │                           │   │
│  │              │  └────────┘ └─────────┘  │                           │   │
│  │              │  ┌────────┐ ┌─────────┐  │                           │   │
│  │              │  │ Human  │ │ DeepEval│  │                           │   │
│  │              │  │ Grader │ │ Metrics │  │                           │   │
│  │              │  └────────┘ └─────────┘  │                           │   │
│  │              └──────────────────────────┘                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    OBSERVABILITY PLANE (Langfuse)                     │  │
│  │                                                                      │  │
│  │  Traces → Spans → Scores → Dashboards → Alerts                      │  │
│  │  (every LLM call, tool call, agent handoff fully instrumented)       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    STORAGE PLANE                                      │  │
│  │                                                                      │  │
│  │  PostgreSQL    │ Cassandra        │ Blob Storage   │ Langfuse Cloud  │  │
│  │  (eval defs,   │ (eval runs,      │ (detailed      │ (traces, scores │  │
│  │   user evals)  │  run metadata)   │  results)      │  dashboards)    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

### Three Eval Engines

| Engine | Who Uses It | When | Example |
|--------|-------------|------|---------|
| **Offline Eval** | Dev team | Before release, CI | "Does this prompt change improve factual accuracy across 50 test cases?" |
| **Online Eval** | Automated + Ops | In production, on every run | "Did this report pass completeness > 3.5 and neutrality = Pass?" |
| **User-Defined Eval** | End users | On demand, per their needs | "Score my reports on SAP product knowledge coverage with threshold 4.0" |

---

## 4. Architecture: Low-Level Design (LLD) {#4-lld}

### 4.1 Core Abstractions

```python
# === GRADER PROTOCOL (the Plugin Interface) ===

class GraderType(str, Enum):
    CODE = "code"           # Deterministic, rule-based
    LLM_JUDGE = "llm_judge" # LLM-as-judge with rubric
    DEEPEVAL = "deepeval"   # DeepEval GEval metrics
    HUMAN = "human"         # Human annotation
    COMPOSITE = "composite" # Weighted combination of other graders

class GradeResult(BaseModel):
    """Universal output from any grader."""
    metric_name: str
    score: float                  # Normalized 0.0 - 1.0
    raw_score: float | None       # Original scale (e.g., 1-5)
    passed: bool                  # Score >= threshold
    reasoning: str                # Why this score
    evidence: list[str] | None    # Supporting quotes/data
    metadata: dict[str, Any]      # Grader-specific extras

class BaseGrader(ABC):
    """All graders implement this interface."""
    
    @abstractmethod
    def grade(self, input: GraderInput) -> GradeResult: ...
    
    @abstractmethod
    def schema(self) -> GraderSchema: ...  # For discovery/registry
    
    @property
    @abstractmethod
    def grader_type(self) -> GraderType: ...

class GraderInput(BaseModel):
    """Standardized input to any grader."""
    # What's being evaluated
    actual_output: str
    # Context (optional, depends on grader)
    input_query: str | None = None
    expected_output: str | None = None
    retrieval_context: list[str] | None = None
    source_citations: list[str] | None = None
    # Pipeline trace data
    trace_id: str | None = None
    span_data: dict[str, Any] | None = None
```

### 4.2 Eval Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     EVAL PIPELINE                                 │
│                                                                   │
│  ┌────────────┐    ┌───────────────┐    ┌─────────────────────┐  │
│  │ EVAL SET   │───▶│ EVAL RUNNER   │───▶│ RESULT AGGREGATOR   │  │
│  │            │    │               │    │                     │  │
│  │ • Cases    │    │ • Load case   │    │ • Compute means     │  │
│  │ • Gold set │    │ • Run graders │    │ • Compare baseline  │  │
│  │ • Rubrics  │    │ • Collect     │    │ • Generate report   │  │
│  │ • Versions │    │   scores      │    │ • Ship/no-ship      │  │
│  └────────────┘    └───────────────┘    └─────────────────────┘  │
│                           │                                       │
│                    ┌──────┴──────┐                                 │
│                    │ GRADER POOL │                                 │
│                    │             │                                 │
│                    │ [Code]      │                                 │
│                    │ [LLM Judge] │                                 │
│                    │ [DeepEval]  │                                 │
│                    │ [Human]     │                                 │
│                    └─────────────┘                                 │
└──────────────────────────────────────────────────────────────────┘
```

### 4.3 Registry Pattern (Extensibility)

```python
# === GRADER REGISTRY (mirrors existing evaluation_registry.py pattern) ===

class GraderRegistry:
    """Singleton registry of all available graders.
    
    Follows the same pattern as EVALUATION_DEFINITIONS_REGISTRY
    but for grading methods rather than evaluation types.
    """
    _graders: dict[str, Type[BaseGrader]] = {}
    
    @classmethod
    def register(cls, name: str):
        """Decorator to register a grader class."""
        def wrapper(grader_cls: Type[BaseGrader]):
            cls._graders[name] = grader_cls
            return grader_cls
        return wrapper
    
    @classmethod
    def get(cls, name: str) -> Type[BaseGrader]:
        return cls._graders[name]
    
    @classmethod
    def list_available(cls) -> list[GraderSchema]:
        return [g.schema() for g in cls._graders.values()]

# === USAGE ===

@GraderRegistry.register("citation_validity")
class CitationValidityGrader(BaseGrader):
    """Code-based grader: checks if citation URLs resolve."""
    grader_type = GraderType.CODE
    
    def grade(self, input: GraderInput) -> GradeResult:
        # Extract URLs, check if they resolve
        ...

@GraderRegistry.register("factual_accuracy")
class FactualAccuracyGrader(BaseGrader):
    """LLM-as-judge: scores factual claims against gold set."""
    grader_type = GraderType.LLM_JUDGE
    
    def grade(self, input: GraderInput) -> GradeResult:
        # Prompt LLM with rubric, parse structured output
        ...
```

### 4.4 Eval Configuration Model (User-Extensible)

```python
class EvalConfiguration(BaseModel):
    """User-configurable evaluation setup.
    
    This is what enables the user-centric eval product.
    Users can create their own configurations via the API.
    """
    id: str
    name: str
    description: str
    owner_type: Literal["system", "organization", "user"]
    
    # What to evaluate
    target_type: Literal["report", "section", "research", "edit", "chat_response"]
    
    # Which graders to run
    metrics: list[MetricConfig]
    
    # Thresholds
    pass_threshold: float  # Overall pass score
    
    # Scheduling
    run_mode: Literal["auto", "on_demand", "ci_only"]
    
class MetricConfig(BaseModel):
    """Single metric within an eval configuration."""
    grader_name: str                    # Must exist in GraderRegistry
    weight: float = 1.0                 # For weighted average
    threshold: float = 0.5             # Per-metric pass/fail
    params: dict[str, Any] = {}        # Grader-specific parameters
    
    # User-customizable parts
    custom_criteria: str | None = None  # Override default assessment criteria
    custom_rubric: str | None = None    # Override default rubric
```

---

## 5. The 4×4 Eval Matrix — Applying Andrew Ng's Framework {#5-the-4x4-eval-matrix}

Andrew Ng's 2×2 (code vs LLM-judge × per-example vs universal ground truth) extended for EGDR with two additional axes: **eval level** (E2E vs component) and **eval timing** (offline vs online).

### The Extended Matrix for EGDR

```
                        ┌────────────────────────────────────────┐
                        │         GRADING METHOD                  │
                        ├──────────────────┬─────────────────────┤
                        │  Code-Based      │  LLM-as-Judge       │
          ┌─────────────┼──────────────────┼─────────────────────┤
          │ Per-Example  │ Citation URLs    │ Factual accuracy    │
 GROUND   │ Ground Truth │ match source     │ vs gold answer      │
 TRUTH    │              │ list             │                     │
 TYPE     ├──────────────┼──────────────────┼─────────────────────┤
          │ Universal    │ Report length    │ Coherence rubric    │
          │ Rule/Rubric  │ within bounds,   │ check, neutrality   │
          │              │ section count ≥3 │ 9-param audit       │
          └──────────────┴──────────────────┴─────────────────────┘
```

### EGDR-Specific 4×4 Eval Grid

| Component | Code-Based (w/ ground truth) | Code-Based (universal) | LLM Judge (w/ gold set) | LLM Judge (rubric) |
|-----------|:---:|:---:|:---:|:---:|
| **C2: Outline** | Expected sections ⊆ output | Section count ≥ 3, has objective | Plan quality vs gold plan | Coverage of research question |
| **C3: Research** | — | Tool call count ≤ max | — | Source relevance to brief |
| **C4: Web Search** | Gold URLs ∈ results (F1) | Result count ≥ 5 | — | Result quality assessment |
| **C10: Synthesis** | — | Has citations, < max length | Synthesis vs source content | Synthesis fidelity rubric |
| **C11: Section** | — | Word count in range | — | Quality rubric (structure, depth) |
| **C13: Full Report** | Gold topic coverage (F1) | Format, length, citation count | Factual accuracy vs gold | Completeness, coherence, relevance |
| **Neutrality** | — | — | — | 9-parameter neutrality audit ✅ |

---

## 6. Component Decomposition + Error Analysis Map {#6-component-decomposition}

### Applying Andrew Ng's Error Analysis to EGDR

When a report is bad, **where did it go wrong?** This is the error analysis spreadsheet template:

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│  ERROR ANALYSIS SPREADSHEET (from Andrew Ng Module 4, applied to EGDR)            │
│                                                                                    │
│  Instructions:                                                                     │
│  1. Collect 20-50 reports rated poorly by users or below eval thresholds           │
│  2. For each, examine the Langfuse trace (every span)                              │
│  3. Mark which component(s) failed                                                 │
│  4. Count up error rates → fix highest rate with actionable ideas                  │
│                                                                                    │
│  ┌─────────┬─────────┬──────────┬────────┬──────────┬───────────┬───────────────┐  │
│  │ Report  │ Outline │ Research │ Search │ Synthesis│ Section   │ Report        │  │
│  │ ID      │ Quality │ Agent    │ Results│ Fidelity │ Writing   │ Assembly      │  │
│  ├─────────┼─────────┼──────────┼────────┼──────────┼───────────┼───────────────┤  │
│  │ R-001   │         │ ❌ wrong │        │          │           │               │  │
│  │         │         │ tools    │        │          │           │               │  │
│  │ R-002   │ ❌ too  │          │ ❌ blog│          │ ❌ thin   │               │  │
│  │         │ narrow  │          │ posts  │          │ content   │               │  │
│  │ R-003   │         │          │        │ ❌ lost  │           │               │  │
│  │         │         │          │        │ nuance   │           │               │  │
│  │ ...     │         │          │        │          │           │               │  │
│  │ R-050   │         │          │ ❌ old │          │           │ ❌ duplicate  │  │
│  │         │         │          │ sources│          │           │ content       │  │
│  ├─────────┼─────────┼──────────┼────────┼──────────┼───────────┼───────────────┤  │
│  │ ERROR   │  12%    │  18%     │  40%   │  25%     │  15%      │  5%           │  │
│  │ RATE    │         │          │  🎯    │          │           │               │  │
│  └─────────┴─────────┴──────────┴────────┴──────────┴───────────┴───────────────┘  │
│                                                                                    │
│  → Fix search results first (40%), then synthesis (25%), then research agent (18%) │
│  → Remember: percentages are NOT mutually exclusive!                               │
│  → Check cascading: bad search → bad synthesis might not be synthesis's fault      │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### Component-Level Eval Design (per Andrew Ng lesson 04)

For each component identified as a bottleneck:

| Component | Isolated Eval | Gold Standard | Metric | Hyperparameters to Tune |
|-----------|---------------|---------------|--------|-------------------------|
| **Web Search (C4)** | Query → search results | Expert-curated URL lists per topic | F1 score (gold URLs ∈ results) | Search engine, result count, date range, query reformulation |
| **Research Agent (C3)** | Brief → tool selections + calls | Expert trace showing ideal tool sequence | Tool selection accuracy, call efficiency | Prompt, model, max iterations, available tools |
| **Synthesis (C10)** | Raw research → synthesis | Expert-written synthesis from same sources | Fidelity score (LLM judge), information loss check | Prompt, model, temperature, max tokens |
| **Section Writing (C11)** | Brief + research → section | Expert-written section from same inputs | Quality rubric (depth, structure, citations) | Prompt, model, writing style params |
| **Outline (C2)** | User query → outline | Expert outlines for same queries | Coverage score, structure match | Prompt, model, example outlines |

### Improvement Playbook (from Andrew Ng lesson 05)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  WHEN ERROR ANALYSIS POINTS TO A COMPONENT, FOLLOW THIS:                    │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Is it LLM-based or Non-LLM?                                        │   │
│  │                                                                      │   │
│  │  NON-LLM (search, tools, DB):          LLM (agents, evaluators):    │   │
│  │  1. Tune hyperparameters               1. Improve prompts            │   │
│  │  2. Replace provider                   2. Try different model        │   │
│  │     (e.g., switch search engine)       3. Split complex step into    │   │
│  │                                           2-3 simpler steps          │   │
│  │                                        4. Fine-tune (LAST resort)    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ALWAYS validate with END-TO-END eval after component fix!                  │
│  (Component improvement ≠ guaranteed system improvement)                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. User-Centric Eval System (The Product Vision) {#7-user-centric-evals}

This is the **cross-app evaluation product** from the conversation — where users become first-class participants in evaluation.

### Vision

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    USER-CENTRIC EVAL LAYERS                             │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 3: USER-DEFINED METRICS                                    │  │
│  │  Users create their own eval criteria aligned with what THEY care  │  │
│  │  about. E.g., "My reports must cover SAP S/4HANA migration topics" │  │
│  │  or "Financial accuracy must be above 90% for our CFO reports"     │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                  │                                      │
│  ┌───────────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 2: ORGANIZATION DEFAULTS                                   │  │
│  │  Org admins set baseline quality requirements for all reports.     │  │
│  │  E.g., "All reports must pass neutrality check, min 3 sources"    │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                  │                                      │
│  ┌───────────────────────────────▼───────────────────────────────────┐  │
│  │  LAYER 1: SYSTEM DEFAULTS (our internal quality bar)              │  │
│  │  Completeness, Structure, Relevance, Overall Quality, Neutrality  │  │
│  │  These ALWAYS run. Non-negotiable.                                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### User-Facing Eval Features

| Feature | What Users Can Do | How It Feeds Back to Us |
|---------|-------------------|------------------------|
| **Custom Metrics** | Define criteria in natural language: "Report must discuss competitive landscape with at least 3 named competitors" | Reveals what users actually care about → improves our prompts |
| **Threshold Tuning** | Set their own pass/fail thresholds per metric | Shows which metrics correlate with user satisfaction |
| **Eval Templates** | Choose from pre-built eval suites: "CFO Report", "Market Analysis", "Account Plan" | Reveals use case distribution → helps prioritize improvements |
| **On-Demand Eval** | Run evals on any past report, compare versions | Provides labeled data for our eval set |
| **Feedback + Rating** | Thumbs up/down, star ratings, free-text comments on sections | Directly populates our gold set + calibrates LLM judges |
| **Eval Dashboard** | See scores over time, compare across reports | User engagement = implicit quality signal |

### Data Flow: User Evals → System Improvement

```
┌──────────────┐     ┌────────────────┐     ┌──────────────────┐
│ User creates  │────▶│ Eval runs on   │────▶│ Results stored   │
│ custom eval   │     │ user's reports │     │ in Langfuse +    │
│ configuration │     │                │     │ Cassandra        │
└──────────────┘     └────────────────┘     └────────┬─────────┘
                                                      │
                                                      ▼
┌───────────────────────────────────────────────────────────────┐
│                    DUAL VALUE EXTRACTION                       │
│                                                               │
│  FOR THE USER:                  FOR US:                        │
│  • Score visibility             • Labeled preference data      │
│  • Quality assurance            • Custom criteria = what users │
│  • Prompt iteration               actually want                │
│    guidance                     • User ratings calibrate our   │
│  • Compliance evidence            LLM judges                   │
│                                 • High-rated reports → gold set│
│                                 • Low-rated reports → eval set │
│                                   regression cases             │
└───────────────────────────────────────────────────────────────┘
```

### API Design for User Evals

```python
# GraphQL Mutations (extending existing evaluation resolvers)

mutation CreateUserEvaluation {
    createEvaluation(input: {
        name: "CFO Financial Report Quality"
        description: "Metrics aligned with CFO expectations"
        target_type: "report"
        metrics: [
            {
                grader_name: "factual_accuracy"
                weight: 2.0   # Financial accuracy matters most
                threshold: 0.9
            },
            {
                grader_name: "geval_custom"
                weight: 1.5
                custom_criteria: "Report must include revenue projections with cited sources"
                threshold: 0.7
            },
            {
                grader_name: "completeness"
                weight: 1.0
                threshold: 0.6
            }
        ]
        pass_threshold: 0.75
        run_mode: "auto"  # Run on every report
    }) {
        id
        name
        status
    }
}

mutation RunEvaluationOnReport {
    runEvaluation(input: {
        evaluation_id: "user-eval-001"
        artifact_id: "report-xyz-123"
    }) {
        evaluation_run_id
        status
    }
}
```

---

## 8. Metric Catalog — Complete Reference {#8-metric-catalog}

### System Metrics (Layer 1 — Always Run)

| Metric | Type | Grading Method | Scale | Current Status |
|--------|------|---------------|-------|:---:|
| **Completeness** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Structure** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Relevance** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Research Depth** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Source Quality** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Analytical Rigor** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Practical Value** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Balance & Objectivity** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Writing Quality** | E2E Quality | LLM Judge | 1-5 | ✅ Exists |
| **Neutrality (9-param)** | Ethics | LLM Judge | Pass/Fail + Severity | ✅ Exists |
| **Groundedness** | E2E Quality | LLM Judge | Claim-level bool | ✅ Prompt exists |
| **Correctness** | E2E Quality | LLM Judge (needs gold) | 1-5 | ✅ Prompt exists |

### New Metrics to Build (Priority Order)

| Metric | Type | Grading Method | Why Needed | Priority |
|--------|------|---------------|------------|:---:|
| **Citation Validity** | Code | URL resolution check | Basic trust signal | 🔴 P0 |
| **Topic Coverage** | Code + LLM | Gold topics ∈ output | Completeness ground truth | 🔴 P0 |
| **Latency** | Code | Wall-clock measurement | User experience | 🔴 P0 |
| **Cost per Query** | Code | Token + tool cost sum | Unit economics | 🟡 P1 |
| **Source Diversity** | Code | Count unique domains | Against single-source bias | 🟡 P1 |
| **Synthesis Fidelity** | LLM | Compare synthesis to raw sources | Catch distortion | 🟡 P1 |
| **Outline-Report Alignment** | LLM | Outline sections → report sections | Catch drift | 🟡 P1 |
| **Tool Selection Accuracy** | LLM | Compare tool choices to expert | Research agent quality | 🟢 P2 |
| **Search Query Quality** | LLM | Compare generated queries to expert | Research input quality | 🟢 P2 |
| **User Satisfaction Proxy** | Composite | CSAT + implicit behavior signals | Ultimate validation | 🟢 P2 |

---

## 9. Grader Architecture {#9-grader-architecture}

### Code-Based Graders

```python
@GraderRegistry.register("citation_validity")
class CitationValidityGrader(BaseGrader):
    """Checks if cited URLs are valid and resolve."""
    grader_type = GraderType.CODE
    
    def grade(self, input: GraderInput) -> GradeResult:
        urls = extract_markdown_urls(input.actual_output)
        valid = sum(1 for url in urls if check_url_resolves(url))
        score = valid / len(urls) if urls else 1.0
        return GradeResult(
            metric_name="citation_validity",
            score=score,
            passed=score >= self.threshold,
            reasoning=f"{valid}/{len(urls)} citations resolve",
        )

@GraderRegistry.register("latency_check")
class LatencyGrader(BaseGrader):
    """Checks if pipeline completed within acceptable time."""
    grader_type = GraderType.CODE
    
    def grade(self, input: GraderInput) -> GradeResult:
        duration_ms = input.span_data.get("duration_ms", 0)
        max_ms = self.params.get("max_ms", 120_000)
        score = 1.0 if duration_ms <= max_ms else max(0, 1 - (duration_ms - max_ms) / max_ms)
        return GradeResult(
            metric_name="latency",
            score=score,
            raw_score=duration_ms,
            passed=duration_ms <= max_ms,
            reasoning=f"Completed in {duration_ms}ms (limit: {max_ms}ms)",
        )

@GraderRegistry.register("source_diversity")
class SourceDiversityGrader(BaseGrader):
    """Checks variety of citation domains."""
    grader_type = GraderType.CODE
    
    def grade(self, input: GraderInput) -> GradeResult:
        urls = extract_markdown_urls(input.actual_output)
        domains = set(urlparse(url).netloc for url in urls)
        min_domains = self.params.get("min_domains", 3)
        score = min(1.0, len(domains) / min_domains)
        return GradeResult(
            metric_name="source_diversity",
            score=score,
            raw_score=len(domains),
            passed=len(domains) >= min_domains,
            reasoning=f"{len(domains)} unique domains from {len(urls)} citations",
        )
```

### LLM-as-Judge Graders

```python
@GraderRegistry.register("factual_accuracy")
class FactualAccuracyGrader(BaseGrader):
    """LLM evaluates factual claims against gold reference."""
    grader_type = GraderType.LLM_JUDGE
    
    RUBRIC = """
    Score the factual accuracy of the report against the reference answer.
    
    5 = All major facts correct, no contradictions with reference
    4 = Most facts correct, minor discrepancies
    3 = Core facts correct, some notable errors
    2 = Several factual errors that could mislead reader
    1 = Major factual errors, fundamentally unreliable
    
    Output JSON: {"score": <1-5>, "reasoning": "...", "incorrect_claims": [...]}
    """
    
    def grade(self, input: GraderInput) -> GradeResult:
        prompt = self.RUBRIC.format(
            report=input.actual_output,
            reference=input.expected_output,
            query=input.input_query,
        )
        result = self.judge_model.invoke(prompt)
        parsed = parse_structured_output(result)
        normalized = parsed["score"] / 5.0
        return GradeResult(
            metric_name="factual_accuracy",
            score=normalized,
            raw_score=parsed["score"],
            passed=normalized >= self.threshold,
            reasoning=parsed["reasoning"],
            evidence=parsed.get("incorrect_claims", []),
        )

@GraderRegistry.register("geval_custom")
class GEvalCustomGrader(BaseGrader):
    """DeepEval-compatible GEval with user-customizable criteria."""
    grader_type = GraderType.LLM_JUDGE
    
    def grade(self, input: GraderInput) -> GradeResult:
        criteria = self.params.get("custom_criteria", self.default_criteria)
        # Can use DeepEval's GEval when available, or fall back to direct LLM judge
        ...
```

### Composite Grader (Weighted Ensemble)

```python
@GraderRegistry.register("report_quality_composite")
class ReportQualityComposite(BaseGrader):
    """Weighted combination of multiple graders = single quality score."""
    grader_type = GraderType.COMPOSITE
    
    DEFAULT_WEIGHTS = {
        "completeness": 0.20,
        "factual_accuracy": 0.25,
        "source_quality": 0.15,
        "coherence": 0.10,
        "relevance": 0.15,
        "neutrality": 0.15,
    }
    
    def grade(self, input: GraderInput) -> GradeResult:
        results = {}
        for metric_name, weight in self.weights.items():
            grader = GraderRegistry.get(metric_name)()
            results[metric_name] = grader.grade(input)
        
        weighted_score = sum(
            results[m].score * w for m, w in self.weights.items()
        ) / sum(self.weights.values())
        
        return GradeResult(
            metric_name="report_quality_composite",
            score=weighted_score,
            passed=weighted_score >= self.threshold,
            reasoning=self._build_composite_reasoning(results),
            metadata={"component_scores": {m: r.score for m, r in results.items()}},
        )
```

---

## 10. Eval Set Management {#10-eval-set-management}

### Structure

```
eval_sets/
├── v1.0/
│   ├── manifest.json            # Version metadata, creation date, case count
│   ├── cases/
│   │   ├── case_001.json        # Real production query + gold answer
│   │   ├── case_002.json
│   │   └── ...
│   ├── gold_set/
│   │   ├── gold_001.json        # Expert-verified reference answers
│   │   └── ...
│   ├── rubrics/
│   │   ├── factual_accuracy.md  # Grading rubric for human calibration
│   │   ├── coherence.md
│   │   └── ...
│   └── baselines/
│       ├── baseline_2026-04-17.json  # Recorded baseline scores
│       └── ...
├── v1.1/
│   └── ... (with added cases from production feedback)
└── archive/
    └── retired_cases/           # Consistently passing cases moved here
```

### Eval Case Schema

```json
{
    "case_id": "case_001",
    "source": "production",
    "added_date": "2026-04-15",
    "added_reason": "user_negative_feedback",
    
    "input": {
        "user_query": "Analyze SAP's competitive position in the ERP market for enterprise customers",
        "context": { "org_id": "demo", "user_role": "account_executive" }
    },
    
    "gold_standard": {
        "expected_topics": ["market share", "S/4HANA", "Oracle", "Microsoft", "Workday", "cloud migration"],
        "expected_sources_minimum": 5,
        "reference_answer": "...(expert-written reference)...",
        "expert_outline": ["Executive Summary", "Market Overview", "Competitive Analysis", "..."],
        "verified_by": "brad.powley",
        "confidence": "high"
    },
    
    "component_gold": {
        "ideal_search_queries": ["SAP ERP market share 2025", "S/4HANA vs Oracle Cloud"],
        "ideal_source_urls": ["gartner.com/...", "sap.com/...", "oracle.com/..."],
        "ideal_outline_sections": 7
    },
    
    "tags": ["competitive_analysis", "erp", "enterprise"],
    "difficulty": "medium"
}
```

### Freshness Process (from white paper §6)

| Action | Cadence | Source |
|--------|---------|--------|
| **Add from production** | Monthly | Low-CSAT queries, user re-prompts, abandoned outputs |
| **Retire stale cases** | Quarterly | Cases passing with >0.9 for 3+ releases → archive |
| **Add from incidents** | On incident | Every user-reported failure → regression test case |
| **Re-baseline** | On major eval set change | Re-run all metrics, record new baseline |
| **Version tag** | On every change | Semantic versioning for traceability |

---

## 11. Langfuse + DeepEval Integration Architecture {#11-langfuse-deepeval}

### How Everything Connects

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RUNTIME (Every Report Generation)                     │
│                                                                         │
│  EGDR Pipeline ──── Langfuse Callbacks ──── Traces + Spans              │
│       │                                          │                      │
│       ▼                                          ▼                      │
│  Report Generated                        Langfuse Dashboard             │
│       │                                  (cost, latency, trace tree)    │
│       │                                                                 │
│       ├──▶ Online Eval (evaluation_workflow.py)                         │
│       │    • Completeness, Structure, Relevance, Overall Quality        │
│       │    • Results → Langfuse Scores (write_trace_scores)             │
│       │    • Results → Cassandra (evaluation_run_entity_handler)        │
│       │                                                                 │
│       ├──▶ User Feedback                                                │
│       │    • Thumbs up/down → Langfuse Score (chat_feedback_resolvers)  │
│       │    • Free text → eval set candidate                             │
│       │                                                                 │
│       └──▶ User-Defined Evals (NEW)                                     │
│            • Run user's custom metrics on report                        │
│            • Results → Langfuse Scores + User Dashboard                 │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                    OFFLINE (CI/CD + Manual)                              │
│                                                                         │
│  Eval Set ──── Offline Eval Runner ──── Results                         │
│       │              │                     │                            │
│       │        ┌─────┴──────┐              ▼                            │
│       │        │ Code       │    Compare vs Baseline                    │
│       │        │ Graders    │         │                                 │
│       │        │ (CI gate)  │    Ship / No-Ship                         │
│       │        └────────────┘                                           │
│       │        ┌────────────┐                                           │
│       │        │ LLM Judges │    (DeepEval GEval                        │
│       │        │ (release   │     OR direct Langfuse judge              │
│       │        │  candidate)│     — depends on dep resolution)          │
│       │        └────────────┘                                           │
│       │        ┌────────────┐                                           │
│       │        │ Human      │    Calibration sample                     │
│       │        │ Review     │    (periodic)                             │
│       │        └────────────┘                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### DeepEval Resolution Strategy

Current blocker: `deepeval` conflicts with `sap-ai-sdk-core` on `click` version.

| Option | Approach | Pros | Cons | Recommendation |
|--------|----------|------|------|:---:|
| **A. Separate eval venv** | Install deepeval in isolated env, run offline evals as standalone process | Clean separation, no dep conflicts | Extra process management | ✅ **Best for offline** |
| **B. Direct LLM-judge** | Replace DeepEval GEval with custom Langfuse-native LLM-as-judge | Zero new deps, uses existing infra | Need to re-implement rubric logic | ✅ **Best for online** |
| **C. Wait for fix** | Monitor deepeval for click>=8.3 support | No work needed | Blocks progress indefinitely | ❌ Don't wait |

**Recommendation: Hybrid A+B**
- Online evals (in server process): Use direct LLM-as-judge via existing evaluation_workflow.py (already working!)
- Offline evals (CI/release): Use DeepEval in isolated venv for full GEval metrics with rubrics

---

## 12. Continuous Improvement Loop {#12-continuous-improvement}

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CONTINUOUS IMPROVEMENT FLYWHEEL                        │
│                                                                          │
│    ┌─────────────┐                                                       │
│    │ PRODUCTION   │                                                       │
│    │ • Reports    │                                                       │
│    │ • Langfuse   │──────────┐                                           │
│    │   traces     │          │                                           │
│    │ • User       │          ▼                                           │
│    │   feedback   │   ┌──────────────┐                                   │
│    └─────────────┘   │  SIGNAL       │                                   │
│                       │  COLLECTION   │                                   │
│                       │              │                                   │
│                       │ • Low CSAT   │                                   │
│                       │ • Re-prompts │──────────┐                        │
│    ┌─────────────┐   │ • Abandoned  │          │                        │
│    │ SHIP        │   │ • User evals │          ▼                        │
│    │ • Deploy    │   └──────────────┘   ┌──────────────┐                │
│    │ • Monitor   │                       │  EVAL SET    │                │
│    │ • Repeat    │◀──────────┐          │  MAINTENANCE  │                │
│    └─────────────┘          │          │              │                │
│                              │          │ • Add failing│                │
│    ┌─────────────┐          │          │   cases      │                │
│    │ VALIDATE    │          │          │ • Retire     │──┐              │
│    │             │          │          │   stale cases│  │              │
│    │ • E2E eval  │          │          │ • Version    │  │              │
│    │ • Meets     │──────────┘          └──────────────┘  │              │
│    │   threshold?│                                        │              │
│    └──────▲──────┘                                        │              │
│           │                                               ▼              │
│    ┌──────┴──────┐                               ┌──────────────┐       │
│    │  TUNE       │                               │  ERROR        │       │
│    │             │◀──────────────────────────────│  ANALYSIS     │       │
│    │ • Prompts   │                               │              │       │
│    │ • Models    │                               │ • Traces     │       │
│    │ • Topology  │                               │ • Spreadsheet│       │
│    │ • Params    │                               │ • Prioritize │       │
│    └─────────────┘                               └──────────────┘       │
└──────────────────────────────────────────────────────────────────────────┘
```

### Andrew Ng's Build ↔ Analyze Cycle Applied

| Phase | Build Activity | Analyze Activity |
|:-----:|---------------|-----------------|
| **Now** | Fix DeepEval dep, build code graders | Manually review 20 traces from Langfuse |
| **Week 2-3** | Build offline eval runner, first 20 eval cases | Run error analysis on those 20 cases, build spreadsheet |
| **Week 4-5** | Fix top bottleneck component | Component-level evals for that component |
| **Week 6-8** | Build user-facing eval config API | Collect user-defined metrics, calibrate LLM judges |
| **Ongoing** | Iterate on prompts, models, topology | E2E + component evals, error analysis on new failures |

---

## 13. Roadmap & Prioritization {#13-roadmap}

### Phase 1: Foundation (Weeks 1-2) — 🔴 DO NOW

| Task | Owner | Dependencies | Deliverable |
|------|-------|-------------|-------------|
| Resolve DeepEval dep conflict (isolated venv for offline) | Dev | None | Working `eval/` environment |
| Build 3 code-based graders (citation, latency, source diversity) | Dev | None | Graders in CI pipeline |
| Pull 20 real queries from Langfuse → first eval cases | Dev + Brad | Langfuse access | `eval_sets/v0.1/` |
| Run existing evaluation_workflow on those 20 cases | Dev | eval cases | First baseline numbers |

### Phase 2: Error Analysis + Component Evals (Weeks 3-4)

| Task | Owner | Dependencies | Deliverable |
|------|-------|-------------|-------------|
| Error analysis on 20 failing reports (spreadsheet) | Dev | Langfuse traces | Error rate per component |
| Component eval for #1 bottleneck (likely web search) | Dev | Error analysis | F1 metric + gold URLs |
| Fix #1 bottleneck, validate with E2E eval | Dev | Component eval | Measurable improvement |
| Expand eval set to 50 cases | Dev + QA | Production data | `eval_sets/v0.2/` |

### Phase 3: User-Centric Evals (Weeks 5-8)

| Task | Owner | Dependencies | Deliverable |
|------|-------|-------------|-------------|
| Design EvalConfiguration GraphQL API | Dev | Phase 2 | API spec |
| Implement GraderRegistry + BaseGrader pattern | Dev | Phase 2 | Extensible framework |
| Build user eval creation UI | Frontend | API | Users can create evals |
| Implement `geval_custom` grader (user criteria) | Dev | GraderRegistry | User-defined LLM judge |
| Deploy user feedback → eval set pipeline | Dev | UI + backend | Automated eval set growth |

### Phase 4: Production Maturity (Weeks 8-12)

| Task | Owner | Dependencies | Deliverable |
|------|-------|-------------|-------------|
| Define ship/no-ship thresholds (calibrate vs CSAT) | Dev + PM | Baseline + user data | Release gate criteria |
| CI integration (code graders gate every build) | DevOps | Phase 1 graders | Automated quality gate |
| Eval dashboard in Langfuse (scores over time) | Dev | All scores flowing | Team visibility |
| Human calibration protocol (monthly) | QA | LLM judges running | Judge accuracy tracking |

---

## Summary: What Makes This Design Special

| Aspect | How We Applied Learning |
|--------|------------------------|
| **Andrew Ng's 2×2 Grid** | Extended to 4×4 with eval level + timing axes, mapped every EGDR component |
| **Error Analysis (Module 4)** | Full spreadsheet template mapped to EGDR pipeline, with cascading-error awareness |
| **Component-Level Evals** | Isolated eval design for each agent/tool with gold standards + F1 metrics |
| **Improvement Playbook** | LLM vs non-LLM fix strategies mapped to each EGDR component |
| **Latency/Cost Prioritization** | Quality first, then latency, then cost — with per-step benchmarking |
| **Build ↔ Analyze Cycle** | Explicit roadmap alternating build + analyze phases |
| **White Paper Alignment** | Every roadmap milestone maps to Brad's 8-milestone plan |
| **User-Centric Vision** | 3-layer eval ownership (system → org → user) with bi-directional value |
| **Existing Infra Leverage** | Builds on what's already working (Langfuse, evaluation_workflow, registry pattern) |
| **Extensibility** | GraderRegistry + BaseGrader pattern = new metrics are just a decorated class |

> 💡 **Eval banana = product banana. Jab user khud eval bana sakta hai, toh usne bataya ki usse kya chahiye — aur humein free mein labeled data mil gaya. Win-win! 🏆**

---

*This document is a living artifact. Version it, iterate on it, and treat it with the same rigor as the code it evaluates.*

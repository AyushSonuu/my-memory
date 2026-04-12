# White Paper Summary — Brad Powley's Eval Framework

> **Source:** `experience-generation-docs/research/white-papers/eval-framework.md`
> **Author:** Brad Powley
> **Distilled:** 2026-04-12

## Core Thesis

EGDR compresses days of analyst work into minutes using multi-agent architecture (planning → research → synthesis). But errors compound across steps — a fluent report can be substantively wrong. Evaluation closes the gap between *appears capable* and *actually delivers*.

## Three Dimensions of Evaluation

### 1. End-to-End Quality (Black Box)
- **Factual accuracy** — % of claims that are correct vs gold set
- **Source quality** — % of cited sources that are relevant + authoritative
- **Coverage** — degree output addresses all aspects of the question
- **Coherence** — logical structure, internal consistency
- **Groundedness** — % of claims supported by cited sources (not hallucinated)
- **Conciseness** — appropriately scoped, no repetition/filler

### 2. Intermediate Step Correctness (Where did it break?)
- **Orchestration quality** — did orchestrator decompose task well?
- **Plan completeness** — does research plan cover right sub-questions?
- **Source relevance** — per-source score for relevance to sub-question
- **Source diversity** — number of distinct, non-redundant sources
- **Synthesis fidelity** — does synthesis faithfully represent sources?

### 3. Efficiency (Cost of producing the result)
- **Latency** — wall-clock seconds from query to output
- **Token consumption** — total input/output/cache tokens across all LLM calls
- **Tool call count** — number of external tool invocations
- **Cost per query** — estimated dollar cost (LLM + tools + compute)

## Three Grading Methods (Layered)

| Method | Use For | Scale | Role |
|--------|---------|-------|------|
| **Code-based** | Citation URLs, topic coverage, latency | Every build (CI) | Automated gates |
| **LLM-as-judge** | Accuracy, coherence, groundedness, fidelity | Release candidates | Quality scoring |
| **Human** | Gold set creation, LLM judge calibration, edge cases | Periodic sampling | Ground truth |

## Two Evaluation Modes

| Mode | When | Purpose |
|------|------|---------|
| **Offline** | Before release, against eval set | Gate product decisions, apples-to-apples comparison |
| **Online** | In production, on live traffic | Monitor real-world performance, validate offline metrics |

## Key Concepts

- **Eval set** — maintained collection of test cases (queries + reference answers + rubrics)
- **Gold set** — high-confidence subset verified by human experts
- **Baseline** — recorded scores representing current system performance
- **Ship/no-ship thresholds** — minimum acceptable scores per metric dimension

## Continuous Improvement

### User Feedback
- **Direct:** thumbs up/down, surveys, free-text comments
- **Implicit:** acceptance, revision requests, re-prompting (strong negative signal), section copying, abandonment

### Eval Set Freshness
- Rotate cases from production (monthly, weighted toward low-CSAT)
- Retire stale cases (consistently passing → archive)
- Add from incidents (every failure → regression test)
- Version the eval set (tag each version for traceability)

### Tuning Levers
1. **Prompt engineering** — fastest, lowest risk
2. **Model selection** — swap LLM for specific agent
3. **Temperature/sampling** — tune for reliability (pass^k > pass@k)
4. **Agent topology** — restructure how agents connect
5. **Supervised fine-tuning (SFT)** — last resort, highest effort

## 8-Milestone Roadmap

| # | Milestone | Target Date | Status |
|---|-----------|-------------|:------:|
| 1 | Instrument observability (Langfuse) | Feb 28 | ✅ DONE |
| 2 | Code-based grading pipeline | Mar 13 | ❌ |
| 3 | LLM-as-judge grading pipeline | Mar 20 | ⚠️ Code exists, dep blocked |
| 4 | Begin tuning cycle | Mar 23 | ❌ |
| 5 | Build offline eval set (50-100 cases) | Mar 31 | ❌ |
| 6 | Deploy user feedback collection | Mar 31 | 🟡 Backend exists |
| 7 | Establish baseline metrics | Apr 17 | ❌ |
| 8 | Define ship/no-ship thresholds | May 8 | ❌ |

## Benchmarks Considered

| Benchmark | Tests | Limitation for EGDR |
|-----------|-------|---------------------|
| **GAIA** | General AI assistant tasks | Only final-answer correctness, no process eval |
| **Humanity's Last Exam** | Expert-level academic Q&A | ~30% bio/chem answers may be wrong |
| **MultiAgentBench** | Multi-agent collaboration | Not tuned to research tasks |
| **LMArena** | Head-to-head model comparison | Win/loss format, not reproducible |

**Conclusion:** Rely primarily on internal eval set built from real production queries.

## Risks Acknowledged
- Eval set representativeness (can drift from reality)
- LLM judge reliability (non-deterministic, biases)
- Adversarial inputs (not covered, needs separate red-teaming)
- Subjective quality dimensions (insight, actionability — hard to metric-ize)
- Cost of evaluation itself

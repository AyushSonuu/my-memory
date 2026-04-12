# EGDR Evals — Current Status

> **Last Updated:** 2026-04-12
> **Phase:** Design Complete → Ready for Implementation

## ✅ Done

- [x] Read and analyzed Brad's white paper (`eval-framework.md`)
- [x] Deep codebase audit — all 16 evaluable components catalogued
- [x] Mapped existing eval infrastructure (Langfuse ✅, DeepEval ⚠️ blocked, evaluation_workflow ✅)
- [x] Read all Module 4 notes (evals, error analysis, component evals, improvement playbook)
- [x] Web research (Anthropic eval guide, DeepEval docs, Langfuse eval overview)
- [x] Full HLD + LLD design document written
- [x] 4×4 eval matrix designed (extending Andrew Ng's 2×2)
- [x] Error analysis spreadsheet template for EGDR pipeline
- [x] User-centric eval product vision (3-layer ownership model)
- [x] Grader architecture (BaseGrader → GraderRegistry pattern)
- [x] Roadmap with 4 phases mapped to Brad's 8 milestones
- [x] Working folder created for persistent context

## 🔴 Blockers

| Blocker | Impact | Resolution |
|---------|--------|------------|
| DeepEval `click` conflict with `sap-ai-sdk-core` | Can't run DeepEval GEval in server process | **Hybrid A+B**: isolated venv for offline + direct LLM-judge for online |

## 🟡 Next Actions (Priority Order)

### This Week (Phase 1: Foundation)
1. [ ] Set up isolated eval venv for DeepEval (Option A)
2. [ ] Build 3 code-based graders: citation validity, latency check, source diversity
3. [ ] Pull 20 real queries from Langfuse production traces → first eval cases
4. [ ] Run existing `evaluation_workflow` on those 20 cases → record baseline

### Next 2 Weeks (Phase 2: Error Analysis)
5. [ ] Error analysis on 20 failing reports (the Andrew Ng spreadsheet method)
6. [ ] Build component-level eval for #1 bottleneck
7. [ ] Fix #1 bottleneck, validate with E2E eval
8. [ ] Expand eval set to 50 cases

### Weeks 5-8 (Phase 3: User-Centric)
9. [ ] Design EvalConfiguration GraphQL API
10. [ ] Implement GraderRegistry + BaseGrader pattern
11. [ ] Build user eval creation UI
12. [ ] Deploy user feedback → eval set pipeline

## 📊 Key Metrics to Track

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Eval set size | 0 | 50+ | 🔴 |
| Code-based graders in CI | 0 | 3+ | 🔴 |
| LLM-judge metrics running | 8 (online) | 12+ (online + offline) | 🟡 |
| Baseline established | No | Yes | 🔴 |
| Ship/no-ship thresholds | None | Defined + calibrated | 🔴 |
| User-facing eval API | No | Yes | 🔴 |

## 🧠 Key Decisions Made

1. **Hybrid DeepEval strategy** — isolated venv for offline, direct LLM-judge for online
2. **Extensible grader pattern** — BaseGrader → GraderRegistry (mirrors existing evaluation_registry.py)
3. **3-layer eval ownership** — System (always run) → Org defaults → User-defined
4. **Error analysis first** — before building new infra, do the spreadsheet on 20 traces
5. **Quality → Latency → Cost** — optimization priority order (Andrew Ng)

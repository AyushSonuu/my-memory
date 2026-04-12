# Architecture Decision Records (ADRs)

## ADR-001: Hybrid DeepEval Strategy

**Date:** 2026-04-12
**Status:** Proposed
**Context:** DeepEval `^2.9.4` has a `click` package conflict with `sap-ai-sdk-core`. Code for DeepEval integration exists (`evaluations/metrics.py`, `evaluations/report_evaluator.py`, `evaluations/evaluation_model.py`) but can't be installed.

**Decision:** Use a hybrid approach:
- **Online evals (server process):** Direct LLM-as-judge via existing `evaluation_workflow.py` — no DeepEval dependency needed
- **Offline evals (CI/release):** Install DeepEval in isolated venv, run as standalone process

**Rationale:**
- Online evals already work without DeepEval (7 evaluator agents operational)
- Offline evals benefit from DeepEval's GEval rubric engine + test runner
- Isolated venv avoids dependency conflicts entirely
- Brad's white paper explicitly says offline eval runs outside production

**Alternatives Considered:**
- Wait for DeepEval to support `click >=8.3` — blocks progress indefinitely
- Force-install with `--no-deps` — brittle, hard to maintain
- Replace DeepEval entirely with custom LLM-judge — loses DeepEval's rubric framework

---

## ADR-002: GraderRegistry Extensibility Pattern

**Date:** 2026-04-12
**Status:** Proposed
**Context:** Need to support code-based graders, LLM judges, DeepEval metrics, human grading, and user-defined custom metrics — all through a single interface.

**Decision:** Implement `BaseGrader` abstract class + `GraderRegistry` singleton with decorator-based registration, mirroring the existing `EVALUATION_DEFINITIONS_REGISTRY` pattern.

**Rationale:**
- Existing codebase uses registry pattern for evaluations (`evaluation_registry.py`) and agents (`@agent(id=...)`)
- Decorator registration is familiar to the team
- Universal `GradeResult` output enables uniform score storage
- `GraderInput` standardizes what graders receive
- New graders = one decorated class, auto-discovered

---

## ADR-003: Three-Layer Eval Ownership

**Date:** 2026-04-12
**Status:** Proposed
**Context:** Team discussion identified user-centric evals as a potential cross-app product. Users want to define their own quality criteria.

**Decision:** Three ownership layers:
1. **System (Layer 1):** Our internal quality metrics (completeness, structure, relevance, quality, neutrality) — ALWAYS run, non-negotiable
2. **Organization (Layer 2):** Org admins set baseline requirements for all users — e.g., "min 3 sources"
3. **User (Layer 3):** Individual users create custom metrics aligned with their specific needs

**Rationale:**
- System metrics protect our quality bar regardless of user preferences
- Org defaults handle compliance/industry requirements
- User metrics capture what individuals actually care about (which we learn from!)
- User-created evals provide free labeled preference data for improving our system
- Mirrors SaaS tenant hierarchy (platform → org → user)

---

## ADR-004: Error Analysis Before Building

**Date:** 2026-04-12
**Status:** Accepted
**Context:** Multiple new components could be built (code graders, offline runner, user API). Need to decide what to work on first.

**Decision:** Before building new eval infrastructure, do Andrew Ng's error analysis exercise:
1. Pull 20 failing reports from Langfuse
2. Read traces span by span
3. Build error analysis spreadsheet (component × failure)
4. Count error rates
5. Fix highest-rate component with actionable ideas

**Rationale:**
- Andrew Ng: "Gut feeling leads to months of work with very little progress"
- Error analysis tells us WHERE to invest — building without it risks solving the wrong problem
- 20 examples is enough to reveal patterns
- We already have full Langfuse traces to analyze
- This is the highest-ROI first step

---

## ADR-005: Quality → Latency → Cost Priority

**Date:** 2026-04-12
**Status:** Accepted
**Context:** Multiple optimization dimensions compete for attention.

**Decision:** Strictly prioritize: output quality first, latency second, cost third.

**Rationale:**
- Andrew Ng's explicit recommendation from Module 4
- A fast, cheap system that produces garbage is worthless
- Cost optimization is "a good problem to have" (means users exist)
- Latency affects UX directly; cost affects unit economics at scale
- Both are only worth optimizing AFTER quality is reliably good

# 🛠️ Module 4 — Practical Tips for Building Agentic AI

> Building is easy, making it work reliably is the real game — evals, error analysis, and optimization.

---

## 📊 Progress

| # | Lesson | Confidence | Revised |
|---|--------|-----------|---------|
| 01 | [Evaluations (Evals)](01-evaluations.md) | 🟡 | 2026-03-31 |
| 02 | [Error Analysis & Prioritizing](02-error-analysis.md) | 🟡 | 2026-03-31 |
| 03 | [More Error Analysis Examples](03-more-error-analysis.md) | 🟡 | 2026-03-31 |
| 04 | [Component-Level Evals](04-component-level-evals.md) | 🟡 | 2026-03-31 |
| 05 | [How to Address Problems](05-addressing-problems.md) | 🟡 | 2026-03-31 |
| 06 | [Latency & Cost Optimization](06-latency-cost.md) | 🟡 | 2026-03-31 |
| 07 | [Development Process Summary](07-dev-process-summary.md) | 🟡 | 2026-03-31 |

---

## 📚 Sources
> - 🎓 [Agentic AI](https://learn.deeplearning.ai/courses/agentic-ai) — Module 4

## 30-Second Recall 🧠
> Build quick → look at outputs → spot failures → build evals (2×2: code/LLM-judge × per-example/no ground truth) → error analysis spreadsheet (count errors per component, don't go by gut!) → fix the worst offender (non-LLM: tune/replace; LLM: prompt→model→split→fine-tune) → component-level evals for fast feedback → confirm with end-to-end eval → THEN optimize latency (parallelism, smaller models) and cost (benchmark each step). The whole thing is a Build ↔ Analyze cycle — analysis is equally important as coding.

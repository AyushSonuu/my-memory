# 🪞 Module 2 — Reflection Design Pattern

> AI that critiques its own work, finds flaws, and iterates — like a developer doing code review on their own PR.

---

## 📊 Progress

| # | Lesson | Confidence | Revised |
|---|--------|-----------|---------|
| 01 | [Reflection to Improve Outputs](01-reflection-to-improve-outputs.md) | 🟡 | — |
| 02 | [Why Not Just Direct Generation?](02-why-not-direct-generation.md) | 🟡 | — |
| 03 | [Chart Generation Workflow](03-chart-generation-workflow.md) | 🟡 | — |
| 04 | [Evaluating Impact of Reflection](04-evaluating-reflection.md) | 🟡 | — |
| 05 | [Reflection with External Feedback](05-external-feedback.md) | 🟡 | — |

---

## 🧠 Memory Fragments

- 💡 Reflection = simplest agentic pattern. Generate → critique → improve.
- 🪞 Different LLMs for generation vs reflection = powerful combo (fast model + reasoning model)
- 📊 Multimodal reflection = critic LLM **sees the image**, not just reads the code
- 📏 Evals: Objective (code-based, ground truth) vs Subjective (LLM-as-Judge + binary rubric)
- ❌ Never use LLM pair comparison — position bias kills reliability
- 🔦 External feedback (code errors, web search, regex, word count) breaks the performance plateau
- 📈 **3 tiers of power:** Direct generation < Reflection < Reflection + External Feedback

---

## 📚 Sources
> - 🎓 [Agentic AI](https://learn.deeplearning.ai/courses/agentic-ai) — Module 2
> - 📄 Self-Refine paper (Madaan et al., 2023) — reflection beats direct generation across 7 tasks

## 30-Second Recall 🧠
> Reflection is the simplest agentic pattern: generate v1 → critique → produce v2. Use **different models** for generation vs critique. For charts/images, use **multimodal reflection** — the critic sees the actual image. Always **eval** the impact: objective tasks get code-based ground truth checks, subjective tasks get **binary rubric scoring** (NOT pair comparison — position bias!). The real power-up is **external feedback** — code execution errors, web search results, regex pattern matching, word counts. These give the LLM genuinely new information it couldn't have known, breaking the performance plateau that direct prompting hits.

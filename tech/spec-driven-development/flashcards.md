# 🃏 Spec-Driven Development — Flashcards

> Revision deck for SDD. Pull from all lessons + related topics.

---

## Lesson 01 — Introduction

**Q: What is Spec-Driven Development in one sentence?**
A: Write a markdown spec defining what to build → feed it to a coding agent → it implements that spec. You focus on context, not code.

---

**Q: Name the 3 main benefits of SDD.**
A: 1) **Downstream Amplification** — small spec changes → large code changes. 2) **Context Preservation** — specs survive across stateless agent sessions. 3) **Intent Fidelity** — you define the problem, agent elaborates a plan aligned to your vision.

---

**Q: What is "downstream amplification" in SDD?**
A: One sentence in a spec (e.g., "use SQLite with Prisma ORM") can affect hundreds of lines of code. Change that sentence to "use MongoDB" → same cascading effect. Writing specs is far more efficient than writing code.

---

**Q: Why do agents suffer from "context decay"?**
A: Agents are **stateless** — each new session starts from zero. Without a spec loaded at boot, the agent loses all non-negotiable project decisions from prior sessions.

---

**Q: What is a "constitution" in SDD?**
A: A project-level document defining **immutable standards** — tech stack, architecture, conventions. It's developed through conversation with an agent (greenfield) or generated from existing code (brownfield).

---

**Q: What's the SDD workflow at a high level?**
A: Constitution (project-level immutables) → iterate **feature development loops** (plan → implement → verify on own branch) → clean slate between features.

---

**Q: Greenfield vs Brownfield in SDD — what's the difference?**
A: **Greenfield** = from scratch, develop constitution by conversing with agent. **Brownfield** = existing codebase, generate constitution from existing code. Both then follow the same feature loop workflow.

---

**Q: What happens when teams use coding agents WITHOUT a spec?**
A: Different agents under different developers build quickly but in **contradictory ways** → unmaintainable code, weird products, downstream headaches.

---

**Q: What's the ROI argument for writing specs?**
A: Agent may code for 20–30 min (= hours of dev work). Spending 3–4 min writing clear instructions upfront is a massive time multiplier — and prevents random/contradictory output.

---

**Q: How do you actually write a spec? (4 steps)**
A: 1) Converse with an agent (Claude Code, Gemini, Codex). 2) Make key architectural choices using YOUR knowledge of trade-offs. 3) Agent summarizes decisions into markdown. 4) That markdown = your spec/constitution.

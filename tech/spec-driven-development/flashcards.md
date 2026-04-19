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

---

## Lesson 02 — Why Spec-Driven Development?

**Q: What's the core difference between vibe coding and SDD?**
A: Vibe coding = vague prompt → hope → fix → repeat (produces disposable code + tech debt). SDD = detailed spec (what + why) → agent implements (how) → validate (produces engineered, maintainable code). SDD **decouples specification from implementation**.

---

**Q: Why doesn't vibe coding scale to large projects?**
A: Three reasons: 1) Long dialogue history that **isn't even saved**. 2) Produces disposable code with mounting tech debt. 3) No contract between humans or with the agent — decisions are ad-hoc and lost.

---

**Q: What is the "paradigm shift" in SDD?**
A: Specification (what + why) is **decoupled** from Implementation (how). Your job shifts from writing code to **converting intentions into clear specifications**.

---

**Q: How does context decay affect coding agents?**
A: As you work with an agent, its **context window fills up** → more mistakes as it copes with full working memory. Specs persist between sessions AND agents, anchoring to core context.

---

**Q: What is the Compiler Analogy for SDD?**
A: Compilers convert source code → machine code. SDD agents convert **specs → source code**. Both abstract away lower-level details. Bonus: specs are in human language, accessible to anyone (PMs, stakeholders, not just devs).

---

**Q: How are specs different from prompts?**
A: Prompts die with the chat session, are freeform, and serve one interaction. Specs are **permanent technical artifacts** — structured, project/feature-scoped, reusable across sessions AND agents, and readable by both humans and agents.

---

## Lesson 03 — Workflow Overview

**Q: What are the 3 pillars of an SDD Constitution?**
A: 1) **Mission** — vision, target audience, scope (the "why"). 2) **Tech Stack** — development & deployment technologies and constraints. 3) **Roadmap** — living document with sequence of phases, each with its own feature spec.

---

**Q: How is a Constitution different from agents.md?**
A: `agents.md` = agent-specific instructions for one tool. Constitution = **agent-agnostic**, more structured, captures project-level decisions agreed upon by both humans and agents (and between humans too).

---

**Q: What are the 4 phases of the SDD workflow cycle?**
A: 1) **Plan** — write feature spec. 2) **Implement** — agent codes from spec. 3) **Validate** — review & accept/reject. 4) **Replan** — revise constitution, update roadmap, improve the process itself. Then repeat for next feature.

---

**Q: What's the "right level of detail" rule in SDD?**
A: Treat the agent as a **highly capable pair programmer**. Provide LOTS of context about goals, mission, audience, constraints. Provide LESS about low-level implementation decisions the agent can figure out on its own.

---

**Q: What is the Architect Analogy in SDD?**
A: You = architect (design, supervise, review/accept). Agent = builder (constructs from your drawings). Focus on providing **context the builder doesn't know** — don't tell them how to do their job.

---

**Q: What happens during the Replanning phase?**
A: Three things get revised: 1) **Constitution** — update based on learnings. 2) **Roadmap** — re-prioritize remaining features. 3) **Process itself** — improve how you write specs, validate, etc. SDD is a continuous improvement loop.

---

**Q: Who does the Constitution serve as an agreement between?**
A: Two agreements: 1) Between **human and agent** (key decisions on how to build). 2) Between **humans** on the team (shared understanding of mission, tech stack, roadmap).

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

---

## Lesson 06 — Creating the Constitution

**Q: How do you actually create a Constitution? (8-step process)**
A: 1) Provide project description to agent. 2) Point to stakeholder input (README.md). 3) Tell agent: "work with me on mission, tech stack, roadmap." 4) Agent asks clarifying questions. 5) You answer (make key decisions). 6) Agent writes 3 spec files. 7) Human reviews & iterates. 8) Git commit.

---

**Q: Why write the Constitution WITH the agent instead of alone?**
A: Agent asks surprisingly good questions — architecture patterns, external packages, tradeoffs (speed vs data fidelity). It's collaborative: your business context + agent's technical knowledge = better specs than either could write alone.

---

**Q: Why should you ask the agent to edit specs instead of editing manually?**
A: Keeps all artifacts **consistent**. Manual edits risk missing updates to related documents. The agent tracks cross-references across mission.md, tech-stack.md, and roadmap.md.

---

**Q: What belongs in mission.md vs tech-stack.md?**
A: **mission.md** = business context: vision, target audience, scope, problems to solve (stuff the agent can't know). **tech-stack.md** = architecture decisions: API pipelines, DB schema, data catalogs, smoke tests (engineering separated from business).

---

**Q: Why define the DB schema in the constitution upfront?**
A: It's a **headache to update later**. Getting the schema right early means features build on a stable data foundation from day one.

---

**Q: What's the "two versions" approach for constitution docs?**
A: Start with a **detailed version** (long, comprehensive — totally normal). Then generate a **pared-down version** for daily use. Both have value — detailed for reference, light for the agent's working context.

---

**Q: How does the agent act as a spec REVIEWER?**
A: The agent finds inconsistencies, asks about ambiguities, and suggests decisions. Examples: threshold inconsistencies in logic, security vs convenience tradeoffs, missing schema versions, alignment between mission and tech-stack docs.

---

## Lesson 08 — Feature Implementation

**Q: What's the first thing to do before implementing a feature?**
A: Run `/clear` to reset the agent's context. Stale context from previous work can contaminate the build. Start fresh with only the feature spec.

---

**Q: When should you implement task groups one at a time instead of all at once?**
A: When small mistakes can **compound later** — especially in **security** or **database management**. Smaller steps = smaller commits = easier to catch issues early.

---

## Lesson 09 — Feature Validation

**Q: What should you focus on during feature validation/code review?**
A: **High-level concerns**: Does the feature work? Does it reflect the spec? Are conventions followed? Are components structured correctly? DON'T focus on low-level details like CSS classes or variable naming.

---

**Q: When a code bug flows from a spec mistake, what do you fix?**
A: Fix **BOTH** — ask the agent to update the spec (add missing requirement) AND the code (implement it). Code mistakes from spec mistakes need correction at both levels.

---

**Q: What is "drift" in SDD and why is manual editing dangerous?**
A: **Drift** = when artifacts (specs, READMEs, code) go out of sync. Even "easy" manual edits cause drift because other documents won't know about the change. Always ask the agent to make changes so it updates all related mentions.

---

**Q: What is "cognitive debt"?**
A: The **mental load** of tracking what your code is doing and how it evolved. Agents write code so fast you can't keep up. SDD reduces it by keeping changes manageable (small feature loops) and using specs as review checklists.

---

**Q: When should spec updates go on a separate branch vs the feature branch?**
A: **Small updates** (checking off a roadmap step) → same branch as the feature. **Major constitution updates** → separate branch. Associating which specs created which code changes is an evolving topic.

---

## Lesson 10 — Project Replanning

**Q: What are the three levels of replanning in SDD?**
A: 1) **Feature-level** — update specs + code for recent feature (e.g., add testing). 2) **Project-level** — revise constitution + roadmap (consolidate phases, new requirements). 3) **Workflow-level** — improve the SDD process itself (build agent skills to automate).

---

**Q: When should a new requirement be implemented directly vs scheduled as a new feature?**
A: **Small change early in development** → implement directly during replanning. **Big change** → schedule as its own feature phase on the roadmap. Use your judgment.

---

**Q: What are agent skills in SDD?**
A: Packages of instructions + resources that give agents new capabilities. For **definable, repeatable workflows** needing project/org context. Examples: changelog updates on merge, validation (lint, format, test, README update). Can be project-specific or global across all projects.

---

**Q: Why does the course say "run slow to run fast"?**
A: Replanning prevents compounding mistakes. Taking time between features to update the constitution, revise the roadmap, and improve your workflow saves massive headaches later.

---

**Q: When adding testing retroactively, what THREE things do you tell the agent?**
A: 1) State your testing policy (framework, approach). 2) Update **existing** feature specs + implementation to match. 3) Actually **write the tests** — agent sets up the framework but won't write tests unless you ask.

---

## Lesson 11 — The Second Feature Phase

**Q: What is AI fatigue and how do you fight it?**
A: **AI fatigue** = exhaustion from reviewing massive amounts of agent-generated code. Fight it with: clean breaks between features, /clear agent context, high-level reviews (not nitpicking), and manageable change sizes.

---

**Q: What's the Flow State Checklist before starting a new feature?**
A: 4 checks: 1) Unfinished work cleared? 2) Last feature branch merged to main? 3) Next roadmap item still correct? 4) Agent context `/clear`'d (specs capture intent, not memory snapshots)?

---

**Q: Why use sub-agents for deep review during validation?**
A: Sub-agents **preserve the main agent's context window** (deep review is context-heavy). They have more space to think. Agent usually finds important issues on a second look. Validates you "weren't lied to."

---

**Q: Are spec omissions (like missing coding conventions) a failure?**
A: **No.** You're **evolving the spec** as you discover new details. Capturing discoveries leads to better future results. The spec is a living document — omissions are part of the evolution process.

---

**Q: When should you implement a feature in parts instead of all at once?**
A: When the feature seems **too big to implement all at once**. Ask agent to implement part of the plan first — keeps changes manageable and reduces AI fatigue.

---

## Lesson 12 — The MVP

**Q: When is it safe to implement the rest of the roadmap in one big chunk?**
A: Only when: 1) Constitution quality is **high**. 2) Previous feature specs are solid. 3) You can handle reviewing the big diff. 4) You're confident in context quality. The MVP is an **extreme test** of your SDD foundation.

---

**Q: What happens if the MVP result doesn't match your vision?**
A: You need **responsible replanning** to eliminate whatever led the agent astray. It means gaps in specs → agent filled with incorrect assumptions. Fix the root cause before building more features.

---

**Q: How is MVP validation different from regular feature validation?**
A: Regular: you validate the code (“does it work?”). MVP: **agent validates the specs** (“where are the holes in our planning?”). The evaluation of planning gaps is shared with stakeholders for their review.

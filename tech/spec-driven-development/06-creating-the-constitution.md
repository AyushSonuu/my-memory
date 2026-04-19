# 06 · Creating the Constitution 📜

---

## 🎯 One Line

> **Write the Constitution WITH the agent, not alone.** Mission (why) + Tech Stack (how) + Roadmap (when) → three files in `specs/` that guide everything.

---

## 🖼️ The Constitution Creation Flow

```mermaid
graph TB
    subgraph INPUT["📥 Your Context"]
        BIZ["Business knowledge<br/>Audience, constraints, vision"]
        STAKE["Stakeholder input<br/>(README.md)"]
    end

    subgraph CONVO["💬 Conversation with Agent"]
        Q["Agent asks great questions<br/>Architecture? Packages? Tradeoffs?"]
        A["You make decisions<br/>Tone, tech preferences, granularity"]
    end

    subgraph OUTPUT["📁 specs/ Directory"]
        M["mission.md"]
        TS["tech-stack.md"]
        RM["roadmap.md"]
    end

    INPUT --> CONVO
    CONVO --> OUTPUT
    OUTPUT --> REV["👤 Human Review"]
    REV -->|"ask agent to fix"| CONVO
    REV -->|"looks good"| COMMIT["✅ Git Commit"]

    style CONVO fill:#4caf50,color:#fff
    style OUTPUT fill:#2196f3,color:#fff
    style COMMIT fill:#ff9800,color:#fff
```

> 💡 *Constitution akele mat likho — agent ke saath conversation mein likho. Agent ke questions sunke tum bhi surprise hoge!* 🤯

---

## 📜 What Goes in Each File

<p align="center">
  <img src="_assets/constitution-pillars.svg" alt="Constitution: Mission + Tech Stack + Roadmap" width="600"/>
</p>

| File | Contains | Key Insight |
|------|----------|-------------|
| **mission.md** | Vision, target audience, scope, problems to solve, constraints | Stuff the agent **can't know** — your business context |
| **tech-stack.md** | Architecture decisions, API pipelines, DB schema, treatments/data catalogs, smoke tests | Separates engineering from business; **headache to change later** |
| **roadmap.md** | Sequence of phases, each as a feature spec | **Living document** — evolves with replanning; keep steps small |

---

## 🛠️ How to Actually Write It (Step by Step)

```mermaid
graph LR
    S1["1. Provide project<br/>description to agent"] --> S2["2. Point to stakeholder<br/>input (README.md)"]
    S2 --> S3["3. Tell agent: work with me<br/>on mission, tech stack,<br/>roadmap"]
    S3 --> S4["4. Agent asks<br/>clarifying questions"]
    S4 --> S5["5. You answer<br/>(make key decisions)"]
    S5 --> S6["6. Agent writes<br/>3 spec files"]
    S6 --> S7["7. Human review<br/>& iterate"]
    S7 --> S8["8. Git commit"]

    style S4 fill:#ff9800,color:#fff
    style S5 fill:#4caf50,color:#fff
    style S7 fill:#e91e63,color:#fff
```

### The Prompt to the Agent

| Element | What to Include |
|---------|----------------|
| **Project description** | What you're building, why |
| **Stakeholder input** | Reference existing docs (e.g., README.md) |
| **Constitution structure** | "Work with me on a mission, tech stack, and roadmap" |
| **Roadmap granularity** | "Organize the roadmap in small steps" |
| **Optional** | Mention `AskUserQuestion` tool for nicer Q&A interface |

---

## ❓ What the Agent Asks (Examples)

The agent asks **surprisingly good questions** you might not have considered:

| Question Area | Example |
|---------------|---------|
| **Tone** | "What tone should mission.md take?" → Playful |
| **Tech preferences** | "Backend language?" → TypeScript (team is used to it) |
| **Granularity** | "How granular should the roadmap be?" → Small steps |
| **Architecture** | Patterns you hadn't considered |
| **Packages** | External packages that already do the work |
| **Tradeoffs** | Speed vs data fidelity, security vs convenience |

---

## 🏥 Example Project: AgentClinic

> A parody of Pet Clinic — a clinic where AI agents get relief from their humans 😂

| Detail | Value |
|--------|-------|
| **Stack** | Next.js backend + React frontend |
| **Features** | Manage appointments, ailments (hallucination, context rot), treatments (context infusion, temperature reduction) |
| **Agent problems** | Hallucinations, context rot, memory issues, sub-agent coordination |

### What the Detailed Spec Includes

| Section | Example Detail |
|---------|---------------|
| **Problems to solve** | Agents check in via API, issues persist over time → track treatment effectiveness |
| **Visit lifecycle** | Includes TRIAGE step + FOLLOW-UP with 3 possible states |
| **Ailment catalog** | Codes, severity levels, custom ailments when symptoms don't match (>0.6 similarity threshold) |
| **API pipeline** | Full flow for POST `/visits` — validate request, search previous visits, etc. |
| **DB schema** | All tables defined upfront (headache to change later!) |
| **Treatment mapping** | Which ailments get which treatments |
| **Smoke tests** | E.g., chronic ailments are detected |
| **Treatment effectiveness** | Exact algorithm specified |

---

## 🔍 Agent as Spec Reviewer

The agent doesn't just write — it **reviews for inconsistencies**:

| What Agent Found | Resolution |
|-----------------|------------|
| Threshold inconsistency in diagnosis flow | Confirmed: 0.4–0.6 confidence = included but flagged as uncertain |
| Dashboard security question | Unprotected is fine — deploying privately in secure environment |
| LLM provider choice | Leave configurable — new models release fast |
| Archiving behavior | Soft-delete — most flexibility for later |
| Mission/tech-stack alignment | Environment variable for LLM should match in both docs |
| Prescription payloads | Add `schema_version` now — lightweight change, big payoff later |
| SSE reconnection | Accept stale state — full refresh pulls fresh state anyway (good enough for MVP) |

---

## ⚠️ Critical Best Practices

| Practice | Why |
|----------|-----|
| **Don't edit specs manually** | Ask the agent to make changes → keeps all artifacts consistent. Manual edits risk missing related documents. |
| **Review before committing** | Human-in-the-loop is essential. Agent may miss business context (e.g., target audience). |
| **Agent asks for write permissions** | Keeps changes under your control. Can approve all instances of a command per session if comfortable. |
| **Commit the Constitution** | It's a living document — git tracks its evolution. |
| **Detailed specs can be long** | Normal. This technique pays off downstream. |
| **Two versions: detailed vs pared down** | Start detailed, generate lighter version for daily use. Both have value. |

---

## 🧪 Quick Check

<details>
<summary>❓ Why should you write the Constitution WITH the agent instead of alone?</summary>

The agent asks great questions you might not have considered — architecture patterns, external packages, tradeoffs. It's a collaborative process where your business context meets the agent's technical knowledge. The conversation produces better specs than either could write alone.
</details>

<details>
<summary>❓ Why should you ask the agent to edit specs instead of editing manually?</summary>

To keep all artifacts **consistent**. If you edit mission.md manually, you might miss updating related references in tech-stack.md or roadmap.md. The agent tracks cross-references across documents.
</details>

<details>
<summary>❓ What's the benefit of defining the DB schema in the constitution upfront?</summary>

It's a **headache to update the schema later**. Getting it right in the constitution means the agent builds features on a stable data foundation from day one.
</details>

---

> **Next →** [Feature Specification](07-feature-specification.md)

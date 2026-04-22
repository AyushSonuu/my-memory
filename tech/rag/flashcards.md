# 🃏 RAG Flashcards — Cross-Module

> From: all modules + related: agentic-ai/, agent-memory/
> Last updated: 2026-04-22

---

> _Cross-module flashcards will be generated as modules are completed._
> _Each module also has its own focused flashcard file._

| Module | Flashcards |
|--------|-----------|
| M1 — RAG Overview | [flashcards](module-1-rag-overview/flashcards.md) |
| M2 — IR & Search | [flashcards](module-2-ir-search-foundations/flashcards.md) |
| M3 — Vector Databases | [flashcards](module-3-ir-vector-databases/flashcards.md) |
| M4 — LLMs & Generation | [flashcards](module-4-llms-text-generation/flashcards.md) |
| M5 — Production | [flashcards](module-5-rag-production/flashcards.md) |

---

## M2 Pulls — Retriever Architecture

<details>
<summary>❓ What makes a retriever architecture “hybrid” in RAG?</summary>

Combining keyword search and semantic search, applying metadata filters, and fusing results into one final ranking.
</details>

<details>
<summary>❓ Why is metadata filtering not replaceable by keyword/semantic search?</summary>

Because metadata filtering enforces strict non-semantic rules (like team, policy scope, or region constraints).
</details>

<details>
<summary>❓ In one line, why does retriever tuning matter?</summary>

Retriever tuning controls which documents the LLM sees, so it directly controls answer quality.
</details>

<details>
<summary>❓ What is the clean mental model for metadata filtering?</summary>

Metadata filtering is a hard policy gate that narrows candidates before final ranking.
</details>

<details>
<summary>❓ Give two examples of user-attribute-based metadata filters in production RAG.</summary>

Subscription filter (exclude paid content for free users) and region filter (only local-region content).
</details>

<details>
<summary>❓ Why does TF-IDF usually beat plain keyword counting?</summary>

Because it weights informative rare terms higher while reducing the influence of overly common terms.
</details>

<details>
<summary>❓ What two fixes were needed before TF-IDF becomes useful in practice?</summary>

Term-frequency scoring (count repeats) and length normalization (avoid long-document bias).
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

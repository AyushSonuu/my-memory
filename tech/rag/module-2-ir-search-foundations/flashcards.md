# 🃏 IR Search Foundations Flashcards

> From: module-2-ir-search-foundations/
> Last updated: 2026-04-22

---

<details>
<summary>❓ In retriever architecture, what are the 4 core stages after prompt arrival?</summary>

Keyword search + semantic search + metadata filtering + fusion/final ranking.
</details>

<details>
<summary>❓ Why is keyword search still important in modern RAG retrieval?</summary>

It captures exact term matches from the user query, which is critical when precise wording matters.
</details>

<details>
<summary>❓ What is the key benefit of semantic search over keyword-only search?</summary>

Semantic search retrieves documents with similar meaning even if exact query words are not present.
</details>

<details>
<summary>❓ Where does metadata filtering fit in the retrieval pipeline?</summary>

After candidate lists are returned by keyword and semantic search, before final ranking/fusion.
</details>

<details>
<summary>❓ Give one real metadata filter example from enterprise RAG.</summary>

Filter by user department (e.g., engineering vs HR) so only department-relevant documents continue.
</details>

<details>
<summary>❓ Why do keyword and semantic lists often overlap but rank differently?</summary>

Because they optimize different relevance signals: exact lexical match vs meaning similarity.
</details>

<details>
<summary>❓ Why is this approach called hybrid search?</summary>

Because final retrieval quality comes from combining multiple search techniques, not relying on one method.
</details>

<details>
<summary>❓ What tuning decision drives retriever quality in a hybrid system?</summary>

How you balance keyword, semantic, and metadata constraints to match product needs.
</details>

<details>
<summary>❓ What kind of criteria does metadata filtering use?</summary>

Rigid criteria on metadata fields such as title, author, publication date, section, access privileges, and region.
</details>

<details>
<summary>❓ In RAG systems, are metadata filters usually derived from query text?</summary>

Usually no. They are often derived from user attributes (e.g., subscription tier, location, team).
</details>

<details>
<summary>❓ Why can metadata filtering enforce behavior that keyword/semantic search cannot?</summary>

Because it can hard-include or hard-exclude documents by policy rules, regardless of textual similarity.
</details>

<details>
<summary>❓ Why is metadata filtering alone insufficient for retrieval quality?</summary>

It ignores document content meaning and offers no relevance ranking; it only narrows candidate sets.
</details>

<details>
<summary>❓ Complete the sentence: Metadata filtering is best used as ______.</summary>

A refinement/constraint layer on top of keyword and semantic retrieval.
</details>

<details>
<summary>❓ In keyword search, what does “bag of words” mean?</summary>

Word order is ignored; only which words appear and how often they appear are used.
</details>

<details>
<summary>❓ Why are keyword vectors called sparse vectors?</summary>

Because vocabulary is large and most word positions are zero for any single prompt/document.
</details>

<details>
<summary>❓ What is a term-document matrix?</summary>

A grid where rows are terms, columns are documents, and values store term counts/weights.
</details>

<details>
<summary>❓ What does an inverted index help you do quickly?</summary>

Start from a word and find all documents that contain it.
</details>

<details>
<summary>❓ Why do we normalize term-frequency scores by document length?</summary>

To avoid unfairly favoring long documents that repeat keywords just because they have more text.
</details>

<details>
<summary>❓ Why does IDF improve keyword ranking quality?</summary>

It down-weights common filler words and up-weights rarer, more informative words.
</details>

<details>
<summary>❓ What does TF-IDF combine?</summary>

Term frequency within a document (TF) and inverse document frequency across the corpus (IDF).
</details>

<details>
<summary>❓ What usually comes after TF-IDF in production keyword retrieval?</summary>

BM25, a refined scoring approach built on similar intuition.
</details>

---

> 💡 **Revision tip:** Cover the answer, explain it out loud, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

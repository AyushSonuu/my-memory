# 🃏 IR Search Foundations Flashcards

> From: module-2-ir-search-foundations/
> Last updated: 2026-04-25

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

<details>
<summary>❓ What does BM25 improve over TF-IDF?</summary>

It adds term-frequency saturation (diminishing returns for repeated words), gentler document-length normalization, and tunable hyperparameters for better corpus-specific ranking.
</details>

<details>
<summary>❓ In BM25, what does term-frequency saturation mean in plain language?</summary>

If a keyword appears many times, each extra repetition helps less and less; 20 mentions are not twice as valuable as 10 mentions.
</details>

<details>
<summary>❓ What is the role of `k1` in BM25?</summary>

`k1` controls how quickly term-frequency rewards saturate. Higher `k1` means slower saturation; lower `k1` means faster saturation.
</details>

<details>
<summary>❓ What is the role of `b` in BM25?</summary>

`b` controls document-length normalization strength. `b=0` means no length penalty; `b=1` means full normalization.
</details>

<details>
<summary>❓ Why is BM25 usually preferred in production retrievers?</summary>

It tends to outperform TF-IDF with similar computational cost and gives tuning knobs (`k1`, `b`) to fit real corpus behavior.
</details>

<details>
<summary>❓ What is hybrid search in retrieval?</summary>

A pipeline that combines keyword search, semantic search, and metadata filtering to leverage the strengths of all three techniques.
</details>

<details>
<summary>❓ In hybrid search, when do keyword and semantic searches run?</summary>

In parallel — both run simultaneously on the same prompt and each return their own ranked list.
</details>

<details>
<summary>❓ What happens to the two ranked lists (keyword + semantic) after they are returned?</summary>

They are each filtered using metadata criteria, then merged using Reciprocal Rank Fusion (RRF) into a single final ranking.
</details>

<details>
<summary>❓ What does Reciprocal Rank Fusion (RRF) do?</summary>

It merges multiple ranked lists into one by scoring documents based on their rank positions (not original scores).
</details>

<details>
<summary>❓ What is the RRF scoring formula?</summary>

Score = Σ (1 / (k + rank)) — documents earn points from each ranking they appear in, summed across all lists.
</details>

<details>
<summary>❓ In RRF, if a document ranks 2nd in keyword search and 10th in semantic search, what is its score when k=0?</summary>

1/2 + 1/10 = 0.5 + 0.1 = **0.6 points**.
</details>

<details>
<summary>❓ What does the RRF parameter `k` control?</summary>

`k` controls how much being ranked #1 dominates the final ranking. k=0 → top rank dominates (10× difference). k=50 → balanced (1.2× difference).
</details>

<details>
<summary>❓ Why is k=50 commonly used in RRF?</summary>

It prevents a single #1 ranking from dominating the overall result, ensuring both keyword and semantic signals matter.
</details>

<details>
<summary>❓ Does RRF use the original scores from keyword/semantic search?</summary>

No — RRF only uses the rank position (1st, 2nd, 3rd, etc.), not the scores that led to those rankings.
</details>

<details>
<summary>❓ What does the beta (β) parameter control in hybrid search?</summary>

β controls the weight balance between semantic and keyword rankings — β=0.7 means 70% semantic, 30% keyword.
</details>

<details>
<summary>❓ What is a good default beta value to start with?</summary>

**β=0.7** (70% semantic, 30% keyword) — works well for most applications.
</details>

<details>
<summary>❓ When should you lower beta (e.g., β=0.3)?</summary>

When exact keyword matching is critical — e.g., technical terms, product codes, API names, error codes.
</details>

<details>
<summary>❓ When should you raise beta (e.g., β=0.8)?</summary>

When semantic meaning matters more than exact words — e.g., customer support queries with many ways to phrase the same question.
</details>

<details>
<summary>❓ What are the three complementary strengths in hybrid search?</summary>

Keyword = exact word match | Semantic = fuzzy meaning match | Metadata = strict yes/no filtering.
</details>

<details>
<summary>❓ What tuning knobs does hybrid search expose?</summary>

`k` (RRF dominance), `β` (keyword vs semantic weight), `k1` and `b` (BM25 parameters), metadata filtering rules.
</details>

<details>
<summary>❓ Why is hybrid search the default choice in production RAG systems?</summary>

It handles both exact keyword matching AND fuzzy semantic similarity, which most real-world queries require.
</details>

---

> 💡 **Revision tip:** Cover the answer, explain it out loud, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

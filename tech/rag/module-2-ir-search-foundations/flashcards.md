# 🃏 IR Search Foundations Flashcards

> From: module-2-ir-search-foundations/
> Last updated: 2026-05-02

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

## Retrieval Metrics (Lesson 10)

<details>
<summary>❓ What are the 3 ingredients required to evaluate a retriever?</summary>

1. **Query** — the search prompt
2. **Retrieved list** — ranked documents the retriever returns
3. **Ground truth** — all relevant documents in the KB (hand-labeled answer key)
</details>

<details>
<summary>❓ What does Precision measure?</summary>

Precision = (Relevant Retrieved) / (Total Retrieved). It measures how trustworthy your results are — what fraction of returned docs are actually relevant.
</details>

<details>
<summary>❓ What does Recall measure?</summary>

Recall = (Relevant Retrieved) / (Total Relevant in KB). It measures how comprehensive you are — what fraction of all relevant docs did you find.
</details>

<details>
<summary>❓ If you retrieved 12 docs and 8 are relevant, but there are 10 relevant docs total in the KB, what is precision? What is recall?</summary>

**Precision** = 8/12 = 66% (8 relevant out of 12 returned)
**Recall** = 8/10 = 80% (found 8 out of 10 total relevant)
</details>

<details>
<summary>❓ What is the typical trade-off between precision and recall?</summary>

Returning more documents often improves recall (find more relevant) but hurts precision (more noise included). Perfect score = return ONLY the relevant documents.
</details>

<details>
<summary>❓ What does "@K" mean in Precision@K or Recall@K?</summary>

It means "looking at only the top K results". E.g., Precision@5 = precision when only considering the top 5 ranked documents.
</details>

<details>
<summary>❓ If the top 10 docs have 6 relevant ones (out of 8 total relevant in KB), what is Precision@10 and Recall@10?</summary>

**Precision@10** = 6/10 = 60%
**Recall@10** = 6/8 = 75%
</details>

<details>
<summary>❓ When should you use stricter metrics like @1, @3, @5 vs. more generous @10, @15?</summary>

**Strict (@1-5):** When only top results matter (e.g., search UX, first-page quality)
**Generous (@10-15):** For general evaluation, more forgiving of ranking imperfections
</details>

<details>
<summary>❓ What does Mean Average Precision (MAP) reward?</summary>

MAP rewards placing relevant documents **high in the ranking**. Irrelevant docs sneaking into top spots hurt the score at every relevant doc below them.
</details>

<details>
<summary>❓ How do you calculate Average Precision (AP)?</summary>

1. Calculate Precision@K at each rank
2. Sum the precisions ONLY at relevant document positions
3. Divide by the number of relevant documents found
</details>

<details>
<summary>❓ In a ranking of 6 docs where ranks 1, 4, 5 are relevant: P@1=1.0, P@4=0.5, P@5=0.6. What is AP@6?</summary>

AP = (1.0 + 0.5 + 0.6) / 3 = 2.1 / 3 = **0.7**
</details>

<details>
<summary>❓ What is Mean Reciprocal Rank (MRR)?</summary>

MRR measures how quickly you find the FIRST relevant document. Reciprocal Rank = 1/rank of first relevant doc. MRR averages this across many queries.
</details>

<details>
<summary>❓ If first relevant appears at rank 4, what is the reciprocal rank?</summary>

**1/4 = 0.25**
</details>

<details>
<summary>❓ For 4 searches where first relevant appears at ranks 1, 3, 6, 2, what is MRR?</summary>

RRs: 1/1=1.0, 1/3=0.33, 1/6=0.17, 1/2=0.5
MRR = (1.0 + 0.33 + 0.17 + 0.5) / 4 = **0.5**
</details>

<details>
<summary>❓ What does MRR = 0.5 mean in plain language?</summary>

"On average, the first relevant result appears around rank 2." Great for search UX — users find something useful quickly.
</details>

<details>
<summary>❓ Match each metric to what it measures: Recall@K, Precision@K, MAP@K, MRR.</summary>

- **Recall@K** → Did I find everything? (completeness)
- **Precision@K** → Are results trustworthy? (no noise)
- **MAP@K** → Overall ranking quality (relevant at top)
- **MRR** → First-result UX (how fast to first hit)
</details>

<details>
<summary>❓ What is the biggest limitation of all retrieval metrics?</summary>

They all require **ground truth** — hand-labeled relevant documents for sample queries. This is expensive and time-consuming to create.
</details>

<details>
<summary>❓ Why is Recall the most cited retriever metric?</summary>

It captures the most fundamental goal: finding all the relevant documents. You can't answer well with an LLM if the retriever missed the good stuff.
</details>

---

> 💡 **Revision tip:** Cover the answer, explain it out loud, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

# 🃏 Vector Databases Flashcards

> From: module-3-ir-vector-databases/
> Last updated: 2026-05-03

---

## Module Introduction (Lesson 01)

<details>
<summary>❓ Why do we need vector databases instead of relational databases for RAG?</summary>

Relational databases perform vector search like inefficient KNN (comparing to every vector). Vector databases use ANN algorithms like HNSW, scaling to millions/billions of vectors efficiently.
</details>

<details>
<summary>❓ What are the main topics covered in Module 3?</summary>

Vector databases, ANN algorithms, chunking, query parsing, reranking, and a hands-on lab building RAG with a vector DB.
</details>

---

## Vector Databases (Lesson 03)

<details>
<summary>❓ What is a vector database designed for?</summary>

Storing high-dimensional vector data and performing vector search using ANN algorithms like HNSW. Optimized for building proximity graphs and computing vector distances at scale.
</details>

<details>
<summary>❓ Name 3 popular vector databases.</summary>

Weaviate (open-source, used in this course), Pinecone, Qdrant, Milvus, Chroma, pgvector — any 3 of these.
</details>

<details>
<summary>❓ What are the 5 setup steps before a vector DB is ready to search?</summary>

1. Database setup (create/connect instance)
2. Load documents
3. Create sparse vectors (for keyword search)
4. Create dense vectors (embeddings for semantic)
5. Build HNSW index (for ANN algorithm)
</details>

<details>
<summary>❓ In Weaviate, what does a "collection" represent?</summary>

A collection is like a table — it holds objects of the same type with defined properties (schema) and a specified vectorizer (embedding model).
</details>

<details>
<summary>❓ What does `batch.add_object()` do in Weaviate?</summary>

It inserts an object into the collection AND automatically counts errors and handles failures — production-ready batch insertion.
</details>

<details>
<summary>❓ What Weaviate method performs semantic (vector) search?</summary>

`collection.query.near_text()` — converts query to vector and finds nearest neighbors.
</details>

<details>
<summary>❓ What Weaviate method performs keyword (BM25) search?</summary>

`collection.query.bm25()` — uses the auto-created inverted index.
</details>

<details>
<summary>❓ What does the `alpha` parameter control in Weaviate hybrid search?</summary>

The weighting between vector and keyword search:
- `alpha=0.0` → 100% keyword, 0% vector
- `alpha=0.25` → 25% vector, 75% keyword
- `alpha=1.0` → 100% vector, 0% keyword
</details>

<details>
<summary>❓ What is a typical production default for hybrid search alpha?</summary>

**alpha=0.25** (25% vector, 75% keyword) — balances semantic similarity with exact keyword matching. Most companies use hybrid search in production.
</details>

<details>
<summary>❓ How do you add metadata filtering in Weaviate?</summary>

Use `filters=Filter.by_property("field").equal("value")` — objects must match the filter to be returned.
</details>

<details>
<summary>❓ What does Weaviate automatically create when you insert documents?</summary>

1. Sparse vectors (inverted index for BM25)
2. Dense vectors (embeddings via specified vectorizer)
3. HNSW index (for ANN search)
</details>

---

## Chunking Concepts (Lesson 05)

<details>
<summary>❓ What is chunking and why do we do it?</summary>

Chunking = breaking longer documents into smaller text pieces. Three reasons:
1. **Token limits** — embedding models have max input length
2. **Improved relevancy** — smaller chunks = sharper, topic-specific vectors
3. **LLM context** — send only relevant chunks, not whole books
</details>

<details>
<summary>❓ What's wrong with vectorizing an entire book as a single vector?</summary>

The vector becomes blurry — it averages ALL topics in the book into one representation. Can't represent specific chapters/pages sharply. Also fills up LLM context window when retrieved.
</details>

<details>
<summary>❓ What's the "Goldilocks problem" with chunk size?</summary>

**Too large (chapter):** Blurry vectors, fills LLM context, averages too many topics.
**Too small (word):** Loses context, reduces relevance — "the" alone means nothing.
**Just right (paragraph):** Sharp vectors, balanced context and specificity.
</details>

<details>
<summary>❓ What is fixed-size chunking?</summary>

The simplest approach: every chunk has the same character count (e.g., 250 characters). Chunk 1 = chars 1-250, Chunk 2 = chars 251-500, etc. Problem: splits may fall mid-word.
</details>

<details>
<summary>❓ Why add overlap to fixed-size chunks?</summary>

Overlap preserves context at chunk boundaries. Words at edges appear in TWO chunks, increasing odds they have relevant context. Example: 250 chars with 25 char (10%) overlap.
</details>

<details>
<summary>❓ What's a good starting point for chunk size and overlap?</summary>

**~500 characters** with **50-100 character overlap** (10-20%). Simple, works well for most cases. Adjust based on relevancy metrics.
</details>

<details>
<summary>❓ What is recursive character splitting?</summary>

Split on meaningful characters (like `\n` between paragraphs) instead of fixed positions. Variable chunk sizes, but related concepts stay together within natural boundaries.
</details>

<details>
<summary>❓ How should you split different document types?</summary>

- **HTML:** Split on `<p>`, `<h1>`, `<h2>` tags
- **Python code:** Split on function/class definitions
- **Markdown:** Split on headers (`#`, `##`)
- **Plain text:** Split on newline characters
</details>

<details>
<summary>❓ What metadata should chunks inherit from their source document?</summary>

**Inherited:** Document title, author, date, category/tags.
**Added:** Chunk index (1, 2, 3...), character position (start-end), page number if applicable.
</details>

<details>
<summary>❓ What's the trade-off of using more overlap?</summary>

**Pro:** Better relevancy — words at boundaries have context.
**Con:** More vectors to store (some redundant information).
</details>

## Advanced Chunking (Lesson 07)

<details>
<summary>❓ What problem does semantic chunking solve that fixed-size chunking doesn't?</summary>

Fixed-size splits can break text mid-thought, losing context. Example: "she dreamed...that she was finally an Olympic champion" could split to make it seem she's already a champion. Semantic chunking groups sentences by **meaning similarity**.
</details>

<details>
<summary>❓ How does the semantic chunking algorithm work?</summary>

1. Move through document sentence by sentence
2. Vectorize current chunk + vectorize next sentence
3. Calculate cosine distance between them
4. If distance < threshold → add to same chunk
5. If distance > threshold → start NEW chunk
</details>

<details>
<summary>❓ What are the pros and cons of semantic chunking?</summary>

**Pros:** Follows author's train of thought, smarter boundaries, higher precision/recall.
**Cons:** Computationally expensive (vector calc per sentence), harder to tune threshold, variable chunk sizes.
</details>

<details>
<summary>❓ How does LLM-based chunking work?</summary>

Give the document to an LLM with instructions like "keep similar concepts together, start new chunk when topic changes." LLM generates chunk output. Black box but very high performing.
</details>

<details>
<summary>❓ What is context-aware chunking?</summary>

Use an LLM to add **context text** to every chunk, explaining its place in the broader document. Example: a list of names becomes "Acknowledgments section thanking contributors: Alice, Bob..."
</details>

<details>
<summary>❓ Why is context-aware chunking a good first improvement to try?</summary>

It works **on top of any chunking strategy** (fixed, semantic, etc.), improves both search relevancy AND LLM understanding, and has no impact on search speed. Just preprocessing cost.
</details>

<details>
<summary>❓ When should you use fixed-size vs semantic vs LLM-based chunking?</summary>

- **Fixed-size:** Prototyping, simple docs (default)
- **Semantic:** Long-form content where topics flow across paragraphs
- **LLM-based:** Complex documents, when LLM costs are acceptable
- **Context-aware:** First upgrade to try on any strategy
</details>

<details>
<summary>❓ What's the practical advice for choosing a chunking strategy?</summary>

1. Start simple (fixed-size with overlap)
2. Measure precision/recall before upgrading
3. Experiment on a **subset** before processing entire KB
4. Context-aware is low-hanging fruit for improvement
</details>

---

## Cross-Encoders & ColBERT (Lesson 09)

<details>
<summary>❓ What are the three architectures for semantic search?</summary>

1. **Bi-Encoder** — documents and prompts embedded separately (default, fast)
2. **Cross-Encoder** — prompt + doc concatenated and scored together (best quality, slow)
3. **ColBERT** — token-level vectors with MaxSim scoring (balanced quality/speed)
</details>

<details>
<summary>❓ Why is a bi-encoder called "bi"?</summary>

Because it embeds **two things separately**: documents are embedded ahead of time, prompts are embedded at query time. They never "see" each other during encoding — only compared as finished vectors.
</details>

<details>
<summary>❓ What makes cross-encoders produce higher quality results?</summary>

Cross-encoders concatenate prompt + document and process them **together**. This allows the model to understand deep contextual interactions between words (e.g., "New York" ↔ "NYC", "eat" ↔ "cuisine").
</details>

<details>
<summary>❓ Why can't cross-encoders be used directly for search at scale?</summary>

Must run the model for EVERY document in the KB for each query. With millions of docs, this takes hours per query. No pre-computation possible because you need the prompt first.
</details>

<details>
<summary>❓ What does ColBERT stand for?</summary>

**C**ontextualized **L**ate **I**nteraction over **BERT** — "late interaction" means document and prompt vectors are computed separately but compared at a more detailed level (tokens).
</details>

<details>
<summary>❓ How does ColBERT differ from bi-encoder in embedding?</summary>

Bi-encoder: 1 vector per document
ColBERT: **N vectors per document** (one per token)

A 2000-token document needs 2000 vectors in ColBERT vs 1 in bi-encoder.
</details>

<details>
<summary>❓ What is MaxSim scoring in ColBERT?</summary>

For each prompt token, find its MAX similarity to any doc token. Sum all the max similarities = final document score. This captures token-level matching (e.g., "New York" ↔ "NYC").
</details>

<details>
<summary>❓ What is the main trade-off of ColBERT vs bi-encoder?</summary>

**Storage explosion.** ColBERT needs N vectors per document (one per token). A 2000-token doc = 2000× more storage than bi-encoder. But provides much richer matching.
</details>

<details>
<summary>❓ When should you use each architecture?</summary>

- **Bi-Encoder:** Default, general search, speed critical
- **Cross-Encoder:** Reranking top K candidates (too slow for initial search)
- **ColBERT:** High-stakes domains (legal, medical) where precision matters and storage cost is acceptable
</details>

<details>
<summary>❓ What is the production pattern for using cross-encoders?</summary>

1. Use bi-encoder to retrieve top K candidates (fast, ~100 docs)
2. Use cross-encoder to re-rank those K candidates (slow but only K docs, not millions)
3. Return the re-ranked top results

Best of both worlds: speed of bi-encoder + quality of cross-encoder.
</details>

---

## Reranking (Lesson 10)

<details>
<summary>❓ What is reranking and when does it happen?</summary>

**Reranking** = re-scoring and re-ordering documents **after** initial retrieval but **before** sending to LLM.

Pipeline: Vector DB retrieves 20-100 docs → Reranker re-scores them → Return top 5-10 to LLM
</details>

<details>
<summary>❓ What is overfetching and why do we do it?</summary>

**Overfetching** = retrieving more documents than you'll ultimately return (e.g., retrieve 50, return 10).

Why: Bi-encoder ranking isn't perfect. The true best document might be at rank 15, not rank 3. Overfetching gives the reranker a chance to find and promote truly relevant docs.
</details>

<details>
<summary>❓ Why can cross-encoders be used for reranking but not initial search?</summary>

Cross-encoders require prompt + document together — no pre-computation possible.

- Initial search: Must score **millions** of docs → infeasible (hours)
- Reranking: Only score **20-100** docs → totally viable (100-500ms)

Bi-encoder narrows candidates, cross-encoder refines.
</details>

<details>
<summary>❓ What's the typical overfetch/return ratio for reranking?</summary>

**Overfetch:** 15-25 docs (up to 100 for high-stakes)
**Return:** 5-10 docs to LLM

The 3-5× ratio gives reranker room to find truly relevant docs that might have ranked lower initially.
</details>

<details>
<summary>❓ What are the two main types of rerankers?</summary>

1. **Cross-encoder reranker:** [prompt + doc] → specialized model → relevance score. Standard approach.
2. **LLM-based reranker:** [prompt + doc] → LLM → scores relevance. Emerging approach, more expensive.

Both have same scaling limits — only viable on small candidate sets (after initial retrieval).
</details>

<details>
<summary>❓ Why is reranking "one of the first techniques to try" for improving RAG?</summary>

1. **Easy to implement** — often just one line/parameter
2. **Minimal latency** — 100-500ms for 20-100 docs
3. **Big quality boost** — cross-encoder deeply understands relevance
4. **Low risk** — doesn't change your architecture, just adds a step

Almost always worth the trade-off unless latency is extremely critical.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

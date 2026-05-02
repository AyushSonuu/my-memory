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

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

# 🃏 Vector Databases Flashcards

> From: module-3-ir-vector-databases/
> Last updated: 2026-05-02

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

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

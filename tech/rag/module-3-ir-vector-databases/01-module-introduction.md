# 01 — Module 3 Introduction: Theory → Production

> IR samajh liya — ab production mein lagana hai! 🚀

---

## The Scaling Problem

You've learned the IR fundamentals:
- Keyword search (TF-IDF, BM25)
- Semantic search (embeddings)
- Hybrid search (RRF fusion)
- Evaluation metrics (Precision, Recall, MAP, MRR)

**But:** Once you need to search **millions or billions** of documents, traditional relational databases slow down significantly — especially for the vector operations underlying semantic search.

> 💡 Theory works at small scale. Production needs vector databases.

---

## Module 3 Roadmap

```
┌─────────────────────────────────────────────────────────────┐
│                    MODULE 3 JOURNEY                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   📚 IR Theory (M2)                                         │
│        ↓                                                    │
│   🗄️ Vector Databases ─── Why they exist                   │
│        ↓                       └── Optimized for vector ops │
│   🔍 ANN Algorithms ───── Fast approximate search           │
│        ↓                                                    │
│   🧰 Weaviate API ─────── Hands-on with a real VDB         │
│        ↓                                                    │
│   ✂️ Document Chunking ── Splitting docs for retrieval      │
│        ↓                                                    │
│   🔎 Query Parsing ────── Breaking down complex queries     │
│        ↓                                                    │
│   🏆 Reranking ────────── Post-retrieval quality boost      │
│        ↓                                                    │
│   🛠️ Lab: RAG + VDB ───── End-to-end implementation        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## What You'll Learn

| Topic | What It Is | Why It Matters |
|-------|-----------|----------------|
| **Vector Databases** | DBs optimized for storing/searching vectors | Scale semantic search to billions of docs |
| **ANN Algorithms** | Approximate Nearest Neighbor search | Trade tiny accuracy for massive speed gains |
| **Chunking** | Splitting documents into searchable pieces | Right chunk size = better retrieval |
| **Query Parsing** | Breaking complex queries into parts | Handle multi-part user questions |
| **Reranking** | Re-scoring retrieved docs with better model | Boost precision after initial retrieval |

---

## Module Structure

| Lesson | Focus |
|--------|-------|
| 01 | Introduction (this lesson) |
| 02-03 | ANN algorithms + Vector database internals |
| 04 | Weaviate API hands-on |
| 05-07 | Document chunking (concepts + lab + advanced) |
| 08 | Query parsing |
| 09-10 | Cross-encoders, ColBERT, reranking |
| 11 | Lab: Full RAG with vector DB |

---

## Key Insight

> 💡 Vector databases have become **almost synonymous with RAG systems** — if you're building production RAG, you're almost certainly using a vector DB.

---

## 🔗 Connections
- ← Built on: [Module 2: IR Foundations](../module-2-ir-search-foundations/) (all the theory)
- → Enables: Production-scale semantic search
- Related: Embedding models (how vectors are created)

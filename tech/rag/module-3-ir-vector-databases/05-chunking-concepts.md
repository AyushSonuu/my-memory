# 05 — Chunking: Breaking Documents for Better Retrieval

> Poori kitaab ek vector mein? Recipe for disaster. Chunks = sharp, relevant retrieval! ✂️

---

## Why Chunk Documents?

| Reason | Problem Without Chunking | Solution |
|--------|-------------------------|----------|
| **Token Limits** | Embedding models have max input length | Smaller chunks fit within limits |
| **Improved Relevancy** | Entire book = blurry vector (averages everything) | Paragraph/page = sharp, topic-specific vectors |
| **LLM Context** | Retrieving whole books fills context window | Send only the relevant chunks to LLM |

---

## The Problem: No Chunking

![Chunking Problem](_assets/05-no-chunking-problem.svg)

```
Knowledge Base: 1,000 books
        ↓
Embedding Model vectorizes each book
        ↓
Result: 1,000 vectors

Problem: Each vector compresses an ENTIRE BOOK
         → Can't represent specific topics sharply
         → Search relevance = poor
         → Retrieves whole books = fills LLM context
```

> 💡 Ek vector mein Mahabharat compress karna = every topic becomes "meh." Chunking karo toh Arjun, Krishna, Karna sab alag alag sharp vectors! 🎯

---

## The Solution: Chunk Your Content

| Granularity | # Vectors | Trade-off |
|-------------|-----------|-----------|
| **Book** | 1,000 | Too coarse — blurry vectors |
| **Chapter** | ~10,000 | Still too large |
| **Page** | ~200,000 | Better relevance |
| **Paragraph** | ~1,000,000 | Good balance ✅ |
| **Sentence** | ~10,000,000 | May lose context |
| **Word** | ~100,000,000 | Useless — no context |

> Vector databases easily scale to millions of vectors. Don't be afraid to chunk small!

---

## Chunk Size: The Goldilocks Problem

![Chunk Size Trade-offs](_assets/05-chunk-size-tradeoffs.svg)

| Too Large (Chapter) | Just Right | Too Small (Word) |
|---------------------|-----------|------------------|
| ❌ Too many topics in one vector | ✅ Balance between context and specificity | ❌ Loses surrounding context |
| ❌ Fills LLM context window | ✅ Sharp semantic representation | ❌ Reduces search relevance |
| ❌ Blurry, averaged meaning | ✅ Retrieves focused content | ❌ "The" doesn't mean anything alone |

---

## Strategy 1: Fixed-Size Chunking

The simplest approach — every chunk has the same character count.

```
Document: "The quick brown fox jumps over the lazy dog..."
Chunk size: 250 characters

Chunk 1: Characters 1-250
Chunk 2: Characters 251-500
Chunk 3: Characters 501-750
...
```

**Problem:** Splits often fall mid-word or break cohesive thoughts.

---

## Strategy 2: Fixed-Size with Overlap

Add overlap between chunks to preserve context at boundaries.

![Overlapping Chunks](_assets/05-overlapping-chunks.svg)

```
Chunk size: 250 characters
Overlap: 25 characters (10%)

Chunk 1: Characters 1-250
Chunk 2: Characters 226-475  (overlaps with chunk 1)
Chunk 3: Characters 451-700  (overlaps with chunk 2)
...
```

| Benefit | Trade-off |
|---------|-----------|
| Words at edges appear in TWO chunks | More vectors = more storage |
| Minimizes words cut off from context | Some redundant information |
| Words in middle have context on both sides | — |

> 💡 **Good starting point:** 500 characters with 50-100 character overlap (10-20%).

---

## Strategy 3: Recursive Character Splitting

Split on meaningful characters (like `\n` between paragraphs) instead of fixed positions.

```
Original text:
"Taylor Swift is performing three sold-out shows...
[newline]
Thousands of fans are traveling to the city...
[newline]
Local hotels are fully booked..."

Split on newline (\n):
├─ Chunk 1: "Taylor Swift is performing..."
├─ Chunk 2: "Thousands of fans are traveling..."
└─ Chunk 3: "Local hotels are fully booked..."
```

| Pros | Cons |
|------|------|
| Accounts for document structure | Variable chunk sizes |
| Related concepts stay together | Very long paragraphs = very large chunks |
| More natural boundaries | Very short paragraphs = tiny chunks |

### Split Different Document Types Differently

| Document Type | Split On |
|--------------|----------|
| **HTML** | `<p>`, `<h1>`, `<h2>` tags |
| **Python code** | Function definitions, class definitions |
| **Markdown** | Headers (`#`, `##`), blank lines |
| **Plain text** | Newline characters (`\n`) |

---

## Chunking Decision Flowchart

```
┌─────────────────────────────────────────────┐
│  What kind of documents?                    │
├─────────────────────────────────────────────┤
│                                             │
│  Plain text / unknown structure             │
│  └─→ Fixed-size with overlap (500 chars)   │
│                                             │
│  Structured (HTML, Markdown, Code)          │
│  └─→ Recursive character splitting          │
│      (split on tags/headers/definitions)    │
│                                             │
│  Need highest relevancy?                    │
│  └─→ Semantic chunking (next lesson)        │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Metadata Preservation

When chunking, chunks should **inherit metadata** from their source:

| Inherited | Added |
|-----------|-------|
| Document title | Chunk index (1, 2, 3...) |
| Author | Character position (start-end) |
| Date | Page number (if applicable) |
| Category/tags | — |

This enables filtering: "Find chunks from documents by author X published after 2023"

---

## Quick Reference: Starting Point

| Parameter | Recommended |
|-----------|-------------|
| **Chunk size** | ~500 characters |
| **Overlap** | 50-100 characters (10-20%) |
| **Strategy** | Fixed-size with overlap (simple, works well) |
| **When to upgrade** | If relevancy metrics are poor → try semantic chunking |

---

## 🔗 Connections
- ← Stored in: [Vector Databases](03-vector-databases.md)
- → Next: [Chunking Lab](06-chunking-lab.md) (hands-on)
- → Advanced: [Advanced Chunking](07-advanced-chunking.md) (semantic, LLM-based)
- Related: [Embedding Models](../module-2-ir-search-foundations/07-embedding-model-deepdive.md) (what creates the vectors)

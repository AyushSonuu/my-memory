# 04 · Keyword Search: TF-IDF 🔤

---

## 🎯 One Line
> TF-IDF ranks documents by rewarding frequent query terms in a document (TF) and giving extra weight to rare, informative terms across the corpus (IDF).

---

## 🖼️ Keyword Search Pipeline (Bag-of-Words)

```mermaid
graph TD
    P[Prompt] --> B1[Bag of Words]
    D[Documents] --> B2[Bag of Words]
    B2 --> IDX[Term-Document Matrix<br/>Inverted Index]
    B1 --> QV[Prompt Sparse Vector]
    IDX --> SCORE[Score Documents]
    QV --> SCORE
    SCORE --> RANK[Rank + Retrieve Top Docs]
```

> 💡 Keyword search ka rule simple hai: prompt ke words jitne strong match honge, doc utna upar aayega.

---

## 🧱 Core Ideas

| Concept | Meaning |
|---|---|
| **Bag of words** | Word order ignored; only word presence + frequency matter |
| **Sparse vector** | One dimension per vocabulary word; most values are zero |
| **Term-document matrix** | Rows = words, columns = documents |
| **Inverted index** | Start from a word, quickly find documents containing that word |

Example prompt: "making pizza without a pizza oven"
- `pizza` appears 2 times
- `making`, `without`, `a`, `oven` appear 1 time each

---

## 📊 Visual: Term-Document Matrix

Query: "making pizza without a pizza oven"

![Term-Document Matrix (Bag of Words)](assets/04-term-document-matrix-bag-of-words.svg)

---

## ⚙️ Scoring Evolution (4 Progressive Improvements)

### Step 1️⃣: Binary Keyword Score

![Query: "pizza oven"](assets/04-query-pizza-oven.svg)

### Step 2️⃣: Term Frequency (TF) Score

![Query: "pizza oven"](assets/04-query-pizza-oven.svg)

### Step 3️⃣: Length Normalization

![Query: "pizza oven"](assets/04-query-pizza-oven.svg)

### Step 4️⃣: IDF Weighting (The Final Piece)

![Inverse Document Frequency (IDF) — Reward Rare Words](assets/04-inverse-document-frequency-idf-reward-rare-words.svg)

---

## 🎯 Complete TF-IDF Example: "making pizza without a pizza oven"

![TF-IDF Scoring Progression](assets/04-tf-idf-scoring-progression.svg)

**Key Insight:** Doc 1 scores highest because it contains the rare keywords `pizza` and `oven` proportionally more than the other docs, even though simpler metrics might rank them differently.

---

## ✅ Why TF-IDF Is a Strong Baseline

- Fast and mature
- Easy to implement and debug
- Captures both frequency (within doc) and rarity (across corpus)
- Still a standard baseline for keyword retrieval quality

## ⚠️ Limitation (and what's next)

TF-IDF is foundational, but production retrievers often use **BM25**, a refined keyword scoring method.

---

> **Next →** [Keyword Search: BM25](05-keyword-search-bm25.md)

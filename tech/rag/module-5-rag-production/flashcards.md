# 🃏 RAG Production Flashcards

> From: module-5-rag-production/
> Last updated: 2026-05-17

---

## Lesson 01-02: Production Challenges & Observability

### Q: What are the 6 major production challenges for RAG systems?
**A:** 
1. **Scale/Performance** — high traffic, latency spikes
2. **Unpredictable prompts** — users creative, can't test all cases
3. **Messy data** — fragmented, missing metadata, non-text (PDFs, images)
4. **Security/Privacy** — proprietary data leaks, prompt injection
5. **Adversarial attacks** — malicious prompts to extract data
6. **Business impact** — mistakes = reputation damage, legal issues

---

### Q: What's the 2D evaluation framework for RAG systems?
**A:** **Scope** (Component vs System) × **Evaluator Type** (Code-based, LLM-as-a-judge, Human feedback)
- **Component-level:** Debug WHERE issues occur (e.g., retriever latency)
- **System-level:** Show WHAT is broken overall (e.g., end-to-end latency)

---

### Q: What's the difference between aggregate statistics and detailed logs?
**A:** 
- **Aggregate stats:** Trends over time (avg latency, throughput) — shows drift/regressions
- **Detailed logs:** Individual request traces — debug specific failures

---

## Lesson 03: Custom Evaluation Datasets

### Q: What is a custom evaluation dataset?
**A:** A collection of **actual production prompts** your system received, plus journey data (retrieved docs, latency, user feedback) — enables debugging by topic and testing redesigns on real-world prompts.

---

### Q: What is the continuous improvement flywheel?
**A:** **Observe** (log production prompts) → **Evaluate** (cluster by topic, find weak spots) → **Experiment** (test redesigns on logged prompts) → **Deploy** (push changes) → Repeat.

---

### Q: How do you cluster prompts by topic?
**A:** 
1. Embed all prompts with same embedding model used for retrieval
2. Run clustering algo (k-means with k=10, or HDBSCAN auto-discovery)
3. Label clusters manually (top prompts per cluster)
4. Analyze performance by cluster (latency, recall, satisfaction)

---

## Lesson 04: Quantization

### Q: What is quantization?
**A:** Compression for LLMs and embedding vectors — replaces high-precision data (32-bit/16-bit) with lower-precision (8-bit/4-bit/1-bit) → smaller, cheaper, faster, with small quality drop.

---

### Q: What are the trade-offs for 8-bit quantization?
**A:** 
- **LLMs:** 50% size reduction, 1-3% quality drop, much faster inference
- **Vectors:** 4× smaller (32-bit → 8-bit), 2-3% recall drop, faster search

---

### Q: What are Matryoshka embedding models?
**A:** Embeddings where **dimensions are sorted by information density** — first 100 dims = 80% of info, last 900 dims = less critical. Allows flexible dim usage: use first 100 for speed, full 1000 for quality, hybrid = best.

---

### Q: What's the hybrid Matryoshka strategy?
**A:** 
1. **First pass:** Retrieve with first 100 dims (fast, cheap, 80% quality)
2. **Rescore:** Pull full 1000 dims from storage, rescore top-K
3. **Result:** Speed of 100-dim search + quality of 1000-dim ranking

---

## Lesson 05: Cost vs Quality

### Q: What are the two biggest costs in RAG systems?
**A:** 
1. **LLM** (pay per token — input + output)
2. **Vector database** (RAM is expensive, needed for fast search)

---

### Q: What are the three vector database storage tiers?
**A:** 
- **RAM** — fastest, most expensive (HNSW index MUST be here)
- **Disk (SSD)** — medium speed/cost (frequently accessed docs)
- **Cloud object storage** — slowest, cheapest (rarely accessed docs, archival)

---

### Q: What is multi-tenancy and why is it important for cost?
**A:** Organize docs by user/org → load tenant data into RAM only when active → massive savings (not paying for 1M docs in RAM 24/7, only ~10k active users at a time).

---

## Lesson 06: Latency vs Quality

### Q: Where does 70-80% of RAG latency come from?
**A:** **LLM generation** (transformer-based, auto-regressive token-by-token generation). Vector search is fast (2-5%), reranker is medium (10-15%).

---

### Q: What are the three strategies to optimize core LLM latency?
**A:** 
1. **Use smaller/quantized models** (fewer params = faster)
2. **Router LLM** (route simple queries to fast model, complex to large model)
3. **Caching** (for repeated prompts, return cached response instantly or personalize with small LLM)

---

### Q: What's the optimization priority order for latency?
**A:** **Step 1:** Core LLM (biggest bottleneck) → **Step 2:** Other transformers (query rewriter, reranker, router) → **Step 3:** Retriever (already fast, use binary quantization or sharding if needed).

---

## Lesson 07: Security

### Q: What are the 3 ways knowledge base data can leak?
**A:** 
1. **Direct prompt injection** — user crafts clever prompt, LLM quotes sensitive data
2. **Cloud LLM providers** — augmented prompt sent to external API, data leaves your control
3. **Database breach** — hacker accesses DB, reconstructs text from vectors

---

### Q: What's the difference between metadata filtering and multi-tenancy for security?
**A:** 
- **Metadata filtering (❌ insecure):** All docs in one tenant, filter by metadata tags — single point of failure
- **Multi-tenancy (✅ secure):** Physically separate tenants by role/org — even if one tenant breached, others safe

---

### Q: Why can't you encrypt dense vectors in a vector database?
**A:** **ANN algorithms (HNSW) need unencrypted vectors** to calculate distances in RAM for fast search. You CAN encrypt chunk text (decrypt when building prompt), but vectors must stay decrypted during search.

---

### Q: What is the vector reconstruction attack?
**A:** Emerging threat where hackers can **reverse-engineer original text from dense vectors** using experimental techniques. High barrier (need DB access + cutting-edge research), but possible. Defenses under research: add noise, transformations, dimensionality reduction (all reduce performance).

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

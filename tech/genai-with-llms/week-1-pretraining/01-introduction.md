# 01 · Introduction - Week 1

> **TL;DR:** Week 1 covers two major topics: transformer architecture (why LLMs work) and GenAI project lifecycle (how to plan your projects).

---

## Week 1 Preview

![Week 1 Topics](assets/01-week1-intro.svg)

---

## Topic 1: Transformer Architecture

**"Attention Is All You Need" (2017)** — the paper that changed everything.

### Why Transformers?

Before transformers, we had **RNNs** (Recurrent Neural Networks):
- Processed text **sequentially** (word by word)
- Slow and hard to parallelize
- Forgot earlier words in long sequences

**Transformers changed the game:**

| RNNs | Transformers |
|------|-------------|
| Sequential processing | Parallel processing |
| Forget long context | Attention sees all |
| Slow on GPUs | Scales massively |

### What You'll Learn

- **Self-attention:** How each word relates to every other word
- **Multi-headed attention:** Multiple perspectives on relationships
- **Why it scales:** GPU parallelization made it practical

### Beyond Text

Transformers aren't just for language:
- **Vision Transformers (ViT)** — images
- **Audio Transformers** — speech, music
- **Multimodal** — text + images together

---

## Topic 2: GenAI Project Lifecycle

When building with LLMs, you face key decisions:

```
1. Use existing model or pre-train from scratch?
   └── Most: use existing foundation model

2. Fine-tune for your data?
   └── Often yes, for specific tasks

3. What model size?
   └── Depends on task complexity

4. Evaluate and deploy
   └── Benchmarks, optimization, production
```

### Model Size Guidance

| Task Type | Recommended Size | Example |
|-----------|------------------|---------|
| Single task | 1-30B | Summarization, customer chatbot |
| Multi-task | 10-100B | Domain-specific assistant |
| General knowledge | 100B+ | History, code, science, philosophy |

**Surprise:** Small models can be fantastic for specific use cases!

---

## Week 1 Coverage

| Lesson | Topic |
|--------|-------|
| 02-03 | Generative AI & LLM Use Cases |
| 04-06 | Transformer Architecture Deep Dive |
| 07-08 | Prompting & Generative Config |
| 09 | GenAI Project Lifecycle |
| 10-14 | Pre-training & Scaling Laws |

---

## Key Insights from Instructors

> *"After the transformer paper, I thought 'I get the math equation, but what's it actually doing?' It took a long time to finally go 'okay, this is why it works.'"* — Andrew Ng

> *"Attention had been around, but transformers made it work in a massively parallel way — that's what made it scale on modern GPUs."* — Mike Chambers

---

## Lab Preview

**Lab 1: Dialogue Summarization**

- Use FLAN-T5 to summarize conversations
- Compare different prompts
- Explore inference parameters
- Gain intuition on improving responses

---

## Key Takeaways

1. **Transformers** = self-attention + parallelization = scale
2. **GenAI Lifecycle** = key decisions framework
3. **Model size** = match to task complexity (small can work!)
4. **This week** = foundations for everything else

# 🤖 Module 4 — LLMs & Text Generation

> Transformers se lekar prompt engineering tak — generation side of RAG! ✨

---

## 🧠 Brain — Module Overview

```mermaid
graph LR
    M4(("Module 4<br/>LLMs & Generation"))
    M4 --> TF["Transformer Architecture"]
    M4 --> SAMP["Sampling Strategies"]
    M4 --> CHOOSE["Choosing Your LLM"]
    M4 --> PE["Prompt Engineering"]
    M4 --> HALL["Hallucinations"]
    M4 --> AGENT["Agentic RAG"]
    M4 --> VSFT["RAG vs Fine-Tuning"]

    style M4 fill:#4caf50,color:#fff
```

## 📊 Progress

| # | Lesson | Confidence | Revised |
|---|--------|-----------|---------|
| 01 | [Module 4 Introduction](01-module-introduction.md) | 🟢 | — |
| 02 | [Transformer Architecture](02-transformer-architecture.md) | 🟢 | 3 SVGs |
| 03 | [LLM Sampling Strategies](03-llm-sampling-strategies.md) | 🟢 | 4 SVGs |
| 04 | [Choosing Your LLM](04-choosing-your-llm.md) | 🟢 | 3 SVGs |
| 05 | [Exploring LLM Capabilities](05-exploring-llm-capabilities.md) | 🔴 | — |
| 06 | [Prompt Engineering: Augmented Prompt](06-prompt-engineering-augmented.md) | 🟢 | 2 SVGs |
| 07 | [Prompt Engineering: Advanced Techniques](07-prompt-engineering-advanced.md) | 🟢 | 2 SVGs |
| 08 | [Prompt Engineering (Lab)](08-prompt-engineering-lab.md) | 🔴 | — |
| 09 | [Handling Hallucinations](09-handling-hallucinations.md) | 🟢 | 2 SVGs |
| 10 | [Evaluating Your LLM's Performance](10-evaluating-llm-performance.md) | 🟢 | 1 SVG |
| 11 | [Agentic RAG](11-agentic-rag.md) | 🟢 | 1 SVG |
| 12 | [RAG vs Fine-Tuning](12-rag-vs-finetuning.md) | 🟢 | 1 SVG |
| 13 | [Lab: Developing a RAG Chatbot](13-lab-rag-chatbot.md) | 🔴 | — |

**Overall confidence:** 🟡 In progress (10/13)

## 🧩 Memory Fragments
> - 🧠 LLM is the "real brains" of RAG — retriever finds, LLM understands and generates
> - 🔄 Transformer = attention + feed-forward, repeated 8-64 times for refinement
> - 👀 Attention = "which tokens should impact MY meaning?" Each token sees ALL others
> - 🎭 Multiple attention heads (8-100+) = multiple perspectives on relationships
> - 💰 Cost grows with prompt length — each token looks at every other (quadratic!)
> - 🎲 LLMs are inherently random — even with good context, might ignore it
> - 🌡️ Temperature reshapes distribution: 0=greedy, 1=original, >1=flatter/random
> - 🎯 Top-P > Top-K because it adapts to model confidence dynamically
> - 📊 5 LLM factors: size, cost, context window, speed, training cutoff
> - 📝 RAG prompt = system + history + docs + query (always query at END)
> - 📚 Few-shot = examples in prompt, reasoning models = built-in CoT (different rules!)
> - 🚫 LLMs predict probable, not true — hallucinations sound plausible!
> - 📏 RAGAS: Response Relevancy (addresses question?) + Faithfulness (grounded in docs?)
> - 🤖 Agentic RAG = multiple LLMs, each specialized for one step (router, evaluator, generator, citation)
> - 💡 Agentic = flowchart thinking. Design workflow, assign different models per node (lightweight for routing, powerful for generation)
> - 📚 RAG = knowledge injection (new info). Fine-tuning = domain adaptation (style/tone/format)
> - 🔄 Fine-tuning changes HOW model responds more than WHAT it knows — not great for teaching new facts
> - 🔧 RAG + Fine-tuning together = best combo (fine-tune for RAG specialization)

---

## 🎬 Teach Mode

| # | Lesson | What You'll Get |
|---|--------|-----------------|
| 01 | Module 4 Introduction | Module roadmap |
| 02 | Transformer Architecture | Attention mechanism, encoder-decoder |
| 03 | Sampling Strategies | Temperature, top-k, top-p |
| 04 | LLM Capabilities | What LLMs can and can't do |
| 05 | Choosing Your LLM | Model selection criteria |
| 06 | Prompt Engineering: Augmented | Building context-rich prompts |
| 07 | Prompt Engineering: Advanced | Few-shot, chain-of-thought, etc. |
| 08 | Prompt Engineering Lab | Hands-on prompt crafting |
| 09 | Hallucinations | Causes, detection, mitigation |
| 10 | Evaluating LLMs | Measuring generation quality |
| 11 | Agentic RAG | RAG + agents = dynamic retrieval |
| 12 | RAG vs Fine-Tuning | When to use which |
| 13 | Lab: RAG Chatbot | Build an end-to-end chatbot |

**Supporting:** [Flashcards](flashcards.md)

---

## 📚 Source
> 🎓 [RAG Course — Module 4](https://learn.deeplearning.ai/courses/retrieval-augmented-generation) — DeepLearning.AI

## 🔗 Connected Topics
> ← [Module 3: Vector Databases](../module-3-ir-vector-databases/) · → [Module 5: RAG in Production](../module-5-rag-production/) · [Agentic AI](../../agentic-ai/)

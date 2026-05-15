# 🃏 LLMs & Text Generation Flashcards

> From: module-4-llms-text-generation/
> Last updated: 2026-05-15

---

## Module Introduction (Lesson 01)

<details>
<summary>❓ What is the LLM's role in a RAG system?</summary>

The LLM is the **"real brains"** of RAG. While the retriever finds and prepares relevant information, the LLM:
1. Deeply understands the retrieved context
2. Uses that information to generate responses
3. Grounds its answers in retrieved facts

Retriever = dabba kholne wala. LLM = jo actually samjhega aur jawab dega!
</details>

---

## Transformer Architecture (Lesson 02)

<details>
<summary>❓ What are the two main components of the original transformer architecture?</summary>

1. **Encoder** — Processes input text, develops deep contextual understanding. Used in embedding models (BERT, Sentence Transformers).

2. **Decoder** — Uses understanding to generate new text. Used in LLMs (GPT, Llama, Claude).

Most modern LLMs are **decoder-only** since they just care about text generation.
</details>

<details>
<summary>❓ What are the 5 steps of a token's journey through an LLM?</summary>

1. **Tokenization** — Split text into tokens
2. **Embedding + Position** — Assign "first guess" vector + position vector
3. **Attention** — Each token decides which others impact its meaning
4. **Feed-forward** — Update embeddings based on context (most parameters here!)
5. **Generation** — Create probability distribution, pick next token

Steps 3-4 repeat 8-64 times (layers) for iterative refinement.
</details>

<details>
<summary>❓ Why are initial token embeddings called "first guesses"?</summary>

Because they're **static** — the same token always gets the same initial vector regardless of context.

The attention and feed-forward layers then **refine** this guess based on surrounding tokens. "dog" in "the brown dog" becomes different from "dog" in "hot dog" after processing.
</details>

<details>
<summary>❓ What does "attention" actually compute in transformers?</summary>

Attention computes: **"Which other tokens should have the biggest impact on MY meaning?"**

Each token assigns attention weights to all other tokens. Example: "dog" might assign:
- 70% to "brown" (describing word)
- 20% to "sat" (action)
- 10% distributed across others
</details>

<details>
<summary>❓ Why do LLMs have multiple attention heads?</summary>

Each head specializes in **different types of relationships**:
- One head tracks object-description relations
- Another tracks spatial relationships
- Others learn abstract patterns during training

Multiple perspectives = richer understanding.
- Small models: 8-16 heads
- Large models: 100+ heads
</details>

<details>
<summary>❓ Where does the "world knowledge" live in a transformer?</summary>

In the **feed-forward layers** — the biggest part of the LLM with the most parameters.

The feed-forward phase takes each token's embedding + attention and generates updated vectors informed by the model's learned knowledge.
</details>

<details>
<summary>❓ How does token generation work after all the attention/feed-forward processing?</summary>

1. Generate a **probability distribution** over all tokens in vocabulary
2. **Pick one token** from this distribution (weighted random)
3. **Append** the chosen token to the prompt
4. **Repeat** the entire process for the next token
5. Stop when token limit reached OR end-of-completion token generated

Early random choices influence later ones!
</details>

<details>
<summary>❓ Why does cost grow with prompt length in transformers?</summary>

Each token must examine **every other token** to compute attention (quadratic complexity):
- 100 tokens → 10,000 attention comparisons
- 1000 tokens → 1,000,000 comparisons

This is why most RAG system costs come from running the transformer, not the retriever.
</details>

<details>
<summary>❓ Based on transformer architecture, why does RAG actually work?</summary>

1. **Attention mechanism** — LLM can connect query tokens to retrieved document tokens
2. **Feed-forward layers** — Contain world knowledge to reason about content
3. **Iterative refinement** — Deep understanding develops through multiple layers

The LLM **genuinely comprehends** injected context — it's not just keyword matching!
</details>

<details>
<summary>❓ What's the key warning about LLMs despite their understanding capabilities?</summary>

LLMs are **inherently random**. Even with meaningful information in the prompt, they may randomly choose NOT to generate text based on that information.

This means:
- Need to control randomness (sampling strategies)
- Must confirm LLM grounds answers in retrieved information
- RAG helps but doesn't eliminate hallucination risk
</details>

---

## LLM Sampling Strategies (Lesson 03)

<details>
<summary>❓ What does an LLM actually output at each generation step?</summary>

A **probability distribution** over the entire vocabulary (~100,000 tokens).

Not text — PROBABILITIES. Sampling strategies decide HOW to pick one token from these probabilities.
</details>

<details>
<summary>❓ What does temperature control in LLM generation?</summary>

Temperature controls the **shape** of the probability distribution:
- **Temp 0** → Spike at highest prob token (greedy/deterministic)
- **Temp 1** → Original distribution (balanced)
- **Temp >1** → Flatter distribution (more random)

Formula: `softmax(logits / temperature)`
</details>

<details>
<summary>❓ What's the difference between Top-K and Top-P sampling?</summary>

| Method | Cutoff Rule | Behavior |
|--------|-------------|----------|
| **Top-K** | Fixed count (K=5) | Always exactly K tokens |
| **Top-P** | Cumulative prob (P=0.9) | Adapts to confidence |

**Top-P wins:** Fewer tokens when confident (peaked dist), more when uncertain (flat dist).
</details>

<details>
<summary>❓ What's greedy decoding and when to use it?</summary>

**Greedy decoding** = Always pick the highest probability token (temperature = 0).

Use for:
- Code generation
- Factual Q&A
- Data extraction
- Anything needing **deterministic** output

Downside: Can get stuck in repetitive loops.
</details>

<details>
<summary>❓ What do repetition penalty and logit bias control?</summary>

Both are **token-specific** controls:

| Control | What | Use Case |
|---------|------|----------|
| **Repetition penalty** | Reduce prob of already-used tokens | Prevent loops |
| **Logit bias** | Permanently adjust specific tokens | Content filtering, force/block words |

Repetition = dynamic (changes per generation). Logit bias = static (same every time).
</details>

<details>
<summary>❓ What are recommended sampling settings for RAG applications?</summary>

```python
{
    "temperature": 0.5-0.7,  # Lower = more factual
    "top_p": 0.9,            # Avoid tail tokens
    "repetition_penalty": 1.1-1.2  # Mild loop prevention
}
```

For factual Q&A: temp 0.3-0.5
For creative: temp 0.8-1.0
</details>

---

## Choosing Your LLM (Lesson 04)

<details>
<summary>❓ What are the 5 quantifiable characteristics for comparing LLMs?</summary>

| Factor | Range | Trade-off |
|--------|-------|-----------|
| **Model Size** | 1B-500B+ params | Larger = more capable but expensive |
| **Cost** | $0.15-$75/M tokens | Output 4-5x more than input |
| **Context Window** | 4K-1M+ tokens | Bigger = more docs, still pay per token |
| **Speed** | TTFT + TPS | Critical for real-time apps |
| **Training Cutoff** | Date in training data | RAG compensates for old cutoffs |

</details>

<details>
<summary>❓ What are the 3 types of LLM quality benchmarks?</summary>

1. **Automated** — Code validates answers (MMLU, HumanEval)
2. **Human-evaluated** — Humans pick preferred response (LLM Arena, ELO ranking)
3. **LLM-as-Judge** — One LLM rates another (cheap but biased!)

Warning: LLM judges prefer their own family — GPT prefers GPT, Gemini prefers Gemini.
</details>

<details>
<summary>❓ What is benchmark saturation and why does it matter?</summary>

**Saturation** = When all models score ~100% on a benchmark, it can no longer differentiate quality.

Pattern:
1. New benchmark → models score low
2. Few years → all models match human experts
3. Benchmark useless → need harder benchmarks
4. Cycle repeats

**Takeaway:** Newer models almost always outperform older ones. Plan for replacement!
</details>

<details>
<summary>❓ What is data contamination in LLM benchmarks?</summary>

If benchmark questions were in the model's training data:
- Model "memorized" the answers
- Scores artificially inflated
- Real-world performance doesn't match

**Check:** Does benchmark score align with actual developer experience?
</details>

---

## Prompt Engineering: Augmented Prompt (Lesson 06)

<details>
<summary>❓ What are the 3 message roles in the OpenAI messages format?</summary>

| Role | Purpose |
|------|---------|
| **system** | High-level instructions, behavior rules, personality |
| **user** | Prompts sent by the human |
| **assistant** | Previous LLM responses |

**Key insight:** LLMs don't "remember" — the ENTIRE conversation is sent every time!
</details>

<details>
<summary>❓ What are the 4 components of a RAG prompt template?</summary>

1. **System prompt** — Behavioral guidance (can be 1000+ words!)
2. **Conversation history** — Previous user/assistant messages
3. **Retrieved documents** — Top-K chunks from retriever
4. **User query** — Current question (always at END!)

Order matters: System → History → Docs → Query
</details>

<details>
<summary>❓ What should a good RAG system prompt include?</summary>

```
1. Role definition
2. Knowledge cutoff + current date
3. RAG-specific instructions:
   - Use ONLY retrieved documents
   - Cite sources as [DOC X]
   - Admit when info is missing
4. Tone and style preferences
5. Safety constraints
```

System prompts can be multiple pages long!
</details>

---

## Advanced Prompt Engineering (Lesson 07)

<details>
<summary>❓ What is in-context learning and what are its two variants?</summary>

**In-context learning** = Adding example Q&As to the prompt to teach the LLM desired structure and tone.

| Variant | Definition |
|---------|------------|
| **Few-shot** | Many examples in prompt |
| **One-shot** | Just one example |

Implementation: Hardcode examples OR use RAG to retrieve similar past conversations!
</details>

<details>
<summary>❓ What is chain-of-thought prompting and why does it improve accuracy?</summary>

**Chain-of-thought** = Give the LLM a "scratchpad" to think before answering.

```
<scratchpad>
Option 1: Could be X because...
Actually, Z makes more sense...
</scratchpad>
Final answer: Z
```

**Why it works:**
- Forces LLM to plan before answering
- Breaks complex problems into steps
- Makes reasoning errors traceable
</details>

<details>
<summary>❓ How do reasoning models differ from regular LLMs in prompting?</summary>

Reasoning models (o1, DeepSeek-R1) have **built-in** chain-of-thought.

| Do | Don't |
|----|-------|
| Clear goals | "Think step-by-step" (they already do!) |
| Strict formats | Few-shot examples (confuses them) |
| Full context dump | Over-engineering prompts |

Trade-off: Slower + more expensive, but better for complex reasoning.
</details>

<details>
<summary>❓ What are 3 context pruning strategies for multi-turn conversations?</summary>

1. **Keep last N messages** — Drop old turns (e.g., keep last 5)
2. **Summarize old messages** — Use LLM to compress older history
3. **Drop reasoning tokens** — Keep only response tokens in history (for reasoning models)

Also: Only include RAG docs for current query, not all previous queries!
</details>

---

## Handling Hallucinations (Lesson 09)

<details>
<summary>❓ Why do LLMs hallucinate?</summary>

LLMs predict **probable** text, not **true** text. They can't tell the difference!

- Probable ≠ True
- Hallucinations sound plausible (harder to detect than nonsense)
- They erode user trust over time

**Types:** Wrong details, invented facts, denial of real facts.
</details>

<details>
<summary>❓ What are the 3 strategies to reduce hallucinations in RAG?</summary>

1. **RAG Grounding** — System prompt: "Only make factual claims based on retrieved info"
2. **Citation Generation** — Force LLM to cite sources [1], [2], etc.
3. **Benchmarks (ALCE)** — Test fluency, correctness, citation quality

**RAG itself is the single most effective step!**
</details>

<details>
<summary>❓ What is ContextCite and why use it?</summary>

**ContextCite** = External system that attributes each sentence to retrieved documents.

| Feature | Purpose |
|---------|---------|
| Sentence attribution | Links claims to docs |
| "No source" tags | Flags unsupported claims |
| Similarity scores | Measures grounding strength |

**Why?** LLMs can hallucinate citations too — external systems more reliable.
</details>

---

## Evaluating LLM Performance (Lesson 10)

<details>
<summary>❓ What is RAGAS Response Relevancy and how is it calculated?</summary>

**Question:** Is the response relevant to the user's prompt?

1. Take RAG response
2. Evaluator LLM generates sample prompts that could lead to this response
3. Embed original + sample prompts
4. Calculate cosine similarity
5. Average = Relevancy score

**Note:** Doesn't check factual accuracy — just relevance!
</details>

<details>
<summary>❓ What is RAGAS Faithfulness and why is it the hallucination detector?</summary>

**Question:** Is response grounded in retrieved documents?

1. LLM extracts all factual claims from response
2. Check each claim against retrieved docs
3. Calculate: supported claims / total claims = Faithfulness

| Score | Meaning |
|-------|---------|
| 100% | All claims grounded |
| Low | LLM making stuff up |

**Low faithfulness = hallucination detected!**
</details>

<details>
<summary>❓ Why do LLM evaluation metrics rely on LLM-as-judge?</summary>

LLM responsibilities in RAG are **subjective**:
- Did it respond clearly?
- Did it incorporate relevant info?
- Did it cite appropriately?
- Did it ignore noise?

**Can't measure objectively** → Use other LLMs to assess quality. All RAGAS metrics use LLM calls at some point.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

# 🃏 LLMs & Text Generation Flashcards

> From: module-4-llms-text-generation/
> Last updated: 2026-05-04

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

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

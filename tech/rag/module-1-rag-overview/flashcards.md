# 🃏 RAG Overview Flashcards

> From: module-1-rag-overview/
> Last updated: 2026-04-04

---

<div class="flashcard-deck" markdown>

<details class="flashcard" markdown>
<summary>What is RAG in one sentence?</summary>

**Retrieval Augmented Generation** = retrieve relevant info from a knowledge base and inject it into the LLM's prompt so it can generate accurate, grounded answers using data it wasn't trained on.

> LLM ko Google de do — pehle dhundo, phir jawab do! 🔍
</details>

<details class="flashcard" markdown>
<summary>What do Retrieval, Augmented, and Generation each mean?</summary>

- **Retrieval** = collecting relevant info from a knowledge base
- **Augmented** = enhancing the prompt by adding retrieved info
- **Generation** = LLM reasons over augmented prompt → generates answer

> Naam hi recipe hai! Dhundo → daalo → jawab do 🍳
</details>

<details class="flashcard" markdown>
<summary>What are the 3 components of a RAG system?</summary>

| Component | Role |
|-----------|------|
| **Knowledge Base** | Trusted, relevant, possibly private info |
| **Retriever** | Searches KB, finds most relevant docs |
| **LLM** | Receives augmented prompt → generates response |
</details>

<details class="flashcard" markdown>
<summary>What is the "key insight" of RAG in the simplest terms?</summary>

**Just put it in the prompt!** Modify the prompt before sending to the LLM — add relevant info from your knowledge base so it has what it needs.

> RAG = open-book exam. Cheat sheet legally de do! 📋😂
</details>

<details class="flashcard" markdown>
<summary>What 3 types of info are LLMs missing that RAG fills?</summary>

| Type | Example |
|------|---------|
| **Private data** | Company policies, internal docs |
| **Real-time data** | Today's news, current events |
| **Specialized data** | Niche domain knowledge |

RAG fills all three by retrieving at query time.
</details>

<details class="flashcard" markdown>
<summary>Traditional RAG vs Agentic RAG — what's the difference?</summary>

| | Traditional | Agentic |
|--|-------------|---------|
| **Decides retrieval** | Human engineer | AI agent |
| **Strategy** | Fixed pipeline | Dynamic, can retry |
| **Error handling** | Fails silently | Routes back & fixes |

> GPS fixed route vs GPS that recalculates! 🛣️
</details>

<details class="flashcard" markdown>
<summary>Why can't you just put ALL documents in the prompt?</summary>

Two problems:

1. **Context window limit** — LLMs have max token capacity
2. **Computational cost** — longer prompts = more computation per token generated

RAG retrieves only the **most relevant** pieces → efficient + focused.
</details>

<details class="flashcard" markdown>
<summary>Name 5 ways RAG is getting better over time</summary>

1. 📉 Lower hallucination rates
2. 🧠 Reasoning models for complex Q&A
3. 📏 Larger context windows
4. 📄 Better document extraction (PDFs, slides)
5. 🤖 Agentic RAG — AI decides what to retrieve
</details>

<details class="flashcard" markdown>
<summary>Name the 5 major RAG application categories</summary>

| App | Knowledge Base |
|-----|---------------|
| 💻 **Code Gen** | Your own codebase |
| 🏢 **Company Chatbots** | Products, policies, FAQs |
| ⚕️ **Healthcare/Legal** | Case files, journals |
| 🌐 **AI Web Search** | The entire internet |
| 👤 **Personal Assistants** | Texts, emails, calendar |
</details>

<details class="flashcard" markdown>
<summary>Why is RAG the ONLY viable option for legal/medical LLM apps?</summary>

1. **Precision imperative** — wrong answers = real consequences
2. **Private data** — case files, patient records can't be in training data
3. **Recent data** — latest journals, new case law not available at training time

RAG is the only way to access this while keeping it private and current.
</details>

<details class="flashcard" markdown>
<summary>How does AI web search (ChatGPT/Perplexity) relate to RAG?</summary>

It **IS** a RAG system — the entire internet is the knowledge base.

**Traditional search** = retriever only (returns URLs)
**AI search** = retriever + LLM summarizer

Same RAG pattern applied at internet scale.
</details>

</div>

---

> 💡 **Revision tip:** Try to answer each card OUT LOUD before flipping.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

# 🃏 RAG Overview Flashcards

> From: module-1-rag-overview/
> Last updated: 2026-04-04

---

### 📌 Core RAG Concepts

<details>
<summary>❓ What is RAG in one sentence?</summary>

**Retrieval Augmented Generation** = retrieve relevant information from a knowledge base and inject it into the LLM's prompt so it can generate accurate, grounded answers using data it wasn't trained on.

> LLM ko Google de do — pehle dhundo, phir jawab do! 🔍
</details>

<details>
<summary>❓ Why do LLMs need RAG? What 3 types of info are they missing?</summary>

LLMs only know their training data. They're missing:

| Type | Example |
|------|---------|
| **Private data** | Company policies, internal docs, confidential databases |
| **Real-time data** | Today's news, current events, live prices |
| **Specialized data** | Niche domain knowledge not widely available online |

RAG gives them access to all of this at query time.
</details>

<details>
<summary>❓ What's the difference between Traditional RAG and Agentic RAG?</summary>

| | Traditional RAG | Agentic RAG |
|--|----------------|-------------|
| **Who decides retrieval?** | Human engineer (hardcoded) | AI agent (dynamic) |
| **Strategy** | Fixed: query → retrieve → generate | Flexible: retrieve → evaluate → maybe retry |
| **Error handling** | Fails silently | Routes back, tries different approach |

> Traditional = GPS fixed route. Agentic = GPS that recalculates on traffic! 🛣️
</details>

<details>
<summary>❓ Why can't you just put ALL documents in the LLM prompt instead of using RAG?</summary>

Two problems:
1. **Context window limit** — LLMs have max token capacity
2. **Computational cost** — longer prompts = more computation (model scans every token before generating each new one)

RAG retrieves only the **most relevant** pieces → efficient + focused.
</details>

<details>
<summary>❓ Name 5 ways RAG is getting better over time</summary>

1. 📉 **Lower hallucination rates** — newer models stay grounded in context
2. 🧠 **Reasoning models** — tackle complex questions over retrieved data
3. 📏 **Larger context windows** — less chunking pressure
4. 📄 **Better doc extraction** — PDFs, slides, images → usable text
5. 🤖 **Agentic RAG** — AI decides what/when/how to retrieve
</details>

### 📌 RAG Applications

<details>
<summary>❓ Name the 5 major RAG application categories</summary>

| # | Application | Knowledge Base |
|---|-------------|---------------|
| 1 | **Code Generation** | Your own codebase (classes, functions, style) |
| 2 | **Company Chatbots** | Products, policies, FAQs, guidelines |
| 3 | **Healthcare / Legal** | Case files, medical journals, private records |
| 4 | **AI Web Search** | The entire internet |
| 5 | **Personal Assistants** | Texts, emails, contacts, calendar, documents |

</details>

<details>
<summary>❓ Why might RAG be the ONLY viable option for legal/medical LLM applications?</summary>

1. **Precision imperative** — wrong answers = real consequences (liability, patient harm)
2. **Private data** — case files, patient records can't be in LLM training data
3. **Recent data** — latest medical journals, new case law not in training data

RAG is the only way to give LLMs access to this information while keeping it private and current.
</details>

<details>
<summary>❓ How does an AI web search (ChatGPT/Perplexity) relate to RAG?</summary>

It IS a RAG system — the **entire internet** is the knowledge base. Traditional search = retriever only (returns URLs). AI search = retriever + LLM summarizer. Same RAG pattern applied at internet scale.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

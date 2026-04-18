# 🃏 RAG Overview Flashcards

> From: module-1-rag-overview/
> Last updated: 2026-04-18

---

### 📌 Core RAG Concepts

<details markdown="1">
<summary>❓ What is RAG in one sentence?</summary>

**Retrieval Augmented Generation** = retrieve relevant information from a knowledge base and inject it into the LLM's prompt so it can generate accurate, grounded answers using data it wasn't trained on.

> LLM ko Google de do — pehle dhundo, phir jawab do! 🔍
</details>

<details markdown="1">
<summary>❓ What do Retrieval, Augmented, and Generation each mean?</summary>

- **Retrieval** = collecting relevant info from a knowledge base
- **Augmented** = enhancing the prompt by adding retrieved info
- **Generation** = LLM reasons over augmented prompt → generates answer

> Naam hi recipe hai! Dhundo → daalo → jawab do 🍳
</details>

<details markdown="1">
<summary>❓ What are the 3 components of a RAG system?</summary>

| Component | Role |
|-----------|------|
| **Knowledge Base** | Trusted, relevant, possibly private information |
| **Retriever** | Searches KB, finds most relevant docs for query |
| **LLM** | Receives augmented prompt → generates response |
</details>

<details markdown="1">
<summary>❓ What is the "key insight" of RAG in the simplest terms?</summary>

**Just put it in the prompt!** Modify the prompt before sending to the LLM — add relevant info from your knowledge base so it has what it needs.

> RAG = open-book exam. Cheat sheet legally de do! 📋😂
</details>

<details markdown="1">
<summary>❓ Why do LLMs need RAG? What 3 types of info are they missing?</summary>

LLMs only know their training data. They're missing:

| Type | Example |
|------|---------|
| **Private data** | Company policies, internal docs, confidential databases |
| **Real-time data** | Today's news, current events, live prices |
| **Specialized data** | Niche domain knowledge not widely available online |

RAG gives them access to all of this at query time.
</details>

<details markdown="1">
<summary>❓ What's the difference between Traditional RAG and Agentic RAG?</summary>

| | Traditional RAG | Agentic RAG |
|--|----------------|-------------|
| **Who decides retrieval?** | Human engineer (hardcoded) | AI agent (dynamic) |
| **Strategy** | Fixed: query → retrieve → generate | Flexible: retrieve → evaluate → maybe retry |
| **Error handling** | Fails silently | Routes back, tries different approach |

> Traditional = GPS fixed route. Agentic = GPS that recalculates on traffic! 🛣️
</details>

<details markdown="1">
<summary>❓ Why can't you just put ALL documents in the LLM prompt instead of using RAG?</summary>

Two problems:
1. **Context window limit** — LLMs have max token capacity
2. **Computational cost** — longer prompts = more computation (model scans every token before generating each new one)

RAG retrieves only the **most relevant** pieces → efficient + focused.
</details>

<details markdown="1">
<summary>❓ Name 5 ways RAG is getting better over time</summary>

1. 📉 **Lower hallucination rates** — newer models stay grounded in context
2. 🧠 **Reasoning models** — tackle complex questions over retrieved data
3. 📏 **Larger context windows** — less chunking pressure
4. 📄 **Better doc extraction** — PDFs, slides, images → usable text
5. 🤖 **Agentic RAG** — AI decides what/when/how to retrieve
</details>

### 📌 RAG Applications

<details markdown="1">
<summary>❓ Name the 5 major RAG application categories</summary>

| # | Application | Knowledge Base |
|---|-------------|---------------|
| 1 | **Code Generation** | Your own codebase (classes, functions, style) |
| 2 | **Company Chatbots** | Products, policies, FAQs, guidelines |
| 3 | **Healthcare / Legal** | Case files, medical journals, private records |
| 4 | **AI Web Search** | The entire internet |
| 5 | **Personal Assistants** | Texts, emails, contacts, calendar, documents |

</details>

<details markdown="1">
<summary>❓ Why might RAG be the ONLY viable option for legal/medical LLM applications?</summary>

1. **Precision imperative** — wrong answers = real consequences (liability, patient harm)
2. **Private data** — case files, patient records can't be in LLM training data
3. **Recent data** — latest medical journals, new case law not in training data

RAG is the only way to give LLMs access to this information while keeping it private and current.
</details>

<details markdown="1">
<summary>❓ How does an AI web search (ChatGPT/Perplexity) relate to RAG?</summary>

It IS a RAG system — the **entire internet** is the knowledge base. Traditional search = retriever only (returns URLs). AI search = retriever + LLM summarizer. Same RAG pattern applied at internet scale.
</details>

### 📌 RAG Architecture

<details markdown="1">
<summary>❓ What are the 5 steps in the RAG pipeline (in order)?</summary>

| Step | What Happens |
|------|-------------|
| 1. Route | Prompt goes to the **retriever** first, not the LLM |
| 2. Query KB | Retriever searches the knowledge base for relevant docs |
| 3. Augment | Original prompt + retrieved docs = **augmented prompt** |
| 4. Generate | Augmented prompt sent to LLM → generates response |
| 5. Respond | User gets the answer (slightly more latency) |

From the user's POV, it's the same: type prompt → get response.
</details>

<details markdown="1">
<summary>❓ What is the ONLY architectural difference between using an LLM directly vs a RAG system?</summary>

The **retriever**. In a RAG system, the prompt is first routed to a retriever that searches the knowledge base, fetches relevant documents, and these are combined with the original prompt into an augmented prompt. The user experience stays identical.
</details>

<details markdown="1">
<summary>❓ Name 5 advantages of RAG</summary>

| # | Advantage | One-liner |
|---|-----------|-----------|
| 1 | **Injects missing knowledge** | Makes info available the LLM was never trained on |
| 2 | **Reduces hallucinations** | Retrieved context grounds the response |
| 3 | **Easy to keep up-to-date** | Update KB like a database, no retraining needed |
| 4 | **Enables source citations** | Citation info flows through to the response |
| 5 | **Focuses LLM on generation** | Retriever = fact-finder, LLM = writer (separation of concerns) |
</details>

<details markdown="1">
<summary>❓ Why is updating a RAG knowledge base better than retraining the LLM?</summary>

Retraining = **costly, time-consuming**, needs massive compute. Updating KB = update entries in a database. Once **indexed**, changes are immediately available. Same result (current info), fraction of the effort.
</details>

<details markdown="1">
<summary>❓ How does RAG enable source citations?</summary>

Citation info (article title, URL, author) can be included in the augmented prompt. The LLM then passes this info through to its response. Readers can verify claims and dig deeper. RAG makes responses **verifiable**, not just accurate.
</details>

<details markdown="1">
<summary>❓ What does "focuses LLM on generation" mean as a RAG advantage?</summary>

Separation of concerns: the **retriever** handles fact-finding and filtering from a vast world of information. The **LLM** focuses purely on writing a good response. Each component does what it's best at — like a researcher + writer team.
</details>

### 📌 LLM Foundations (Lesson 05)

<details markdown="1">
<summary>❓ What does an LLM actually do under the hood? (5-step cycle)</summary>

1. **Read** entire completion so far (prompt + generated tokens)
2. **Understand** relationships between words + overall meaning
3. **Score** every token in vocabulary → probability distribution
4. **Randomly sample** one token from that distribution
5. **Append** to completion → repeat from step 1

It's literally autocomplete — but with billions of parameters and deep contextual understanding.
</details>

<details markdown="1">
<summary>❓ What are tokens, and why don't LLMs just use whole words?</summary>

**Tokens** = pieces of words. Simple words (`London`, `door`) get one token. Compound words (`programmatically` → `program` + `matically`) split into multiple. Punctuation gets its own tokens too.

Why? A vocabulary of 10K–100K tokens can build **any possible word** from smaller pieces — no need for a dedicated token per word. Flexibility over brute-force.
</details>

<details markdown="1">
<summary>❓ Why does the same prompt give different answers each time?</summary>

Because token selection is **random sampling** from a probability distribution, not always picking the highest-probability token. "Shining" might be 80% likely, but "rising" (10%) or even "exploding" (0.01%) could be chosen. Randomness + autoregressive behavior = different completions every time.
</details>

<details markdown="1">
<summary>❓ What does "autoregressive" mean for LLMs?</summary>

**Self-influencing.** Each generated token becomes part of the context for the NEXT token. Once the LLM picks "shining," it continues with "in the sky." If it had picked "warming," it would continue with "our faces." One early choice sets the direction for the entire completion.

> Goa plan bana liya toh hotel, flight, beach sab Goa ke. Manali bol diya hota toh pura trip alag! 🏖️ vs 🏔️
</details>

<details markdown="1">
<summary>❓ How are LLMs trained? (3 key points)</summary>

1. Shown **incomplete text** from training data (trillions of tokens, mostly from open internet)
2. Tries to **predict the next word** → compares against actual
3. **Updates billions of parameters** based on prediction accuracy

Before training = gibberish. After training = learns factual info + linguistic styles from training data.
</details>

<details markdown="1">
<summary>❓ Are hallucinations a malfunction?</summary>

**No.** LLMs are designed to generate **probable text, not truthful text**. "Truth" for an LLM = a probabilistically likely word sequence based on training data. When relevant info is missing (private data, recent events), the model still produces plausible-sounding but ungrounded text. Not a bug — it's the design working without the right data.
</details>

<details markdown="1">
<summary>❓ Why can't RAG just dump the entire KB into the prompt?</summary>

Two constraints:
1. **Computation** — before each new token, the model scans EVERY token in the completion. Longer prompt = more compute.
2. **Context window** — max tokens the model can process at once (older: ~4K, newer: millions).

Retriever must select only the **most relevant** pieces to stay within budget.
</details>

<details markdown="1">
<summary>❓ What LLM property makes RAG possible?</summary>

LLMs can **understand and incorporate information from the prompt** into their responses — even info NOT in their training data. RAG exploits this: inject retrieved docs into the prompt → LLM uses them → **grounded** response.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️

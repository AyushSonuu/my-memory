# 🧠 AI Expert Roadmap — Ayush Sonu

> **Identity:** AI/ML Engineer → AI Product Manager (future)
> **Philosophy:** Go deep in AI. Minimum viable SDE skills. Maximum AI depth.
> **Created:** 2026-04-18 | **Replaces:** career-roadmap-2026.md (generic SDE-heavy plan)
> **Review:** Every Sunday, 15 min

---

## 🎯 The Vision

```
NOW (2026)                    1 YEAR                      2-3 YEARS
┌──────────────┐         ┌──────────────────┐       ┌──────────────────┐
│ GenAI/Agentic│         │  Full-Stack AI   │       │   AI Product     │
│ AI Engineer  │ ──────► │  Engineer        │ ────► │   Manager        │
│ (application │         │  (ML + DL + Prod │       │   (tech depth +  │
│  layer only) │         │   + Agentic AI)  │       │    product sense) │
└──────────────┘         └──────────────────┘       └──────────────────┘

Your MOAT: Production AI exp (SAP) + Agentic AI + Eval frameworks + Product thinking
Your GAP:  Core ML/DL theory + PyTorch + CV + Fine-tuning + AI System Design
```

---

## 📊 What You Already Have vs What You Need

| ✅ Have | ❌ Need |
|---------|--------|
| Agentic AI (course + production) | ML fundamentals (regression, trees, clustering) |
| RAG (course in progress + EGDR) | Deep Learning theory (backprop, CNNs, RNNs, Transformers) |
| Agent Memory (course complete) | PyTorch (industry standard framework) |
| Eval frameworks (designed HLD+LLD) | Computer Vision (CNNs, object detection, segmentation) |
| Prompt Engineering | NLP deep (not just LLM prompting — tokenization, embeddings, seq2seq) |
| Python (strong) | Fine-tuning (LoRA, QLoRA, RLHF, DPO) |
| Product thinking (natural) | AI System Design (serving, pipelines, monitoring) |
| LangChain, LangGraph, Deep Agents | MLOps (experiment tracking, model registry, deployment) |

---

## 🗺️ The Master Plan — 5 Phases

> All courses on **DeepLearning.AI** (you have the subscription) unless noted otherwise.
> **Pace:** Phase 1 daily plan — ~2 hrs/day weekdays, ~4-5 hrs/day weekends.

### Phase 1: Foundations (Apr–Jun 2026) — 10 weeks
> *"Pehle neev, phir building. ML/DL ke bina AI Engineer nahi ban sakte."*

| # | What | Resource (DeepLearning.AI / Coursera) | Time | Priority |
|---|------|--------------------------------------|------|----------|
| 1 | **Finish RAG Course** | DeepLearning.AI — RAG (already 6/10 M1) | 3-4 weeks | 🔴 P0 |
| 2 | **ML Specialization** | Andrew Ng's ML Specialization (3 courses, Coursera) | 6-8 weeks | 🔴 P0 |
| | → Supervised Learning | Regression, classification, neural nets, decision trees | ~2 weeks | |
| | → Advanced Learning Algorithms | Neural networks, trees, advice for ML | ~2 weeks | |
| | → Unsupervised + Recommenders + RL | Clustering, anomaly detection, recommender systems | ~2 weeks | |

**Why this first:** You can't understand anything deeper without knowing gradient descent, loss functions, bias/variance, train/test splits. This is the ABCs.

**Parallel (low effort):**
- DSA: 30 min/day, LeetCode easy→medium (Arrays, Strings, HashMap)
- LLD: 1 video/week from Concept && Coding (background, low priority)

---

### Phase 2: Deep Learning + NLP (Jul–Sep 2026) — 12 weeks
> *"Ab andar jaao — neural networks ka poora duniya."*

| # | What | Resource | Time | Priority |
|---|------|----------|------|----------|
| 3 | **Deep Learning Specialization** | Andrew Ng (5 courses, Coursera — through DeepLearning.AI) | 8-10 weeks | 🔴 P0 |
| | → Neural Networks & Deep Learning | Forward/backprop, activation, initialization | ~2 weeks | |
| | → Improving Deep Neural Networks | Regularization, optimization (Adam, RMSprop), batch norm | ~2 weeks | |
| | → Structuring ML Projects | ML strategy, error analysis, transfer learning | ~1 week | |
| | → CNNs (Convolutional Neural Networks) | **Your CV knowledge** — ResNet, YOLO, object detection, neural style transfer | ~2 weeks | |
| | → Sequence Models | RNNs, LSTMs, GRUs, attention mechanism, **Transformers** | ~2 weeks | |
| 4 | **NLP Specialization** (start) | DeepLearning.AI (4 courses, Coursera) | Start here, finish in Phase 3 | 🟡 P1 |
| | → Classification & Vector Spaces | Sentiment analysis, word embeddings | ~2 weeks | |
| | → Probabilistic Models | Autocomplete, POS tagging, word2vec | ~2 weeks | |

**Why DL Spec before NLP Spec:** DL Spec teaches the ARCHITECTURES (CNNs, RNNs, Transformers) that NLP Spec then USES. Order matters.

**Parallel:**
- DSA: continuing 30 min/day (Linked Lists, Trees, Graphs)
- Alex Xu System Design Vol 1: 1 chapter/week (background reading)

---

### Phase 3: NLP + PyTorch + Fine-tuning (Oct–Dec 2026) — 12 weeks
> *"Ab tu LLMs ke andar jaayega — prompt engineering se neeche, model level pe."*

| # | What | Resource | Time | Priority |
|---|------|----------|------|----------|
| 4 | **NLP Specialization** (finish) | DeepLearning.AI (courses 3 & 4) | 4 weeks | 🔴 P0 |
| | → Sequence Models (Attention) | Seq2seq, attention, machine translation | ~2 weeks | |
| | → Attention Models (Transformers) | Full Transformer architecture, BERT, GPT, T5 | ~2 weeks | |
| 5 | **Generative AI with LLMs** | DeepLearning.AI × AWS (Coursera) | 3-4 weeks | 🔴 P0 |
| | | LLM lifecycle: pretraining, fine-tuning, RLHF, deployment | | |
| 6 | **Fine-tuning Short Courses** (pick 2-3) | DeepLearning.AI short courses | 2-3 weeks | 🟡 P1 |
| | → Fine-tuning LLMs | LoRA, QLoRA, PEFT | 1 week | |
| | → Evaluating & Debugging GenAI | Eval metrics, debugging | 1 week | |
| | → Building with Instruction-Tuned LLMs | RLHF, DPO, alignment | 1 week | |
| 7 | **PyTorch** (hands-on) | DeepLearning.AI PyTorch Professional Cert OR fast.ai | 4-6 weeks | 🟡 P1 |

**By end of Phase 3 you can:**
- Train a neural network from scratch
- Fine-tune an LLM with LoRA
- Understand Transformer architecture inside-out
- Read any PyTorch model code

---

### Phase 4: AI System Design + Production (Jan–Mar 2027) — 12 weeks
> *"Ab production mein le jaa — model banana alag, deploy karna alag."*

| # | What | Resource | Time | Priority |
|---|------|----------|------|----------|
| 8 | **Designing ML Systems** (book) | Chip Huyen — THE gold standard for AI system design | 4 weeks | 🔴 P0 |
| 9 | **MLOps Specialization** | Duke University (Coursera) — deployment, monitoring, pipelines | 4-6 weeks | 🟡 P1 |
| 10 | **AI System Design short courses** | DeepLearning.AI — pick relevant ones | 2-3 weeks | 🟡 P1 |
| | → Automated Testing for LLMOps | | | |
| | → LLMOps | | | |
| | → Efficiently Serving LLMs | Quantization, batching, KV cache | | |

**By end of Phase 4 you can:**
- Design an ML system end-to-end (data → train → deploy → monitor)
- Answer "Design a recommendation system" or "Design a RAG pipeline at scale" in interviews
- Deploy and monitor models in production

---

### Phase 5: AI Product Manager Track (Apr–Jun 2027) — 12 weeks
> *"Technical depth ho gayi. Ab product thinking formalize karo."*

| # | What | Resource | Time |
|---|------|----------|------|
| 11 | **AI Product Management Specialization** | Duke University (Coursera) | 4-6 weeks |
| 12 | **AI for Everyone** (if not done) | Andrew Ng — business/strategy perspective | 1 week |
| 13 | **Real-world PM practice** | Lead a feature at SAP end-to-end, write PRDs, own metrics | Ongoing |

---

## 📅 Simplified Timeline

```
2026
Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
├────────────┤├──────────────────┤├──────────────────┤
   PHASE 1        PHASE 2            PHASE 3
   ML Spec +      DL Spec +          NLP finish +
   RAG finish     NLP start          GenAI + PyTorch
                                     + Fine-tuning

2027
Jan  Feb  Mar  Apr  May  Jun
├──────────────────┤├──────────────────┤
    PHASE 4            PHASE 5
    AI Sys Design      AI Product
    + MLOps            Manager
    + Production
```

---

## 🔢 DSA — Minimum Viable (Background Track)

> **Not your main thing. Just enough to clear coding rounds.**

| When | What | Time |
|------|------|------|
| Daily | 1 LeetCode problem (easy/medium) | 30 min |
| Topic order | Arrays → Strings → HashMap → Linked Lists → Trees → Graphs → DP (basics) → done | |
| Target | ~150 problems by Dec 2026 | |
| Resource | NeetCode 150 (curated, no filler) | |
| Tool | Use **me** — file problems + patterns into the vault | |

---

## 📐 LLD — Light Touch (Background Track)

> **Know the patterns, don't grind for 6 months.**

| When | What | Time |
|------|------|------|
| 1x/week | Concept && Coding LLD video (YouTube, free) | 1 hr |
| Key patterns | Strategy, Observer, Factory, Builder, Singleton, Adapter, Decorator, Command | |
| Enough when | You can design a Parking Lot, BookMyShow, or Splitwise in 30 min | |
| Timeline | May–Sep 2026 (background) | |

---

## ⚡ HLD — AI-Flavored (Phase 4, Not Traditional)

> **You DON'T need "Design Twitter" style HLD. You need AI system design.**

| Traditional HLD (skip deep dive) | AI System Design (go deep) |
|----------------------------------|---------------------------|
| Design URL Shortener | Design a RAG pipeline for 10M docs |
| Design Instagram | Design a recommendation engine |
| Design WhatsApp | Design an LLM serving system with GPU optimization |
| Load balancer theory | Model A/B testing + canary deployment |
| CAP theorem | Training pipeline → eval → deploy → monitor loop |

**Light traditional HLD:** Alex Xu Vol 1 — read it cover-to-cover, 1 chapter/week. Don't grind.
**Deep AI system design:** Chip Huyen book + MLOps course. THIS is your "system design."

---

## 📊 Weekly Time Budget (Phase 1, Current)

| Block | Weekday (×5) | Weekend (×2) | Weekly |
|-------|-------------|-------------|--------|
| 🧠 AI Course (RAG → ML Spec) | 30 min commute + 1 hr evening | 2-3 hrs | **~10 hrs** |
| 🔢 DSA | 30 min morning/evening | 1.5 hrs | **~4 hrs** |
| 📐 LLD | — | 1 hr (1x) | **~1 hr** |
| 📖 Alex Xu reading | Commute/lunch gap | — | **~1-2 hrs** |
| **Total** | | | **~16-17 hrs** |

> Less than your old 26 hrs/week plan. Because **consistency > intensity**.
> *"16 honest hours > 26 fantasy hours. Har week."* 💪

---

## 🏁 End State (By Mid-2027)

When this roadmap is done, your LinkedIn reads:

```
Ayush Sonu
AI/ML Engineer | SAP

✅ ML Specialization (Andrew Ng / Stanford)
✅ Deep Learning Specialization (DeepLearning.AI)
✅ NLP Specialization (DeepLearning.AI)
✅ Generative AI with LLMs (DeepLearning.AI × AWS)
✅ PyTorch Professional Certificate
✅ RAG, Agentic AI, Agent Memory (DeepLearning.AI)
✅ 2+ years production AI at SAP (evals, agents, RAG)
✅ AI System Design (Chip Huyen + MLOps)

Building: AI products, eval frameworks, coding agents
Next: AI Product Manager
```

That profile doesn't compete with 10 lakh SDE grinders. It competes with a much smaller, much more valuable pool. 🎯

---

## 📏 Rules

1. **ONE course at a time.** No parallel course-hopping. Finish → next.
2. **Every course goes through the vault.** Transcripts → Ayra → structured notes. No passive watching.
3. **DSA and LLD are BACKGROUND.** They don't eat AI course time. Ever.
4. **Sunday review:** Check this file. Update progress. Be honest.
5. **If you miss a week, don't panic.** Shift the timeline. Don't abandon it.
6. **Phase 1 daily plan (sleep/wake) is STILL prerequisite.** No roadmap survives without a routine.

---

## 📈 Progress Tracker

### Phase 1 (Apr–Jun 2026)
- [x] RAG Module 1 Lesson 05 ✅
- [ ] RAG Course — Module 1 complete
- [ ] RAG Course — Module 2 complete
- [ ] RAG Course — Module 3 complete
- [ ] RAG Course — Module 4 complete
- [ ] RAG Course — Module 5 complete
- [ ] ML Spec — Course 1: Supervised Learning
- [ ] ML Spec — Course 2: Advanced Learning Algorithms
- [ ] ML Spec — Course 3: Unsupervised + Recommenders + RL

### Phase 2 (Jul–Sep 2026)
- [ ] DL Spec — Course 1: Neural Networks & Deep Learning
- [ ] DL Spec — Course 2: Improving DNNs
- [ ] DL Spec — Course 3: Structuring ML Projects
- [ ] DL Spec — Course 4: CNNs
- [ ] DL Spec — Course 5: Sequence Models
- [ ] NLP Spec — Course 1: Classification & Vector Spaces
- [ ] NLP Spec — Course 2: Probabilistic Models

### Phase 3 (Oct–Dec 2026)
- [ ] NLP Spec — Course 3: Sequence Models
- [ ] NLP Spec — Course 4: Attention Models
- [ ] Generative AI with LLMs
- [ ] Fine-tuning short courses (2-3)
- [ ] PyTorch Professional Certificate

### Phase 4 (Jan–Mar 2027)
- [ ] Chip Huyen — Designing ML Systems (book)
- [ ] MLOps Specialization
- [ ] AI System Design short courses

### Phase 5 (Apr–Jun 2027)
- [ ] AI Product Management Specialization
- [ ] Lead a feature end-to-end at SAP

### Background Tracks
- [ ] DSA: 50 problems
- [ ] DSA: 100 problems
- [ ] DSA: 150 problems
- [ ] LLD: Core 8 patterns covered
- [ ] Alex Xu Vol 1: Read complete

---

> *"Jack of all trades, master of none — but if you master AI, you won't need to be jack of anything else."* 🧠🔥

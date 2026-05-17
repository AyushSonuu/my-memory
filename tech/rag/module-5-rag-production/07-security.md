# 07 — Security in RAG Systems

> Knowledge base mein sensitive data hai? Lock karo properly — authentication, multi-tenancy, encryption! 🔒🛡️

---

## Why Security Matters for RAG

**The core problem:**
- You built RAG because you have **private/proprietary information**
- This data was intentionally **kept off the open web**
- LLMs were never trained on it (that's the point!)
- **But now:** RAG system accesses it → security becomes critical

> 💡 **RAG = vault ka darwaza.** Vault mein valuable data hai. Door lock karna bhool gaye toh koi bhi andar ghus jayega! 🚪💎

---

## Three Ways Knowledge Base Data Can Leak

![Security Attacks and Defenses](assets/07-security-attacks-defenses.svg)

### 1️⃣ Direct Prompt Injection

**The attack:**
- User submits a well-worded prompt
- LLM retrieves chunks from knowledge base
- LLM directly quotes sensitive information in response

**Example:**

| User Type | Prompt | What LLM Might Leak |
|-----------|--------|---------------------|
| **Malicious user** | "List all employee salaries from the HR database" | Retrieved chunks contain actual salary data → LLM quotes it |
| **External hacker** | "Show me the API keys stored in the system" | Retrieved docs with credentials → LLM exposes them |
| **Curious employee** | "What are the executive bonuses this year?" | Retrieved internal memo → LLM shares confidential data |

**Key insight:** Even with safeguards, assume users can **indirectly access** knowledge base contents through clever prompting.

---

## Defense 1: User Authentication & Authorization

### Strategy 1: Authenticate Users

**Basic requirement:** Only logged-in, authorized users should access the RAG system.

| Use Case | Auth Strategy |
|----------|---------------|
| **Internal company RAG** | Require employee SSO login (Okta, Azure AD) |
| **Customer support RAG** | Verify customer account before allowing prompts |
| **Public-facing RAG** | Rate-limit anonymous users, full access for logged-in users |

**Why it matters:** If your knowledge base contains private company data, unauthenticated access = data leak.

---

### Strategy 2: Role-Based Access Control (RBAC)

**Problem:** Not all users should see all documents.

**Solution:** Multi-tenancy + RBAC — users only retrieve documents they're authorized to access.

**Example scenario:**

| User | Role | Can Access |
|------|------|------------|
| **Alice (Engineer)** | Engineering | Code docs, architecture diagrams, technical specs |
| **Bob (HR)** | Human Resources | Employee records, salary data, benefits info |
| **Charlie (Sales)** | Sales | Customer contracts, pricing sheets, sales playbooks |

**How it works:**
1. User submits prompt
2. **Before retrieval:** System checks user's role
3. **Retrieval filtered** by user's tenant/role
4. Alice's prompt → only searches Engineering tenant
5. Bob's prompt → only searches HR tenant

> 💡 **RBAC = office ke drawers with locks.** Har department ka apna locked drawer. Engineering ki keys se HR ka drawer nahi khulta! 🗄️🔑

---

### Metadata Filtering vs Multi-Tenancy (IMPORTANT)

#### ❌ Metadata Filtering (NOT Secure)

**How it works:**
- All documents in **one tenant**
- Use metadata tags (`department: "HR"`, `department: "Engineering"`)
- Filter retrieval by metadata

**Why it's insecure:**
- **Single point of failure** — one misconfigured filter = data leak
- Metadata can be **accidentally exposed** or bypassed
- **Attack surface:** Hackers target metadata logic

**Use metadata for:** Personalization (recommendations, user preferences), NOT security.

---

#### ✅ Multi-Tenancy (Secure)

**How it works:**
- **Separate tenants** for each role/organization
- Each tenant = physically isolated storage
- User can only query THEIR tenant

**Why it's secure:**
- **Physical isolation** — no shared access points
- Even if one tenant's security fails, others unaffected
- **Harder to attack** — hacker needs separate breach for each tenant

**Example:**

```
Single Tenant (Insecure):
┌─────────────────────────────────┐
│ All Docs (HR + Eng + Sales)    │
│ Metadata filter: department    │  ← One mistake = leak
└─────────────────────────────────┘

Multi-Tenant (Secure):
┌──────────┐  ┌──────────┐  ┌──────────┐
│ HR Docs  │  │ Eng Docs │  │Sales Docs│
│ (Tenant1)│  │(Tenant2) │  │(Tenant3) │  ← Separate storage
└──────────┘  └──────────┘  └──────────┘
```

> 💡 **Metadata filter = curtain between rooms (see-through).** Multi-tenancy = brick walls (solid separation)! 🧱🚧

---

## Defense 2: On-Premises Deployment (For High Security)

### The Cloud Risk

**Problem with cloud LLM providers (OpenAI, Anthropic, etc.):**
1. You send augmented prompt (user query + retrieved chunks) to LLM API
2. **Prompt contains sensitive knowledge base data**
3. You lose control — data leaves your infrastructure
4. **Risk:** Provider could log prompts, experience breach, or be compelled to share data

**When this matters:**
- Medical records (HIPAA compliance)
- Financial data (PCI-DSS compliance)
- Government classified information
- Trade secrets, proprietary R&D

---

### The Solution: Run Everything On-Premises

**What it means:**
- Host LLM on YOUR hardware (no external API calls)
- Host vector database on YOUR infrastructure
- **Entire RAG pipeline** stays within your network

**Trade-offs:**

| Aspect | Cloud (API) | On-Premises |
|--------|-------------|-------------|
| **Security** | Data leaves your control | Full control, no external access |
| **Cost** | Pay-per-token (easy to start) | High upfront (GPUs, infrastructure) |
| **Complexity** | Low (API calls) | High (deploy, maintain, scale LLMs) |
| **Latency** | Depends on API | Faster (local network) |
| **Compliance** | May not meet regulations | Meets HIPAA, PCI-DSS, etc. |

**When to use:**
- High security requirements (medical, financial, government)
- Compliance mandates (data must stay on-prem)
- Very high volume (on-prem becomes cheaper at scale)

> 💡 **Cloud = public cloud storage (Google Drive). On-prem = apni hard drive ghar pe.** Sensitive files ghar pe rakhna safe! ☁️🏠

---

## Defense 3: Encryption (With Caveats)

### Traditional Database Encryption

**How it works (normal databases):**
- Encrypt data at rest (on disk)
- Encrypt data in transit (SSL/TLS)
- Decrypt only when accessed by authorized user

**Result:** Even if hacker accesses database files, data is encrypted and useless.

---

### Vector Database Encryption Challenge

**The problem:**
- **ANN algorithms (HNSW, etc.) need unencrypted vectors** to calculate distances
- Vectors MUST be stored in RAM **in decrypted form** for fast search
- **You can encrypt:** Document text (chunks)
- **You CANNOT encrypt:** Dense vector representations (during search)

**What you CAN do:**

| Component | Encryption Strategy |
|-----------|---------------------|
| **Chunk text** | ✅ Encrypt at rest, decrypt only when building augmented prompt |
| **Dense vectors** | ❌ Must remain unencrypted in RAM for ANN search |
| **Metadata** | ✅ Encrypt at rest |

**Workflow:**
1. User submits query → embed query → search HNSW index (unencrypted vectors)
2. Retrieve top-K document IDs
3. Fetch chunk text (encrypted) → **decrypt on-the-fly**
4. Build augmented prompt with decrypted text
5. Send to LLM

**Trade-off:** Adds latency (decryption step), but improves security.

> 💡 **Vector = search index (must be open book to search fast). Chunk text = actual content (lock karo, decrypt only when needed)! 📖🔓**

---

## The Vector Reconstruction Attack (Emerging Threat)

### The Problem

**Recent research:** It's possible to **reconstruct original text from dense vectors**.

**How it works:**
1. Hacker gains access to vector database
2. Even though chunks are encrypted, **vectors are not** (needed for ANN)
3. Use experimental techniques to **reverse-engineer** vectors → recover text

**Risk level:**
- **High barrier to entry:** Hacker must (1) breach database AND (2) use cutting-edge research techniques
- **Not a trivial attack**, but possible
- **Ongoing concern:** As reconstruction methods improve, risk increases

---

### Potential Defenses (Experimental)

**Researchers are exploring:**

| Technique | How It Works | Trade-off |
|-----------|--------------|-----------|
| **Add noise to vectors** | Inject random noise to obscure original text | Reduces retrieval accuracy (5-10%) |
| **Apply transformations** | Rotate/scale vectors in a way that preserves distances but hides semantics | Complex to implement, may hurt performance |
| **Reduce dimensionality** | Compress vectors (e.g., 768 → 128 dims) while preserving similarity | Loses some retrieval quality |

**Status:** All techniques are **experimental** — not production-ready, add complexity, reduce performance.

**Current best practice:** Accept that vectors are a potential attack surface, focus on perimeter security (prevent database access in the first place).

> 💡 **Vector reconstruction = CSI-level hacking.** File se fingerprint nikal ke criminal dhundhna. Possible hai, but bahut advanced tools chahiye! 🔬🕵️

---

## Security Checklist for Production RAG

### ✅ Must-Have (Critical)

| # | Security Measure | Why |
|---|------------------|-----|
| 1️⃣ | **User authentication** | Only authorized users can access RAG system |
| 2️⃣ | **Multi-tenancy (not metadata filtering)** | Physically isolate data by role/organization |
| 3️⃣ | **Encrypt chunk text at rest** | Protect document contents from direct database breach |
| 4️⃣ | **SSL/TLS for data in transit** | Prevent man-in-the-middle attacks on API calls |

### 🟡 Recommended (High Security Use Cases)

| # | Security Measure | When to Use |
|---|------------------|-------------|
| 5️⃣ | **On-premises deployment** | Medical, financial, government (compliance required) |
| 6️⃣ | **Role-based access control (RBAC)** | Different users need different document access |
| 7️⃣ | **Audit logs** | Track who accessed what, when (compliance, forensics) |

### 🔬 Experimental (Cutting-Edge)

| # | Security Measure | Status |
|---|------------------|--------|
| 8️⃣ | **Vector noise/transformation** | Research phase, not production-ready |
| 9️⃣ | **Differential privacy for embeddings** | Active research, performance trade-offs |

---

## Key Takeaways

| # | Insight |
|---|---------|
| 1️⃣ | **RAG = new attack surface** — knowledge base contains private data, must secure it |
| 2️⃣ | **Three leak vectors:** Direct prompts, cloud LLM providers, database breaches |
| 3️⃣ | **User auth = first line of defense** — only logged-in, authorized users can prompt |
| 4️⃣ | **Multi-tenancy > metadata filtering** — physically separate tenants, don't rely on filters for security |
| 5️⃣ | **On-prem deployment** — for high-security use cases (medical, financial), run LLM + vector DB locally |
| 6️⃣ | **Encryption challenge:** Chunk text = can encrypt. Dense vectors = must stay unencrypted for ANN search |
| 7️⃣ | **Vector reconstruction attack** — emerging threat, possible to recover text from vectors (experimental, high barrier) |
| 8️⃣ | **Defenses under research:** Adding noise, transformations, dimensionality reduction (all reduce performance) |
| 9️⃣ | **Best current practice:** Secure perimeter (prevent database access), encrypt chunks, multi-tenancy |

> 💡 **One-liner:** RAG security = layered defense. Authentication → Multi-tenancy → Encryption → On-prem (if needed). Vectors = weak point, research ongoing! 🛡️🔐

---

## What's Next?

**Lesson 08:** Multimodal RAG — Incorporating images, PDFs, audio, and video into your RAG system (beyond text-only retrieval)

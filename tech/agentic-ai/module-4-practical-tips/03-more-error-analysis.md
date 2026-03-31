# 03 · More Error Analysis Examples 🔍🔍

---

## 🎯 One Line
> Same error analysis technique applied to two new workflows — invoice processing and customer email responses — to build your intuition for spotting which component is actually the bottleneck.

---

## 🖼️ Why More Examples?

Error analysis is a **skill that improves with practice**. You need to see it applied to different types of workflows before the intuition clicks. This lesson covers two new workflows with full spreadsheet breakdowns.

---

## 📋 Example 1: Invoice Processing

### The Workflow

```
┌──────────┐     ┌──────────────┐     ┌───────────────┐     ┌───────────┐
│  Invoice  │────▶│  PDF to Text │────▶│  LLM Extract  │────▶│  Update   │
│  (PDF)    │     │              │     │  4 Fields      │     │  Database │
└──────────┘     └──────────────┘     └───────────────┘     └───────────┘
                                              │
                                    ┌─────────┴─────────┐
                                    │  4 Required Fields │
                                    │  • Biller          │
                                    │  • Biller address  │
                                    │  • Amount due      │
                                    │  • Due date        │
                                    └───────────────────┘
```

**Observed problem:** System often extracts the **wrong due date**.

### Where could the error come from?

Only **two components** to investigate:

| Component | What Could Go Wrong |
|-----------|-------------------|
| **PDF to Text** | Garbled text extraction — dates are mangled so even a human can't read them |
| **LLM Data Extraction** | Text is fine, but LLM picks the wrong date (e.g., invoice date instead of due date) |

### The Error Analysis Spreadsheet

Select **10-100 invoices where the due date was wrong**, then check each component:

| Input | PDF-to-Text | LLM Data Extraction |
|-------|:-----------:|:-------------------:|
| Invoice 1 | ❌ Errors in extraction | |
| Invoice 2 | | ❌ Wrong date selected |
| Invoice 3 | | ❌ Wrong data selected |
| ... | ... | ... |
| Invoice 20 | ❌ Errors in extraction | ❌ Wrong data selected |
| **Error Rate** | **15%** | **87%** 🎯 |

### Key Takeaways

- **87% of failures came from LLM data extraction** — this is where to focus
- Only 15% from PDF-to-text — fixing the PDF parser won't move the needle much
- **Percentages don't add up to 100%** — errors are NOT mutually exclusive. Invoice 20 had errors in BOTH components
- Without this analysis, a team might spend weeks/months tuning PDF-to-text and see almost no improvement in overall accuracy

> 💡 **Bina error analysis ke PDF parser fix karte raho months tak — end mein pata chale LLM galat date pick kar raha tha. Mehnat barbaad! 😩**

---

## 📋 Example 2: Customer Email Response

### The Workflow

**3 Steps** (from course slides):
1. Extract key information
2. Find relevant customer records
3. Draft response for human review

```
┌─────────────────────────────┐
│  Customer Email              │
│                              │
│  From: Susan Jones           │
│  Subject: Wrong item shipped │
│                              │
│  "I ordered a blue KitchenPro│
│   blender (Order #8847) but  │
│   received a red toaster     │
│   instead. I need the blender│
│   for my daughter's birthday │
│   party this weekend.        │
│   Can you help? — Susan"     │
└──────────────┬──────────────┘
               ▼
┌──────────────────────────────┐
│  LLM: Verify order details   │
│  (writes database query)     │──────▶  Orders DB
│                              │◀──────  (query results)
└──────────────┬──────────────┘
               ▼
┌──────────────────────────────┐
│  LLM: Draft response,       │
│  request review              │
└──────────────┬──────────────┘
               ▼
┌──────────────────────────────┐
│  Human reviews & sends       │
└──────────────────────────────┘
```

**Three possible failure points:**

| Component | What Could Go Wrong |
|-----------|-------------------|
| **LLM-drafted query** | Wrong table, wrong fields, incorrect SQL — doesn't fetch the right data |
| **Orders database** | Corrupted/wrong data in the DB itself — even a perfect query returns bad info |
| **LLM-drafted email** | Given correct data, the email is still wrong — bad tone, missing details, wrong math |

### The Error Analysis Spreadsheet

Find ~50 emails where the final response was unsatisfactory:

| Input | LLM-Drafted Query | Orders Database | LLM-Drafted Email |
|-------|:-----------------:|:---------------:|:-----------------:|
| Email 1 | ❌ Wrong table | | |
| Email 2 | | ❌ Error in database entry | ❌ Didn't address details of order |
| Email 3 | | | ❌ Incorrect math |
| ... | ... | ... | ... |
| Email 50 | | | ❌ Defensive tone |
| **Error Rate** | **75%** 🎯 | **4%** | **30%** |

### Key Takeaways

- **75% of errors trace back to bad database queries** — the LLM is writing wrong SQL (wrong tables, wrong fields)
- Database itself is mostly clean (only 4% errors)
- 30% of the time, the email drafting is also off — wrong tone, missed details, bad math
- **Priority order:** Fix query generation first (75%), then improve email drafting (30%), database cleanup is low priority (4%)
- Again, percentages don't sum to 100% — one email can have multiple component failures

> 💡 **75% query galat, 30% email galat, 4% database galat. Kahan focus karoge? Obviously query pe! Yahi toh error analysis ka magic hai — numbers dikhate hain ki gut feeling galat hoti. 🎯**

---

## 🔄 Patterns Across All Three Examples

| Example | Biggest Offender | Error Rate | Runner-Up | Surprise Finding |
|---------|:----------------:|:----------:|:---------:|:-----------------|
| Research Agent (Lesson 02) | Search Results | 45% | Source Selection (10%) | Search terms were fine (5%) — problem was the engine |
| Invoice Processing | LLM Data Extraction | 87% | PDF-to-Text (15%) | Most teams would've focused on PDF parser first |
| Customer Email | LLM Query Writing | 75% | Email Drafting (30%) | Database was almost never the problem (4%) |

**What these share:**
- The **most obvious** component to blame is often NOT the actual culprit
- **Small eval sets work** — even 20-50 examples reveal clear patterns
- **Error rates aren't mutually exclusive** — one example can have multiple failing components
- The data always surprises you — that's why you count instead of guessing

---

## ⚠️ Gotchas
- ❌ **Percentages don't add up to 100%** — multiple components can fail simultaneously on the same example
- ❌ **Don't assume the most visible component is the problem** — invoice teams would instinctively fix PDF parsing, but 87% of errors were from the LLM
- ❌ **Don't skip "boring" components** — database errors at 4% seem negligible, but for high-stakes applications even that might matter later

---

## 🧪 Quick Check

<details>
<summary>❓ Your invoice pipeline has 15% PDF-to-text errors and 87% LLM extraction errors. A teammate wants to spend 3 weeks improving the PDF parser. What do you tell them?</summary>

Show them the spreadsheet. 87% of wrong due dates come from the LLM picking the wrong date, not from bad text extraction. Even if you fix PDF-to-text perfectly (remove all 15%), you'd still have ~87% of failures. Focus on improving the LLM extraction prompts/approach first.

</details>

<details>
<summary>❓ In the customer email example, why can't we just look at the error rate of the final email (30%) and fix that?</summary>

Because 75% of the time, the email was bad because it was working with **wrong data from a bad query**. Fixing the email prompt won't help if the underlying data is wrong. Fix the query generation first — many of the email errors will disappear automatically once the LLM has correct data to work with.

</details>

<details>
<summary>❓ Why does Andrew emphasize that error percentages are NOT mutually exclusive?</summary>

Because a single failing example can have **multiple broken components**. Invoice 20 had both PDF-to-text errors AND LLM extraction errors. If you assumed they were mutually exclusive, you'd undercount the true error rate of each component. Count each component's failures independently.

</details>

---

> **Next →** [Component-Level Evals](04-component-level-evals.md)

# Flashcards — Generative UI

> _Will be populated after completing modules..._

---

## Module 1: Introduction

### Q: What is Generative UI?
**A:** Instead of agents outputting plain text, they generate visual interfaces on demand (charts, forms, whiteboards, etc.) — the "Windows era" of AI vs "MS-DOS era" of plain chatbots.

---

### Q: What are the 3 patterns of Generative UI?
**A:** 
1. **Controlled UI** — Handcrafted components, agent picks from catalog
2. **Declarative UI (AG-UI)** — Schema-based, agent assembles layouts from building blocks
3. **Open-Ended UI (MCP Apps)** — Full app sandboxes (whiteboards, approval flows)

---

### Q: When would you use Controlled UI vs Declarative UI?
**A:** 
- **Controlled:** Need full control over design/behavior, predictable outputs (e.g., render specific chart)
- **Declarative:** Need flexible layouts without hardcoding every possibility (e.g., generate form with N fields)

---

### Q: What is the AG-UI protocol?
**A:** Open spec co-developed by Google and CopilotKit for declarative generative UI — defines how agents assemble layouts from component schemas.

---

### Q: What is CopilotKit?
**A:** Open-source framework for generative UI that supports all 3 patterns (Controlled, Declarative, Open-ended) with first-party LangGraph, Google Cloud, AWS, Azure integrations.

---

### Q: What's the trade-off in the generative UI spectrum?
**A:** **Your control vs agent freedom**  
- More control (Controlled UI) = less agent creativity, predictable  
- More agent freedom (Open-ended UI) = more creativity, less predictable

---

### Q: What will you build in this course?
**A:** Full-stack agent app with:
1. Charts/cards on demand (Controlled)
2. Shared to-do list agent ↔ UI sync (Declarative)
3. Live collaborative whiteboard (Open-ended MCP app)

# 🧠 My Memory — Learning Vault

> Knowledge that sticks. Open any folder, teach anyone.

---

## 🗺️ The Map

```mermaid
graph TB
    ROOT(("🧠 My Memory"))
    ROOT --> TECH["🔧 Tech"]
    ROOT --> NT["🌍 Non-Tech"]
    
    TECH --> AM["🧠 Agent Memory<br/>7/7 lessons ✅"]
    TECH --> PY["🐍 Python"]
    PY --> AIO["⚡ AsyncIO<br/>1/1 ✅"]

    style ROOT fill:#37474f,color:#fff,stroke:#263238,stroke-width:2px
    style TECH fill:#2196f3,color:#fff,stroke:#1565c0
    style NT fill:#78909c,color:#fff,stroke:#37474f,stroke-dasharray: 5 5
    style AM fill:#ff9800,color:#fff,stroke:#e65100
    style PY fill:#2196f3,color:#fff,stroke:#1565c0
    style AIO fill:#ff9800,color:#fff,stroke:#e65100
```

## 📊 Stats

| Metric | Count |
|--------|-------|
| Topics | 2 |
| Lessons | 8 |
| Flashcards | 50+ |
| Last updated | 2026-03-21 |

## Topics

| Topic | Category | Lessons | Confidence | Source |
|-------|----------|---------|------------|--------|
| [🧠 Agent Memory](tech/agent-memory/) | Tech | 7/7 ✅ | 🟡 Learning | DeepLearning.AI × Oracle |
| [⚡ AsyncIO](tech/python/asyncio/) | Tech / Python | 1/1 ✅ | 🟡 Learning | Corey Schafer (YouTube) |

## How This Works

| Folder | What's Inside |
|--------|--------------|
| [`tech/`](tech/) | All technical topics |
| `non-tech/` | Everything else |
| [`_maps/`](_maps/) | Auto-generated knowledge graphs |
| [`_revision/`](_revision/) | Spaced repetition tracker |
| [`_templates/`](_templates/) | Blueprints for new content |

## The Rules
1. **One folder = one topic**
2. **Numbered files = teaching order** (01, 02, 03...)
3. **Every folder has**: README.md + flashcards.md
4. **Diagram first, text second**
5. **English for concepts, Hinglish for aha! moments**
6. **Open in order = can teach anyone**

---

> Built with ❤️ by Ayra (AI Learning Agent) · [GitHub Pages](https://ayushsonuu.github.io/my-memory/)

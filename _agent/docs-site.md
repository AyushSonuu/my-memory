# Docs Site — MkDocs Material Build & Nav Rules

> Load this module when: building/updating the docs site, adding new topics to nav

The vault is published via **MkDocs Material** (LangChain-style docs).
After adding/updating any lesson, code, or topic (batched with Tier 2 sync):

## Step 1: Update `mkdocs.yml` nav

Add new pages manually to the `nav:` section. Follow these patterns:

**New topic under tech/ (e.g., Redis):**
```yaml
  - 🗄️ Redis:
    - tech/redis/README.md
    - 01 · Introduction: tech/redis/01-introduction.md
    - 🃏 Flashcards: tech/redis/flashcards.md
    - 💻 Code Lab:
      - Overview: tech/redis/code/README.md
      # .ipynb files: add directly
      - L1 Notebook: tech/redis/code/L1/L1.ipynb
      # .py files: use _generated/ path (auto-created by build_docs.py)
      - example.py: _generated/tech/redis/code/L1/example.md
```

**New sub-topic under Python (e.g., Decorators):**
```yaml
  - 🐍 Python:
    - tech/python/README.md
    - ⚡ AsyncIO:
      - ...existing...
    - 🎨 Decorators:             # ← just add here
      - Overview: tech/python/decorators/README.md
      - 01 · Basics: tech/python/decorators/01-basics.md
```

**Key rules:**
- `README.md` in nav = section index page (clickable tab/dropdown header)
- `.ipynb` files → add directly to nav (mkdocs-jupyter renders them)
- `.py` files → use `_generated/{path}/{name}.md` (build_docs.py creates these)
- Lessons: use numbered prefix (`01 ·`, `02 ·`) for teaching order
- Resources: group under a sub-section (`🃏 Flashcards`, `📋 Cheatsheet`, `⚔️ vs`)

## Step 2: Build
```bash
.venv/bin/python build_docs.py
```
This auto-generates markdown wrappers for ALL .py files, renders .ipynb notebooks, builds the full static site, and adds .nojekyll.

## Step 3: Commit
```bash
git add -A && git commit -m "🌐 rebuild docs" && git push origin main
```
GitHub Pages serves from `docs/` folder on main branch.

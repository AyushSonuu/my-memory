# Golden Rules — Content Quality Standards

> Load this module when: writing ANY content (lessons, flashcards, READMEs, KB entries)

## 0. 🧠 HIGHLY RECALLABLE (THE CORE PRINCIPLE)
Everything you write must be **instantly recallable** during revision. This is the #1 priority.
- **Every single point** from the source content MUST be captured — leave NOTHING out
- But capture it in a way that's **compressed, visual, and sticky**
- Use memory hooks: analogies, Hinglish jokes, real-world comparisons, visual patterns
- Structure for scanning: headers → diagram → table → one-liner → details
- The test: "Can Ayush read this in 5 min and recall 90% a week later?"
- If a concept is forgettable as plain text → make it a diagram, a funny analogy, or a comparison table
- **Completeness + Conciseness** — don't drop content to save space, compress it smartly instead
- Think like a textbook that respects your time: nothing missing, nothing wasted

## 1. 🚫 ZERO Hallucination (NON-NEGOTIABLE)
- Only facts from source material or web-verified
- Use confidence tags **inline next to specific claims** when needed:
  - ✅ Direct from source
  - 🔍 Web-searched & verified  
  - 💡 Analogy (marked)
  - ⚠️ Interpretation (verify yourself)
- **Do NOT add meta-commentary** at the top of files (no "Direct from course", "Placeholder", "Confidence: X", "Not started" etc.). Every line in a lesson must teach a concept — no filler, no status tags, no source attribution banners.
- When unsure → **web search first**, don't guess silently

## 2. 📊 Visual FIRST, Text SECOND
- Every concept opens with a visual — pick the **RIGHT tool for the job**:
  - **Mermaid** → cycles, relationships, hierarchies, flows, architectures, pipelines, convergence diagrams
  - **SVG** → complex architectures, multi-column layouts, detailed system diagrams, anything that needs precise positioning, colors, gradients, or drop shadows. SVGs render natively on GitHub and look sharp at any zoom. Use when Mermaid can't capture the full picture cleanly.
  - **Tables** → comparisons, side-by-side, feature lists, cheat sheets
  - **ASCII art** → simple stacks, box layouts, context window depictions, lightweight sketches
  - **Emoji + bold/italic** → quick-scan lists, callouts
- **Don't force one tool** — Mermaid is great for graphs/flows, but a complex architecture with 10+ boxes and feedback loops is better as SVG. A comparison is a table, not a diagram. A simple stack is cleaner as ASCII. Pick what makes that specific concept most visually clear and appealing.
- Text explains the visual, not vice versa
- A good diagram replaces 3 paragraphs
- Mix visual types across sections — variety = visually appealing
- **SVG guidelines:** See detailed **SVG Style Guide** below (Section 7).
  - **ALWAYS save SVGs as standalone `.svg` files in an `assets/` folder** inside the topic/module directory. NEVER inline SVGs in markdown — they don't render in most viewers.
  - Reference as `![Alt text](assets/filename.svg)` in markdown.
  - Escape `&` as `&amp;` in SVG text — it's XML, not HTML.
  - Filename convention: `{lesson-number}-{slug-from-title}.svg` (e.g. `05-bm25-tf-saturation.svg`).

## 3. ✂️ Concise but COMPLETE
- Tables > paragraphs. Bullets > walls of text.
- **Compress without losing ANYTHING from the source.** Every fact, every nuance, every edge case.
- Not writing books, but also not dropping content. Smart compression = same info, fewer words.
- One concept = one scroll max
- If the source says 10 things, your notes have all 10 — just in tighter form
- **Say everything ONCE.** If a diagram already shows it, don't restate in prose. If a table covers it, don't add a paragraph below that says the same thing. ONE visual, all the info, move on.
- **Never repeat the same concept in multiple formats** — no ASCII + table + prose + UX table all saying the same thing. Pick the BEST format for that concept and use it once, completely.
- **Definitions stay exact** — technical definitions as-is, no paraphrasing that loses precision

## 4. 🗣️ User-Friendly Explanations
- **Write like you're explaining to a smart friend, not writing a textbook**
- Every description should make the reader UNDERSTAND, not just know the definition
- If a phrase sounds vague or jargon-y on its own, add a plain-language clarification
- **Define every important term when first introduced** — even a one-liner table with "what is it + example" is enough. Never assume a term is self-explanatory just because it was listed. If it has a name, explain what it means in plain words.
- Avoid lazy shorthand like "not the bottleneck" — say WHY in simple terms
- The test: "Would a reader with zero context understand this line?" If no → rewrite
- When comparing things (e.g., "Why X is the core, not Y"), give a clear REASON, not just a label

## 5. 🗣️ Language, Humor & Analogies
- **English** → definitions, concepts, technical terms
- **Hinglish** → analogies, humor, "aha!" hooks, memory tricks
- Natural mix, not forced. Funny = memorable = recallable.
- The funnier the hook, the longer it sticks in memory 🧠
- **Sprinkle Hinglish funny explanations and analogies throughout** — not just in one-liners, but also in section explanations, table "Remember" columns, and after complex concepts. If something can be explained with a real-world analogy (restaurant, recipe, exam, drawer, washing machine), DO IT.
- **Key concepts deserve a one-liner** — a single punchy sentence that nails it
  - Think: the line you'd say at chai to explain it to a friend
  - Examples:
    - "Stateless agent = goldfish. Memory = diary that survives across sessions."
    - "Context window = exam ka cheat sheet. Memory = jo actually yaad hai."
    - "Summarization = thumbnail 📸. Compaction = original file drawer mein 🗄️"
    - "LLM = customer. execute_tool = waiter. Function = kitchen. Customer ne kabhi gas nahi jalaya! 🍳"
  - Put one-liners in `> 💡` blockquotes so they stand out visually
  - **Don't overuse** — 2-3 per section max. Only for concepts that genuinely benefit from a sticky hook. If every paragraph has a one-liner, none of them stand out.
- **Analogies are NOT decoration — they're memory anchors.** A good analogy makes a concept unforgettable. A boring explanation without one gets forgotten in 2 days. BUT: only where a concept genuinely needs one. If the concept is already simple and clear, don't force a joke. Flooding every paragraph with Hinglish kills the effect — scarcity = impact.

## 6. 🎬 Teach-Ready = YouTube-Ready
- Numbered files (01, 02, 03) = teaching order
- Open folder in order = instant video script. Zero extra prep.

---

## 7. 🎨 SVG Style Guide — Preferred Theme Visual Language based on wibe of the lesson


When creating SVG diagrams, follow this consistent visual language for professional, GitHub-friendly visuals that look sharp and polished.

### Canvas & Background
```xml
<rect width="800" height="400" fill="#0d1117"/>  <!-- GitHub dark background -->
```
- Standard canvas: `800×400` to `800×550` (16:9 or taller)
- Always include dark background — don't rely on viewer's theme

### Color Palette (Semantic Colors)
| Purpose | Color | Hex | Usage |
|---------|-------|-----|-------|
| **Primary action** | Blue | `#2196f3` / `#1976d2` | Retriever, semantic search, primary flow |
| **Success/Good** | Green | `#4caf50` / `#388e3c` | Correct, LLM, positive outcomes |
| **Warning/Highlight** | Orange | `#ff9800` / `#f57c00` | Prompts, augmented content, attention |
| **Danger/Slow** | Red | `#f44336` / `#d32f2f` | Cross-encoder (slow), errors, negatives |
| **Special/Advanced** | Purple | `#9c27b0` / `#7b1fa2` | Knowledge base, reranker, fusion |
| **Neutral/Muted** | Gray | `#8b949e` | Labels, descriptions, secondary text |
| **Text primary** | Light gray | `#e6edf3` | Main text, titles |
| **Card background** | Dark gray | `#161b22` / `#21262d` | Boxes, containers |
| **Accent link** | Bright blue | `#58a6ff` | Highlights, links, callouts |
| **Cyan** | Teal | `#00bcd4` / `#0097a7` | Alternative accent, easy updates |

### Gradients (For Depth & Polish)
```xml
<defs>
  <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:#2196f3"/>
    <stop offset="100%" style="stop-color:#1976d2"/>
  </linearGradient>
</defs>
```
- Use **diagonal gradients** (`x1="0%" y1="0%" x2="100%" y2="100%"`) for depth
- Lighter shade at top-left, darker at bottom-right
- Apply to header bars, buttons, key elements

### Drop Shadows (Lift & Separation)
```xml
<defs>
  <filter id="shadow">
    <feDropShadow dx="2" dy="2" stdDeviation="2" flood-opacity="0.3"/>
  </filter>
</defs>
<rect ... filter="url(#shadow)"/>
```
- Apply to main containers for visual lift
- Consistent `dx="2" dy="2" stdDeviation="2-3"`
- Creates depth hierarchy between elements

### Typography
```xml
<text font-family="Inter, sans-serif" font-size="14" font-weight="bold" text-anchor="middle">
```
| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Title | 18-20px | bold | `#e6edf3` |
| Section header | 12-14px | bold | semantic color |
| Body text | 9-11px | regular | `#8b949e` |
| Labels | 8-9px | regular | `#8b949e` |

- Font: `Inter, sans-serif` (clean, modern)
- Always use `text-anchor="middle"` for centered text
- Use `#e6edf3` for primary text, `#8b949e` for secondary

### Card/Box Pattern (The Workhorse)
```xml
<!-- Container with colored header bar -->
<g transform="translate(50, 60)">
  <rect x="0" y="0" width="200" height="120" rx="10" fill="#161b22" stroke="#4caf50" stroke-width="2" filter="url(#shadow)"/>
  <rect x="0" y="0" width="200" height="30" rx="10" fill="url(#greenGrad)"/>
  <text x="100" y="20" fill="#fff" font-family="Inter, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">Header Text</text>
  <!-- Body content below -->
</g>
```
- Rounded corners: `rx="8"` to `rx="12"`
- Colored header bar with gradient fill
- Body in dark gray (`#161b22` or `#21262d`)
- Optional stroke matching the semantic color
- Use `transform="translate(x, y)"` for positioning groups

### Arrows & Flow Lines
```xml
<!-- Line with arrow head -->
<line x1="100" y1="50" x2="200" y2="50" stroke="#8b949e" stroke-width="2"/>
<polygon points="200,50 190,44 190,56" fill="#8b949e"/>

<!-- Curved path -->
<path d="M 100 50 L 150 50 L 150 100" stroke="#2196f3" stroke-width="2" fill="none"/>
```
- Use semantic colors for directional meaning
- Arrow heads as filled polygons (6px offset from tip)
- Stroke width: 2px for connections

### Layout Patterns
| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Pipeline/Flow** | Sequential processes | Retriever → Reranker → LLM |
| **Comparison (2-3 col)** | Side-by-side options | Bi-encoder vs Cross-encoder |
| **Hub diagram** | Central concept + connections | RAG advantages radiating from center |
| **Table/Grid** | Data comparison, scoring | RRF calculation, token similarity matrix |
| **Before/After** | Transformations | Training evolution, chunking results |
| **Scale bar** | Spectrum/continuum | Chunk size too small ↔ too large |

### Emoji Usage in SVGs
- Sparingly in titles/headers for visual scanning
- Common emojis: 📝 (prompt), 🔍 (search), 🧠 (LLM), 📚 (KB), ✅ (success), ❌ (error), 🎯 (target), ⚡ (fast), 🐢 (slow)
- Position emoji before text in headers

### Standard SVG Template
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4caf50"/>
      <stop offset="100%" style="stop-color:#388e3c"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="2" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="800" height="400" fill="#0d1117"/>

  <!-- Title -->
  <text x="400" y="30" fill="#e6edf3" font-family="Inter, sans-serif" font-size="18" font-weight="bold" text-anchor="middle">Diagram Title</text>

  <!-- Main content groups -->
  <g transform="translate(50, 60)">
    <!-- Cards, arrows, content -->
  </g>

  <!-- Legend or footer (optional) -->
  <g transform="translate(50, 350)">
    <text x="0" y="0" fill="#8b949e" font-family="Inter, sans-serif" font-size="10">Footer note or insight</text>
  </g>
</svg>
```

### When to Use SVG vs Mermaid
| Use SVG when... | Use Mermaid when... |
|-----------------|---------------------|
| Precise positioning needed | Simple flow/hierarchy |
| Multi-column layouts | Quick diagram |
| Gradients, shadows, visual polish | Standard graph shapes |
| Complex architectures (10+ elements) | Sequence diagrams |
| Side-by-side comparisons | Basic flowcharts |
| Data visualization (grids, matrices) | Class/entity relationships |
| Want it to look *beautiful* | Just need it to be *clear* |

### Common Mistakes to Avoid
- ❌ Forgetting `&amp;` for `&` in text (XML requirement)
- ❌ Inlining SVG in markdown (won't render)
- ❌ No background (looks weird on light themes)
- ❌ Inconsistent colors across diagrams
- ❌ Too-small text (< 8px becomes unreadable)
- ❌ Crowded layouts (leave whitespace!)

---

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
- **SVG guidelines:** dark theme (`#0d1117` background), gradient fills, drop shadows, color-coded sections. Save in `_assets/`. Reference as `<img src="_assets/filename.svg"/>` in markdown.

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

# Lesson 05: Keyword Search — BM25

## 📌 Overview

While TF-IDF is a classic keyword search algorithm, most modern retrievers use **BM25 (Best Matching 25)** — the 25th variant in a series of scoring functions. BM25 improves upon TF-IDF with two critical insights: **term frequency saturation** and **diminishing length penalties**, plus tunable hyperparameters for production optimization.

---

## 🎯 Key Concepts

### 1. BM25 Formula & Structure

BM25 calculates a relevance score per keyword, then sums across all query keywords:

$$\text{BM25}(D, Q) = \sum_{i}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot (1 - b + b \cdot \frac{|D|}{avgdl})}$$

Where:
- $f(q_i, D)$ = frequency of query term $q_i$ in document $D$
- $|D|$ = length of document (word count)
- $avgdl$ = average document length in corpus
- $k_1$ = term frequency saturation parameter (typical: 1.5)
- $b$ = length normalization parameter (typical: 0.75)

---

### 2. Term Frequency Saturation

**Problem with TF-IDF:** Document with "pizza" 20 times scores 2x higher than "pizza" 10 times — unrealistic relevance boost.

**BM25 Solution:** Scoring plateaus. Adding more repetitions yields diminishing returns.

<svg viewBox="0 0 900 350" xmlns="http://www.w3.org/2000/svg" style="border: 1px solid #ddd; background: #f9f9f9; max-width: 100%; height: auto;">
  <!-- Title -->
  <text x="450" y="25" font-size="18" font-weight="bold" text-anchor="middle" fill="#222">Term Frequency Saturation: TF-IDF vs BM25</text>
  
  <!-- Left chart: TF-IDF (linear) -->
  <g id="tfidf-chart">
    <text x="150" y="55" font-size="14" font-weight="bold" fill="#222">TF-IDF: Linear Growth</text>
    
    <!-- Axes -->
    <line x1="80" y1="300" x2="80" y2="80" stroke="#333" stroke-width="2"/>
    <line x1="80" y1="300" x2="280" y2="300" stroke="#333" stroke-width="2"/>
    
    <!-- Axis labels -->
    <text x="40" y="305" font-size="11" fill="#555">Score</text>
    <text x="170" y="330" font-size="11" fill="#555">Term Frequency</text>
    
    <!-- Grid & ticks -->
    <line x1="75" y1="260" x2="280" y2="260" stroke="#eee" stroke-width="1"/>
    <text x="60" y="265" font-size="10" fill="#999">0.5</text>
    
    <line x1="75" y1="220" x2="280" y2="220" stroke="#eee" stroke-width="1"/>
    <text x="60" y="225" font-size="10" fill="#999">1.0</text>
    
    <line x1="75" y1="180" x2="280" y2="180" stroke="#eee" stroke-width="1"/>
    <text x="60" y="185" font-size="10" fill="#999">1.5</text>
    
    <line x1="75" y1="140" x2="280" y2="140" stroke="#eee" stroke-width="1"/>
    <text x="60" y="145" font-size="10" fill="#999">2.0</text>
    
    <!-- X-axis ticks: 1,5,10,15,20 -->
    <line x1="100" y1="298" x2="100" y2="305"/>
    <text x="95" y="320" font-size="10" fill="#555">1</text>
    
    <line x1="140" y1="298" x2="140" y2="305"/>
    <text x="132" y="320" font-size="10" fill="#555">5</text>
    
    <line x1="180" y1="298" x2="180" y2="305"/>
    <text x="172" y="320" font-size="10" fill="#555">10</text>
    
    <line x1="220" y1="298" x2="220" y2="305"/>
    <text x="212" y="320" font-size="10" fill="#555">15</text>
    
    <line x1="260" y1="298" x2="260" y2="305"/>
    <text x="252" y="320" font-size="10" fill="#555">20</text>
    
    <!-- TF-IDF curve (linear: score = TF/2) -->
    <polyline points="100,280 140,260 180,240 220,220 260,200" fill="none" stroke="#FF6B6B" stroke-width="3" stroke-linecap="round"/>
    
    <!-- Points -->
    <circle cx="100" cy="280" r="4" fill="#FF6B6B"/>
    <circle cx="140" cy="260" r="4" fill="#FF6B6B"/>
    <circle cx="180" cy="240" r="4" fill="#FF6B6B"/>
    <circle cx="220" cy="220" r="4" fill="#FF6B6B"/>
    <circle cx="260" cy="200" r="4" fill="#FF6B6B"/>
    
    <!-- Annotation: +100% at 10 freq -->
    <path d="M 180 240 L 180 160" stroke="#FF6B6B" stroke-width="1" stroke-dasharray="3,3"/>
    <text x="190" y="165" font-size="10" fill="#FF6B6B">+100%</text>
  </g>
  
  <!-- Right chart: BM25 (saturating, k1=1.5) -->
  <g id="bm25-chart">
    <text x="600" y="55" font-size="14" font-weight="bold" fill="#222">BM25: Saturation (k₁=1.5)</text>
    
    <!-- Axes -->
    <line x1="530" y1="300" x2="530" y2="80" stroke="#333" stroke-width="2"/>
    <line x1="530" y1="300" x2="730" y2="300" stroke="#333" stroke-width="2"/>
    
    <!-- Axis labels -->
    <text x="490" y="305" font-size="11" fill="#555">Score</text>
    <text x="620" y="330" font-size="11" fill="#555">Term Frequency</text>
    
    <!-- Grid & ticks -->
    <line x1="525" y1="260" x2="730" y2="260" stroke="#eee" stroke-width="1"/>
    <text x="510" y="265" font-size="10" fill="#999">0.5</text>
    
    <line x1="525" y1="220" x2="730" y2="220" stroke="#eee" stroke-width="1"/>
    <text x="510" y="225" font-size="10" fill="#999">1.0</text>
    
    <line x1="525" y1="180" x2="730" y2="180" stroke="#eee" stroke-width="1"/>
    <text x="510" y="185" font-size="10" fill="#999">1.5</text>
    
    <line x1="525" y1="140" x2="730" y2="140" stroke="#eee" stroke-width="1"/>
    <text x="510" y="145" font-size="10" fill="#999">2.0</text>
    
    <!-- X-axis ticks: 1,5,10,15,20 -->
    <line x1="550" y1="298" x2="550" y2="305"/>
    <text x="545" y="320" font-size="10" fill="#555">1</text>
    
    <line x1="590" y1="298" x2="590" y2="305"/>
    <text x="582" y="320" font-size="10" fill="#555">5</text>
    
    <line x1="630" y1="298" x2="630" y2="305"/>
    <text x="622" y="320" font-size="10" fill="#555">10</text>
    
    <line x1="670" y1="298" x2="670" y2="305"/>
    <text x="662" y="320" font-size="10" fill="#555">15</text>
    
    <line x1="710" y1="298" x2="710" y2="305"/>
    <text x="702" y="320" font-size="10" fill="#555">20</text>
    
    <!-- BM25 curve (saturating): score = TF * (k1+1) / (TF + k1) where k1=1.5 -->
    <!-- At TF=1: 1*2.5/(1+1.5) = 2.5/2.5 = 1.0 -->
    <!-- At TF=5: 5*2.5/(5+1.5) = 12.5/6.5 ≈ 1.92 -->
    <!-- At TF=10: 10*2.5/(10+1.5) = 25/11.5 ≈ 2.17 -->
    <!-- At TF=15: 15*2.5/(15+1.5) = 37.5/16.5 ≈ 2.27 -->
    <!-- At TF=20: 20*2.5/(20+1.5) = 50/21.5 ≈ 2.33 -->
    <!-- Normalized: scale to 0-2.0 range where 1.0 maps to score 1.0, 2.33 maps to 2.0 -->
    <polyline points="550,282 590,240 630,215 670,205 710,200" fill="none" stroke="#4CAF50" stroke-width="3" stroke-linecap="round"/>
    
    <!-- Points -->
    <circle cx="550" cy="282" r="4" fill="#4CAF50"/>
    <circle cx="590" cy="240" r="4" fill="#4CAF50"/>
    <circle cx="630" cy="215" r="4" fill="#4CAF50"/>
    <circle cx="670" cy="205" r="4" fill="#4CAF50"/>
    <circle cx="710" cy="200" r="4" fill="#4CAF50"/>
    
    <!-- Annotation: +40% at 10 freq -->
    <path d="M 630 215 L 630 140" stroke="#4CAF50" stroke-width="1" stroke-dasharray="3,3"/>
    <text x="635" y="145" font-size="10" fill="#4CAF50">+40%</text>
    
    <!-- Saturation zone -->
    <rect x="670" y="190" width="50" height="25" fill="#4CAF50" opacity="0.1" stroke="#4CAF50" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="680" y="215" font-size="9" fill="#4CAF50">plateaus</text>
  </g>
  
  <!-- Legend -->
  <g id="legend" transform="translate(350, 310)">
    <text x="0" y="0" font-size="11" fill="#555" font-style="italic">TF-IDF score doubles 10→20. BM25 score increases only 15%.</text>
  </g>
</svg>

---

### 3. Document Length Normalization

**Problem with TF-IDF:** Long documents penalized too aggressively — a 1000-word relevant document scores lower than a 100-word marginally relevant document.

**BM25 Solution:** Diminishing length penalties. Long documents still score high if keyword frequency is substantial.

<svg viewBox="0 0 900 350" xmlns="http://www.w3.org/2000/svg" style="border: 1px solid #ddd; background: #f9f9f9; max-width: 100%; height: auto;">
  <!-- Title -->
  <text x="450" y="25" font-size="18" font-weight="bold" text-anchor="middle" fill="#222">Document Length Normalization: TF-IDF vs BM25</text>
  
  <!-- Left chart: TF-IDF (aggressive penalty) -->
  <g id="tfidf-length">
    <text x="150" y="55" font-size="14" font-weight="bold" fill="#222">TF-IDF: Aggressive Penalty</text>
    
    <!-- Axes -->
    <line x1="80" y1="300" x2="80" y2="80" stroke="#333" stroke-width="2"/>
    <line x1="80" y1="300" x2="280" y2="300" stroke="#333" stroke-width="2"/>
    
    <!-- Axis labels -->
    <text x="40" y="305" font-size="11" fill="#555">Score</text>
    <text x="140" y="330" font-size="11" fill="#555">Doc Length (words)</text>
    
    <!-- Grid -->
    <line x1="75" y1="260" x2="280" y2="260" stroke="#eee" stroke-width="1"/>
    <text x="60" y="265" font-size="10" fill="#999">0.5</text>
    
    <line x1="75" y1="220" x2="280" y2="220" stroke="#eee" stroke-width="1"/>
    <text x="60" y="225" font-size="10" fill="#999">1.0</text>
    
    <line x1="75" y1="180" x2="280" y2="180" stroke="#eee" stroke-width="1"/>
    <text x="60" y="185" font-size="10" fill="#999">1.5</text>
    
    <!-- X-axis ticks: 100,500,1000,2000 words -->
    <line x1="100" y1="298" x2="100" y2="305"/>
    <text x="85" y="320" font-size="10" fill="#555">100</text>
    
    <line x1="150" y1="298" x2="150" y2="305"/>
    <text x="130" y="320" font-size="10" fill="#555">500</text>
    
    <line x1="200" y1="298" x2="200" y2="305"/>
    <text x="185" y="320" font-size="10" fill="#555">1000</text>
    
    <line x1="250" y1="298" x2="250" y2="305"/>
    <text x="235" y="320" font-size="10" fill="#555">2000</text>
    
    <!-- TF-IDF penalty curve (1/sqrt(length)) -->
    <polyline points="100,180 150,140 200,120 250,100" fill="none" stroke="#FF6B6B" stroke-width="3" stroke-linecap="round"/>
    
    <!-- Points -->
    <circle cx="100" cy="180" r="4" fill="#FF6B6B"/>
    <circle cx="150" cy="140" r="4" fill="#FF6B6B"/>
    <circle cx="200" cy="120" r="4" fill="#FF6B6B"/>
    <circle cx="250" cy="100" r="4" fill="#FF6B6B"/>
    
    <!-- Annotations -->
    <text x="110" y="170" font-size="9" fill="#FF6B6B">1.0</text>
    <text x="155" y="135" font-size="9" fill="#FF6B6B">0.63</text>
    <text x="205" y="110" font-size="9" fill="#FF6B6B">0.45</text>
    
    <!-- Problem zone -->
    <rect x="200" y="95" width="55" height="100" fill="#FF6B6B" opacity="0.1" stroke="#FF6B6B" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="205" y="160" font-size="9" fill="#FF6B6B">too low</text>
  </g>
  
  <!-- Right chart: BM25 (gentle penalty, b=0.75) -->
  <g id="bm25-length">
    <text x="600" y="55" font-size="14" font-weight="bold" fill="#222">BM25: Gentle Penalty (b=0.75)</text>
    
    <!-- Axes -->
    <line x1="530" y1="300" x2="530" y2="80" stroke="#333" stroke-width="2"/>
    <line x1="530" y1="300" x2="730" y2="300" stroke="#333" stroke-width="2"/>
    
    <!-- Axis labels -->
    <text x="490" y="305" font-size="11" fill="#555">Score</text>
    <text x="590" y="330" font-size="11" fill="#555">Doc Length (words)</text>
    
    <!-- Grid -->
    <line x1="525" y1="260" x2="730" y2="260" stroke="#eee" stroke-width="1"/>
    <text x="510" y="265" font-size="10" fill="#999">0.5</text>
    
    <line x1="525" y1="220" x2="730" y2="220" stroke="#eee" stroke-width="1"/>
    <text x="510" y="225" font-size="10" fill="#999">1.0</text>
    
    <line x1="525" y1="180" x2="730" y2="180" stroke="#eee" stroke-width="1"/>
    <text x="510" y="185" font-size="10" fill="#999">1.5</text>
    
    <!-- X-axis ticks: 100,500,1000,2000 words -->
    <line x1="550" y1="298" x2="550" y2="305"/>
    <text x="535" y="320" font-size="10" fill="#555">100</text>
    
    <line x1="600" y1="298" x2="600" y2="305"/>
    <text x="585" y="320" font-size="10" fill="#555">500</text>
    
    <line x1="650" y1="298" x2="650" y2="305"/>
    <text x="635" y="320" font-size="10" fill="#555">1000</text>
    
    <line x1="700" y1="298" x2="700" y2="305"/>
    <text x="685" y="320" font-size="10" fill="#555">2000</text>
    
    <!-- BM25 penalty curve (gentler) -->
    <polyline points="550,180 600,160 650,150 700,145" fill="none" stroke="#4CAF50" stroke-width="3" stroke-linecap="round"/>
    
    <!-- Points -->
    <circle cx="550" cy="180" r="4" fill="#4CAF50"/>
    <circle cx="600" cy="160" r="4" fill="#4CAF50"/>
    <circle cx="650" cy="150" r="4" fill="#4CAF50"/>
    <circle cx="700" cy="145" r="4" fill="#4CAF50"/>
    
    <!-- Annotations -->
    <text x="555" y="175" font-size="9" fill="#4CAF50">1.0</text>
    <text x="605" y="150" font-size="9" fill="#4CAF50">0.89</text>
    <text x="655" y="140" font-size="9" fill="#4CAF50">0.82</text>
    
    <!-- Still-high zone -->
    <rect x="650" y="140" width="55" height="25" fill="#4CAF50" opacity="0.1" stroke="#4CAF50" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="658" y="160" font-size="9" fill="#4CAF50">still high</text>
  </g>
  
  <!-- Legend -->
  <g id="legend" transform="translate(300, 310)">
    <text x="0" y="0" font-size="11" fill="#555" font-style="italic">TF-IDF: 2000-word doc scores 0.45 × base. BM25: 2000-word doc scores 0.82 × base (fairer).</text>
  </g>
</svg>

---

### 4. Hyperparameters: $k_1$ and $b$

BM25's power comes from **two tunable hyperparameters**, allowing optimization for your specific corpus:

| Parameter | Role | Typical Value | Effect |
|-----------|------|---------------|--------|
| **$k_1$** | Term Frequency Saturation | 1.5 | Controls how quickly TF rewards plateau. Higher = slower saturation. |
| **$b$** | Length Normalization Strength | 0.75 | Controls penalty for long docs. 0 = no length penalty, 1.0 = full normalization. |

<svg viewBox="0 0 900 250" xmlns="http://www.w3.org/2000/svg" style="border: 1px solid #ddd; background: #f9f9f9; max-width: 100%; height: auto;">
  <!-- Title -->
  <text x="450" y="25" font-size="18" font-weight="bold" text-anchor="middle" fill="#222">Hyperparameter Impact on BM25 Scoring</text>
  
  <!-- k1 parameter chart -->
  <g id="k1-chart">
    <text x="220" y="55" font-size="13" font-weight="bold" fill="#222">Tuning $k_1$ (TF Saturation)</text>
    
    <line x1="80" y1="220" x2="80" y2="70" stroke="#333" stroke-width="2"/>
    <line x1="80" y1="220" x2="280" y2="220" stroke="#333" stroke-width="2"/>
    
    <text x="40" y="225" font-size="11" fill="#555">Score</text>
    <text x="160" y="245" font-size="11" fill="#555">Term Freq</text>
    
    <!-- Grid -->
    <line x1="75" y1="175" x2="280" y2="175" stroke="#eee" stroke-width="1"/>
    <text x="65" y="180" font-size="9" fill="#999">0.5</text>
    
    <line x1="75" y1="130" x2="280" y2="130" stroke="#eee" stroke-width="1"/>
    <text x="65" y="135" font-size="9" fill="#999">1.0</text>
    
    <!-- X-axis ticks -->
    <line x1="110" y1="218" x2="110" y2="224"/>
    <text x="105" y="238" font-size="9" fill="#555">5</text>
    
    <line x1="170" y1="218" x2="170" y2="224"/>
    <text x="165" y="238" font-size="9" fill="#555">15</text>
    
    <line x1="230" y1="218" x2="230" y2="224"/>
    <text x="225" y="238" font-size="9" fill="#555">25</text>
    
    <!-- k1=0.5 (steep saturation) -->
    <polyline points="110,190 170,145 230,125" fill="none" stroke="#FF9800" stroke-width="2.5"/>
    <text x="245" y="125" font-size="10" fill="#FF9800">k₁=0.5 (steep)</text>
    
    <!-- k1=1.5 (standard) -->
    <polyline points="110,170 170,120 230,110" fill="none" stroke="#2196F3" stroke-width="3"/>
    <text x="245" y="110" font-size="10" fill="#2196F3">k₁=1.5</text>
    
    <!-- k1=3.0 (gentle) -->
    <polyline points="110,155 170,110 230,95" fill="none" stroke="#4CAF50" stroke-width="2.5"/>
    <text x="245" y="95" font-size="10" fill="#4CAF50">k₁=3.0 (gentle)</text>
  </g>
  
  <!-- b parameter chart -->
  <g id="b-chart">
    <text x="670" y="55" font-size="13" font-weight="bold" fill="#222">Tuning $b$ (Length Normalization)</text>
    
    <line x1="530" y1="220" x2="530" y2="70" stroke="#333" stroke-width="2"/>
    <line x1="530" y1="220" x2="730" y2="220" stroke="#333" stroke-width="2"/>
    
    <text x="490" y="225" font-size="11" fill="#555">Score</text>
    <text x="610" y="245" font-size="11" fill="#555">Doc Length</text>
    
    <!-- Grid -->
    <line x1="525" y1="175" x2="730" y2="175" stroke="#eee" stroke-width="1"/>
    <text x="515" y="180" font-size="9" fill="#999">0.5</text>
    
    <line x1="525" y1="130" x2="730" y2="130" stroke="#eee" stroke-width="1"/>
    <text x="515" y="135" font-size="9" fill="#999">1.0</text>
    
    <!-- X-axis ticks -->
    <line x1="560" y1="218" x2="560" y2="224"/>
    <text x="550" y="238" font-size="9" fill="#555">500w</text>
    
    <line x1="620" y1="218" x2="620" y2="224"/>
    <text x="610" y="238" font-size="9" fill="#555">1500w</text>
    
    <line x1="680" y1="218" x2="680" y2="224"/>
    <text x="670" y="238" font-size="9" fill="#555">3000w</text>
    
    <!-- b=0 (no length penalty) -->
    <polyline points="560,175 620,175 680,175" fill="none" stroke="#FF9800" stroke-width="2.5"/>
    <text x="695" y="175" font-size="10" fill="#FF9800">b=0 (none)</text>
    
    <!-- b=0.75 (standard) -->
    <polyline points="560,175 620,145 680,135" fill="none" stroke="#2196F3" stroke-width="3"/>
    <text x="695" y="135" font-size="10" fill="#2196F3">b=0.75</text>
    
    <!-- b=1.0 (full) -->
    <polyline points="560,175 620,130 680,105" fill="none" stroke="#4CAF50" stroke-width="2.5"/>
    <text x="695" y="105" font-size="10" fill="#4CAF50">b=1.0 (full)</text>
  </g>
</svg>

---

## 📊 BM25 vs TF-IDF Comparison Table

| Aspect | TF-IDF | BM25 |
|--------|--------|------|
| **TF Scoring** | Linear (f(q, D)) | Saturating with $k_1$ parameter |
| **Length Penalty** | $1/\sqrt{len}$ (aggressive) | Diminishing via $b$ parameter (configurable) |
| **Tunable** | No hyperparameters | Two hyperparameters ($k_1$, $b$) |
| **Production Ready** | Older, less common | Industry standard (used in Elasticsearch, Solr, etc.) |
| **Computational Cost** | Very low | Very low (similar to TF-IDF) |
| **Typical Performance** | Baseline | 10-30% better than TF-IDF on real corpora |

---

## 🔑 Keyword Search Summary

### Core Principle
Match documents to queries by keyword presence frequency. Both queries and documents converted to **sparse vectors** (word counts), then scored using TF-IDF or **BM25** (modern standard).

### Strengths ✅
1. **Simplicity** — Straightforward, easy to understand and implement
2. **Exactness** — Guarantees retrieved docs contain query keywords (critical for technical searches, product names)
3. **Speed** — Fast computation, can be competitive benchmark
4. **Flexibility** — Can be tuned (BM25 hyperparameters)

### Weaknesses ❌
1. **Lexical Gap** — Fails when user query has different wording than matching document
   - Query: "fast vehicle"
   - Document: "quick car" ← Missed (no keyword overlap)
2. **Synonyms** — Doesn't understand "automobile" ≈ "car"
3. **Semantic Misses** — Query meaning present but keywords absent

---

## 🚀 Why BM25 Is the Standard

- **Decades-Tested** — Proven in production since 1990s
- **Good Balance** — Complexity vs. real-world performance
- **Tunable** — Hyperparameters let you optimize per domain
- **Competitive** — Often matches or beats more complex methods
- **Foundation** — Frequently combined with semantic search in hybrid retrievers

---

## 📚 Key Takeaways

1. **BM25 improves TF-IDF** with term frequency saturation (diminishing returns on repeated terms) and flexible length normalization
2. **Hyperparameters $k_1$ and $b$** allow optimization for your specific corpus and use case
3. **Keyword search strength** is exactness (retrieves docs with actual keywords), critical for technical/product queries
4. **Keyword search weakness** is lexical gap (synonyms, paraphrasing cause misses)
5. **BM25 is the production standard**, industry-wide choice for keyword retrieval in production systems

---

## 💡 Flashcards

### Card 01: BM25 Purpose
**Q:** Why is BM25 used instead of TF-IDF in most modern retrievers?
**A:** BM25 adds term frequency saturation (diminishing returns on repeated keywords) and configurable length normalization, plus two tunable hyperparameters ($k_1$, $b$) that allow optimization for specific corpora. It performs 10-30% better than TF-IDF on real data with similar computational cost.

### Card 02: Term Frequency Saturation
**Q:** What is term frequency saturation in BM25, and why is it important?
**A:** Saturation means scores plateau as term frequency increases—a doc with "pizza" 20 times doesn't score twice as high as "pizza" 10 times (unlike TF-IDF). This is more realistic: beyond a certain repetition count, additional keyword instances add little relevance boost.

### Card 03: Hyperparameter $k_1$
**Q:** What does the $k_1$ hyperparameter control in BM25?
**A:** $k_1$ controls how quickly term frequency saturation occurs. Typical value is 1.5. Higher $k_1$ = slower saturation (rewards more term repetitions). Lower $k_1$ = faster saturation (penalizes repetition more aggressively).

### Card 04: Hyperparameter $b$
**Q:** What does the $b$ hyperparameter control in BM25?
**A:** $b$ controls the strength of length normalization (penalty for long documents). Typical value is 0.75. $b=0$ means no length penalty. $b=1.0$ means full normalization. BM25's diminishing penalties keep long docs relevant if keyword frequency is high (unlike TF-IDF's aggressive penalties).

### Card 05: Length Normalization Difference
**Q:** How does BM25 handle long documents differently than TF-IDF?
**A:** TF-IDF uses $1/\sqrt{length}$ (aggressive penalty). BM25 uses diminishing penalties controlled by $b$. Result: a 2000-word document with high keyword frequency scores 0.82× base in BM25 vs. 0.45× in TF-IDF—much fairer for relevant long documents.

### Card 06: Tunable vs Non-Tunable
**Q:** What's the advantage of BM25's hyperparameters over TF-IDF's fixed approach?
**A:** BM25's $k_1$ and $b$ can be tuned per corpus/domain to optimize performance. TF-IDF has no hyperparameters. This makes BM25 more flexible for production systems where you can A/B test or learn optimal settings from training data.

### Card 07: BM25 Formula Structure
**Q:** Summarize what the BM25 formula does conceptually.
**A:** For each query keyword, calculate IDF × (a term frequency component scaled by $k_1$ and length-normalized by $b$). Sum across all keywords to get total relevance score. This combines rarity (IDF), frequency saturation ($k_1$), and fair length treatment ($b$).

### Card 08: Keyword Search Strength
**Q:** What is the primary strength of keyword search (TF-IDF/BM25)?
**A:** **Exactness**: Guarantees retrieved documents contain the actual keywords from the user's query. Critical for technical searches, product names, or exact term requirements where semantic similarity isn't sufficient.

### Card 09: Keyword Search Weakness
**Q:** What is the primary weakness of keyword search?
**A:** **Lexical gap**: Fails when the query and document have the same meaning but different words. Example: query "fast vehicle" won't match document "quick car" because no keywords overlap. Synonyms and paraphrases are invisible to keyword search.

### Card 10: BM25 Production Adoption
**Q:** Why is BM25 the industry standard for keyword retrieval?
**A:** Decades-tested (since 1990s), good balance of simplicity and performance, tunable hyperparameters, computational efficiency (similar to TF-IDF), and proven effectiveness. Often used as a baseline—more complex methods must beat BM25 to justify the added cost.

---

## 🔗 Related Topics
- **04-keyword-search-tfidf.md** — Foundation: TF-IDF scoring (what BM25 improves on)
- **06-semantic-search-embeddings.md** — Next: Semantic search (addresses keyword search's lexical gap)
- **07-hybrid-retrieval.md** — Integration: Combining keyword (BM25) + semantic search

---

**Status:** 🟢 Complete | **Last Revised:** 2026-04-22 | **Confidence:** 🟢 Solid

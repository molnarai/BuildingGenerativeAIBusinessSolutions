+++
title = "RAG Retrieval Evaluation"
description = "Ranking metrics for evaluating retrieved chunks in RAG systems"
weight = 75
outputs = ["Reveal"]
math = true
thumbnail = "/imgs/slides/rag-retrieval-evaluation.png"

[reveal_hugo]
custom_theme = "css/reveal-robinson.css"
slide_number = true
transition = "convex"
+++

# RAG Retrieval Evaluation

### Ranking Metrics for Retrieved Chunks

MSA 8700 — Module 7

---

## What You Will Learn

| Category | Metrics | Key Question |
|----------|---------|-------------|
| **Precision-Oriented** | P@K, AP, MAP, R-Precision, AUC-PR | "Of the chunks we retrieved, how many were useful?" |
| **Recall-Oriented** | R@K, MR@K, Coverage Recall | "Of all useful chunks, how many did we find?" |
| **Rank-Sensitive** | DCG, NDCG, RR, MRR, ERR | "Are the best chunks ranked highest?" |
| **RAG-Specific** | Context Precision/Recall, Hit Rate, Chunk Attribution | "Does retrieval help generation?" |
| **Evaluation Protocol** | Nugget Recall, Metric@K Curves, Stratified Eval | "How do we run a rigorous evaluation?" |

---

## Core Concepts

In ranked retrieval evaluation, you need three things:

1. **A query** — the user's question or information need
2. **A ranked list of retrieved chunks** — ordered by retriever confidence (index 0 = top)
3. **Relevance judgments** — ground-truth labels for each chunk

---

## Binary vs. Graded Relevance

| Type | Values | Example | When to Use |
|------|--------|---------|-------------|
| **Binary** | relevant / not relevant | `{"c1", "c3", "c5"}` | Simple yes/no relevance |
| **Graded** | 0, 1, 2, ... | `{"c1": 2, "c2": 0, "c3": 1}` | Chunk partially answers query |

The challenge in RAG: relevance is often **partial** — a chunk may contain *part* of an answer.

Binary judgments are often insufficient. **Graded relevance** captures this nuance.

---

## Sample Data

```python
RETRIEVED = ["c1", "c2", "c3", "c4", "c5",
             "c6", "c7", "c8", "c9", "c10"]
RELEVANT  = {"c1", "c3", "c5", "c8"}

# Graded relevance: 0=not relevant, 1=partial, 2=highly relevant
GRADES = {
    "c1": 2, "c2": 0, "c3": 1, "c4": 0,
    "c5": 2, "c6": 0, "c7": 0, "c8": 1,
    "c9": 0, "c10": 0,
}
```

```text
Rank:  1    2    3    4    5    6    7    8    9   10
Chunk: c1   c2   c3   c4   c5   c6   c7   c8   c9  c10
       ✓         ✓         ✓              ✓
```

---

# Part 1: Precision-Oriented Metrics

**"Of the chunks we retrieved, how many were actually useful?"**

These metrics penalize the retriever for returning irrelevant chunks.

---

## 1.1 Precision@K (P@K)

The fraction of the top-K retrieved chunks that are relevant.

$$P@K = \frac{|\lbrace\text{relevant chunks in top-K}\rbrace|}{K}$$

**Key properties:**
- Ignores rank order *within* K — position 1 and position K are equal
- Sensitive to your choice of K
- Common choices: K ∈ {1, 3, 5, 10}

```text
retrieved = [c1, c2, c3, c4, c5]    relevant = {c1, c3}

P@3 = 2/3 ≈ 0.667   (c1 and c3 are relevant; c2 is not)
P@5 = 2/5 = 0.400
```

---

## 1.2 Average Precision (AP)

**AP** computes P@K at each position where a relevant chunk appears, then averages.

$$AP = \frac{1}{|R|} \sum_{k=1}^{n} P@k \cdot \mathbb{1}[\text{retrieved}[k] \in R]$$

**Key properties:**
- Heavily rewards placing relevant chunks near the top
- Penalizes gaps between relevant results
- Summarizes the full precision-recall curve in a single number

```text
retrieved = [c1, c2, c3, c4, c5]    relevant = {c1, c3}

Hit at rank 1: P@1 = 1/1 = 1.000
Hit at rank 3: P@3 = 2/3 = 0.667
AP = (1.000 + 0.667) / 2 = 0.833
```

---

## Why AP Matters

AP distinguishes between **good** and **bad** rankings:

```text
Good ranking (relevant chunks at top):
  [c1, c3, c5, c8, c2, c4, c6, c7, c9, c10]
  AP = 1.000 (all relevant chunks ranked first)

Bad ranking (relevant chunks buried):
  [c2, c4, c6, c7, c9, c1, c3, c5, c8, c10]
  AP = 0.354 (relevant chunks scattered at bottom)
```

P@K alone would not distinguish rank quality — AP captures this.

---

## 1.3 Mean Average Precision (MAP)

**MAP** is the mean of AP scores across multiple queries — the standard aggregate metric for comparing retrieval systems.

$$MAP = \frac{1}{|Q|} \sum_{q=1}^{|Q|} AP(q)$$

```python
def mean_average_precision(queries):
    ap_scores = [average_precision(r, rel) for r, rel in queries]
    return float(np.mean(ap_scores))
```

---

## 1.4 R-Precision

Precision at exactly rank R, where R = |relevant|.

$$\text{R-Precision} = P@R \quad \text{where } R = |\text{relevant}|$$

**Self-normalizes** across queries with different numbers of relevant chunks.

```text
relevant = {c1, c3, c5, c8}  →  R = 4
Top 4 retrieved: [c1, c2, c3, c4]
Hits in top-4: {c1, c3} → 2 of 4

R-Precision = 2/4 = 0.500
```

---

## 1.5 Interpolated Precision-Recall Curve & AUC-PR

The **interpolated P-R curve** plots precision at standard recall breakpoints (0.0, 0.1, ..., 1.0).

**Interpolation rule:** At each recall level $r$, precision is the max precision at any $r' \geq r$:

$$P_{\text{interp}}(r) = \max_{r' \geq r} P(r')$$

**AUC-PR** = Area under this curve (trapezoidal rule) — summarizes the entire curve in one number.

---

# Part 2: Recall-Oriented Metrics

**"Of all the relevant chunks that exist, how many did we actually retrieve?"**

In RAG, recall is arguably **more important** than precision — a missed relevant chunk can mean a missed fact, leading to **hallucination or incomplete answers**.

---

## 2.1 Recall@K (R@K)

The fraction of all relevant chunks that appear in the top-K results.

$$R@K = \frac{|\lbrace\text{relevant chunks in top-K}\rbrace|}{|\text{all relevant chunks}|}$$

**Key difference from P@K:**
- P@K divides by **K** (the retrieval cutoff)
- R@K divides by **|relevant|** (the total number of relevant chunks)

```text
relevant = {c1, c3, c5, c8}  (4 relevant chunks)

R@1 = 1/4 = 0.250  (found c1)
R@3 = 2/4 = 0.500  (found c1, c3)
R@5 = 3/4 = 0.750  (found c1, c3, c5)
R@10 = 4/4 = 1.000 (found all)
```

---

## Precision vs. Recall Trade-off

As K increases:
- **Precision tends to decrease** — more irrelevant chunks included
- **Recall tends to increase** — more relevant chunks found

```text
K     P@K      R@K
──    ─────    ─────
1     1.000    0.250   ← High precision, low recall
3     0.667    0.500
5     0.600    0.750
8     0.500    1.000
10    0.400    1.000   ← Low precision, high recall
```

The optimal K balances both — depends on your application.

---

## 2.2 Coverage Recall

A RAG-specific variant: does the retrieved set collectively cover all **sub-questions or facets** of a complex query?

$$\text{Coverage Recall} = \frac{|\lbrace\text{facets with} \geq 1 \text{ retrieved chunk}\rbrace|}{|\text{all facets}|}$$

Essential for **multi-hop or multi-faceted queries**.

```text
Query: "Tell me about the Eiffel Tower"
  Facet 1 (construction): {c1, c2}  → covered by c1 ✓
  Facet 2 (design):       {c3, c5}  → covered by c3 ✓
  Facet 3 (renovation):   {c8, c9}  → covered by c8? depends on K
  Facet 4 (tourism):      {c6, c7}  → not in top-5 ✗

Coverage Recall @5 = 3/4 = 0.750
```

---

# Part 3: Rank-Sensitive Combined Metrics

These metrics account for **where** in the ranked list relevant chunks appear, and can handle **graded relevance** (not just binary).

Particularly well-suited to RAG — chunk relevance is rarely binary.

---

## 3.1 DCG@K (Discounted Cumulative Gain)

Uses graded relevance with a **logarithmic discount** to lower-ranked positions.

$$DCG@K = \sum_{i=1}^{K} \frac{\text{grade}_i}{\log_2(i + 1)}$$

The logarithmic discount:

| Rank | Divisor | Credit |
|------|---------|--------|
| 1 | $\log_2(2) = 1.000$ | 100% |
| 2 | $\log_2(3) = 1.585$ | 63% |
| 5 | $\log_2(6) = 2.585$ | 39% |
| 10 | $\log_2(11) = 3.459$ | 29% |

Higher-ranked relevant chunks contribute **more** to the score.

---

## DCG@K Example

```text
Retrieved: [c1, c2, c3, c4, c5]
Grades:     2    0    1    0    2

DCG@5 Calculation:
  Rank 1: grade=2  →  2 / log₂(2) = 2.000
  Rank 2: grade=0  →  0 / log₂(3) = 0.000
  Rank 3: grade=1  →  1 / log₂(4) = 0.500
  Rank 4: grade=0  →  0 / log₂(5) = 0.000
  Rank 5: grade=2  →  2 / log₂(6) = 0.774
                                     ─────
  DCG@5 = 3.274
```

---

## 3.2 NDCG@K (Normalized DCG)

The **gold standard** for ranked evaluation. Normalizes DCG by the **Ideal DCG (IDCG)**.

$$NDCG@K = \frac{DCG@K}{IDCG@K}$$

- **NDCG = 1.0** → perfect ranking (most relevant items first)
- **NDCG = 0.0** → no relevant items retrieved

```text
Actual DCG@5  = 3.274  (our ranking)
Ideal ranking = [c1, c5, c3, c8, ...]  (sorted by grade)
IDCG@5        = 4.131  (best possible DCG)

NDCG@5 = 3.274 / 4.131 = 0.793
```

---

## 3.3 Reciprocal Rank (RR) & MRR

**RR** = $1 / \text{rank}$ of the **first** relevant chunk found.

$$RR = \frac{1}{\text{rank of first relevant chunk}}$$

**MRR** = mean of RR across multiple queries.

$$MRR = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \frac{1}{\text{rank}_q}$$

**Answers:** "How quickly does the system surface *at least one* relevant chunk?"

**Limitation:** Only considers the first hit — ignores the rest of the ranked list.

```text
Retrieved = [c1, c2, c3, ...]    c1 is relevant
RR = 1/1 = 1.000

Retrieved = [c2, c4, c1, ...]    c1 is first relevant (rank 3)
RR = 1/3 = 0.333
```

---

## 3.4 Expected Reciprocal Rank (ERR)

Extends MRR by modeling the probability a user is **satisfied** at each rank, with **graded relevance**.

$$ERR = \sum_{r=1}^{n} \frac{1}{r} \cdot R_r \cdot \prod_{i=1}^{r-1} (1 - R_i)$$

where $R_i = \text{grade}_i / \text{max\_grade}$

**Cascading effect:** If a highly relevant chunk is found early, the user is less likely to keep scanning.

```text
Rank 1: grade=2 → R₁=1.0  P(satisfied)=1.0  → 1.0 × 1/1 = 1.000
Rank 2: grade=0 → R₂=0.0  P(reach rank 2)=0.0
ERR = 1.000  (user satisfied immediately at rank 1)
```

---

# Part 4: RAG-Specific Adapted Metrics

Metrics developed specifically for the RAG paradigm — bridging **retrieval quality** with **generation quality**.

---

## 4.1 Context Precision (RAGAS-style)

Measures whether relevant chunks appear **earlier** in the ranked list.

Computed as **Average Precision** — equivalent to MAP for a single query. Popularized by the [RAGAS](https://docs.ragas.io/) framework.

$$\text{Context Precision} = AP(\text{retrieved}, \text{relevant})$$

```text
Good order: [c1, c3, c5, c8, c2]   → Context Precision = 1.000
Bad order:  [c2, c4, c1, c3, c5]   → Context Precision = 0.533

Same chunks retrieved, different rankings → different scores.
```

---

## 4.2 Context Recall (RAGAS-style, LLM-based)

How much of the **ground-truth answer** can be attributed to retrieved context?

Uses an **LLM judge** to check whether each claim in a reference answer is supported.

$$\text{Context Recall} = \frac{|\lbrace\text{claims supported by context}\rbrace|}{|\text{all reference claims}|}$$

```text
Reference claims:
  1. "Eiffel Tower is 330m tall"        → supported ✓
  2. "Built in 1889"                    → supported ✓
  3. "Designed by Gustave Eiffel"       → NOT supported ✗
  4. "Most visited monument in world"   → supported ✓

Context Recall = 3/4 = 0.750
```

This is **semantic, generation-aware recall** — not pure retrieval.

---

## 4.3 Hit Rate @K

The simplest retrieval metric: what fraction of queries have **at least one** relevant chunk in the top-K?

$$\text{Hit Rate@K} = \frac{|\lbrace\text{queries with} \geq 1 \text{ hit in top-K}\rbrace|}{|\text{all queries}|}$$

Coarse but practical — especially when you only need **one good chunk** to answer a question.

```text
Query 1: top-3 has relevant chunk  → hit ✓
Query 2: top-3 has relevant chunk  → hit ✓
Query 3: top-3 has NO relevant     → miss ✗
Query 4: top-3 has relevant chunk  → hit ✓

Hit Rate @3 = 3/4 = 0.750
```

---

## 4.4 Chunk Attribution Rate

What fraction of retrieved chunks are actually **cited or used** by the generator?

$$\text{Attribution Rate} = \frac{|\lbrace\text{retrieved chunks cited in answer}\rbrace|}{|\text{retrieved chunks}|}$$

**Low attribution** → the retriever fetches technically relevant but practically ignored chunks — wasting context window space.

```text
Retrieved: [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
Cited:     {c1, c3, c5}

Attribution Rate = 3/10 = 0.300
```

This bridges retrieval quality with generation quality.

---

# Part 5: Evaluation Protocol

Beyond individual metrics, rigorous RAG evaluation requires careful **protocol design**.

---

## 5.1 Nugget-based Recall

Decompose a reference answer into **atomic facts ("nuggets")** and check which are covered by retrieved chunks.

More fine-grained than document-level judgments — handles multi-faceted queries better.

```text
Nuggets for "Tell me about the Eiffel Tower":
  1. "tower height"       → supported by {c1, c2}  ✓
  2. "construction year"  → supported by {c3}       ✓
  3. "architect name"     → supported by {c8}       ✓
  4. "visitor statistics"  → supported by {c11}      ✗

Nugget Recall = 3/4 = 0.750  (c11 not retrieved)
```

---

## 5.2 Sensitivity Analysis: Metric@K Curves

Plot your metric as K varies from 1 to your context window limit.

The curve shape reveals:
- Does the ranker **degrade gracefully** or drop off sharply?
- What is the **optimal K** — how many chunks to pass to the LLM?

```text
K     P@K     R@K     NDCG@K
──    ─────   ─────   ──────
1     1.000   0.250   0.613
3     0.667   0.500   0.686
5     0.600   0.750   0.793   ← sweet spot?
8     0.500   1.000   0.870
10    0.400   1.000   0.870   ← diminishing returns
```

---

## 5.3 Stratified Evaluation

Break your query set into categories and report metrics **per stratum**.

A retriever might excel at factoid queries but fail on multi-hop ones — aggregate metrics can hide this.

**Common strata:**
- Factoid vs. multi-hop queries
- Short vs. long queries
- Temporal vs. static queries
- Domain-specific categories

```text
Stratum      MAP     MRR     MR@5    HitRate@5
─────────    ─────   ─────   ─────   ─────────
factoid      0.875   1.000   0.875   1.000
multi_hop    0.655   0.750   0.688   1.000
```

---

# Part 6: All Metrics at a Glance

---

## Complete Metric Summary

```text
Retrieved: [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
Relevant:  {c1, c3, c5, c8}
Grades:    c1:2  c2:0  c3:1  c4:0  c5:2  c6:0  c7:0  c8:1  c9:0  c10:0

PRECISION-ORIENTED              RECALL-ORIENTED
  P@1   = 1.000                   R@1   = 0.250
  P@3   = 0.667                   R@3   = 0.500
  P@5   = 0.600                   R@5   = 0.750
  P@10  = 0.400                   R@10  = 1.000
  AP    = 0.729                   Coverage = 0.750
  R-Precision = 0.500

RANK-SENSITIVE                  RAG-SPECIFIC
  DCG@5  = 3.274                  Context Precision = 0.729
  NDCG@5 = 0.793                  Hit Rate @3 = 0.750
  RR     = 1.000                  Hit Rate @5 = 1.000
  ERR    = 1.000                  Attribution Rate = 0.300
```

---

# Part 7: Choosing the Right Metric

---

## Metric Selection by Use Case

| Use Case | Recommended Metrics | Rationale |
|----------|-------------------|-----------|
| **Missing chunks is catastrophic** (medical, legal) | Recall@K, Context Recall | Must find all relevant evidence |
| **Tight context window** (few chunks) | NDCG@K, P@K with small K | Every slot must count |
| **Conversational assistant** | MRR | Just need one relevant chunk fast |
| **General benchmarking** (graded) | NDCG | Most principled overall choice |
| **Multi-faceted queries** | Coverage Recall, Nugget Recall | Must cover all aspects |
| **Debug retriever vs. generator** | Chunk Attribution Rate | Is the retriever helping? |
| **Compare retrieval systems** | MAP, Stratified Evaluation | Fair aggregate comparison |

---

## Metric Selection Decision Tree

```text
Is missing a relevant chunk catastrophic?
├── YES → Use Recall@K + Context Recall
└── NO
    │
    Is the relevance binary or graded?
    ├── BINARY → Use MAP + MRR
    └── GRADED → Use NDCG@K + ERR
        │
        Do you need per-category analysis?
        ├── YES → Add Stratified Evaluation
        └── NO  → Report aggregate + P/R curves

Always also consider:
  • Metric@K curves to find optimal K
  • Chunk Attribution Rate to debug retriever-generator gap
```

---

## General Advice

1. **Never rely on a single metric** — report at least one precision, one recall, and one rank-sensitive metric

2. **Always stratify** by query type to avoid hiding failures behind strong aggregate numbers

3. **Plot Metric@K curves** to find the optimal number of chunks to retrieve

4. **Use NDCG when possible** — it is the most principled choice for graded relevance

---

# Summary

---

## 17 Metrics Across 5 Categories

### Precision-Oriented — "How many retrieved chunks are useful?"
- **P@K** — fraction of top-K that are relevant
- **AP / MAP** — rank-sensitive precision averaged over queries
- **R-Precision** — self-normalizing precision at rank R
- **AUC-PR** — area under the interpolated precision-recall curve

### Recall-Oriented — "How many useful chunks did we find?"
- **R@K / MR@K** — fraction of relevant chunks retrieved
- **Coverage Recall** — fraction of query facets covered

---

## 17 Metrics (continued)

### Rank-Sensitive — "Are the best chunks ranked highest?"
- **DCG / NDCG** — graded relevance with logarithmic rank discount
- **RR / MRR** — speed to first relevant result
- **ERR** — cascading satisfaction model with graded relevance

### RAG-Specific — "Does retrieval quality help generation?"
- **Context Precision** — are relevant chunks ranked first?
- **Context Recall** — are reference claims supported by context?
- **Hit Rate** — did we find at least one relevant chunk?
- **Chunk Attribution Rate** — are retrieved chunks actually used?

### Evaluation Protocol — "How do we run a rigorous evaluation?"
- **Nugget Recall**, **Metric@K Curves**, **Stratified Evaluation**

---

## Code

**Retrieval Evaluation** assess the text-chunk retrieval and ranking of the RAG system

- Example notebook [RAG_Retrieval_Evaluation](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/RAG/RAG-Evaluation/notebooks/RAG_Retrieval_Evaluation.ipynb)
- Example code in [retrieval_evaluation](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/RAG/RAG-Evaluation/retrieval_evaluation/__init__.py)


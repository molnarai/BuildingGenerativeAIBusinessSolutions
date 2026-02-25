# RAG Evaluation: Ranking Metrics for Retrieved Chunks

Evaluating ranked retrieval in RAG systems borrows heavily from Information Retrieval (IR) theory but adapts it to the nuances of chunk-level relevance. Here's a comprehensive breakdown.

---

## Core Concepts Before the Metrics

In ranked retrieval evaluation, you need three things: a **query**, a **ranked list of retrieved chunks**, and **relevance judgments** (binary or graded) for each chunk. The challenge in RAG is that relevance can be partial — a chunk may contain part of an answer — so binary judgments are often insufficient.

---

## Precision-Oriented Metrics

**Precision@K (P@K)** is the fraction of the top-K retrieved chunks that are relevant. It answers "of the first K results, how many were useful?" It ignores rank order within K, treats position 1 and position K equally, and is sensitive to your choice of K. A common choice is K ∈ {1, 3, 5, 10}.

**Mean Average Precision (MAP)** addresses the rank-insensitivity of P@K by computing Average Precision (AP) for a single query — the mean of P@K values calculated at each position where a relevant chunk appears — and then averaging AP across all queries. It heavily rewards systems that place relevant chunks near the top and penalizes gaps between relevant results.

**R-Precision** computes precision at exactly rank R, where R is the total number of relevant chunks for that query. This self-normalizes across queries with different numbers of relevant chunks and is especially useful when the relevant set size varies significantly.

**Precision at Recall Breakpoints** plots precision at fixed recall levels (0.0, 0.1, ..., 1.0), producing an interpolated precision-recall curve. The area under this curve (AUC-PR) summarizes overall retrieval quality. This is more informative than a single threshold metric.

---

## Recall-Oriented Metrics

**Recall@K** measures the fraction of all relevant chunks that appear in the top-K results. In RAG, this is arguably more important than precision because a missed relevant chunk can mean a missed fact, leading to hallucination or incomplete answers. The denominator (total relevant chunks) must be known, which requires thorough relevance annotation.

**Mean Recall@K (MR@K)** is simply the average of Recall@K across all queries in your evaluation set.

**Coverage Recall** is a RAG-specific variant that measures whether the retrieved set collectively *covers* all sub-questions or facets of a complex query. A single chunk might be relevant but only partial; you need to check if the union of retrieved chunks satisfies all informational needs of the query.

---

## Rank-Sensitive Combined Metrics

**NDCG (Normalized Discounted Cumulative Gain)** is arguably the gold standard for ranked evaluation. It uses graded relevance (e.g., 0 = not relevant, 1 = partially relevant, 2 = highly relevant) and applies a logarithmic discount to lower-ranked positions. DCG@K sums `relevance / log2(rank + 1)` over K results; NDCG@K normalizes by the ideal DCG (IDCG), giving a score between 0 and 1. This is particularly well-suited to RAG because chunk relevance is rarely binary.

**MRR (Mean Reciprocal Rank)** computes `1/rank` for the first relevant chunk found, then averages across queries. It answers "how quickly does the system surface at least one relevant result?" It's useful for single-answer retrieval scenarios but collapses to measuring only the first hit and ignores the rest of the ranked list.

**Expected Reciprocal Rank (ERR)** extends MRR by modeling the probability that a user is satisfied at each rank position, incorporating graded relevance. It accounts for the cascading effect of relevance — if a highly relevant chunk is found early, the user is less likely to continue scanning.

---

## RAG-Specific Adapted Metrics

**Context Precision** (popularized by frameworks like RAGAS) measures whether the retrieved chunks that are relevant are ranked higher than irrelevant ones. It is computed similarly to AP but specifically asks: in the ranked list, do relevant chunks precede irrelevant ones?

**Context Recall** (RAGAS) measures how much of the ground-truth answer can be attributed to the retrieved context. It uses an LLM to check whether each sentence or claim in a reference answer is supported by at least one retrieved chunk. This is a semantic, generation-aware recall rather than a pure retrieval metric.

**Hit Rate** (also called Recall@1 or Top-K Hit) is a simplified metric: did at least one relevant chunk appear in the top-K results? It's a coarse but practical measure, especially when you only need one good chunk to answer a question.

**Chunk Attribution Rate** measures what fraction of retrieved chunks are actually cited or used by the generator in its final answer. This bridges retrieval quality with generation quality and can expose cases where the retriever fetches technically relevant but practically ignored chunks.

---

## Evaluation Protocol Considerations

**Relevance annotation depth** matters enormously. Shallow pools (judging only top-10) can underestimate recall since relevant chunks beyond rank 10 go unjudged. Pooling strategies from TREC-style evaluations, where results from multiple systems are pooled before annotation, can help create more complete judgment sets.

**Nugget-based evaluation** decomposes a reference answer into atomic facts ("nuggets") and checks which nuggets are covered by retrieved chunks. This is more fine-grained than document-level judgments and handles multi-faceted queries better.

**Stratified evaluation** breaks your query set into categories (factoid, multi-hop, temporal, etc.) and reports metrics per stratum. A retriever might excel at simple factoid queries but fail badly on multi-hop ones, and aggregate metrics can hide this.

**Sensitivity analysis across K** involves plotting your metric (P@K, R@K, NDCG@K) as K varies from 1 to your context window limit. The shape of this curve reveals whether your ranker degrades gracefully or drops off sharply, informing decisions about how many chunks to pass to the LLM.

---

## Choosing the Right Metric

The right choice depends on your RAG use case. If missing a relevant chunk is catastrophic (e.g., medical or legal QA), prioritize **Recall@K** and **Context Recall**. If you have a tight context window and can only pass a few chunks, **NDCG@K** and **P@K** with a small K are most relevant. For conversational assistants where finding one good answer quickly matters, **MRR** is a natural fit. For general benchmarking across query types with graded relevance, **NDCG** is the most principled choice overall.
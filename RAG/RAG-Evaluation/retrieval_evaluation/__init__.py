"""
RAG Retrieval Ranking Evaluation Metrics
==========================================
Comprehensive Python implementations of precision, recall, and rank-sensitive
metrics for evaluating ranked chunk retrieval in RAG systems.

Data Conventions:
  - retrieved: list of chunk IDs in ranked order (index 0 = top result)
  - relevant:  set/list of chunk IDs that are ground-truth relevant
  - grades:    dict mapping chunk_id -> relevance score (int, e.g. 0/1/2)
  - queries:   list of (retrieved, relevant[, grades]) tuples for multi-query metrics
"""

import math
import numpy as np
from typing import List, Set, Dict, Tuple, Optional


# ---------------------------------------------------------------------------
# 0. Sample Data
# ---------------------------------------------------------------------------

# Single query example
RETRIEVED = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10"]
RELEVANT  = {"c1", "c3", "c5", "c8"}   # ground-truth relevant chunks

# Graded relevance: 0=not relevant, 1=partially relevant, 2=highly relevant
GRADES = {
    "c1": 2, "c2": 0, "c3": 1, "c4": 0,
    "c5": 2, "c6": 0, "c7": 0, "c8": 1,
    "c9": 0, "c10": 0,
}

# Multi-query dataset  (retrieved_list, relevant_set)
QUERIES = [
    (["c1", "c2", "c3", "c4", "c5"],          {"c1", "c3"}),
    (["c6", "c7", "c1", "c8", "c9"],          {"c6", "c8"}),
    (["c2", "c5", "c3", "c10", "c4"],         {"c3", "c10"}),
    (["c1", "c3", "c2", "c5", "c8"],          {"c1", "c3", "c5", "c8"}),
]

# Multi-query with graded relevance
QUERIES_GRADED = [
    (
        ["c1", "c2", "c3", "c4", "c5"],
        {"c1": 2, "c2": 0, "c3": 1, "c4": 0, "c5": 2},
    ),
    (
        ["c6", "c7", "c1", "c8", "c9"],
        {"c6": 2, "c7": 0, "c1": 0, "c8": 1, "c9": 0},
    ),
]


# ===========================================================================
# 1. PRECISION-ORIENTED METRICS
# ===========================================================================

def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    P@K: fraction of top-K retrieved chunks that are relevant.

    Args:
        retrieved: Ranked list of chunk IDs (position 0 = rank 1).
        relevant:  Set of ground-truth relevant chunk IDs.
        k:         Cutoff rank.

    Returns:
        Precision@K in [0, 1].

    Example:
        retrieved = ["c1", "c2", "c3", "c4", "c5"]
        relevant  = {"c1", "c3"}
        P@3 = 1/3 ≈ 0.333   (c1 and c3 are relevant; c2 is not; 2 hits in top-3)
        P@5 = 2/5 = 0.4
    """
    if k <= 0:
        raise ValueError("k must be a positive integer")
    top_k = retrieved[:k]
    hits  = sum(1 for chunk in top_k if chunk in relevant)
    return hits / k


def average_precision(retrieved: List[str], relevant: Set[str]) -> float:
    """
    AP: mean of P@k values computed at each rank where a relevant chunk appears.

    Rewards systems that place all relevant chunks near the top.
    AP = (1/|R|) * Σ P@k  for each k where retrieved[k-1] is relevant

    Returns:
        Average Precision in [0, 1].  Returns 0.0 if relevant set is empty.

    Example:
        retrieved = ["c1", "c2", "c3", "c4", "c5"]
        relevant  = {"c1", "c3"}
        Relevant hits at ranks 1 and 3:
          P@1 = 1/1 = 1.0
          P@3 = 2/3 ≈ 0.667
        AP = (1.0 + 0.667) / 2 ≈ 0.833
    """
    if not relevant:
        return 0.0
    hits = 0
    precision_sum = 0.0
    for rank, chunk in enumerate(retrieved, start=1):
        if chunk in relevant:
            hits += 1
            precision_sum += hits / rank
    return precision_sum / len(relevant)


def mean_average_precision(queries: List[Tuple[List[str], Set[str]]]) -> float:
    """
    MAP: mean of Average Precision scores across multiple queries.

    Args:
        queries: List of (retrieved, relevant) tuples.

    Returns:
        MAP in [0, 1].

    Example:
        queries = [
            (["c1","c2","c3","c4","c5"], {"c1","c3"}),  # AP ≈ 0.833
            (["c6","c7","c1","c8","c9"], {"c6","c8"}),  # AP = (1.0 + 0.5) / 2 = 0.75
        ]
        MAP = (0.833 + 0.75) / 2 ≈ 0.792
    """
    ap_scores = [average_precision(r, rel) for r, rel in queries]
    return float(np.mean(ap_scores))


def r_precision(retrieved: List[str], relevant: Set[str]) -> float:
    """
    R-Precision: precision at rank R, where R = |relevant|.

    Self-normalizes across queries with different relevant-set sizes.
    Equivalent to P@R.

    Example:
        retrieved = ["c1", "c2", "c3", "c4", "c5"]
        relevant  = {"c1", "c3", "c5"}   → R = 3
        Top-3 = ["c1","c2","c3"] → 2 hits → R-Precision = 2/3 ≈ 0.667
    """
    r = len(relevant)
    if r == 0:
        return 0.0
    return precision_at_k(retrieved, relevant, k=r)


def interpolated_precision_recall_curve(
    retrieved: List[str],
    relevant: Set[str],
    recall_levels: Optional[List[float]] = None,
) -> Dict[float, float]:
    """
    Computes interpolated precision at standard recall breakpoints.

    Interpolation: P(r) = max(P(r') for r' >= r)

    Args:
        retrieved:     Ranked chunk list.
        relevant:      Ground-truth relevant set.
        recall_levels: Recall thresholds to evaluate at (default: 0.0 to 1.0).

    Returns:
        Dict mapping recall_level -> interpolated precision.

    Example:
        At recall 0.5, we look at the minimum rank needed to cover 50% of
        relevant chunks, then take max precision at or beyond that point.
    """
    if recall_levels is None:
        recall_levels = [i / 10 for i in range(11)]  # 0.0, 0.1, ..., 1.0

    total_relevant = len(relevant)
    if total_relevant == 0:
        return {r: 0.0 for r in recall_levels}

    # Build raw (recall, precision) pairs at each rank
    raw_points: List[Tuple[float, float]] = []
    hits = 0
    for rank, chunk in enumerate(retrieved, start=1):
        if chunk in relevant:
            hits += 1
            rec  = hits / total_relevant
            prec = hits / rank
            raw_points.append((rec, prec))

    # Interpolate: for each level, take max precision at recall >= level
    interpolated = {}
    for level in recall_levels:
        candidates = [p for (r, p) in raw_points if r >= level]
        interpolated[level] = max(candidates) if candidates else 0.0
    return interpolated


def auc_pr(retrieved: List[str], relevant: Set[str]) -> float:
    """
    Area under the Precision-Recall curve using the trapezoidal rule.

    Returns:
        AUC-PR in [0, 1].
    """
    curve = interpolated_precision_recall_curve(retrieved, relevant)
    levels = sorted(curve.keys())
    precisions = [curve[l] for l in levels]
    auc = float(np.trapz(precisions, levels))
    return auc


# ===========================================================================
# 2. RECALL-ORIENTED METRICS
# ===========================================================================

def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    R@K: fraction of all relevant chunks that appear in the top-K results.

    In RAG, this is critical — a missed relevant chunk = a missed fact.

    Args:
        retrieved: Ranked chunk list.
        relevant:  Ground-truth relevant set.
        k:         Cutoff rank.

    Returns:
        Recall@K in [0, 1].

    Example:
        retrieved = ["c1","c2","c3","c4","c5"]
        relevant  = {"c1","c3","c5"}
        Recall@3 = 2/3 ≈ 0.667  (c1, c3 found; c5 not yet)
        Recall@5 = 3/3 = 1.0
    """
    if not relevant:
        return 0.0
    top_k = set(retrieved[:k])
    hits  = len(top_k & relevant)
    return hits / len(relevant)


def mean_recall_at_k(queries: List[Tuple[List[str], Set[str]]], k: int) -> float:
    """
    MR@K: average Recall@K across multiple queries.

    Example:
        queries = [
            (["c1","c2","c3","c4","c5"], {"c1","c3"}),  # R@3 = 1.0 (both in top-3)
            (["c6","c7","c1","c8","c9"], {"c6","c8"}),  # R@3 = 0.5 (only c6)
        ]
        MR@3 = (1.0 + 0.5) / 2 = 0.75
    """
    scores = [recall_at_k(r, rel, k) for r, rel in queries]
    return float(np.mean(scores))


def coverage_recall(
    retrieved: List[str],
    facets: List[Set[str]],
) -> float:
    """
    Coverage Recall: fraction of query facets (sub-questions) covered by
    at least one retrieved chunk.

    Useful for multi-hop or multi-faceted queries where a single chunk
    may not address all aspects.

    Args:
        retrieved: Retrieved chunk IDs (unranked or ranked).
        facets:    List of sets; each set contains chunk IDs that satisfy
                   one facet/sub-question of the query.

    Returns:
        Fraction of facets covered in [0, 1].

    Example:
        retrieved = ["c1", "c3", "c7"]
        facets = [
            {"c1", "c2"},    # facet 1: answered by c1 ✓
            {"c5", "c6"},    # facet 2: neither c5 nor c6 retrieved ✗
            {"c3", "c7"},    # facet 3: answered by c3 ✓
        ]
        coverage_recall = 2/3 ≈ 0.667
    """
    if not facets:
        return 0.0
    retrieved_set = set(retrieved)
    covered = sum(1 for facet in facets if retrieved_set & facet)
    return covered / len(facets)


# ===========================================================================
# 3. RANK-SENSITIVE COMBINED METRICS
# ===========================================================================

def dcg_at_k(
    retrieved: List[str],
    grades: Dict[str, int],
    k: int,
    log_base: int = 2,
) -> float:
    """
    DCG@K: Discounted Cumulative Gain.

    DCG@K = Σ grade_i / log_base(rank_i + 1)  for rank_i in [1, K]

    Higher-ranked relevant chunks contribute more; logarithmic discount
    reduces the contribution of lower-ranked results.

    Args:
        retrieved: Ranked chunk list.
        grades:    Dict of chunk_id -> relevance grade (non-negative int).
        k:         Cutoff rank.
        log_base:  Logarithm base (2 is standard).

    Returns:
        DCG@K score (non-negative float).

    Example:
        retrieved = ["c1","c2","c3","c4","c5"]
        grades    = {"c1":2, "c2":0, "c3":1, "c4":0, "c5":2}
        DCG@5 = 2/log2(2) + 0/log2(3) + 1/log2(4) + 0/log2(5) + 2/log2(6)
              = 2.0 + 0 + 0.5 + 0 + 0.861 ≈ 3.361
    """
    dcg = 0.0
    for rank, chunk in enumerate(retrieved[:k], start=1):
        grade = grades.get(chunk, 0)
        dcg += grade / math.log(rank + 1, log_base)
    return dcg


def ndcg_at_k(
    retrieved: List[str],
    grades: Dict[str, int],
    k: int,
    log_base: int = 2,
) -> float:
    """
    NDCG@K: Normalized DCG — DCG@K divided by the Ideal DCG@K (IDCG).

    IDCG is computed by sorting all chunks by relevance grade descending.
    NDCG = 1.0 means the ranking is perfect (most relevant items first).

    Args:
        retrieved: Ranked chunk list.
        grades:    Dict of chunk_id -> relevance grade.
        k:         Cutoff rank.

    Returns:
        NDCG@K in [0, 1].

    Example:
        retrieved = ["c1","c2","c3","c4","c5"]
        grades    = {"c1":2, "c2":0, "c3":1, "c4":0, "c5":2}
        DCG@5  ≈ 3.361
        Ideal order = ["c1","c5","c3","c2","c4"]  (grades: 2,2,1,0,0)
        IDCG@5 = 2/log2(2) + 2/log2(3) + 1/log2(4) ≈ 2.0 + 1.262 + 0.5 = 3.762
        NDCG@5 = 3.361 / 3.762 ≈ 0.893
    """
    actual_dcg = dcg_at_k(retrieved, grades, k, log_base)
    # Ideal: sort all judged chunks by grade descending
    ideal_ranking = sorted(grades.keys(), key=lambda c: grades[c], reverse=True)
    ideal_dcg = dcg_at_k(ideal_ranking, grades, k, log_base)
    if ideal_dcg == 0:
        return 0.0
    return actual_dcg / ideal_dcg


def mean_ndcg_at_k(
    queries: List[Tuple[List[str], Dict[str, int]]],
    k: int,
) -> float:
    """
    Mean NDCG@K across multiple queries.

    Args:
        queries: List of (retrieved, grades_dict) tuples.

    Returns:
        Mean NDCG@K in [0, 1].
    """
    scores = [ndcg_at_k(r, g, k) for r, g in queries]
    return float(np.mean(scores))


def reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
    """
    RR: Reciprocal Rank — 1 / rank of the first relevant chunk found.

    Returns 0.0 if no relevant chunk is retrieved.

    Example:
        retrieved = ["c2", "c4", "c1", "c3"]
        relevant  = {"c1", "c3"}
        First hit at rank 3 (c1) → RR = 1/3 ≈ 0.333
    """
    for rank, chunk in enumerate(retrieved, start=1):
        if chunk in relevant:
            return 1.0 / rank
    return 0.0


def mean_reciprocal_rank(queries: List[Tuple[List[str], Set[str]]]) -> float:
    """
    MRR: Mean Reciprocal Rank across multiple queries.

    Answers: "on average, how quickly does the system surface a relevant chunk?"

    Example:
        queries = [
            (["c1","c2","c3"], {"c1"}),  # RR = 1/1 = 1.0
            (["c2","c1","c3"], {"c1"}),  # RR = 1/2 = 0.5
            (["c2","c3","c1"], {"c1"}),  # RR = 1/3 ≈ 0.333
        ]
        MRR = (1.0 + 0.5 + 0.333) / 3 ≈ 0.611
    """
    rr_scores = [reciprocal_rank(r, rel) for r, rel in queries]
    return float(np.mean(rr_scores))


def expected_reciprocal_rank(
    retrieved: List[str],
    grades: Dict[str, int],
    max_grade: int = 2,
) -> float:
    """
    ERR: Expected Reciprocal Rank.

    Models the probability that a user is satisfied at each rank, accounting
    for graded relevance. A highly relevant result early on makes it less
    likely the user continues scanning.

    P(satisfied at rank r) = relevance_probability(r) * Π(1 - relevance_probability(i)) for i < r
    ERR = Σ (1/r) * P(satisfied at rank r)

    where relevance_probability(r) = grade_r / max_grade

    Example:
        retrieved = ["c1","c2","c3"]
        grades    = {"c1":2, "c2":0, "c3":1}
        max_grade = 2
        p(c1) = 2/2 = 1.0 → user fully satisfied at rank 1
        ERR ≈ 1.0 * (1/1) = 1.0  (user stops at rank 1 with probability 1)
    """
    err = 0.0
    p_not_satisfied = 1.0  # probability user has NOT been satisfied yet
    for rank, chunk in enumerate(retrieved, start=1):
        grade = grades.get(chunk, 0)
        rel_prob = grade / max_grade  # probability of satisfaction at this rank
        err += p_not_satisfied * rel_prob * (1.0 / rank)
        p_not_satisfied *= (1.0 - rel_prob)
        if p_not_satisfied < 1e-10:
            break  # user almost certainly satisfied, stop early
    return err


# ===========================================================================
# 4. RAG-SPECIFIC METRICS
# ===========================================================================

def context_precision(retrieved: List[str], relevant: Set[str]) -> float:
    """
    Context Precision (RAGAS-style): are relevant chunks ranked above
    irrelevant ones?

    Computed as Average Precision — equivalent to MAP for a single query.
    Measures whether retrieved chunks that ARE relevant appear earlier in
    the ranked list than those that are NOT.

    Returns:
        Context Precision in [0, 1].

    Example:
        retrieved = ["c1","c2","c3","c4","c5"]  (c1,c3 relevant)
        AP = (P@1 + P@3) / 2 = (1.0 + 0.667) / 2 ≈ 0.833

        Compare: retrieved = ["c2","c4","c1","c3","c5"]  (relevant still c1,c3)
        AP = (P@3 + P@4) / 2 = (0.333 + 0.5) / 2 = 0.417
    """
    return average_precision(retrieved, relevant)


def context_recall_llm_based(
    retrieved_texts: List[str],
    reference_claims: List[str],
    claim_supported: List[bool],
) -> float:
    """
    Context Recall (RAGAS-style): fraction of reference answer claims
    that are supported by at least one retrieved chunk.

    In practice this requires an LLM judge to assign claim_supported.
    This function takes pre-computed support labels as input to simulate
    what the LLM judge would return.

    Args:
        retrieved_texts:  Text of each retrieved chunk (for LLM judge input).
        reference_claims: Atomic claims/sentences from the reference answer.
        claim_supported:  Boolean list — True if an LLM judged the claim
                          as attributable to the retrieved context.

    Returns:
        Context Recall in [0, 1].

    Example:
        reference_claims = [
            "The Eiffel Tower was built in 1889.",
            "It is located in Paris.",
            "It is 330 meters tall.",
        ]
        claim_supported = [True, True, False]   # 3rd claim not in retrieved chunks
        context_recall  = 2/3 ≈ 0.667
    """
    if not reference_claims:
        return 0.0
    if len(reference_claims) != len(claim_supported):
        raise ValueError("reference_claims and claim_supported must be the same length")
    return sum(claim_supported) / len(reference_claims)


def hit_rate_at_k(queries: List[Tuple[List[str], Set[str]]], k: int) -> float:
    """
    Hit Rate @K: fraction of queries where at least one relevant chunk
    appears in the top-K results.

    Coarse but fast metric; useful as a baseline or sanity check.

    Args:
        queries: List of (retrieved, relevant) tuples.
        k:       Cutoff rank.

    Returns:
        Hit Rate in [0, 1].

    Example:
        queries = [
            (["c1","c2","c3"], {"c1"}),  # hit ✓
            (["c4","c5","c6"], {"c1"}),  # miss ✗
            (["c2","c1","c3"], {"c1"}),  # hit ✓
        ]
        Hit Rate@2 = 2/3 ≈ 0.667
    """
    hits = sum(
        1 for retrieved, relevant in queries
        if set(retrieved[:k]) & relevant
    )
    return hits / len(queries)


def chunk_attribution_rate(
    retrieved: List[str],
    cited_chunks: Set[str],
) -> float:
    """
    Chunk Attribution Rate: fraction of retrieved chunks that were actually
    cited/used by the generator in its final answer.

    Bridges retrieval quality with generation quality. Low attribution
    suggests the retriever is fetching technically relevant but practically
    ignored chunks.

    Args:
        retrieved:    List of chunk IDs passed to the LLM context.
        cited_chunks: Set of chunk IDs the LLM cited in its answer.

    Returns:
        Attribution rate in [0, 1].

    Example:
        retrieved    = ["c1","c2","c3","c4","c5"]
        cited_chunks = {"c1","c3"}
        attribution  = 2/5 = 0.4
    """
    if not retrieved:
        return 0.0
    cited = sum(1 for c in retrieved if c in cited_chunks)
    return cited / len(retrieved)


# ===========================================================================
# 5. EVALUATION PROTOCOL UTILITIES
# ===========================================================================

def nugget_recall(
    retrieved: List[str],
    nuggets: List[Tuple[str, Set[str]]],
) -> float:
    """
    Nugget-based Recall: fraction of atomic facts (nuggets) covered by
    the retrieved chunks.

    Each nugget is a (fact_description, supporting_chunk_ids) pair.
    A nugget is "covered" if at least one of its supporting chunks was retrieved.

    Args:
        retrieved: Retrieved chunk IDs.
        nuggets:   List of (nugget_label, set_of_supporting_chunk_ids).

    Returns:
        Nugget recall in [0, 1].

    Example:
        nuggets = [
            ("tower height",   {"c1", "c2"}),   # covered if c1 or c2 retrieved
            ("construction year", {"c3"}),        # covered if c3 retrieved
            ("architect name", {"c5", "c6"}),    # covered if c5 or c6 retrieved
        ]
        retrieved = ["c1", "c4", "c5"]
        Covered: nugget 1 (c1 ✓), nugget 3 (c5 ✓) → 2/3 ≈ 0.667
    """
    if not nuggets:
        return 0.0
    retrieved_set = set(retrieved)
    covered = sum(1 for _, support in nuggets if retrieved_set & support)
    return covered / len(nuggets)


def metric_at_k_curve(
    retrieved: List[str],
    relevant: Set[str],
    metric_fn,
    k_values: Optional[List[int]] = None,
) -> Dict[int, float]:
    """
    Compute any @K metric across a range of K values.

    Useful for sensitivity analysis — plot results to see where your
    retriever degrades. Pass precision_at_k or recall_at_k as metric_fn.

    Args:
        retrieved:  Ranked chunk list.
        relevant:   Ground-truth relevant set.
        metric_fn:  A function with signature (retrieved, relevant, k) -> float.
        k_values:   K values to evaluate (default: 1 to len(retrieved)).

    Returns:
        Dict mapping k -> metric value.

    Example:
        curve = metric_at_k_curve(RETRIEVED, RELEVANT, recall_at_k)
        # {1: 0.25, 2: 0.25, 3: 0.5, 4: 0.5, 5: 0.75, ...}
    """
    if k_values is None:
        k_values = list(range(1, len(retrieved) + 1))
    return {k: metric_fn(retrieved, relevant, k) for k in k_values}


def stratified_evaluation(
    queries_by_type: Dict[str, List[Tuple[List[str], Set[str]]]],
    k: int = 5,
) -> Dict[str, Dict[str, float]]:
    """
    Stratified Evaluation: compute MAP, MRR, MR@K, Hit Rate per query stratum.

    Useful for identifying where your retriever fails (e.g., good at factoid
    queries but poor at multi-hop).

    Args:
        queries_by_type: Dict mapping stratum_name -> list of (retrieved, relevant).
        k:               Cutoff for recall and hit rate metrics.

    Returns:
        Dict mapping stratum_name -> {metric_name: score}.

    Example:
        queries_by_type = {
            "factoid":   [(["c1","c2"], {"c1"}), ...],
            "multi_hop": [(["c3","c4"], {"c3","c4"}), ...],
        }
    """
    results = {}
    for stratum, queries in queries_by_type.items():
        results[stratum] = {
            "MAP":         mean_average_precision(queries),
            "MRR":         mean_reciprocal_rank(queries),
            f"MR@{k}":     mean_recall_at_k(queries, k),
            f"HitRate@{k}": hit_rate_at_k(queries, k),
        }
    return results


# ===========================================================================
# 6. DEMO — run all metrics on the sample data
# ===========================================================================

def _fmt(label: str, value: float) -> str:
    return f"  {label:<40} {value:.4f}"


def run_demo():
    sep = "=" * 55

    print(f"\n{sep}")
    print("  SAMPLE DATA")
    print(sep)
    print(f"  Retrieved : {RETRIEVED}")
    print(f"  Relevant  : {sorted(RELEVANT)}")
    print(f"  Grades    : {GRADES}")

    # --- Precision ---
    print(f"\n{sep}")
    print("  PRECISION-ORIENTED METRICS")
    print(sep)
    for k in [1, 3, 5, 10]:
        print(_fmt(f"Precision@{k}", precision_at_k(RETRIEVED, RELEVANT, k)))
    print(_fmt("Average Precision (AP)", average_precision(RETRIEVED, RELEVANT)))
    print(_fmt("MAP (4 queries)",        mean_average_precision(QUERIES)))
    print(_fmt("R-Precision",            r_precision(RETRIEVED, RELEVANT)))
    print(_fmt("AUC-PR",                 auc_pr(RETRIEVED, RELEVANT)))

    curve = interpolated_precision_recall_curve(RETRIEVED, RELEVANT)
    print("\n  Interpolated P-R Curve:")
    for level in sorted(curve):
        bar = "█" * int(curve[level] * 20)
        print(f"    Recall={level:.1f}  P={curve[level]:.3f}  {bar}")

    # --- Recall ---
    print(f"\n{sep}")
    print("  RECALL-ORIENTED METRICS")
    print(sep)
    for k in [1, 3, 5, 10]:
        print(_fmt(f"Recall@{k}", recall_at_k(RETRIEVED, RELEVANT, k)))
    print(_fmt("Mean Recall@5 (4 queries)", mean_recall_at_k(QUERIES, 5)))

    facets = [{"c1", "c2"}, {"c3", "c5"}, {"c8", "c9"}, {"c6", "c7"}]
    print(_fmt("Coverage Recall (4 facets)", coverage_recall(RETRIEVED[:5], facets)))

    # --- Rank-Sensitive ---
    print(f"\n{sep}")
    print("  RANK-SENSITIVE METRICS")
    print(sep)
    for k in [3, 5, 10]:
        print(_fmt(f"DCG@{k}",  dcg_at_k(RETRIEVED, GRADES, k)))
        print(_fmt(f"NDCG@{k}", ndcg_at_k(RETRIEVED, GRADES, k)))
    print(_fmt("Reciprocal Rank (RR)",    reciprocal_rank(RETRIEVED, RELEVANT)))
    print(_fmt("MRR (4 queries)",         mean_reciprocal_rank(QUERIES)))
    print(_fmt("Mean NDCG@5 (2 graded queries)",
               mean_ndcg_at_k(QUERIES_GRADED, 5)))
    print(_fmt("ERR (graded)",
               expected_reciprocal_rank(RETRIEVED, GRADES, max_grade=2)))

    # --- RAG-Specific ---
    print(f"\n{sep}")
    print("  RAG-SPECIFIC METRICS")
    print(sep)
    print(_fmt("Context Precision",       context_precision(RETRIEVED, RELEVANT)))
    print(_fmt("Hit Rate@3 (4 queries)",  hit_rate_at_k(QUERIES, 3)))
    print(_fmt("Hit Rate@5 (4 queries)",  hit_rate_at_k(QUERIES, 5)))

    cited = {"c1", "c3", "c5"}
    print(_fmt("Chunk Attribution Rate",
               chunk_attribution_rate(RETRIEVED, cited)))

    claims = [
        "The Eiffel Tower was built in 1889.",
        "It is located in Paris.",
        "It is 330 meters tall.",
    ]
    supported = [True, True, False]
    print(_fmt("Context Recall (LLM-based, simulated)",
               context_recall_llm_based(RETRIEVED[:3], claims, supported)))

    # --- Evaluation Protocol Utilities ---
    print(f"\n{sep}")
    print("  EVALUATION PROTOCOL UTILITIES")
    print(sep)

    nuggets = [
        ("tower height",      {"c1", "c2"}),
        ("construction year", {"c3"}),
        ("architect name",    {"c5", "c6"}),
        ("location",          {"c8", "c10"}),
    ]
    print(_fmt("Nugget Recall (4 nuggets)",
               nugget_recall(RETRIEVED[:5], nuggets)))

    print("\n  Precision@K curve:")
    p_curve = metric_at_k_curve(RETRIEVED, RELEVANT, precision_at_k)
    for k, val in sorted(p_curve.items()):
        bar = "█" * int(val * 20)
        print(f"    K={k:<2}  P={val:.3f}  {bar}")

    print("\n  Recall@K curve:")
    r_curve = metric_at_k_curve(RETRIEVED, RELEVANT, recall_at_k)
    for k, val in sorted(r_curve.items()):
        bar = "█" * int(val * 20)
        print(f"    K={k:<2}  R={val:.3f}  {bar}")

    # --- Stratified Evaluation ---
    queries_by_type = {
        "factoid":   QUERIES[:2],
        "multi_hop": QUERIES[2:],
    }
    strat = stratified_evaluation(queries_by_type, k=5)
    print(f"\n{sep}")
    print("  STRATIFIED EVALUATION")
    print(sep)
    for stratum, metrics in strat.items():
        print(f"\n  [{stratum}]")
        for metric_name, score in metrics.items():
            print(_fmt(metric_name, score))

    print(f"\n{sep}\n")


if __name__ == "__main__":
    run_demo()

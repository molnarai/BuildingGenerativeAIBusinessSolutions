"""
Response evaluation metrics: BLEU, ROUGE, and METEOR.

Extracted from detailed_metric_walkthrough.py into reusable functions.
"""

from collections import Counter
import math


def get_ngrams(tokens, n):
    """Extract n-grams from a token list.

    Args:
        tokens: List of string tokens.
        n: Size of n-grams to extract.

    Returns:
        List of n-gram tuples.
    """
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def _tokenize(text):
    """Split text into lowercase whitespace tokens."""
    return text.lower().split() if isinstance(text, str) else list(text)


# ---------------------------------------------------------------------------
# BLEU
# ---------------------------------------------------------------------------

def bleu_score(reference, candidate, max_n=4, weights=None):
    """Compute BLEU score between a reference and candidate sentence.

    Uses clipped n-gram precision with a brevity penalty, following the
    original Papineni et al. formulation.

    Args:
        reference: Reference sentence (string or list of tokens).
        candidate: Candidate sentence (string or list of tokens).
        max_n: Maximum n-gram order (default 4 for BLEU-4).
        weights: Tuple of weights for each n-gram order.  Defaults to
            uniform weights (1/max_n each).

    Returns:
        float: BLEU score in [0, 1].
    """
    ref_tokens = _tokenize(reference)
    cand_tokens = _tokenize(candidate)

    if weights is None:
        weights = tuple(1.0 / max_n for _ in range(max_n))

    # --- n-gram precisions ---
    precisions = []
    for n in range(1, max_n + 1):
        ref_ngrams = Counter(get_ngrams(ref_tokens, n))
        cand_ngrams = Counter(get_ngrams(cand_tokens, n))
        matching = sum((cand_ngrams & ref_ngrams).values())
        total = sum(cand_ngrams.values())
        precisions.append(matching / total if total > 0 else 0.0)

    # If any precision is 0 the geometric mean is 0
    if any(p == 0 for p in precisions):
        return 0.0

    # --- weighted geometric mean of precisions ---
    log_avg = sum(w * math.log(p) for w, p in zip(weights, precisions))
    geometric_mean = math.exp(log_avg)

    # --- brevity penalty ---
    ref_len = len(ref_tokens)
    cand_len = len(cand_tokens)
    if cand_len == 0:
        return 0.0
    ratio = cand_len / ref_len if ref_len > 0 else 0
    brevity_penalty = math.exp(1 - 1 / ratio) if ratio < 1 else 1.0

    return geometric_mean * brevity_penalty


# ---------------------------------------------------------------------------
# ROUGE
# ---------------------------------------------------------------------------

def rouge_n(reference, candidate, n=1):
    """Compute ROUGE-N (n-gram overlap) between reference and candidate.

    Args:
        reference: Reference sentence (string or list of tokens).
        candidate: Candidate sentence (string or list of tokens).
        n: N-gram order (1 for ROUGE-1, 2 for ROUGE-2, etc.).

    Returns:
        dict with keys ``precision``, ``recall``, and ``f1``.
    """
    ref_tokens = _tokenize(reference)
    cand_tokens = _tokenize(candidate)

    ref_ngrams = Counter(get_ngrams(ref_tokens, n))
    cand_ngrams = Counter(get_ngrams(cand_tokens, n))

    matching = sum((cand_ngrams & ref_ngrams).values())
    ref_total = sum(ref_ngrams.values())
    cand_total = sum(cand_ngrams.values())

    precision = matching / cand_total if cand_total > 0 else 0.0
    recall = matching / ref_total if ref_total > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)
           if (precision + recall) > 0 else 0.0)

    return {"precision": precision, "recall": recall, "f1": f1}


def _lcs_length(ref_tokens, cand_tokens):
    """Compute the length of the longest common subsequence via DP."""
    m, n = len(ref_tokens), len(cand_tokens)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_tokens[i - 1] == cand_tokens[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])
    return matrix[m][n]


def rouge_l(reference, candidate):
    """Compute ROUGE-L (longest common subsequence) between reference and candidate.

    Args:
        reference: Reference sentence (string or list of tokens).
        candidate: Candidate sentence (string or list of tokens).

    Returns:
        dict with keys ``precision``, ``recall``, and ``f1``.
    """
    ref_tokens = _tokenize(reference)
    cand_tokens = _tokenize(candidate)

    lcs_len = _lcs_length(ref_tokens, cand_tokens)

    precision = lcs_len / len(cand_tokens) if len(cand_tokens) > 0 else 0.0
    recall = lcs_len / len(ref_tokens) if len(ref_tokens) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)
           if (precision + recall) > 0 else 0.0)

    return {"precision": precision, "recall": recall, "f1": f1}


# ---------------------------------------------------------------------------
# METEOR (simplified – exact-match only, no synonym/stemming support)
# ---------------------------------------------------------------------------

def _count_chunks(ref_tokens, cand_tokens):
    """Count the number of contiguous matching chunks between reference and candidate.

    A chunk is a maximal sequence of matched tokens that are adjacent in both
    the reference and the candidate in the same relative order.
    """
    ref_set = set(ref_tokens)
    cand_set = set(cand_tokens)
    common = ref_set & cand_set

    if not common:
        return 0, 0  # chunks, matches

    # Map each candidate token to whether it's a match, tracking positions
    # Walk through candidate in order and mark aligned ref positions
    ref_positions = {}
    for i, tok in enumerate(ref_tokens):
        if tok in common:
            ref_positions.setdefault(tok, []).append(i)

    # Greedily align candidate tokens to reference positions
    aligned_ref_indices = []
    used = {tok: 0 for tok in common}
    for tok in cand_tokens:
        if tok in common and used[tok] < len(ref_positions[tok]):
            aligned_ref_indices.append(ref_positions[tok][used[tok]])
            used[tok] += 1

    # Count chunks: a new chunk starts whenever the reference index
    # is not consecutive with the previous one
    if not aligned_ref_indices:
        return 0, 0

    chunks = 1
    for i in range(1, len(aligned_ref_indices)):
        if aligned_ref_indices[i] != aligned_ref_indices[i - 1] + 1:
            chunks += 1

    return chunks, len(aligned_ref_indices)


def meteor_score(reference, candidate, beta=3.0, penalty_weight=0.5):
    """Compute a simplified METEOR score between reference and candidate.

    This implements exact-match METEOR with a word-order (chunking) penalty.
    Full METEOR also uses stemming and synonym matching which are not included
    here.

    Args:
        reference: Reference sentence (string or list of tokens).
        candidate: Candidate sentence (string or list of tokens).
        beta: Recall weight (default 3.0 — recall is weighted 3x over precision).
        penalty_weight: Maximum penalty fraction (default 0.5).

    Returns:
        float: METEOR score in [0, 1].
    """
    ref_tokens = _tokenize(reference)
    cand_tokens = _tokenize(candidate)

    ref_set = set(ref_tokens)
    cand_set = set(cand_tokens)
    matches = ref_set & cand_set
    num_matches = len(matches)

    if num_matches == 0:
        return 0.0

    precision = num_matches / len(cand_tokens) if len(cand_tokens) > 0 else 0.0
    recall = num_matches / len(ref_tokens) if len(ref_tokens) > 0 else 0.0

    if precision + recall == 0:
        return 0.0

    # Weighted harmonic mean (emphasises recall when beta > 1)
    f_score = ((1 + beta ** 2) * precision * recall
               / (beta ** 2 * precision + recall))

    # Word-order penalty based on chunking
    chunks, aligned = _count_chunks(ref_tokens, cand_tokens)
    if aligned > 0:
        fragmentation = chunks / aligned
        penalty = penalty_weight * fragmentation
    else:
        penalty = 0.0

    return f_score * (1 - penalty)

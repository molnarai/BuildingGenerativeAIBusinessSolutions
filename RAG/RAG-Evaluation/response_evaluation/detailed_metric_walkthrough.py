"""
STEP-BY-STEP WALKTHROUGH: BLEU, ROUGE, and METEOR
Detailed calculations with intermediate steps shown
"""

from collections import Counter
import math


print("\n" + "="*80)
print("PART 1: BLEU SCORE - STEP BY STEP")
print("="*80)

reference = "the cat is on the mat"
candidate = "the cat on the mat"

print(f"\nReference: '{reference}'")
print(f"Candidate: '{candidate}'")

ref_tokens = reference.split()
cand_tokens = candidate.split()

print(f"\nStep 0: Tokenize")
print(f"  Reference tokens: {ref_tokens}")
print(f"  Candidate tokens: {cand_tokens}")
print(f"  Ref length: {len(ref_tokens)}, Cand length: {len(cand_tokens)}")

# BLEU uses n-grams (1-gram through 4-gram typically)
print(f"\nStep 1: Extract N-grams")

def get_ngrams(tokens, n):
    """Extract n-grams from token list"""
    ngrams_list = []
    for i in range(len(tokens) - n + 1):
        ngrams_list.append(tuple(tokens[i:i+n]))
    return ngrams_list

# Calculate for 1-grams, 2-grams, 3-grams, 4-grams
for n in range(1, 5):
    ref_ngrams = get_ngrams(ref_tokens, n)
    cand_ngrams = get_ngrams(cand_tokens, n)
    
    print(f"\n  {n}-grams:")
    print(f"    Reference {n}-grams: {ref_ngrams}")
    print(f"    Candidate {n}-grams: {cand_ngrams}")
    
    # Count matches
    ref_counter = Counter(ref_ngrams)
    cand_counter = Counter(cand_ngrams)
    
    # Matching n-grams (clip counts to reference max)
    matching_count = sum((cand_counter & ref_counter).values())
    total_cand = sum(cand_counter.values())
    
    precision = matching_count / total_cand if total_cand > 0 else 0.0
    
    print(f"    Matching {n}-grams: {matching_count}")
    print(f"    Total candidate {n}-grams: {total_cand}")
    print(f"    {n}-gram precision: {matching_count}/{total_cand} = {precision:.4f}")

print(f"\nStep 2: Calculate Geometric Mean of Precisions")
print(f"  We use equal weights for BLEU-4: (0.25, 0.25, 0.25, 0.25)")

precisions = []
for n in range(1, 5):
    ref_ngrams = Counter(get_ngrams(ref_tokens, n))
    cand_ngrams = Counter(get_ngrams(cand_tokens, n))
    matching = sum((cand_ngrams & ref_ngrams).values())
    total = sum(cand_ngrams.values())
    prec = matching / total if total > 0 else 0.0
    precisions.append(prec)
    print(f"  P{n} = {prec:.4f}")

print(f"\n  Geometric mean = (P1 × P2 × P3 × P4)^(1/4)")
print(f"                 = ({precisions[0]:.4f} × {precisions[1]:.4f} × {precisions[2]:.4f} × {precisions[3]:.4f})^(1/4)")

if all(p > 0 for p in precisions):
    log_sum = sum(math.log(p) for p in precisions)
    geometric_mean = math.exp(log_sum / 4)
    print(f"                 = exp((ln({precisions[0]:.4f}) + ln({precisions[1]:.4f}) + ln({precisions[2]:.4f}) + ln({precisions[3]:.4f})) / 4)")
    print(f"                 = exp(({sum(math.log(p) for p in precisions):.4f}) / 4)")
    print(f"                 = exp({log_sum/4:.4f})")
    print(f"                 = {geometric_mean:.4f}")
else:
    geometric_mean = 0.0
    print(f"  → One or more precisions is 0, so geometric mean = 0")

print(f"\nStep 3: Apply Brevity Penalty")
print(f"  Brevity penalty penalizes if candidate is shorter than reference")
print(f"  Reference length: {len(ref_tokens)}")
print(f"  Candidate length: {len(cand_tokens)}")
print(f"  Ratio: {len(cand_tokens)} / {len(ref_tokens)} = {len(cand_tokens)/len(ref_tokens):.4f}")

ratio = len(cand_tokens) / len(ref_tokens) if len(ref_tokens) > 0 else 0
if ratio < 1:
    brevity_penalty = math.exp(1 - 1/ratio) if ratio > 0 else 0
    print(f"  Ratio < 1, so apply penalty")
    print(f"  BP = exp(1 - 1/{ratio:.4f}) = exp(1 - {1/ratio:.4f}) = exp({1 - 1/ratio:.4f})")
    print(f"     = {brevity_penalty:.4f}")
else:
    brevity_penalty = 1.0
    print(f"  Ratio >= 1, so no penalty (BP = 1.0)")

print(f"\nStep 4: Final BLEU Score")
bleu_score = geometric_mean * brevity_penalty
print(f"  BLEU = Geometric Mean × Brevity Penalty")
print(f"       = {geometric_mean:.4f} × {brevity_penalty:.4f}")
print(f"       = {bleu_score:.4f}")


# SECOND EXAMPLE - Perfect match
print("\n\n" + "="*80)
print("BLEU EXAMPLE 2: Perfect Match")
print("="*80)

ref2 = "the cat sat on the mat"
cand2 = "the cat sat on the mat"

print(f"\nReference: '{ref2}'")
print(f"Candidate: '{cand2}'")

ref2_tokens = ref2.split()
cand2_tokens = cand2.split()

print(f"\nSince the sentences are identical:")
print(f"  All n-grams will match perfectly")
print(f"  All precisions = 1.0")
print(f"  Geometric mean = 1.0")
print(f"  Brevity penalty = 1.0 (same length)")
print(f"  BLEU = 1.0 × 1.0 = 1.0")

# THIRD EXAMPLE - No overlap
print("\n\n" + "="*80)
print("BLEU EXAMPLE 3: No N-gram Overlap")
print("="*80)

ref3 = "the dog ran fast"
cand3 = "a cat walked slowly"

print(f"\nReference: '{ref3}'")
print(f"Candidate: '{cand3}'")

ref3_tokens = ref3.split()
cand3_tokens = cand3.split()

print(f"\nReference tokens: {ref3_tokens}")
print(f"Candidate tokens: {cand3_tokens}")
print(f"\nNo tokens in common between reference and candidate")
print(f"  1-gram precision: 0/4 = 0.0")
print(f"  2-gram precision: 0/3 = 0.0")
print(f"  etc.")
print(f"\nGeometric mean = (0.0 × 0.0 × 0.0 × 0.0)^(1/4) = 0.0")
print(f"Brevity penalty doesn't matter when precision = 0")
print(f"BLEU = 0.0 × (anything) = 0.0")


# ============================================================================
# ROUGE WALKTHROUGH
# ============================================================================
print("\n\n" + "="*80)
print("PART 2: ROUGE SCORE - STEP BY STEP")
print("="*80)

reference = "the cat is on the mat"
candidate = "the cat on the mat"

print(f"\nReference: '{reference}'")
print(f"Candidate: '{candidate}'")

ref_tokens = reference.split()
cand_tokens = candidate.split()

print(f"\nReference tokens: {ref_tokens}")
print(f"Candidate tokens: {cand_tokens}")

# ROUGE-1
print("\n" + "-"*80)
print("ROUGE-1: Unigram Overlap (single words)")
print("-"*80)

print(f"\nStep 1: Create word counters")
ref_counter = Counter(ref_tokens)
cand_counter = Counter(cand_tokens)
print(f"  Reference word counts: {dict(ref_counter)}")
print(f"  Candidate word counts: {dict(cand_counter)}")

print(f"\nStep 2: Find common words (intersection with min counts)")
common = cand_counter & ref_counter  # Takes minimum count for each word
print(f"  Common words: {dict(common)}")
print(f"  Total common: {sum(common.values())}")

print(f"\nStep 3: Calculate ROUGE-1 Recall")
print(f"  Recall = (matching words) / (total reference words)")
matching_words = sum(common.values())
ref_total = sum(ref_counter.values())
recall = matching_words / ref_total if ref_total > 0 else 0.0
print(f"         = {matching_words} / {ref_total}")
print(f"         = {recall:.4f}")

print(f"\nStep 4: Calculate ROUGE-1 Precision")
print(f"  Precision = (matching words) / (total candidate words)")
cand_total = sum(cand_counter.values())
precision = matching_words / cand_total if cand_total > 0 else 0.0
print(f"           = {matching_words} / {cand_total}")
print(f"           = {precision:.4f}")

print(f"\nStep 5: Calculate ROUGE-1 F1 Score")
if precision + recall > 0:
    f1 = 2 * (precision * recall) / (precision + recall)
else:
    f1 = 0.0
print(f"  F1 = 2 × (Precision × Recall) / (Precision + Recall)")
print(f"     = 2 × ({precision:.4f} × {recall:.4f}) / ({precision:.4f} + {recall:.4f})")
print(f"     = 2 × {precision * recall:.4f} / {precision + recall:.4f}")
print(f"     = {f1:.4f}")

# ROUGE-2
print(f"\n" + "-"*80)
print("ROUGE-2: Bigram Overlap (2-word sequences)")
print("-"*80)

print(f"\nStep 1: Extract bigrams")
ref_bigrams = get_ngrams(ref_tokens, 2)
cand_bigrams = get_ngrams(cand_tokens, 2)
print(f"  Reference bigrams: {ref_bigrams}")
print(f"  Candidate bigrams: {cand_bigrams}")

print(f"\nStep 2: Create bigram counters")
ref_bigram_counter = Counter(ref_bigrams)
cand_bigram_counter = Counter(cand_bigrams)
print(f"  Reference bigram counts: {dict(ref_bigram_counter)}")
print(f"  Candidate bigram counts: {dict(cand_bigram_counter)}")

print(f"\nStep 3: Find matching bigrams")
common_bigrams = cand_bigram_counter & ref_bigram_counter
print(f"  Common bigrams: {dict(common_bigrams)}")
matching_bigrams = sum(common_bigrams.values())
print(f"  Total matching: {matching_bigrams}")

print(f"\nStep 4: Calculate ROUGE-2")
ref_bigram_total = sum(ref_bigram_counter.values())
cand_bigram_total = sum(cand_bigram_counter.values())
recall_2 = matching_bigrams / ref_bigram_total if ref_bigram_total > 0 else 0.0
precision_2 = matching_bigrams / cand_bigram_total if cand_bigram_total > 0 else 0.0
f1_2 = 2 * (precision_2 * recall_2) / (precision_2 + recall_2) if (precision_2 + recall_2) > 0 else 0.0
print(f"  Recall:    {matching_bigrams} / {ref_bigram_total} = {recall_2:.4f}")
print(f"  Precision: {matching_bigrams} / {cand_bigram_total} = {precision_2:.4f}")
print(f"  F1:        {f1_2:.4f}")

# ROUGE-L (Longest Common Subsequence)
print(f"\n" + "-"*80)
print("ROUGE-L: Longest Common Subsequence (LCS)")
print("-"*80)

print(f"\nStep 1: What is LCS?")
print(f"  It's the longest sequence that appears in both (in order, but not necessarily contiguous)")
print(f"  Reference: {ref_tokens}")
print(f"  Candidate: {cand_tokens}")

print(f"\nStep 2: Build LCS Matrix using Dynamic Programming")
m, n = len(ref_tokens), len(cand_tokens)
lcs_matrix = [[0] * (n + 1) for _ in range(m + 1)]

print(f"  Rows (reference): {m}, Columns (candidate): {n}")
print(f"  Initialize all values to 0")
print(f"  For each cell [i,j]:")
print(f"    If ref[i-1] == cand[j-1]: matrix[i][j] = matrix[i-1][j-1] + 1")
print(f"    Else: matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1])")

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if ref_tokens[i-1] == cand_tokens[j-1]:
            lcs_matrix[i][j] = lcs_matrix[i-1][j-1] + 1
        else:
            lcs_matrix[i][j] = max(lcs_matrix[i-1][j], lcs_matrix[i][j-1])

print(f"\n  Final LCS Matrix:")
print(f"       ", " ".join(f"{t:>3}" for t in [""] + cand_tokens))
for i, ref_token in enumerate([""] + ref_tokens):
    row = " ".join(f"{val:>3}" for val in lcs_matrix[i])
    print(f"  {ref_token:>3}  {row}")

lcs_length = lcs_matrix[m][n]
print(f"\n  LCS length = {lcs_length}")

print(f"\nStep 3: Calculate ROUGE-L")
recall_l = lcs_length / len(ref_tokens) if len(ref_tokens) > 0 else 0.0
precision_l = lcs_length / len(cand_tokens) if len(cand_tokens) > 0 else 0.0
f1_l = 2 * (precision_l * recall_l) / (precision_l + recall_l) if (precision_l + recall_l) > 0 else 0.0
print(f"  Recall:    {lcs_length} / {len(ref_tokens)} = {recall_l:.4f}")
print(f"  Precision: {lcs_length} / {len(cand_tokens)} = {precision_l:.4f}")
print(f"  F1:        {f1_l:.4f}")

print(f"\nStep 4: ROUGE-L is order-aware")
print(f"  LCS preserves word order in the sequence")
print(f"  If words appear in different order, LCS is shorter")

# ROUGE Example 2
print("\n\n" + "="*80)
print("ROUGE EXAMPLE 2: Different Word Order")
print("="*80)

ref_ex2 = "alice gave a book to bob"
cand_ex2 = "bob received a book from alice"

print(f"\nReference: '{ref_ex2}'")
print(f"Candidate: '{cand_ex2}'")

ref_ex2_tokens = ref_ex2.split()
cand_ex2_tokens = cand_ex2.split()

print(f"\nReference tokens: {ref_ex2_tokens}")
print(f"Candidate tokens: {cand_ex2_tokens}")

# ROUGE-1
ref_ex2_counter = Counter(ref_ex2_tokens)
cand_ex2_counter = Counter(cand_ex2_tokens)
common_ex2 = cand_ex2_counter & ref_ex2_counter
matching_ex2 = sum(common_ex2.values())
print(f"\nCommon words: {dict(common_ex2)}")
print(f"Total matching: {matching_ex2}")

recall_ex2_1 = matching_ex2 / len(ref_ex2_tokens)
precision_ex2_1 = matching_ex2 / len(cand_ex2_tokens)
f1_ex2_1 = 2 * (precision_ex2_1 * recall_ex2_1) / (precision_ex2_1 + recall_ex2_1)

print(f"ROUGE-1 F1: {f1_ex2_1:.4f}")

# ROUGE-L
m2, n2 = len(ref_ex2_tokens), len(cand_ex2_tokens)
lcs_matrix_2 = [[0] * (n2 + 1) for _ in range(m2 + 1)]
for i in range(1, m2 + 1):
    for j in range(1, n2 + 1):
        if ref_ex2_tokens[i-1] == cand_ex2_tokens[j-1]:
            lcs_matrix_2[i][j] = lcs_matrix_2[i-1][j-1] + 1
        else:
            lcs_matrix_2[i][j] = max(lcs_matrix_2[i-1][j], lcs_matrix_2[i][j-1])

lcs_length_2 = lcs_matrix_2[m2][n2]
recall_ex2_l = lcs_length_2 / len(ref_ex2_tokens)
precision_ex2_l = lcs_length_2 / len(cand_ex2_tokens)
f1_ex2_l = 2 * (precision_ex2_l * recall_ex2_l) / (precision_ex2_l + recall_ex2_l)

print(f"ROUGE-L F1: {f1_ex2_l:.4f}")
print(f"\n→ Notice: ROUGE-1 is high (same words) but ROUGE-L is lower (different order)")
print(f"  ROUGE-1 doesn't care about word order, ROUGE-L does!")


# ============================================================================
# METEOR WALKTHROUGH
# ============================================================================
print("\n\n" + "="*80)
print("PART 3: METEOR SCORE - STEP BY STEP")
print("="*80)

reference = "the cat is on the mat"
candidate = "the cat on the mat"

print(f"\nReference: '{reference}'")
print(f"Candidate: '{candidate}'")

ref_tokens = reference.split()
cand_tokens = candidate.split()

print(f"\nReference tokens: {ref_tokens}")
print(f"Candidate tokens: {cand_tokens}")

print(f"\nStep 1: Find Exact Token Matches")
ref_set = set(ref_tokens)
cand_set = set(cand_tokens)
matches = ref_set & cand_set
print(f"  Reference tokens (unique): {ref_set}")
print(f"  Candidate tokens (unique): {cand_set}")
print(f"  Matches: {matches}")
print(f"  Number of matches: {len(matches)}")

print(f"\nStep 2: Calculate Precision and Recall")
precision = len(matches) / len(cand_tokens) if len(cand_tokens) > 0 else 0.0
recall = len(matches) / len(ref_tokens) if len(ref_tokens) > 0 else 0.0
print(f"  Precision = matches / candidate tokens = {len(matches)} / {len(cand_tokens)} = {precision:.4f}")
print(f"  Recall    = matches / reference tokens = {len(matches)} / {len(ref_tokens)} = {recall:.4f}")

print(f"\nStep 3: Calculate Harmonic Mean (F-score with beta=3)")
print(f"  METEOR emphasizes recall (beta=3 means recall is weighted 3x)")
print(f"  F-score = ((1 + beta²) × P × R) / (beta² × P + R)")
alpha = 3.0
if precision + recall > 0:
    f_score = (1 + alpha**2) * (precision * recall) / ((alpha**2 * precision) + recall)
else:
    f_score = 0.0
print(f"  F-score = ((1 + 9) × {precision:.4f} × {recall:.4f}) / (9 × {precision:.4f} + {recall:.4f})")
print(f"         = (10 × {precision * recall:.4f}) / ({9*precision + recall:.4f})")
print(f"         = {10 * precision * recall:.4f} / {9*precision + recall:.4f}")
print(f"         = {f_score:.4f}")

print(f"\nStep 4: Apply Word Order Penalty (Simplified)")
print(f"  METEOR penalizes if matches are fragmented (not contiguous)")
print(f"  Simplified version: penalty = 0.5 × (# chunks) / (# matches)")
print(f"  For this example, penalty would be applied if matches were fragmented")
print(f"  Since most matches are contiguous, penalty is minimal")

meteor_score = f_score  # Simplified - ignoring penalty for clarity
print(f"\nStep 5: Final METEOR Score")
print(f"  METEOR = {f_score:.4f} (without detailed penalty calculation)")

# METEOR Example 2: With Synonyms
print("\n\n" + "="*80)
print("METEOR EXAMPLE 2: Why Synonyms Matter")
print("="*80)

ref_syn = "the quick brown fox jumps"
cand_syn = "the fast brown fox leaps"

print(f"\nReference: '{ref_syn}'")
print(f"Candidate: '{cand_syn}'")

ref_syn_tokens = ref_syn.split()
cand_syn_tokens = cand_syn.split()

print(f"\nReference tokens: {ref_syn_tokens}")
print(f"Candidate tokens: {cand_syn_tokens}")

# Exact match
matches_exact = set(ref_syn_tokens) & set(cand_syn_tokens)
print(f"\nExact matches: {matches_exact}")
print(f"Count: {len(matches_exact)}")

prec_exact = len(matches_exact) / len(cand_syn_tokens)
recall_exact = len(matches_exact) / len(ref_syn_tokens)
f_exact = (1 + 9) * (prec_exact * recall_exact) / (9*prec_exact + recall_exact) if (prec_exact + recall_exact) > 0 else 0

print(f"\nExact-match METEOR:")
print(f"  Precision: {len(matches_exact)}/{len(cand_syn_tokens)} = {prec_exact:.4f}")
print(f"  Recall:    {len(matches_exact)}/{len(ref_syn_tokens)} = {recall_exact:.4f}")
print(f"  METEOR:    {f_exact:.4f}")

print(f"\nFull METEOR (with synonym matching):")
print(f"  'quick' matches 'fast' (synonym)")
print(f"  'jumps' matches 'leaps' (synonym)")
print(f"  So actual matches would be: the, brown, fox, quick↔fast, jumps↔leaps")
print(f"  With synonyms: 5/5 = 1.0 (perfect score)")
print(f"\n→ This is why METEOR is better for paraphrasing:")
print(f"  It recognizes that 'quick' and 'fast' mean the same thing")

# METEOR Example 3: Word Order Matters
print("\n\n" + "="*80)
print("METEOR EXAMPLE 3: Word Order Penalty")
print("="*80)

ref_order = "alice gave book to bob"
cand_order = "bob book gave alice to"

print(f"\nReference: '{ref_order}'")
print(f"Candidate: '{cand_order}'")

ref_order_tokens = ref_order.split()
cand_order_tokens = cand_order.split()

print(f"\nAll tokens match, but order is scrambled!")

matches_order = set(ref_order_tokens) & set(cand_order_tokens)
print(f"Matching tokens: {matches_order} (count: {len(matches_order)})")

# Precision and recall
prec_order = len(matches_order) / len(cand_order_tokens)
recall_order = len(matches_order) / len(ref_order_tokens)
f_order = (1 + 9) * (prec_order * recall_order) / (9*prec_order + recall_order) if (prec_order + recall_order) > 0 else 0

print(f"\nBefore word order penalty:")
print(f"  Precision: {len(matches_order)}/{len(cand_order_tokens)} = {prec_order:.4f}")
print(f"  Recall:    {len(matches_order)}/{len(ref_order_tokens)} = {recall_order:.4f}")
print(f"  F-score:   {f_order:.4f}")

print(f"\nWord order penalty:")
print(f"  Reference word order: alice → gave → book → to → bob")
print(f"  Candidate word order: bob → book → gave → alice → to")
print(f"  These are in completely different order")
print(f"  Penalty would be large: penalty = 0.5 × (# chunks) / (# matches)")
print(f"  # chunks = # of contiguous matching sequences = high")
print(f"  Final METEOR = F-score × (1 - penalty) = {f_order:.4f} × (smaller multiplier)")
print(f"  Resulting METEOR << {f_order:.4f}")

print(f"\n→ Key insight: METEOR punishes scrambled word order!")
print(f"  This makes it more sophisticated than simple token matching")

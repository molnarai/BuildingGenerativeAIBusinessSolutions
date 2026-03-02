# BLEU vs ROUGE vs METEOR: Teaching Guide

## Quick Summary Table

| Aspect | BLEU | ROUGE | METEOR |
|--------|------|-------|--------|
| **Core Idea** | N-gram precision | N-gram recall | Matched words + order |
| **Precision vs Recall** | Precision-focused | Recall-focused | Balanced (R-favored) |
| **Word Order** | Via n-grams | ROUGE-L uses LCS | Penalty for scrambling |
| **Synonyms** | ❌ No | ❌ No | ✅ Yes |
| **Stemming** | ❌ No | ❌ No | ✅ Yes |
| **Best For** | Translation | Summarization | Translation, QA |
| **Computational Cost** | Fast | Fast | Slower |
| **Human Correlation** | Moderate | Good | Very Good |

---

## Example 1: Perfect Match

```
Reference: "The cat sat on the mat"
Candidate: "The cat sat on the mat"

Expected: All metrics should be 1.0 (perfect match)

BLEU:   1.0000  ✓ All n-grams match perfectly
ROUGE-1: 1.0000  ✓ All unigrams match
ROUGE-L: 1.0000  ✓ LCS = full length
METEOR: 1.0000  ✓ All tokens match
```

**Lesson:** When answers are identical, all metrics agree they're perfect.

---

## Example 2: One Word Missing (the "is")

```
Reference: "The cat is on the mat"  (6 words)
Candidate: "The cat on the mat"     (5 words)

Tokens match: the(2), cat(1), on(1), mat(1) = 5 out of 6 from reference

BLEU Analysis:
  1-grams: 5/5 = 1.0 ✓ (all single words match)
  2-grams: 3/4 = 0.75 ⚠️ (some bigrams broken by missing "is")
  3-grams: 1/3 = 0.33 ⚠️ (fewer trigrams match)
  4-grams: 0/2 = 0.0  ❌ (no 4-grams match)
  → Geometric mean drops to 0 because one n-gram = 0

BLEU: 0.0000  ❌ HARSH PENALTY FOR MISSING ONE WORD!

ROUGE-1 Analysis:
  Common words: 5
  Recall: 5/6 = 0.833 ✓ (caught 5 of 6 words)
  Precision: 5/5 = 1.0 ✓ (all predicted words were correct)
  F1: 0.909  ✓

ROUGE-L Analysis:
  LCS: "the cat on the mat" = 5 words match in order
  Length recall: 5/6 = 0.833
  F1: 0.909  ✓

METEOR Analysis:
  Matched tokens: 4 (the, cat, on, mat) - "is" missing
  Precision: 4/5 = 0.8
  Recall: 4/6 = 0.667
  F-score: 0.678  ✓

Summary:
  BLEU:    0.0000  ← PENALIZES HARD (no 4-grams matched)
  ROUGE-1: 0.909   ← FORGIVING (missing 1 word, ignore order)
  ROUGE-L: 0.909   ← FORGIVING (missing 1 word, but order matters)
  METEOR:  0.678   ← MODERATE (missing 1 token, balanced P/R)
```

**Key Lesson:** 
- BLEU is **too strict** - one missing word → geometric mean becomes 0
- ROUGE is **forgiving** - gives credit for what's there
- METEOR is **balanced** - accounts for both presence and absence
- **For RAG, BLEU alone is problematic!**

---

## Example 3: Paraphrase (Same Meaning, Different Words)

```
Reference: "The Eiffel Tower was built in 1889"
Candidate: "The Tower of Eiffel was constructed in 1889"

Content: Both say same thing, but different phrasing
Missing: "The Eiffel" vs "The Tower of"
Different verb: "built" vs "constructed"

BLEU Analysis:
  Common unigrams: the(2), in(1), 1889(1) = 3 words match
  But "Eiffel" ≠ "Tower", "built" ≠ "constructed"
  N-gram overlap drops significantly
  Most higher n-grams don't match (different word order)
  
BLEU: ~0.3-0.4  ❌ PENALIZES PARAPHRASING HEAVILY

ROUGE-1 Analysis:
  Common words: the, in, 1889 = 3
  Recall: 3/7 = 0.43
  But wait, let's check exactly...
  Reference: [the, eiffel, tower, was, built, in, 1889]
  Candidate: [the, tower, of, eiffel, was, constructed, in, 1889]
  Common: {the, tower, eiffel, in, 1889} = 5!
  
  Recall: 5/7 = 0.714
  Precision: 5/8 = 0.625
  F1: 0.667  ✓ BETTER

ROUGE-L Analysis:
  "The ... [tower/eiffel] ... was ... in 1889"
  LCS = [the, [tower or eiffel], was, in, 1889] ≈ 4-5 words
  F1: ~0.6-0.7  ✓ BETTER THAN BLEU

METEOR Analysis (with synonym matching):
  Exact matches: the, in, 1889, tower, eiffel, was = 6
  Synonym matches: "built" ≈ "constructed"
  Total: 7/7 = potentially high score
  
METEOR: ~0.8-0.9  ✓ BEST AT HANDLING PARAPHRASING

Summary:
  BLEU:    0.3-0.4  ← FAILS on paraphrasing (exact phrases matter)
  ROUGE-1: 0.667    ← OKAY (ignores order, just word bags)
  ROUGE-L: 0.6-0.7  ← OKAY (considers sequence)
  METEOR:  0.8-0.9  ← BEST (handles synonyms)
```

**Key Lesson:**
- BLEU **hates paraphrasing** (different word choices = lower score)
- ROUGE **tolerates paraphrasing** (word bag matching)
- METEOR **excels at paraphrasing** (synonym/stem awareness)
- **For RAG with abstractive answers, ROUGE > BLEU**
- **For highest quality, add METEOR to the mix**

---

## Example 4: Complete Nonsense (Different Order)

```
Reference: "Alice gave a book to Bob"
Candidate: "Bob gave a book to Alice"

All same words, but completely different MEANING!

BLEU Analysis:
  1-grams: all match (6/6 = 1.0)
  2-grams: some match
    Ref: [Alice-gave, gave-a, a-book, book-to, to-Bob]
    Cand: [Bob-gave, gave-a, a-book, book-to, to-Alice]
    Match: [gave-a, a-book, book-to] = 3/5 = 0.6
  3-grams: fewer match
  BLEU: ~0.4  ← PENALIZES BUT NOT ENOUGH!

ROUGE-1 Analysis:
  All words match: Alice, gave, a, book, to, Bob
  Recall: 6/6 = 1.0
  Precision: 6/6 = 1.0
  F1: 1.0  ❌ FAILS TO CATCH MEANING CHANGE

ROUGE-L Analysis:
  Longest common subsequence...
  Ref: [Alice, gave, a, book, to, Bob]
  Cand: [Bob, gave, a, book, to, Alice]
  LCS: [gave, a, book, to] = 4 (missing Alice/Bob distinction)
  Recall: 4/6 = 0.667
  F1: ~0.8  ← BETTER, but still high

METEOR Analysis:
  Matched tokens: Alice, gave, a, book, to, Bob = all match
  But word order penalty kicks in:
  Reference: Alice → gave → a → book → to → Bob
  Candidate: Bob → gave → a → book → to → Alice
  Alice and Bob positions are swapped
  Penalty reduces score significantly
  
  METEOR: ~0.6-0.7  ← CATCHES THE PROBLEM

Summary:
  BLEU:    0.4    ← Detects problem via n-grams
  ROUGE-1: 1.0    ← FAILS (word bag, ignores order)
  ROUGE-L: 0.8    ← PARTIAL (catches some scrambling)
  METEOR:  0.6-0.7 ← BEST (order penalty)
```

**Key Lesson:**
- ROUGE-1 **completely fails** on scrambled word order (bag-of-words problem)
- ROUGE-L **helps** via longest common subsequence
- BLEU **detects** via n-gram penalties
- METEOR **explicitly penalizes** word order scrambling
- **Need word-order-aware metrics for logical correctness!**

---

## Example 5: Partial Answer (Missing Info)

```
Reference: "The Eiffel Tower was built in 1889 by Gustave Eiffel for the Paris Exposition"
Candidate: "The Eiffel Tower was built in 1889"

Candidate is CORRECT but INCOMPLETE (missing architect, purpose)

BLEU Analysis:
  First 5 tokens match exactly: "The Eiffel Tower was built in 1889"
  But candidate is shorter, so brevity penalty applies
  BLEU: ~0.3-0.4 (penalizes brevity)

ROUGE-1 Analysis:
  Recall: matches / reference = 7/14 = 0.5  (only half the info)
  Precision: matches / candidate = 7/7 = 1.0  (all given info is correct)
  F1: 2×(1.0×0.5)/(1.0+0.5) = 0.667
  
  PRECISION vs RECALL TRADEOFF!

ROUGE-L Analysis:
  LCS: "The Eiffel Tower was built in 1889" = 7 tokens
  Recall: 7/14 = 0.5 (catches the correct prefix)
  Precision: 7/7 = 1.0 (all are correct)
  F1: 0.667

METEOR Analysis:
  Similar to ROUGE-L (simpler matching)
  Score: ~0.6-0.7

Summary:
  BLEU:    0.3-0.4  ← PENALIZES (brevity penalty)
  ROUGE-1: 0.667    ← SPLIT (high precision, low recall)
  ROUGE-L: 0.667    ← SPLIT (high precision, low recall)
  METEOR:  0.6-0.7  ← SPLIT (similar to ROUGE)
  
  PRECISION: ~1.0   (everything said is correct)
  RECALL:    ~0.5   (only said half the required info)
```

**Key Lesson:**
- For incomplete answers, look at **Precision and Recall separately**
- High Precision + Low Recall = "Correct but insufficient"
- Report both P and R, or use weighted F-score if you need a single number
- **ROUGE-1 Precision tells you "did the model avoid hallucinations?"**
- **ROUGE-1 Recall tells you "did the model capture all key info?"**

---

## Teaching Decision Tree

When choosing which metric(s) to use:

```
START: What type of QA task?

├─ Exact factual (dates, names, numbers)
│  └─ Use: EM (Exact Match)
│     Expect: 1.0 if correct, 0.0 if wrong
│     Example: "When was Python created?" → "1991"

├─ Concise factual (short answers)
│  └─ Use: Token F1 + EM
│     Reason: Allows partial credit if a word is missed
│     Example: "Who created Python?" → "Guido van Rossum" (vs "Guido")

├─ Short paraphrased QA (a few sentences)
│  └─ Use: ROUGE-1 + ROUGE-L
│     Reason: Flexible on wording, catches word order issues
│     Example: "Why is the sky blue?" → acceptable paraphrases

├─ Long abstractive QA (multiple sentences)
│  └─ Use: ROUGE-1 (Recall-focused)
│     Reason: Care about capturing all key info
│     Also report: ROUGE-2, ROUGE-L for more detail

└─ Machine translation / High quality requirement
   └─ Use: METEOR + BLEU + ROUGE
      Reason: Combination catches different issues
      - METEOR: synonym/stem matching
      - BLEU: phrase consistency
      - ROUGE: overall recall
```

---

## RAG Evaluation Recommended Setup

### For Simple RAG (factual retrieval)
```python
scores = {
    'EM': exact_match(ref, cand),
    'Token_F1': token_f1(ref, cand),
    'ROUGE_1': rouge_1_f1(ref, cand)
}
# Average or weight them based on importance
```

### For Abstractive RAG (synthesized answers)
```python
scores = {
    'ROUGE_1_R': rouge_1_recall(ref, cand),  # Did we say all key info?
    'ROUGE_1_P': rouge_1_precision(ref, cand),  # Did we avoid hallucination?
    'ROUGE_L': rouge_l_f1(ref, cand),  # Word order matters
    'METEOR': meteor_score(ref, cand)  # Synonyms okay?
}
# High ROUGE_1_R + High ROUGE_1_P = good answer
# High ROUGE_L = maintains logical flow
# High METEOR = good paraphrasing
```

---

## Common Mistakes When Using These Metrics

### Mistake 1: Using BLEU-4 for Short QA
```
Question: "When was Eiffel Tower built?"
Reference: "1889"
Candidate: "1889"

BLEU: 1.0  ✓ (correct)
But 4-grams don't really make sense here!

Solution: Use EM or Token F1 for short answers
```

### Mistake 2: Using ROUGE-1 Alone for Order-Dependent Tasks
```
Reference: "The drug should not be taken with alcohol"
Candidate: "Should not the drug be taken with alcohol?"

ROUGE-1: 0.95 ✓ (almost all words match)
But meaning is reversed! (modal "should not" vs standard word order)

Solution: Always use ROUGE-L or BLEU for logical correctness
```

### Mistake 3: Interpreting F1 Without Precision/Recall
```
ROUGE-1 F1: 0.7

But is it:
- 0.9 precision + 0.6 recall? (missing info)
- 0.6 precision + 0.9 recall? (hallucinating)

Solution: Report both P and R, especially for RAG evaluation
```

### Mistake 4: Relying Only on Token Metrics
```
ROUGE-1 F1: 0.8
METEOR: 0.8
But manual inspection shows: Answer is wrong!

Why? Token metrics miss:
- Factual errors (e.g., "born in 1990" vs "born in 1980")
- Logical errors (temporal contradictions)
- Semantic drift (word choice implications)

Solution: Always validate with human evaluation on sample
```

---

## Summary for Your Lecture

**Key Points to Emphasize:**

1. **BLEU is strict** → Use for phrase-based matching, not flexible paraphrasing
2. **ROUGE is flexible** → Use for summarization and abstractive QA
3. **METEOR is sophisticated** → Use when you need synonyms/stemming
4. **No perfect metric** → Combine multiple metrics for comprehensive eval
5. **Token metrics are surface-level** → Always validate with human judgment
6. **Report Precision AND Recall** → Single F1 hides important tradeoffs
7. **Choose based on task type** → Different tasks need different metrics

**Recommended combinations:**
- **Factual QA:** EM + Token F1
- **Abstractive QA:** ROUGE-1 + ROUGE-L
- **Translation:** BLEU + METEOR + ROUGE
- **General RAG:** EM + ROUGE-1 (Recall) + ROUGE-L

**Always remember:** Metrics are tools for automation, not ground truth. They should be:
1. Computed across entire evaluation set (for statistics)
2. Sampled for manual review (to catch metric failures)
3. Correlated with human judgment (to validate their usefulness)

+++
title = "RAG Evaluation"
description = "Evaluating Retrieval-Augmented Generation systems"
weight = 7
outputs = ["Reveal"]
math = true
thumbnail = "/imgs/slides/rag-evaluation.png"

[reveal_hugo]
custom_theme = "css/reveal-robinson.css"
slide_number = true
transition = "convex"

+++

# Evaluating RAG Systems

### MSA 8700 — Module 7

---

## Learning Objectives

1. Explain the **evaluation pipeline** for RAG systems using curated test sets
2. Compute and interpret **token-based metrics** (Exact Match, Token F1, BLEU, ROUGE, METEOR)
3. Identify the **limitations** of token-based metrics
4. Describe how **LLMs are used as judges**
5. Compare **general-purpose vs. specialized** LLM evaluators
6. Explain the **RAGAS** and **ARES** frameworks
7. Evaluate the evaluation frameworks themselves

---

# Part 1

## The RAG Evaluation Pipeline

---

## The Core Problem

You have built a RAG system. It retrieves documents and generates answers.

**But how do you know if the answers are any good?**

---

## The Evaluation Pipeline

```text
Step 1: Create a curated Question/Answer test set (ground truth)
            ↓
Step 2: Feed the questions to your RAG system → get RAG responses
            ↓
Step 3: Compare RAG responses with ground truth answers
            ↓
Step 4: Calculate evaluation metrics
            ↓
Step 5: Analyze results and identify areas for improvement
```

---

## The Test Set

A curated test set consists of:

| Component | Description | Example |
|-----------|-------------|---------|
| **Question** | A question a user might ask | "When was Python created?" |
| **Ground Truth** | The correct, verified answer | "Python was created in 1989 by Guido van Rossum" |
| **Retrieved Context** | Documents the RAG system retrieved | Documents about Python history |
| **RAG Response** | What your RAG system generated | "Python was developed in 1989" |

---

## Sample Test Set

```python
test_set = [
  { "question": "When was the Eiffel Tower built?",
    "ground_truth": "The Eiffel Tower was built in 1889 for the Paris Exposition",
    "rag_response": "The Eiffel Tower was constructed in 1889 for the Paris World Fair",
    "context": "The Eiffel Tower was built in 1889 by Gustave Eiffel..." },
  { "question": "Who invented the telephone?",
    "ground_truth": "The telephone was invented in 1876 by Alexander Graham Bell",
    "rag_response": "Alexander Graham Bell invented the telephone in 1876 and his
     assistant Margaret Thomson conducted crucial experiments",
    "context": "Alexander Graham Bell patented the telephone in 1876." },
  # ... more examples
]
```

---

# Part 2

## Token-Based Evaluation Metrics

---

## Token-Based Metrics Overview

Token-based metrics measure **surface-level similarity** between RAG response and ground truth.

> *"How similar is this answer to the reference answer in terms of word/token overlap?"*

---

## Quick Comparison

| Metric | Core Idea | Precision vs Recall | Synonyms? | Word Order? |
|--------|-----------|---------------------|-----------|-------------|
| **Exact Match** | Binary match | N/A | No | Yes |
| **Token F1** | Set overlap | Balanced | No | No |
| **BLEU** | N-gram precision | Precision | No | Via n-grams |
| **ROUGE-1** | Unigram overlap | Recall | No | No |
| **ROUGE-L** | Longest common subseq. | Balanced | No | Yes (LCS) |
| **METEOR** | Matched words + ordering | Balanced (R-favored) | Yes | Yes (penalty) |

---

## 2.1 Exact Match (EM)

The simplest metric: **Is the generated answer exactly the same as the reference?**

$$\text{EM} = \begin{cases} 1 & \text{if normalize(response) = normalize(reference)} \\\\  0 & \text{otherwise} \end{cases}$$

- **Use when:** Single correct answer (dates, names, numbers)
- **Limitation:** Too strict for paraphrases

```python
def exact_match(reference, candidate):
    """Binary: 1 if exact match after normalization, 0 otherwise."""
    return 1.0 if reference.lower().strip() == candidate.lower().strip() else 0.0
```

---

## 2.2 Token F1 Score

Treats both texts as **sets of tokens**:

$$\text{Precision} = \frac{|\text{common tokens}|}{|\text{candidate tokens}|}$$

$$\text{Recall} = \frac{|\text{common tokens}|}{|\text{reference tokens}|}$$

$$\text{F1} = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

- **Limitation:** Ignores word order — "Alice gave book to Bob" and "Bob gave book to Alice" get F1 = 1.0

---

## Token F1 — Code

```python
def token_f1(reference, candidate):
    """Compute precision, recall, and F1 at the token (set) level."""
    ref_set  = set(reference.lower().split())
    cand_set = set(candidate.lower().split())
    common   = ref_set & cand_set

    precision = len(common) / len(cand_set) if cand_set else 0.0
    recall    = len(common) / len(ref_set)  if ref_set  else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) \
         if (precision + recall) > 0 else 0.0
    return f1, precision, recall
```

---

## 2.3 BLEU Score

BLEU measures **n-gram precision**: what fraction of candidate n-grams appear in the reference?

$$\text{BLEU} = \text{BP} \times \exp\left(\sum_{n=1}^{N} w_n \log p_n\right)$$

- $p_n$ = precision of n-grams
- $w_n$ = weights (typically $1/N$)
- $\text{BP}$ = brevity penalty

### Key characteristics
- **Precision-focused** — rewards exact phrase matches
- **Uses geometric mean** — if any n-gram precision is 0, BLEU = 0
- **Harsh on paraphrasing** — different word choices are penalized

---

## BLEU — Step by Step

```text
Reference: "the cat is on the mat"
Candidate: "the cat on the mat"  (missing "is")

1-gram precision: 5/5 = 1.0000
2-gram precision: 3/4 = 0.7500
3-gram precision: 1/3 = 0.3333
4-gram precision: 0/2 = 0.0000

BLEU-4 = 0.0000
```

**One missing word can kill the score!**

Because 4-gram precision is 0, the geometric mean collapses.

---

## 2.4 ROUGE

ROUGE is **recall-focused** — "Of the words in the reference, how many appear in the candidate?"

### ROUGE-1 (Unigram Overlap)

$$\text{ROUGE-1 Recall} = \frac{\text{matching unigrams}}{\text{total reference unigrams}}$$

### ROUGE-L (Longest Common Subsequence)

Uses **LCS** — the longest sequence of words that appear in both texts in order.

$$\text{ROUGE-L Recall} = \frac{\text{LCS length}}{\text{reference length}}$$

**Key insight:** ROUGE-1 = bag of words, ROUGE-L = order-aware

---

## Why Word Order Matters

```text
Reference: "Alice gave a book to Bob"
Candidate: "Bob gave a book to Alice"

Meaning is COMPLETELY DIFFERENT!

ROUGE-1 F1 = 1.0000   (same words → perfect match!)
ROUGE-L F1 = 0.8333   (LCS = "gave a book to" → lower score)
```

ROUGE-L can detect word order changes that ROUGE-1 cannot.

---

## 2.5 METEOR

METEOR improves on BLEU and ROUGE by:

1. **Matching synonyms** ("built" ≈ "constructed")
2. **Matching stems** ("running" ≈ "runs")
3. **Penalizing word order scrambling** via fragmentation penalty

$$F\_{\text{METEOR}} = \frac{(1 + \beta^2) \cdot P \cdot R}{\beta^2 \cdot P + R}$$

- **Best correlation with human judgment** among token-based metrics
- **Computationally heavier** (requires synonym database)

---

## Metric Comparison on Test Set

```text
Example 1 — Eiffel Tower (good paraphrase):
  EM=0.0  F1=0.73  BLEU=0.23  ROUGE-1=0.73  ROUGE-L=0.58

Example 2 — Telephone (hallucinated detail: "Margaret Thomson"):
  EM=0.0  F1=0.64  BLEU=0.14  ROUGE-1=0.73  ROUGE-L=0.64

Example 3 — Ottawa (hallucinated founding claim):
  EM=0.0  F1=0.33  BLEU=0.04  ROUGE-1=0.44  ROUGE-L=0.38

Example 4 — Washington ("Emperor" instead of "President"):
  EM=0.0  F1=0.93  BLEU=0.74  ROUGE-1=0.93  ROUGE-L=0.93
```

---

## What Do These Scores Tell Us?

**Example 4** (Washington / Emperor): Metrics show **high similarity (0.9+)** because almost all words match.

But "Emperor" instead of "President" is a **critical factual error**. The metrics completely miss this!

**Example 3** (Ottawa / Rousseau): Decent scores, but contains a **fabricated claim** about a fictional French explorer.

Token-based metrics **cannot distinguish real facts from hallucinated ones**.

---

# Part 3

## Limitations of Token-Based Metrics

---

## What Token Metrics Cannot Measure

| Question | Dimension | Can Token Metrics Measure? |
|----------|-----------|---------------------------|
| "Is the answer relevant to the question?" | **Relevancy** | No |
| "Are the facts in the answer true?" | **Truthfulness** | No |
| "Does the answer read naturally?" | **Fluency** | No |
| "Did the model make up false information?" | **Hallucinations** | No |

---

## Why Not?

| Property | Implication |
|----------|-------------|
| **Reference-dependent** | Need a gold-standard answer to compare against |
| **Surface-level** | Work at word/phrase level, not semantic level |
| **Non-factual** | Don't check facts against reality |
| **Non-linguistic** | Don't evaluate grammar or fluency |
| **Similarity-focused** | Measure how "similar" not how "correct" |

---

## Failure Case: Truthfulness

A factually **wrong** answer can score 0.95+:

```text
Reference: "...first President of the United States..."
Generated: "...first Emperor of the United States..."

ROUGE-1 F1 = 0.93   Token F1 = 0.93   BLEU = 0.74
```

Only **one word** is different — but the meaning is completely wrong!

---

## Failure Case: Fluency

A **scrambled, ungrammatical** answer can score 1.0:

```text
Reference: "Photosynthesis is the process by which plants
            convert sunlight into chemical energy"
Generated: "Sunlight into chemical energy plants convert
            process is photosynthesis"

ROUGE-1 F1 = 1.0   (same words, completely unreadable!)
```

---

## Failure Case: Hallucinations

A hallucinated answer with fabricated facts can score well:

```text
Reference: "Ottawa is the capital of Canada. It is located in Ontario."
Generated: "Ottawa is the capital of Canada. It was founded in 1826
            by French explorer Jean-Baptiste Rousseau."

ROUGE-1 F1 = 0.44   (decent — partially overlapping!)
```

The fabricated founding claim goes completely undetected.

---

## Token Metrics Summary

```text
CAN Measure:                  CANNOT Measure:
✓ Surface similarity           ✗ Question relevancy
✓ N-gram overlap               ✗ Factual correctness
✓ Word order (ROUGE-L)         ✗ Fluency / Grammar
                               ✗ Hallucinations

Use them for:                  Don't rely on them for:
✓ Reproducible baseline        ✗ Judging answer quality alone
✓ Automated screening          ✗ Detecting hallucinations
✓ Quick comparison             ✗ Evaluating relevancy
```

**ALWAYS COMBINE WITH:** Semantic metrics, LLM-as-Judge, Human evaluation

---

# Part 4

## LLMs as Judges

---

## The Idea

Instead of counting word overlaps, ask a **large language model** to evaluate the answer like a human would.

Assess: relevancy, accuracy, fluency, and hallucinations.

---

## Why LLMs Can Do What Token Metrics Cannot

| Aspect | Token Metrics | LLM Judge | Human Judge |
|--------|---------------|-----------|-------------|
| **Speed** | Instant | 1–5 sec | 5–10 min |
| **Cost** | Free | $0.001–0.01/eval | $0.50–2.00/eval |
| **Scalability** | Unlimited | Unlimited | Limited |
| **Relevancy** | No | Yes (0.80–0.90 corr.) | Yes |
| **Truthfulness** | No | Partial (0.65–0.80) | Yes |
| **Fluency** | No | Yes (0.80–0.90) | Yes |
| **Hallucinations** | No | Partial (0.60–0.75) | Yes |

---

## How It Works

1. **Construct a prompt** that asks the LLM to evaluate specific dimensions
2. **Provide context**: question, generated answer, reference, source documents
3. **Request structured output** (JSON) for easy parsing
4. **Set low temperature** (0.3–0.5) for consistent scoring
5. **Validate** with human samples (target correlation > 0.7)

---

## 4.1 Evaluation Dimensions

### Relevancy
- Does the answer address the question?
- **LLM reliability:** High (0.80–0.90 correlation with humans)

### Accuracy / Truthfulness
- Are the factual claims correct?
- **LLM reliability:** Medium (0.65–0.80) — LLMs can't verify facts beyond training data

### Fluency
- Is the answer well-written, grammatical, and clear?
- **LLM reliability:** High (0.80–0.90)

### Hallucinations
- Does the answer contain fabricated facts?
- **LLM reliability:** Medium-Low (0.60–0.75) — LLMs can hallucinate while detecting hallucinations!

---

## Simple Relevancy Prompt

```python
relevancy_prompt = """
You are a QA evaluator.

QUESTION: {question}
ANSWER: {answer}

Score relevancy (0-5):
5 = Perfectly answers the question
4 = Addresses question with minor gaps
3 = Addresses question with some gaps
2 = Partially addresses the question
1 = Barely relevant
0 = Off-topic

RESPOND: SCORE: [0-5] REASON: [one sentence]
"""
```

---

## Comprehensive Evaluation Prompt

```python
comprehensive_prompt = """
You are an expert QA evaluator.

QUESTION: {question}
REFERENCE ANSWER: {reference}
SOURCE DOCUMENTS: {sources}
GENERATED ANSWER: {answer}

Evaluate on 4 dimensions (0-5 each):
1. RELEVANCY: Does it address the question?
2. ACCURACY: Are facts correct?
3. FLUENCY: Is it well-written and clear?
4. HALLUCINATIONS: Any made-up facts? (5=none, 0=mostly fabricated)

Respond in JSON:
{
  "relevancy": <0-5>, "accuracy": <0-5>,
  "fluency": <0-5>, "hallucinations": <0-5>,
  "explanation": "<brief explanation>"
}
"""
```

---

## Hallucination Detection Prompt

```python
hallucination_prompt = """
You are checking for hallucinations (made-up facts).

REFERENCE: {reference}
ANSWER: {answer}

For each claim in the answer, mark as:
  SUPPORTED    — In the reference
  UNCLEAR      — Not explicitly stated but reasonable
  UNSUPPORTED  — Not in reference, not contradicted
  HALLUCINATION — Made up, contradicted, or incorrect

Respond in JSON:
{
  "hallucination_score": <0-5 where 5=none>,
  "claims": [
    {"claim": "...", "status": "...", "evidence": "..."}
  ]
}
"""
```

---

## Advanced LLM Judge Techniques

### 1. Chain-of-Thought Evaluation
Ask the LLM to **explain its reasoning before scoring**

### 2. Comparison-Based Scoring
**Compare two answers** instead of absolute 0–5 scales — often easier for LLMs

### 3. Multi-Step Evaluation
Break into focused steps: Fact Extraction → Fact Checking → Scoring

### 4. Role-Specific Judges
- Judge 1 (Fact Checker): "You are a researcher. Check facts."
- Judge 2 (Writing Coach): "You are an English professor."
- Judge 3 (Domain Expert): "You are a [domain] expert."

Then **aggregate** their scores.

---

## Best Practices for LLM Judges

| Practice | Why |
|----------|-----|
| **Define scales explicitly** | "5 = all facts correct" not just "rate 0-5" |
| **Use structured output (JSON)** | Easy to parse and aggregate |
| **Include context** | Question + reference + sources |
| **Assign a role** | "You are an expert evaluator..." |
| **Give examples (few-shot)** | Show what 5/5 vs 1/5 looks like |
| **Use low temperature** | 0.3–0.5 for consistent scores |
| **Max 3–4 dimensions** | Too many confuses the LLM |
| **Always validate** | Correlate with human labels (target > 0.7) |

---

# Part 5

## General-Purpose vs. Specialized LLM Evaluators

---

## General-Purpose LLMs as Judges

Models like Claude, GPT-4, and Llama-70B evaluate using **prompting alone** — no training required.

| Model | Speed | Cost/Eval | Quality |
|-------|-------|-----------|---------|
| Claude Opus | Medium | ~$0.01 | Excellent |
| Claude Sonnet | Fast | ~$0.003 | Very Good |
| GPT-4 | Medium | ~$0.01 | Excellent |
| GPT-4 Turbo | Fast | ~$0.005 | Very Good |
| Llama-70B | Medium | Low (self-hosted) | Good |

**Advantages:** Works immediately, flexible, explains reasoning

**Disadvantages:** Per-eval cost, API-dependent, not domain-specialized

---

## Specialized / Fine-Tuned Evaluators

Small models (7–13B parameters) **fine-tuned specifically for evaluation**.

**Advantages:**
- 100–500x **faster** than LLM judges
- 100–1000x **cheaper** per evaluation
- **Domain-specialized** (trained on YOUR data)
- Runs **offline**, fully reproducible

**Disadvantages:**
- Requires 1–2 weeks setup
- $1000–5000 upfront investment
- Less capable for complex / nuanced evaluation
- Needs retraining when documents change

---

## When to Choose Each

```text
< 10,000 evaluations     → General-purpose LLM judges
10,000 – 100,000 evals   → Either approach works
> 100,000 evaluations    → Specialized / fine-tuned models
Real-time scoring needed → Only specialized models (10-100ms)
```

---

# Part 6

## The RAGAS Framework

---

## What is RAGAS?

**RAGAS** (RAG Assessment) — open-source framework with **pre-built evaluation metrics** for RAG systems.

- **Creator:** Exploding Gradients (open-source team)
- **GitHub:** github.com/explodinggradients/ragas
- **Key feature:** Works out of the box with minimal setup

---

## RAGAS Architecture

```text
        Question
            │
            ▼
     ┌────────────-──┐
     │   Retriever   │ ← Context Precision (are retrieved docs relevant?)
     │               │ ← Context Recall (are all needed facts retrieved?)
     └──────┬────────┘
            │
       Retrieved Docs
            │
            ▼
     ┌───────────-───┐
     │  Generator    │ ← Faithfulness (is answer grounded in context?)
     │   (LLM)       │ ← Answer Relevancy (does it answer the question?)
     └──────┬────────┘
            │
        Generated Answer
```

---

## RAGAS Metric 1: Faithfulness

**Does the answer only contain information from the retrieved context?**

1. LLM extracts claims from the generated answer
2. For each claim, LLM checks if it's supported by context
3. Score = (supported claims) / (total claims)

```text
Context: "Python was created in 1989 by Guido van Rossum"
Answer:  "Python was created in 1989 by Guido van Rossum at MIT"
Score:   0.67 — "at MIT" is NOT in the context (hallucination)
```

---

## RAGAS Metric 2: Answer Relevancy

**Does the generated answer address the question?**

Clever **reverse-question approach**:
1. LLM generates 3–4 alternative questions from the answer
2. If generated questions match the original → answer is relevant
3. Score based on semantic similarity

```text
Original Q:    "When was Python created?"
Answer:        "Python was created in 1989"
Generated Qs:  "What year was Python released?" ✓
               "When did Python development start?" ✓
Score: 1.0 — all generated questions align with original
```

---

## RAGAS Metrics 3 & 4: Context Quality

### Context Precision
Of the retrieved documents, how many are relevant?

$$\text{Context Precision} = \frac{\text{relevant retrieved docs}}{\text{total retrieved docs}}$$

Low precision = **too much noise** in retrieval.

### Context Recall
Of the information needed, how much is in the context?

$$\text{Context Recall} = \frac{\text{needed facts in context}}{\text{total facts needed}}$$

Low recall = **important information missing** from retrieval.

---

## RAGAS Usage Example

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness, answer_relevancy,
    context_precision, context_recall
)

test_data = {
    "question": ["When was Python created?"],
    "answer": ["Python was created in 1989"],
    "contexts": [["Python was created in 1989 by Guido van Rossum"]],
    "ground_truth": ["1989"]
}

results = evaluate(
    test_data,
    metrics=[faithfulness, answer_relevancy,
             context_precision, context_recall]
)
# {'faithfulness': 0.95, 'answer_relevancy': 0.92,
#  'context_precision': 1.0, 'context_recall': 1.0}
```

---

## RAGAS Strengths and Limitations

| Strengths | Limitations |
|-----------|-------------|
| Zero setup — works out of the box | LLM-dependent (costs per eval) |
| Excellent documentation | Not specialized to your domain |
| Pre-built metrics for RAG | Limited metric customization |
| Active community | Slower than fine-tuned models |
| Easy integration | Can't run offline (needs LLM API) |

---

# Part 7

## The ARES Framework

---

## What is ARES?

**ARES** (Automated Retrieval Evaluation with Synthetic data) — Stanford research framework.

> Instead of paying for LLM evaluation every time, **train specialized models once** and evaluate cheaply forever.

---

## The Three Stages of ARES

```text
┌────────────────────────────────────────────────────┐
│ STAGE 1: SYNTHETIC DATA GENERATION (One-Time)      │
│  Your Documents → LLM generates Q&A pairs          │
│  Output: 1000-5000 labeled examples                │
│  Cost: ~$10-100 (one-time)                         │
└────────────────────┬───────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────┐
│ STAGE 2: TRAIN EVALUATOR MODELS (One-Time)         │
│  Fine-tune small models (Mistral-7B, DistilBERT)   │
│  Train 3 specialized evaluators:                   │
│    • Retrieval Evaluator                           │
│    • Answer Relevance Evaluator                    │
│    • Factuality Evaluator                          │
│  Cost: ~$500-1000 (compute)                        │
└────────────────────┬───────────────────────────────┘
                     ↓
┌────────────────────────────────────────────────────┐
│ STAGE 3: EVALUATE (Fast & Cheap — Repeated!)       │
│  Speed: 10-100ms per evaluation                    │
│  Cost: ~$0 per evaluation                          │
│  Can run offline                                   │
└────────────────────────────────────────────────────┘
```

---

## ARES Synthetic Data Generation

```text
Document: "Python was created in 1989 by Guido van Rossum"

Generated Questions:
  Q1: "When was Python created?"
  Q2: "Who created Python?"
  Q3: "What language did Guido van Rossum create?"

Training Examples:
  ✓ Positive: (Q1, Python_history_doc, "1989")   → RELEVANT
  ✗ Negative: (Q1, Java_programming_doc, "1989") → IRRELEVANT
```

---

## ARES Fine-Tuning

Each evaluator is a **binary classifier** trained on synthetic data:

```python
from transformers import AutoModelForSequenceClassification, Trainer

model = AutoModelForSequenceClassification.from_pretrained(
    "mistralai/Mistral-7B",
    num_labels=2  # Binary: relevant or not
)
trainer = Trainer(
    model=model,
    train_dataset=synthetic_data,
    args=TrainingArguments(learning_rate=2e-5, num_train_epochs=3)
)
trainer.train()
```

**LoRA** (Low-Rank Adaptation) can reduce training cost by 90%.

---

## ARES Strengths and Limitations

| Strengths | Limitations |
|-----------|-------------|
| Domain-specialized (trained on YOUR docs) | Complex setup (1–2 weeks) |
| Extremely fast (10–100ms/eval) | Upfront cost ($1000–5000) |
| Extremely cheap at scale (~$0/eval) | Synthetic data may have biases |
| Runs offline, fully reproducible | Needs retraining when docs change |
| Deterministic output | Less capable for nuanced evaluation |

---

# Part 8

## Comparing Evaluation Approaches

---

## Comprehensive Comparison Matrix

| Feature | Token Metrics | LLM Judge | RAGAS | ARES |
|---------|---------------|-----------|-------|------|
| **Setup Time** | None | Minutes | Minutes | 1–2 Weeks |
| **Setup Cost** | $0 | $0 | $0 | $1000–5000 |
| **Per-Eval Cost** | $0 | $0.001–0.01 | $0.001–0.01 | ~$0 |
| **Speed/Eval** | Instant | 1–5 sec | 1–10 sec | 10–100ms |
| **Accuracy** | 50–60% | 75–85% | 70–75% | 75–85% |
| **Domain-Specific** | No | No | Limited | Yes |
| **Runs Offline** | Yes | No | Partial | Yes |

---

## Cost-Time-Accuracy Tradeoff

```text
Method              | Cost (10k evals) | Time (10k evals) | Accuracy
────────────────────┼──────────────────┼──────────────────┼─────────
Token Metrics       | $0               | < 1 sec          | 50-60%
RAGAS               | $10-100          | 1-10 hrs         | 70-75%
LLM Judge           | $10-100          | 10-50 hrs        | 75-85%
ARES (post-setup)   | $0.10            | 2-5 min          | 75-85%
Human evaluation    | $5000+           | 50+ hrs          | 90-95%
```

---

## Decision Tree

```text
START: "I need to evaluate my RAG system"
│
├─ Is this a prototype/POC?
│  YES → Token Metrics + RAGAS
│  Cost: $0, Time: hours
│
├─ < 10,000 evaluations?
│  YES → LLM Judges + RAGAS
│  Cost: $10-100, Time: days
│
├─ 10,000-100,000 evaluations?
│  YES → LLM Judges + human sampling
│  Cost: $100-500, Time: days
│
└─ > 100,000 evaluations?
   YES → ARES + LLM Judges for edge cases
   Cost: $2000-5000 setup, then ~$0
```

---

## The Hybrid Approach (Best Practice)

```text
Tier 1: Fast Screening (ARES or RAGAS)
  → Score ALL answers
  → Cost: ~$0-10, Time: minutes
          │
    ┌─────┴────────┐
    ▼              ▼
  Flagged       Good Items
  (Low scores)   → Accept
    │
    ├─ Tier 2: LLM Judge (20% of flagged)
    │  → Deeper analysis, Cost: $100-500
    │
    └─ Tier 3: Human Expert (5% of flagged)
       → Final validation, Cost: $500+

Result: 95-99% issue detection at 20% of LLM-only cost
```

---

# Part 9

## Evaluating the Evaluation Frameworks

---

## How Do We Know Our Metrics Work?

We evaluate the evaluators by examining:

1. **Score distributions** — Are scores well-distributed or clustered?
2. **Correlation with human judgment** — Do automated scores agree with human ratings?
3. **Cross-metric correlation** — Do different metrics agree with each other?

### Validation Strategy
1. Get human labels for ~100 examples
2. Compute automated scores on the same examples
3. Calculate Spearman's $\rho$ for ranking correlation
4. Target: **correlation > 0.7 = reliable metric**

---

## Spearman Rank Correlation

$$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$

Where $d_i$ = difference in ranks between metric and human score.

**Interpretation:**

| Range | Quality | Action |
|-------|---------|--------|
| $\rho > 0.8$ | Excellent | Use metric with confidence |
| $0.7 < \rho < 0.8$ | Good | Use with sampling validation |
| $0.6 < \rho < 0.7$ | Acceptable | Needs more human oversight |
| $\rho < 0.6$ | Poor | Revise approach |

---

## Score Distributions

A good metric should produce **well-distributed scores** that discriminate between good and bad answers.

If all scores cluster around one value, the metric is **not useful**.

```text
Example: Simulated score distributions (n=100)

Human scores:   well-distributed across 0-5
LLM Judge:      well-distributed (good discrimination)
ROUGE:          clustered around 2-3 (poor discrimination)
RAGAS:          moderate spread (acceptable)
```

---

## Cross-Metric Agreement

Check if different automated metrics **agree with each other**.

If they don't, some may be measuring different things (or nothing useful).

```text
Typical Cross-Metric Correlation Matrix:

              Human    ROUGE    LLM Judge   RAGAS
Human          1.00     0.52      0.85      0.72
ROUGE          0.52     1.00      0.48      0.55
LLM Judge      0.85     0.48      1.00      0.70
RAGAS          0.72     0.55      0.70      1.00
```

LLM Judge shows highest correlation with human judgment.

---

## Error Analysis

The most informative analysis: cases where **metrics disagree with human judgment**.

- High human / Low metric → Metric is **too strict**
- Low human / High metric → Metric is **too lenient** (dangerous!)
- Systematic patterns → Reveal metric blind spots

### Key questions:
- Which types of errors does each metric miss?
- Are there domains where metrics consistently fail?
- Can we combine metrics to cover each other's weaknesses?

---

## Practical Validation Workflow

```text
Step 1: Get human labels for ~100 examples
Step 2: Run all automated metrics on those 100 examples
Step 3: Compute Spearman correlation for each metric
Step 4: Decision:
        • ρ > 0.7  → Metric is reliable, use it
        • ρ < 0.7  → Revise prompt/approach, retry
Step 5: In production, periodically re-validate
        • Check for score drift over time
        • Flag outliers for manual review
```

---

# Summary

## Key Takeaways

---

## The Evaluation Landscape

```text
2022: Token metrics (ROUGE/BLEU)    → Fast but inaccurate
2023: LLM judges (Claude/GPT-4)     → Accurate but expensive
2024: Frameworks (RAGAS/ARES)        → Structured, scalable
2025: Hybrid systems                 → Best of all worlds
```

---

## Key Principles

1. **No single metric is sufficient** — Need multiple metrics across multiple dimensions

2. **Token metrics = Similarity, not Quality** — They measure if you match a reference, not if you're correct

3. **LLM judges bridge the gap** — Fast screening for relevancy, accuracy, fluency, hallucinations

4. **Frameworks reduce complexity** — RAGAS for quick start, ARES for production scale

5. **Always validate with humans** — Compute correlation, target > 0.7

6. **The hybrid approach wins** — Automated screening + LLM judges + human validation

---

## Recommended Evaluation Pipeline

| Layer | Method | Coverage | Cost |
|-------|--------|----------|------|
| **Layer 1** | Token metrics (ROUGE, BLEU) | All examples | Free |
| **Layer 2** | RAGAS / ARES framework | All examples | Low |
| **Layer 3** | LLM Judge (Claude/GPT-4) | Flagged + sample | Medium |
| **Layer 4** | Human evaluation | 5–10% sample | High |

---

## Final Decision Guide

| Your Situation | Recommendation |
|----------------|----------------|
| Quick prototype | Token metrics + RAGAS |
| < 10k evaluations | LLM Judges |
| 10k–100k evaluations | RAGAS + LLM Judges |
| > 100k evaluations | ARES + LLM Judges for edge cases |
| High-stakes domain | Full hybrid + human validation |

---

## Code

**Response Evaluation** based on the comparison of RAG responses to given questions to the ground truth answer

- Example notebook [RAG_Evaluation](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/RAG/RAG-Evaluation/notebooks/RAG_Evaluation.ipynb)
- Example code in [response_evaluation](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/RAG/RAG-Evaluation/response_evaluation/__init__.py)
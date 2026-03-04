+++
title = "NLP and Text Processing"
description = "Overview of classical NLP and text processing techniques"
weight = 80
outputs = ["Reveal"]
math = true
thumbnail = "/imgs/slides/nlp-text-processing.png"

[reveal_hugo]
custom_theme = "css/reveal-robinson.css"
slide_number = true
transition = "none"

+++
{{< slide background-image="/imgs/slides/nlp-text-processing.png" >}}

<h1 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >End-to-End Example<br />Deal Intelligence Agent</h1>

<h3 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >Bringing Every Technique Together</h3>
<p style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >
MSA 8700 — Module 8: NLP and Text Processing
</p>

***

## The Business Scenario

A **deal intelligence agent** monitors news feeds, emails, and web pages to keep a venture capital firm informed about competitors, acquisitions, and market moves.

Every day, hundreds of raw documents arrive — HTML pages, plain-text emails, and press releases. The firm wants structured, actionable intelligence, not piles of unread text.

***

## What the Agent Must Do

1. **Ingest** raw HTML and email text
2. **Clean** and extract content from messy sources
3. **Identify** who, what, where, when, and how much
4. **Classify** each document by topic and sentiment
5. **Reason** over the structured data using an LLM

Each step maps to a technique we studied in this module.

***

## The Pipeline at a Glance

```text
Raw HTML / Email
       ↓
① Beautiful Soup + Regex    → clean text + structured fields
       ↓
② Tokenization + Lemmatization → normalized tokens
       ↓
③ POS Tagging + NER (spaCy)  → entities + descriptors
       ↓
④ TF-IDF Classifier          → topic routing
   VADER Sentiment            → sentiment score
       ↓
⑤ LDA Topic Model            → emerging themes
       ↓
⑥ LLM Reasoning              → narrative summary + recommendations
```

---

# Step ① — From Raw HTML to Clean Text

### Beautiful Soup + Regex

***

## The Raw Input

Imagine the agent fetches this HTML from a news site:

```html
<html>
<body>
  <nav><a href="/">Home</a> | <a href="/news">News</a></nav>
  <div class="ad">Buy premium analytics tools!</div>
  <article>
    <h1>Acme Corp Acquires DataFlow for $240M</h1>
    <p class="meta">Published 2026-03-01 | Business News</p>
    <p>Acme Corp announced on March 1, 2026 that it would
    acquire DataFlow Inc., a San Francisco-based data
    startup, for $240 million in cash.</p>
    <p>CEO Jane Rivera said the deal strengthens Acme's
    position in the real-time analytics market.</p>
  </article>
  <script>trackPageView();</script>
</body>
</html>
```

***

## Cleaning with Beautiful Soup

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

# Remove noise: nav, ads, scripts
for tag in soup.find_all(["nav", "script"]):
    tag.decompose()
for ad in soup.find_all("div", class_="ad"):
    ad.decompose()

# Extract the article content
article = soup.find("article")
title = article.find("h1").get_text(strip=True)
paragraphs = [p.get_text(strip=True)
              for p in article.find_all("p")]
```

**Result:** Clean title and paragraphs — no HTML, no ads, no scripts.

***

## Extracting Structured Fields with Regex

```python
import re

full_text = " ".join(paragraphs)

# Extract date (ISO format)
dates = re.findall(r"\d{4}-\d{2}-\d{2}", full_text)

# Extract dollar amounts
amounts = re.findall(r"\$[\d,]+(?:\.\d{2})?\s*(?:million|billion)?",
                     full_text, re.IGNORECASE)

# Extract the article's publication date from meta
meta_text = article.find("p", class_="meta").get_text()
pub_date = re.search(r"\d{4}-\d{2}-\d{2}", meta_text).group()
```

**Result:** `dates = ["2026-03-01"]`, `amounts = ["$240 million"]`

***

## Why This Matters

| What We Did | Why |
|-------------|-----|
| Beautiful Soup removed noise | Saves LLM tokens, improves focus |
| Regex extracted dates + amounts | 100% reliable on known formats |
| Deterministic, microseconds | No API cost, no hallucination |

> **Rule**: Extract structured fields deterministically. Reserve the LLM for reasoning.

---

# Step ② — Lexical Processing

### Tokenization + Lemmatization

***

## Normalizing the Text

```python
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

tokens = word_tokenize(full_text.lower())
tagged = pos_tag(tokens)

# Lemmatize with correct POS, remove stop words
clean_tokens = []
for word, tag in tagged:
    if word.isalpha() and word not in stop_words:
        pos = get_wordnet_pos(tag)  # map to WordNet POS
        clean_tokens.append(lemmatizer.lemmatize(word, pos))
```

***

## What Lemmatization Gives Us

| Raw Token | Lemma |
|-----------|-------|
| acquired | acquire |
| strengthens | strengthen |
| announced | announce |
| analytics | analytics |

- "acquire", "acquired", "acquires", "acquiring" → all become **acquire**
- Enables consistent keyword matching and feature extraction downstream

***

## Agentic Use

- A **rule-based alert** can trigger on the lemma `acquire` — catching all inflected forms
- The normalized tokens feed into the **TF-IDF vectorizer** and **LDA topic model** in later steps
- Stemming would also work here, but lemmatization keeps real words (better for display)

---

# Step ③ — NER and POS Tagging

### spaCy for Entity Extraction

***

## Running spaCy NER

```python
import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp(full_text)

entities = {}
for ent in doc.ents:
    entities.setdefault(ent.label_, []).append(ent.text)
```

**Extracted entities:**

| Type | Entities |
|------|----------|
| **ORG** | Acme Corp, DataFlow Inc. |
| **PERSON** | Jane Rivera |
| **GPE** | San Francisco |
| **MONEY** | $240 million |
| **DATE** | March 1, 2026 |

***

## Cross-Validation: Regex ↔ spaCy

```python
# Regex found: $240 million
# spaCy found: $240 million  ✓ Match

# Regex found date: 2026-03-01
# spaCy found date: March 1, 2026  ✓ Consistent
```

If classical tools and LLM **disagree** on critical fields → escalate to a human or retry.

This cross-validation pattern is a key safety mechanism in agentic systems.

***

## POS-Based Descriptor Extraction

```python
# Extract adjective-noun pairs for market descriptors
descriptors = []
for i in range(len(doc) - 1):
    if doc[i].pos_ == 'ADJ' and doc[i+1].pos_ == 'NOUN':
        descriptors.append(f"{doc[i].text} {doc[i+1].text}")

# Result: ["real-time analytics"]
```

These descriptors characterize the **market context** of the deal — useful for the LLM reasoning step.

---

# Step ④ — Classification and Sentiment

### TF-IDF Classifier + VADER

***

## Topic Classification

A pre-trained TF-IDF + Logistic Regression classifier routes the article:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Pre-trained on labeled articles
X_new = vectorizer.transform([full_text])
category = clf.predict(X_new)[0]
confidence = clf.predict_proba(X_new).max()

# Result: category = "M&A", confidence = 94%
```

**Fast, free, deterministic** — the classifier routes hundreds of articles per second.

***

## Sentiment Analysis with VADER

```python
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
scores = sia.polarity_scores(full_text)

# Result:
# compound = +0.72 → POSITIVE
# The language ("strengthens", "position") is positive
```

| Score | Value | Interpretation |
|-------|-------|---------------|
| Positive | 0.28 | Moderate positive language |
| Neutral | 0.72 | Most of the text is factual |
| Negative | 0.00 | No negative language |
| **Compound** | **+0.72** | **Overall positive** |

***

## Alert Logic

```python
# Agentic alert rules
if category == "M&A" and any(a for a in amounts
        if "million" in a or "billion" in a):
    alert = "HIGH PRIORITY — M&A deal detected"

if scores['compound'] < -0.3:
    alert += " — NEGATIVE SENTIMENT"
```

The classical NLP layer generates **structured signals** — topic, sentiment, priority — that feed into the LLM reasoning layer.

---

# Step ⑤ — Topic Discovery with LDA

### Finding Emerging Themes

***

## When You Don't Have Labels

The classifier from Step ④ handles **known categories** (M&A, earnings, product launch).

But what about **emerging themes** nobody anticipated?

**LDA** runs over the full corpus of recent articles — unsupervised, no labels — and discovers latent topics.

***

## Running LDA

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# Build document-term matrix from all recent articles
count_vec = CountVectorizer(stop_words='english',
                            min_df=2, max_df=0.9)
dtm = count_vec.fit_transform(all_articles)

# Fit LDA with 5 topics
lda = LatentDirichletAllocation(n_components=5,
                                 random_state=42)
lda.fit(dtm)
```

***

## Discovered Topics

| Topic | Top Words | Suggested Label |
|-------|-----------|----------------|
| 1 | acquire, deal, million, startup, funding | **M&A Activity** |
| 2 | data, privacy, regulation, compliance, GDPR | **Data Privacy** |
| 3 | revenue, quarter, growth, earnings, profit | **Earnings Reports** |
| 4 | AI, model, research, launch, platform | **AI Product Launches** |
| 5 | layoff, restructure, cut, workforce, hire | **Workforce Changes** |

LDA discovered these **without any labels** — the topics emerge from word co-occurrence patterns in the corpus.

***

## The LLM Labels the Topics

The LDA model gives you word lists. The LLM turns them into human-readable labels:

```text
Prompt: "Given these top words for a discovered topic:
  acquire, deal, million, startup, funding
  Suggest a concise, descriptive label."

LLM Response: "M&A Activity and Startup Funding"
```

**Unsupervised discovery (LDA) + natural language labeling (LLM)** — each does what it's best at.

---

# Step ⑥ — LLM Reasoning

### The Intelligence Layer

***

## The Structured Record

After Steps ①–⑤, the agent has built this structured record:

```json
{
  "title": "Acme Corp Acquires DataFlow for $240M",
  "pub_date": "2026-03-01",
  "organizations": ["Acme Corp", "DataFlow Inc."],
  "people": ["Jane Rivera"],
  "locations": ["San Francisco"],
  "amounts": ["$240 million"],
  "dates": ["March 1, 2026"],
  "category": "M&A",
  "category_confidence": 0.94,
  "sentiment_compound": 0.72,
  "lda_topic": "M&A Activity",
  "descriptors": ["real-time analytics"]
}
```

***

## What the LLM Does with It

The LLM receives the structured record **plus** the clean text and reasons over it:

```text
Prompt: "You are a deal intelligence analyst. Given:
  - Acme Corp acquired DataFlow Inc. for $240M
  - Location: San Francisco
  - Sector: real-time analytics
  - Sentiment: positive
  - CEO Jane Rivera described it as strategic

  1. How does this affect our portfolio company X?
  2. Is Acme Corp now a competitor in our space?
  3. What follow-up actions should we take?"
```

***

## Why This Works Better Than Raw LLM

| Approach | Problem |
|----------|---------|
| Send raw HTML to LLM | Wastes tokens on ads, nav, scripts |
| Ask LLM to extract entities | May hallucinate amounts or dates |
| Ask LLM to classify 1000 articles | $100+ per run, minutes of latency |

| Our Approach | Benefit |
|-------------|---------|
| Classical NLP extracts + classifies | Free, fast, deterministic |
| LLM reasons over structured data | Focused, accurate, cost-efficient |

> The LLM sees **clean, verified, structured input** — not raw noise.

---

# The Complete Architecture

***

## Pipeline Summary

```text
┌─────────────────────────────────────────────────┐
│         DEAL INTELLIGENCE AGENT                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ① Beautiful Soup + Regex                      │
│    → Clean text, dates, amounts                 │
│                                                 │
│  ② NLTK Tokenization + Lemmatization           │
│    → Normalized tokens for downstream use       │
│                                                 │
│  ③ spaCy NER + POS Tagging                     │
│    → ORG, PERSON, GPE, MONEY, DATE              │
│    → Adjective-noun descriptors                 │
│    → Cross-validation with regex                │
│                                                 │
│  ④ TF-IDF Classifier + VADER Sentiment         │
│    → Topic routing + sentiment score            │
│                                                 │
│  ⑤ LDA Topic Model                             │
│    → Emerging theme discovery                   │
│                                                 │
│  ⑥ LLM Reasoning                               │
│    → Narrative summary + recommendations        │
│                                                 │
└─────────────────────────────────────────────────┘
```

***

## Technique Map

| Step | Technique | Role | Notebook |
|------|-----------|------|----------|
| ① | Beautiful Soup, Regex | Deterministic extraction | 01 |
| ② | Tokenization, Lemmatization | Text normalization | 02 |
| ③ | spaCy NER, POS tagging | Entity + descriptor extraction | 04 |
| ④ | TF-IDF + LogReg, VADER | Classification + sentiment | 05 |
| ⑤ | LDA | Unsupervised topic discovery | 05 |
| ⑥ | LLM | Reasoning + generation | — |

Each technique handles what it does best. Together they form a system that is **reliable, fast, cheap, and intelligent**.

***

## The Design Principle

### Classical NLP for extraction. LLMs for reasoning.

- **Regex and parsers** → hard extraction of dates, amounts, IDs
- **NER and POS models** → structured entity annotations
- **Classifiers and sentiment** → high-volume routing and scoring
- **Topic models** → unsupervised theme discovery
- **LLMs** → synthesis, reasoning, natural language output

> Use deterministic methods for what they do best. Use LLMs for what *they* do best.

---

# Cost-Efficient "First Pass" Pattern

***

## The 80/20 Rule in Practice

Most agent tasks operate over **large volumes** — millions of log lines, reviews, or emails.

The classical NLP layer handles the bulk:

```text
1,000 incoming articles per day
         ↓
Classical classifier routes 80% with high confidence
   → 400 M&A    → 200 Earnings  → 200 Product
         ↓
VADER flags 50 with negative sentiment
         ↓
Only 50 high-priority items sent to LLM
   → Narrative summaries
   → Risk assessments
   → Recommended actions
```

***

## Cost Comparison

| Approach | Articles/Day | LLM Calls | Est. Cost |
|----------|-------------|-----------|-----------|
| Send everything to LLM | 1,000 | 1,000 | ~$50/day |
| Classical first pass | 1,000 | 50 | ~$2.50/day |

**95% cost reduction** — same intelligence quality on the items that matter.

The classical layer is free after training. The LLM budget is focused on high-value reasoning.

---

# Cross-Validation and Safety

***

## When Tools Disagree

```text
Regex extracted:    $240 million
spaCy NER found:   $240 million     ✓ AGREE

Regex extracted:    2026-03-01
spaCy NER found:   March 1, 2026    ✓ CONSISTENT
LLM summary says:  March 2026       ✗ IMPRECISE
  → Flag for review
```

If classical tools and LLM **disagree on critical fields**, the agent can:

1. Retry with a different prompt
2. Escalate to a human reviewer
3. Log the discrepancy for monitoring

***

## Monitoring and Determinism

Classical NLP outputs are **deterministic** for a fixed model:

- Same input → same entities, same classification, same sentiment
- You can write **unit tests** for extraction logic
- You can detect **drift** when a new model version changes behavior

LLM outputs are **stochastic**:

- Same input may give slightly different responses
- Harder to test, harder to monitor

> Combining both gives you **reliability where it matters** (extraction) and **flexibility where it matters** (reasoning).

---

# Summary

***

## What We Built

A **deal intelligence agent** that processes raw news articles through a six-step pipeline:

1. **Beautiful Soup + Regex** — clean text and extract structured fields
2. **Tokenization + Lemmatization** — normalize for downstream processing
3. **spaCy NER + POS Tagging** — extract entities and descriptors
4. **TF-IDF Classifier + VADER** — route by topic and score sentiment
5. **LDA Topic Model** — discover emerging themes
6. **LLM Reasoning** — generate narratives and recommendations

***

## The Core Principle

> **Classical NLP and LLMs are not competitors — they are collaborators.**

| Classical NLP | LLM |
|--------------|-----|
| Fast (microseconds) | Slow (seconds) |
| Free at inference | Per-token cost |
| Deterministic | Stochastic |
| Structured extraction | Narrative reasoning |
| High volume | High value |

Use each for what it does best. Together, they form agent systems that are **reliable, efficient, and intelligent**.

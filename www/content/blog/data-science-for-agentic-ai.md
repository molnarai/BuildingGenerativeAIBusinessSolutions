---
title: "Data Science for Agentic AI: Managing, Monitoring, and Evaluating Intelligent Agent Systems"
description: "How to make generative models produce data structures, database queries, and program code that machines can reliably consume."
date: 2026-03-19
lastmod: 2026-03-19
weight: 11
---
An agentic AI system is a business process. It receives inputs, executes a sequence of operations, consumes resources, produces outputs, and fails in predictable, measurable ways. Every data science technique you have learned — from funnel analysis to queueing theory to A/B testing — applies directly. You do not need new methods. You need new mappings.
<!--more-->
---

## Topic 1 — Agent Logs as Event Data

> **Business Analogy: Clickstream / Customer Journey Analytics**

### What Agent Traces Look Like

An agent execution trace is a timestamped sequence of events: the user query arrives, the orchestrator selects a plan, the agent invokes tools (search, retrieval, API calls), reads from memory, calls the LLM one or more times, assembles a response, and returns it. Each event carries metadata — latency, token counts, tool parameters, intermediate outputs, success/failure flags.

This is structurally identical to a **web session log**. A user lands on a site, navigates pages, clicks products, adds to cart, and either converts or drops off. The session is a sequence of timestamped events with metadata.

### The Mapping

| Web Analytics Concept | Agent Analytics Equivalent |
|---|---|
| Session | Agent task execution (from query to response) |
| Pageview / event | Individual step: tool call, LLM invocation, memory read |
| Sessionization | Grouping events by task ID or conversation thread |
| Conversion rate | **Task completion rate** — did the agent produce a satisfactory output? |
| Pages per session | **Mean steps-to-completion** — how many operations did the agent need? |
| Bounce rate | Agent fails or returns a refusal on the first step |
| Funnel drop-off | Point in the execution path where the agent most often fails or loops |
| Click frequency distribution | **Tool call frequency distribution** — which tools are called, how often, in what order? |

### Key Metrics

- **Task completion rate** — the agent's conversion rate. Track daily, weekly, by query category.
- **Mean and median steps-to-completion** — efficiency measure. Rising step count may indicate confusion or unnecessary looping.
- **Tool call frequency distribution** — reveals over-reliance on specific tools or underutilization of available capabilities.
- **Path diversity** — how many distinct execution paths exist? High diversity may indicate inconsistency; low diversity may indicate rigidity.

### Visualization

**Sankey diagrams** of agent execution paths serve the same function as customer journey maps. Nodes represent agent actions (retrieve, search, compute, format); edges represent transitions; width encodes frequency. The visualization immediately reveals the dominant paths, the rare paths, and the failure exits — exactly as a Sankey reveals the dominant customer journeys through a website.

> **Discussion Prompt:** "What does a 'bounce' look like in an agent system? Is it always bad? When might a single-step completion be desirable, and when does it signal a problem?"

---

## Topic 2 — Performance Monitoring & Degradation Detection (15 min)

> **Business Analogy: KPI Trend Monitoring / Demand Forecasting / SLA Tracking**

### The Core Problem

Agent systems degrade silently. Unlike a server crash — which triggers an alert — a 5% decline in answer quality over three weeks produces no error. Users notice before dashboards do, unless the dashboards are designed with data science thinking.

This is the same problem faced by any business tracking KPIs: revenue doesn't crash overnight, it erodes. Customer satisfaction drifts. Forecast accuracy decays. The methods for catching silent degradation are identical.

### Quality Metrics Over Time

Track these as time series:

- **Answer correctness** (human-rated or LLM-judged on a sample)
- **Task success rate** (binary: did the agent complete the task?)
- **Latency** (end-to-end and per-step)
- **Token consumption** (cost proxy)
- **User satisfaction** (if feedback is collected)

### Time-Series Analysis

Apply standard decomposition: **trend** (is quality declining?), **seasonality** (do certain times of day or week show different performance — e.g., batch jobs competing for GPU resources?), **residual** (noise vs. signal). Rolling averages (7-day, 28-day) smooth noise and reveal trend.

### Statistical Process Control (SPC)

**Control charts** — X-bar, R-charts, CUSUM — are used identically in manufacturing QA, service level monitoring, and agent performance tracking. The logic:

1. Establish a baseline period of stable performance.
2. Compute control limits (typically ±3σ).
3. Plot ongoing metrics against these limits.
4. Flag violations: single point outside limits, runs of 7+ above/below center, trending sequences.

**CUSUM (Cumulative Sum) charts** are particularly valuable for detecting small, sustained shifts — the kind of slow degradation that agents exhibit when upstream data changes or model weights drift subtly.

### Change-Point Detection

Algorithms like PELT (Pruned Exact Linear Time) or Bayesian Online Change-Point Detection identify the *moment* a distribution shifts. In manufacturing, this detects when a machine tool begins producing slightly out-of-spec parts. In agent systems, it detects when answer quality shifts — perhaps because the retrieval index was updated, a model version changed, or the distribution of user queries evolved.

### Concept Drift

**Concept drift** in business forecasting occurs when the relationship between features and target changes — a demand model trained in 2024 underperforms in 2025 because consumer behavior shifted. In agent systems, the equivalent is **task distribution drift**: the queries users ask evolve, the documents in the knowledge base age, or the external APIs the agent calls change their response format. The agent's behavior degrades not because the agent changed, but because the world did.

> **Key Insight:** "How do you know your agent got worse before your users tell you?" The answer is the same as in any business: instrument the process, track the metrics, set control limits, and automate anomaly detection. SPC is not a manufacturing technique — it is a *process monitoring* technique that applies to any repeated operation.

---

## Topic 3 — Classifying Agent Failures 

> **Business Analogy: Customer Complaint Classification / Fraud Detection / Ticket Routing**

### Taxonomy of Agent Failures

Agent outputs fail in categorizable ways. A working taxonomy:

| Failure Category | Description | Business Analogy |
|---|---|---|
| **Hallucination** | Agent generates factually incorrect content with high confidence | Fraudulent transaction — looks legitimate, isn't |
| **Tool failure** | External tool returns an error or unexpected result | Supply chain disruption — upstream dependency fails |
| **Misrouting** | Agent selects the wrong tool or wrong sub-agent for the task | Ticket misrouted to the wrong department |
| **Context loss** | Agent loses track of conversation history or task state | Customer has to repeat their problem to a new rep |
| **Prompt injection** | Adversarial input causes the agent to deviate from instructions | Social engineering attack on a call center agent |
| **Infinite loop** | Agent enters a cycle of repeated actions without progress | Escalation loop — ticket bounces between departments |
| **Partial completion** | Agent completes part of the task but misses key requirements | Order shipped incomplete |

### Multi-Label Classification

A single agent output can exhibit *multiple* failure modes simultaneously — a hallucinated answer that also lost context and was produced after a silent tool failure. This is a **multi-label classification** problem, not multi-class. The distinction matters for metric selection (use Hamming loss, subset accuracy, or per-label F1 rather than simple accuracy).

### Cost-Sensitive Classification

The cost asymmetry is severe and asymmetric — exactly as in fraud detection:

- **False negative** (missed hallucination): User acts on incorrect information. Reputational damage, safety risk, liability. *High cost.*
- **False positive** (flagged a correct answer as hallucination): Answer gets reviewed unnecessarily. Human effort wasted. *Low cost.*

This asymmetry demands threshold tuning, class weighting, or cost-sensitive loss functions — the same toolkit used in fraud detection, medical screening, and safety-critical classification.

### The Label Definition Problem

> **Key Insight:** Deciding what counts as "failure" is a **domain problem**, not a modeling problem. This is identical to the challenge of defining "churn" in a CRM system (inactive for 30 days? 60 days? Reduced usage? Canceled subscription?) or defining "fraud" in a payments system (rule-based threshold? Statistical anomaly? Confirmed investigation?). The taxonomy above is a starting point — every deployment will require domain-specific refinement based on the use case, the user population, and the consequences of each failure type.

### Active Learning for Efficient Labeling

Agent failure labels are expensive to obtain — they require expert review of each output. **Active learning** addresses this by prioritizing the most informative examples for labeling:

- **Uncertainty sampling**: Label the examples where the current classifier is least confident — exactly the strategy used to efficiently label rare fraud cases or ambiguous medical images.
- **Query-by-committee**: Multiple models vote; label the examples where they disagree most.

The result: a usable classifier with far fewer labeled examples than random sampling would require.

### Confusion Matrix Walkthrough

Consider a binary "hallucination detector" evaluated on 500 agent outputs:

|  | Predicted: Hallucination | Predicted: Correct |
|---|---|---|
| **Actual: Hallucination** | 38 (TP) | 12 (FN) |
| **Actual: Correct** | 25 (FP) | 425 (TN) |

- **Precision:** 38/63 = 60% — many flagged outputs are actually fine.
- **Recall:** 38/50 = 76% — 24% of hallucinations slip through.
- **For this use case, recall matters more.** A missed hallucination is costlier than a false flag. Tune the threshold to push recall toward 90%+ even at the expense of precision — same reasoning as in fraud detection.

> **Discussion Prompt:** "In your own agent system, what failure categories would you define? How would you decide the boundary between 'partially correct' and 'failure'?"

---

## Topic 4 — Retrieval Quality Analytics

> **Business Analogy: Search Relevance / Recommendation Systems / Catalog Coverage**

### The Metrics

RAG system retrieval quality is evaluated with the same metrics used in **e-commerce search** and **recommendation engine** evaluation:

- **Precision@k** — Of the top-k retrieved documents, how many are relevant? (Same as: of the top-k search results on an e-commerce site, how many match the shopper's intent?)
- **Recall@k** — Of all relevant documents in the corpus, how many appear in the top-k? (Same as: does the search engine surface *all* relevant products, or miss some?)
- **NDCG (Normalized Discounted Cumulative Gain)** — Are the most relevant documents ranked highest? (Same as: are the best products at the top of the search results page?)

### Retrieval Scores as Predictive Features

A natural analytical question: **does retrieval similarity score predict answer quality?** This is a regression / correlation analysis problem. Extract features from retrieval:

- Top-1 similarity score
- Mean and variance of top-k scores
- Gap between top-1 and top-2 scores (confidence margin)
- Chunk length of retrieved documents
- Query-document lexical overlap

Fit a regression model predicting answer quality (human-rated or LLM-judged) from these features. The feature importance ranking tells you *which aspects of retrieval matter most* for downstream quality — actionable intelligence for tuning the retrieval pipeline.

### Coverage Analysis

Which **query clusters** have poor retrieval performance? Embed user queries, cluster them (K-means or HDBSCAN), and compute per-cluster retrieval metrics. This reveals **underserved segments** — query types where the knowledge base has gaps or the embedding model performs poorly.

This is identical to identifying **underserved customer segments** in retail analytics: which customer cohorts have low conversion rates? What products are they searching for that the catalog doesn't carry?

> **Key Insight:** RAG quality is a regression problem. Predict answer quality from retrieval features, identify the weak spots, and invest in the clusters where retrieval fails. The analytical framework is identical to diagnosing why certain customer segments have poor conversion on an e-commerce site.

---

## Topic 5 — Multi-Agent Coordination as Operations Analytics

> **Business Analogy: Call Center Workforce Management / Supply Chain Optimization / Hospital Patient Flow**

### Agent Pipelines as Queuing Systems

A multi-agent system is a **queuing network**. Queries arrive, wait for an available agent instance, get processed through a sequence of steps (sub-agents, tools, LLM calls), and exit. This is structurally identical to:

- A **call center**: calls arrive, wait in queue, get handled by agents, transfer between departments.
- A **hospital emergency department**: patients arrive, triage, wait, get treated by specialists, discharge.
- A **supply chain**: orders arrive, get processed through manufacturing stages, ship.

### Little's Law

**L = λW**

- **L** = average number of tasks in the system (in-progress)
- **λ** = average arrival rate (queries per second)
- **W** = average time a task spends in the system (end-to-end latency)

This holds for *any* stable queuing system. If your agent handles λ = 5 queries/minute and each takes W = 30 seconds on average, you'll have L = 2.5 tasks in-flight on average. If W increases to 60 seconds, L doubles — and if you only have 3 agent instances, the queue begins to grow.

Little's Law is taught in every operations management course. It applies to agent systems without modification.

### Bottleneck Identification

**Theory of Constraints (TOC):** The throughput of the entire system is limited by its slowest component. In a multi-agent pipeline:

- Measure **utilization** of each sub-agent and tool: utilization = (busy time) / (total time).
- The component with the highest utilization is the bottleneck.
- Improving any *non-bottleneck* component has zero impact on system throughput.

This is the same analysis used to identify the bottleneck station in a manufacturing line or the overloaded department in a call center.

### Service Time Distributions

Tool call durations and sub-agent processing times are rarely normally distributed. They typically follow **Log-Normal** or **Gamma** distributions — a long right tail with occasional slow calls. Fitting the correct distribution matters for:

- Capacity planning (how many instances do you need to meet SLA at the 95th percentile?)
- Anomaly detection (is a 45-second tool call genuinely unusual, or just the tail of the distribution?)

This is the same distributional modeling used for **service times in retail checkout**, **hospital procedure durations**, and **warehouse pick times**.

### Visualization

**Gantt-style charts** of parallel agent execution reveal the critical path — the longest sequential chain of dependencies that determines end-to-end latency. This is identical to **critical path analysis** in project management. Shorten the critical path and you shorten total latency; shorten a non-critical parallel branch and you change nothing.

> **Discussion Prompt:** "In your own agent system, which component do you suspect is the bottleneck? How would you measure it? What would you do if you confirmed it?"

---

## Topic 6 — Evaluation as Experimental Design

> **Business Analogy: A/B Testing / Marketing Campaign Experiments / Clinical Trials**

### Controlled Experiments for Agents

To compare agent configurations (different models, prompts, tool sets, retrieval strategies), run a **controlled experiment**:

1. **Hold the task set constant** — use a fixed evaluation benchmark of representative queries.
2. **Vary one configuration dimension** at a time (or use factorial design for interactions).
3. **Randomize** the assignment of queries to configurations to avoid selection bias.

This is standard A/B testing methodology, applied to agent configurations rather than website layouts or ad copy.

### Statistical Significance Testing

Compare quality scores between configurations:

- **t-test** (or Welch's t-test) when quality scores are approximately normal.
- **Mann-Whitney U test** when distributions are skewed or ordinal — common with Likert-scale ratings or LLM-judged scores.
- **Paired tests** when you can run both configurations on the same queries (within-subjects design) — more statistical power.

### Effect Size

> **Key Insight:** Statistical significance ≠ practical significance. A new retrieval strategy might produce a statistically significant 0.3-point improvement on a 100-point quality scale with p < 0.01 — and be completely irrelevant in practice. Always report **effect size** (Cohen's d, or raw difference in meaningful units) alongside the p-value. This is the same lesson taught in every marketing experimentation course: a statistically significant 0.1% lift in click-through rate is real but may not justify the engineering effort.

### Multi-Armed Bandit for Online Evaluation

When you cannot afford to commit 50% of traffic to a possibly inferior configuration for weeks, use **multi-armed bandit** algorithms (Thompson Sampling, UCB) to adaptively allocate traffic. Configurations that perform well get more traffic; poor performers get less. This is the same approach used in **dynamic ad serving** and **personalized recommendation** — exploit the best-known option while continuing to explore.

### LLM-as-Judge: Measurement Instrument Validation

When using an LLM to judge agent output quality, treat the LLM-judge as a **measurement instrument** subject to the same validation requirements as a survey instrument in social science:

- **Systematic bias**: Does the judge favor longer answers? More formal tone? Answers that agree with its own knowledge?
- **Calibration**: Does a judge score of "4/5" mean the same thing across different query types?
- **Inter-rater agreement**: If you run the same judgment twice (or with two different judge models), how consistent are the scores? Compute **Cohen's kappa** or **Krippendorff's alpha** — the same metrics used to validate human annotation schemes.

> **Discussion Prompt:** "If you were to run an A/B test on your own agent system, what is the single most important metric you would track, and how many queries would you need to detect a meaningful difference?"

---

## Topic 7 — Unsupervised Discovery of Behavior Patterns (5 min)

> **Business Analogy: Customer Segmentation / Market Basket Analysis / Behavioral Cohort Analysis**

### Clustering Agent Sessions

Represent each agent session as a **behavioral feature vector**: tool usage profile (which tools, how often), task length, latency, token count, outcome (success/failure), number of retries. Apply **K-means**, **HDBSCAN**, or **Gaussian Mixture Models** to discover natural groupings.

These clusters are agent behavioral segments — the equivalent of customer segments in CRM analytics. You may discover that your agent has two distinct "modes": a fast, efficient path for simple queries and a slow, exploratory path for complex ones. Or that a cluster of sessions all fail at the same tool call — a systematic issue invisible in aggregate metrics.

### Association Rule Mining

Apply **Apriori** or **FP-Growth** to tool call sequences to discover frequent patterns: "When the agent calls web_search, it almost always calls citation_formatter next" or "Retrieval followed by a second retrieval attempt is associated with task failure." This is **market basket analysis** applied to agent behavior rather than shopping carts.

### Dimensionality Reduction for Visualization

Embed agent traces (using their behavioral feature vectors or by embedding the full trace text) and project to 2D with **UMAP** or **t-SNE**. The resulting scatter plot reveals clusters, outliers, and structural patterns in agent behavior — a behavioral landscape map.

### Outlier Detection

**Isolation Forest**, **Local Outlier Factor (LOF)**, or **DBSCAN's noise points** flag unusual agent sessions — sessions that don't fit any normal behavioral cluster. This is the same anomaly detection pipeline used in **fraud analytics**, **network intrusion detection**, and **rare event identification in CRM**.

> **Key Insight:** Unsupervised methods are discovery tools. They answer the question you didn't know to ask: "What behavioral patterns exist in my agent system that I haven't designed for?"

---

## Unified Mapping Table

| Classic Analytics Problem | Agentic AI Equivalent | Key Technique |
|---|---|---|
| Conversion funnel analysis | Task completion path analysis | Sankey diagrams, sequence analysis |
| Concept drift in forecasting | Agent performance degradation | Change-point detection, SPC control charts |
| Customer complaint classification | Agent failure taxonomy | Multi-label classification, cost-sensitive learning |
| Search relevance optimization | Retrieval quality in RAG pipelines | NDCG, Precision@k, Recall@k |
| Call center queueing / workforce mgmt | Multi-agent coordination & load balancing | Little's Law, utilization analysis, bottleneck ID |
| A/B testing marketing campaigns | Agent configuration experiments | t-test, Mann-Whitney U, effect size estimation |
| Customer segmentation | Agent behavioral clustering | K-means, HDBSCAN, UMAP |
| Fraud / anomaly detection | Unusual agent behavior detection | Isolation Forest, LOF, DBSCAN |
| Survey instrument validation | LLM-as-judge calibration | Cohen's kappa, inter-rater reliability |
| Demand forecasting | Query volume & resource planning | Time-series decomposition, capacity models |

---

## Case Study Activity — "The Struggling Research Assistant"

**System Description**

A large research university has deployed an agentic AI research assistant to support graduate students across all departments. The system architecture:

- **Retrieval pipeline:** Semantic search (dense embeddings) over a corpus of 50,000 indexed academic papers
- **Tools:** Web search API, citation formatting tool, abstract summarization module
- **LLM backbone:** GPT-4-class model via API
- **Deployment:** 8 parallel agent instances behind a load balancer
- **Volume:** ~500 queries per day

The system has been running for 10 weeks. It was well-received at launch.

**The Problem — Six Weeks Post-Launch**

The following issues have been reported or observed:

1. **User satisfaction has dropped** from 4.2/5 to 3.4/5 over six weeks (collected via post-interaction survey).
2. **Users report answers that "sound right but cite wrong papers"** — the answers are fluent and plausible, but the cited sources do not support the claims made.
3. **Average response time has increased** from 8 seconds to 22 seconds.
4. **Load imbalance:** One of the 8 agent instances is handling approximately 60% of all queries. The other 7 share the remaining 40%.
5. **Silent retrieval failures:** The retrieval tool is returning empty results (no documents found) for 12% of queries — but it does so without raising an error. The agent proceeds to answer without retrieved context.

<!-- ---

### GROUP ACTIVITY INSTRUCTIONS

Your group has **10 minutes** to work through the questions below. You will not answer all of them in depth — **prioritize the one assigned to your group** and be prepared to present a 1-minute summary. Skim the others for context. -->

---

**Question 1 — Diagnose the Performance Drop**

The satisfaction score declined from 4.2 to 3.4 over six weeks.

- What data would you collect to identify the root cause? Be specific about data sources (logs, metrics, traces, user feedback).
- What visualizations would you build to reveal the problem? Name the chart type and what it would show.
- Which of the five reported issues do you think is the *primary* driver of the satisfaction decline? Why?
- Map each reported issue to a specific data science technique covered in today's session.

---

**Question 2 — Design a Failure Classifier**

Users report answers that "sound right but cite wrong papers."

- Define the failure categories you would use for this system. Be specific — go beyond the generic taxonomy. What failure modes are unique to a research assistant?
- What features would you extract from agent logs to train a classifier? List at least 8 candidate features.
- What is the cost asymmetry? Which type of misclassification is more dangerous, and what is the real-world consequence?
- How would you collect labels efficiently? What active learning strategy would you use?

---

**Question 3 — Analyze the Queueing Imbalance**

One agent instance handles 60% of traffic while seven others share 40%.

- What metrics would you compute to characterize this imbalance? (Think utilization, queue length, wait times.)
- Apply Little's Law: if the system handles 500 queries/day and average processing time is 22 seconds, what is the average number of in-flight queries? What happens to the overloaded instance?
- What does this imbalance imply about the load balancer design? What could cause it?
- What business analogy applies? Describe a parallel situation in call center management or supply chain operations and how it would be diagnosed.

---

**Question 4 — Design an Evaluation Experiment**

The engineering team wants to test a new retrieval strategy (hybrid search: dense + sparse) against the current approach (dense only).

- What is the **unit of randomization**? (Individual queries? Users? Time periods?)
- What **metrics** would you measure? Name a primary metric and at least two guardrail metrics.
- How would you determine **sample size**? What effect size would be practically meaningful for this system?
- How long would you run the experiment? What factors determine the duration?
- What are the risks of running this experiment in production? How would you mitigate them?

---

**Question 5 — Propose a Monitoring Dashboard**

You are asked to design an ongoing Grafana dashboard for this system with exactly **5 KPIs**.

- Name each KPI, define how it is computed, and state what threshold or control limit would trigger an alert.
- For each KPI, name the business operations dashboard equivalent (e.g., "this is the agent equivalent of daily revenue tracking in an e-commerce dashboard").
- Which of the five reported problems would each KPI have caught *before* users complained?
- Sketch the dashboard layout: what goes in the top row (hero metrics) vs. the detail panels below?

---



## Recap

Return to the opening thesis: **an agentic AI system is a business process**. Every technique covered today — funnel analysis, SPC, classification, queueing theory, experimental design, clustering — is a technique students already know, applied to a new domain. The mapping is not metaphorical; it is structural. Agent logs are event data. Agent failures are classifiable defects. Agent pipelines are queuing networks. Agent evaluations are experiments.

### Key Takeaway

You already have all the tools. The concepts transfer directly. The challenge is not learning new techniques — it is recognizing which technique applies to which agent management problem, and having the discipline to instrument, measure, and analyze before intervening.



### Recommended Reading

| Topic | Recommended Reading |
|---|---|
| Agent Logs as Event Data | [Langfuse Documentation — Observability & Tracing](https://langfuse.com/docs/observability/overview). Open-source LLM engineering platform with tracing and session analytics. |
| Performance Monitoring & SPC | Montgomery, D.C. — *Introduction to Statistical Quality Control*, 8th ed. (Wiley, 2019). Ch. 5–6 on control charts. ISBN 978-1119399308 |
| Classifying Agent Failures | Settles, B. — [*Active Learning Literature Survey*](https://burrsettles.com/pub/settles.activelearning.pdf), University of Wisconsin-Madison, Computer Sciences Technical Report 1648, 2009. Foundational reference on efficient labeling. |
| Retrieval Quality Analytics | Manning, C.D., Raghavan, P. & Schütze, H. — [*Introduction to Information Retrieval*](https://nlp.stanford.edu/IR-book/) (Cambridge University Press, 2008). Ch. 8 on evaluation. ISBN 978-0-521-86571-5. Freely available online. |
| Multi-Agent Coordination | Hillier, F.S. & Lieberman, G.J. — [*Introduction to Operations Research*](https://info.mheducation.com/rs/128-SJW-347/images/Preface_Hillier_Intro_Operations_Research_11e.pdf), 11th ed. (McGraw-Hill, 2021). Ch. 17 on queueing models. ISBN 978-1-259-87299-0 |
| Evaluation as Experimental Design | Kohavi, R., Tang, D. & Xu, Y. — [*Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*](https://www.researchgate.net/publication/339914315_Trustworthy_Online_Controlled_Experiments_A_Practical_Guide_to_AB_Testing) (Cambridge University Press, 2020). ISBN 978-1-108-72426-5 |
| Unsupervised Behavior Discovery | Aggarwal, C.C. — [*Outlier Analysis*](https://charuaggarwal.net/outlierbook.pdf), 2nd ed. (Springer, 2017). Comprehensive treatment of anomaly detection. ISBN 978-3-319-47577-6. Author PDF freely available. |

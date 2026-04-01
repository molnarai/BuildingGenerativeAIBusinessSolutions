---
date: 2026-04-06
classdates: 'Monday 2026-04-06, Wednesday 2026-04-01'
draft: false
title: 'Data Science on Agentic System'
weight: 110
numsession: 11
---

The focus of this session is on managing agentic AI systems using established data science methodologies rather than treating them as unique technical mysteries. We explore how techniques such as funnel analysis, queueing theory, and statistical process control can be directly applied to monitoring and evaluating intelligent systems.
<!--more-->
Through a detailed mapping of classic analytics to AI-specific challenges - including classifying agent failure modes, optimizing retrieval quality, and detecting performance degradation - we illustrate how familiar analogies like clickstream data and call center operations translate to instrumenting execution logs and designing controlled experiments. 

{{<figure src="imgs/Manage_Agentic_AI_with_Traditional_Analytics.png" width="800" alt="Figure 1" >}}

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Manage_Agentic_AI_with_Traditional_Analytics.m4a">
    Your browser does not support the audio element.
</audio>


### Deep Dive
<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Forcing_structured_outputs_with_constrained_decoding.m4a">
    Your browser does not support the audio element.
</audio>


### Presentation
 - [Data Science for Agentic AI](../../slides/slide-11-data-science-agentic-ai/)

### Lecture Notes
- [Data Science for Agentic AI: Managing, Monitoring, and Evaluating Intelligent Agent Systems](../../blog/data-science-for-agentic-ai/)

### Mapping Classic Data Science Techniques to Agentic AI Management

| Classic Analytics Problem | Agentic AI Equivalent | Key Technique | Business Analogy | Primary Metrics |
|---|---|---|---|---|
| Conversion funnel analysis | Task completion path analysis | Sankey diagrams, sequence analysis | Clickstream / Customer Journey Analytics | Task completion rate, Mean steps-to-completion, Tool call frequency, Path diversity |
| Concept drift in forecasting | Agent performance degradation | Change-point detection, SPC control charts | KPI Trend Monitoring / Demand Forecasting / SLA Tracking | Answer correctness, Task success rate, Latency, Token consumption |
| Call center queueing / workforce mgmt | Multi-agent coordination & load balancing | Little's Law, utilization analysis, bottleneck ID | Hospital Patient Flow / Supply Chain Optimization | Utilization rate, throughput, end-to-end latency ($W$), tasks in-flight ($L$) |
| Survey instrument validation | LLM-as-judge calibration | Cohen's kappa, inter-rater reliability | Social science survey validation | Krippendorff's alpha, Cohen's kappa, bias/calibration metrics |
| Search relevance optimization | Retrieval quality in RAG pipelines | NDCG, Precision@k, Recall@k | E-commerce Search / Recommendation Systems | Precision@k, Recall@k, NDCG, Similarity scores |
| Customer complaint classification | Agent failure taxonomy | Multi-label classification, cost-sensitive learning | Fraud Detection / Ticket Routing | Hamming loss, subset accuracy, per-label F1, Precision/Recall |
| A/B testing marketing campaigns | Agent configuration experiments | t-test, Mann-Whitney U, effect size estimation | Marketing Campaign Experiments / Clinical Trials | p-value, Cohen's d (Effect size), Statistical significance |
| Demand forecasting | Query volume & resource planning | Time-series decomposition, capacity models | Retail Demand Forecasting | Trend, Seasonality, Residuals, GPU/Resource utilization |
| Customer segmentation | Agent behavioral clustering | K-means, HDBSCAN, UMAP | CRM Behavioral Cohort Analysis | Cluster membership, silhouette scores (inferred), behavioral feature vectors |
| Fraud / anomaly detection | Unusual agent behavior detection | Isolation Forest, LOF, DBSCAN | Network Intrusion Detection | Outlier scores, noise points |



# Question 1 - Diagnose the Performance Drop
*20 valid responses*

The satisfaction score declined from 4.2 to 3.4 over six weeks.

- What data would you collect to identify the root cause? Be specific about data sources (logs, metrics, traces, user feedback).
- What visualizations would you build to reveal the problem? Name the chart type and what it would show.
- Which of the five reported issues do you think is the *primary* driver of the satisfaction decline? Why?
- Map each reported issue to a specific data science technique covered in today's session.

## Summary

Student responses demonstrated a generally good understanding of the problem and the data needed to diagnose it. Most students correctly identified the importance of combining quantitative data (logs, metrics, traces) with qualitative data (user feedback). The suggested visualizations were generally appropriate, with line charts for trends and funnel charts being popular choices. Identifying the *primary* driver of the decline was more challenging; while many recognized performance/latency as a likely culprit, some struggled to articulate a compelling rationale beyond a general understanding of user frustration. Mapping data science techniques to the reported issues was the weakest area, revealing a less thorough understanding of how specific techniques could address specific problems. Overall, the responses showed a good grasp of the diagnostic process, but lacked depth in reasoning and the application of data science methodologies.

## Core Ideas

* **Importance of Combined Data:** A recurring theme was the necessity of blending quantitative and qualitative data. Students recognized that logs, metrics, and traces needed to be complemented by user feedback (CSAT comments, tickets, reviews) to understand the "why" behind the numbers.
* **Time-Series Analysis:** The vast majority of students prioritized time-series visualizations (line charts) to track satisfaction and related metrics over time. Recognizing the temporal aspect of the problem was key.
* **Segmentation and Cohort Analysis:** Several responses correctly suggested segmenting data by user type (device, region, new vs returning) to pinpoint areas of concentrated impact.  Cohort analysis (especially by signup date) was also highlighted as a valuable diagnostic tool.
* **Focus on Latency & Performance:** Most students identified performance/latency as a likely primary driver, understanding the immediate and widespread impact of slow response times on user experience.
* **Funnel Analysis:** Several responses included the suggestion of funnel charts to understand where users were dropping off in the experience, a logical step in identifying bottlenecks.

## Common Gaps

* **Distinguishing Correlation from Causation:** While students often identified correlations (e.g., satisfaction vs. latency), fewer explicitly discussed how to investigate *causation*.  There was limited discussion of controlled experiments or other methods to establish causality.
* **Depth of Data Science Technique Application:** The mapping of issues to data science techniques was frequently superficial. Students often listed techniques (e.g., "change-point detection") without demonstrating a clear understanding of *how* they would be applied to a specific problem.  For example, "multi-label classification" was suggested for UI issues, but the specific features to be extracted from support tickets were not discussed.
* **Understanding "Primary Driver" Reasoning:** Students often named latency as the primary driver but lacked detailed reasoning. They didn't fully explore how other issues (e.g., retrieval relevance) could *exacerbate* latency's impact, or how a different issue might have a more direct link to the satisfaction drop.
* **Log Analysis Detail:** While students mentioned logs, descriptions of *what* to look for in those logs were often generic ("errors," "exceptions").  More specific examples (e.g., examining database query performance, tracing request latency through microservices) would have demonstrated a deeper understanding.
* **Embedding Drift Detection - Lack of Understanding:** Several students cited embedding drift detection.  However, few demonstrated a clear grasp of what embedding drift *is* and why it would specifically contribute to a satisfaction decline, particularly in a search context.

---

# Question 2 - Design a Failure Classifier
*20 valid responses*

Users report answers that "sound right but cite wrong papers."

- Define the failure categories you would use for this system. Be specific - go beyond the generic taxonomy. What failure modes are unique to a research assistant?
- What features would you extract from agent logs to train a classifier? List at least 8 candidate features.
- What is the cost asymmetry? Which type of misclassification is more dangerous, and what is the real-world consequence?
- How would you collect labels efficiently? What active learning strategy would you use?

## Summary

Overall, the student responses demonstrated a good understanding of the need for a nuanced failure classifier for a research assistant AI, going beyond basic hallucination detection. Most students attempted to define specific failure categories and propose relevant features, and they recognized the cost asymmetry inherent in this type of classification task. While the quality of the proposed features and labeling strategies varied, the responses generally grasped the seriousness of allowing false negatives to slip through. A significant portion of responses suggested uncertainty sampling as an active learning strategy, although the depth of understanding about how to *effectively* implement this varied. Several responses struggled to articulate unique failure modes specific to a research assistant.

## Core Ideas

- **Beyond Hallucination:** Almost all responses correctly identified the need to move beyond the generic "hallucination" classification and define more specific failure modes.
- **Cost Asymmetry:** The majority of responses correctly understood that false negatives (allowing incorrect citations to pass) are significantly more dangerous than false positives (flagging correct citations). The real-world consequences, ranging from academic integrity issues to flawed policy decisions, were often mentioned.
- **Uncertainty Sampling:**  This was the most frequently proposed active learning strategy, demonstrating a general awareness of how to efficiently utilize expert labelers.
- **Specific Failure Categories:** Students offered a range of specific failure categories including: phantom citations (non-existent papers), citation-claim mismatches (paper doesn't support the claim), scope inflation (misrepresenting findings), temporal misattribution (outdated citations), and confidence laundering (using citations to appear authoritative).
- **Feature Extraction:**  Numerous features were proposed for training the classifier, including: cosine similarity, retrieval rank, round-trip fidelity, author name perplexity, hedging language detection, claim specificity vs. source vagueness, and publication date relative to field velocity.
- **Unique Research Assistant Failure Modes:** Several responses attempted to articulate failures specific to an AI acting as a research assistant, such as twisting methodology details or misattributing findings.

## Common Gaps

- **Depth of Understanding of Active Learning:** While uncertainty sampling was often mentioned, some responses lacked detail on how to *effectively* implement it.  For example, some didn't consider how to handle initial labeling or how to incorporate diversity sampling to prevent the classifier from getting stuck on a single failure mode.
- **Specificity of Research Assistant Failure Modes:** While students attempted to identify research-specific failure modes, some responses were generic and could apply to AI systems in other domains. A deeper consideration of how a research assistant's unique role (synthesizing information, adhering to academic rigor) leads to specific failure points was often missing.
- **Understanding "Round-Trip Fidelity":** A few students included "round-trip fidelity," but the understanding of this concept (verifying that a re-run of the query returns the same cited paper) was often superficial.
- **Feature Justification:** Some proposed features were listed without sufficient justification or explanation of *why* they would be indicative of a failure.  "Citation confidence score" was frequently listed but without elaborating on what contributes to this score or how it could be misleading.
- **Programmatic Weak Labels:** While a few responses mentioned bootstrapping or using programmatic labels (e.g., DOI resolution failures), a thorough understanding of the potential pitfalls and limitations of this approach was generally lacking.  The challenges of ensuring the accuracy and reliability of programmatic labels were often not addressed.

---

# Question 3 - Analyze the Queueing Imbalance
*21 valid responses*

One agent instance handles 60% of traffic while seven others share 40%.

- What metrics would you compute to characterize this imbalance? (Think utilization, queue length, wait times.)
- Apply Little's Law: if the system handles 500 queries/day and average processing time is 22 seconds, what is the average number of in-flight queries? What happens to the overloaded instance?
- What does this imbalance imply about the load balancer design? What could cause it?
- What business analogy applies? Describe a parallel situation in call center management or supply chain operations and how it would be diagnosed.

## Summary

Overall, the student responses to Question 3 were quite good, demonstrating a solid understanding of queueing principles and their application to a real-world system imbalance. Most students correctly identified the key metrics needed to characterize the problem (utilization, queue length, wait times) and applied Little's Law reasonably well. The call center analogy was a common and effective way to illustrate the problem, though the depth of the explanation varied. A few responses went off on tangents regarding hallucination in LLMs which was not relevant. The level of detail in explaining potential load balancer issues was also varied; some responses offered a comprehensive list of potential causes, while others were more superficial.

## Core Ideas

* **Key Metrics Identification:** Almost all students recognized that metrics like utilization per instance, queue length, and wait times were crucial for identifying and understanding the imbalance. Some also mentioned tail latencies and throughput variance, showing a more sophisticated understanding.
* **Little's Law Application:** Students generally understood the principles of Little's Law and were able to apply it to calculate the average number of in-flight queries.  The calculations themselves were generally correct, although there were minor arithmetic errors in some responses.
* **Load Balancer Issues:** A recurring theme was the recognition that the load balancer was likely the root cause of the imbalance. Several students correctly identified potential issues like sticky sessions, inconsistent hashing, and health check failures.
* **Business Analogy:** The call center analogy was consistently used and usually well-explained, providing a relatable context for the technical problem.  Some responses also drew parallels to supply chain operations.
* **Overloaded Instance Behavior:** Students recognized the overloaded instance would experience increased queue length, longer wait times, and potentially degraded performance that would affect the overall system.

## Common Gaps

* **Understanding of Little's Law Context:** While students could *apply* Little's Law, some struggled to interpret the results within the context of the problem. For example, some didn't adequately connect the low average in-flight queries with the fact that one instance was still heavily overloaded.
* **Root Cause Analysis Depth:** Some responses provided a list of potential causes for the load imbalance but didn't deeply analyze *why* those issues might be occurring.  More probing questions about the load balancer configuration or the nature of the requests would have strengthened these responses.
* **Metrics beyond the Basics:** While most students identified the core metrics, fewer addressed metrics beyond utilization and wait times, such as throughput variance and the coefficient of variation, indicating a potential lack of understanding of more advanced queueing theory.
* **Distinguishing Between Load and Capacity:** Some responses confused the *imbalance* with an overall *capacity* issue. It was important to emphasize that the system as a whole had sufficient capacity, but the distribution was skewed.
* **LLM Hallucinations:** A few responses significantly diverged and explored irrelevant topics like LLM hallucinations, demonstrating a misunderstanding of the question's focus.

---

# Question 4 - Design an Evaluation Experiment
*17 valid responses*

The engineering team wants to test a new retrieval strategy (hybrid search: dense + sparse) against the current approach (dense only).

- What is the unit of randomization? Individual queries? Users? Time periods?)
- What metrics would you measure? Name a primary metric and at least two guardrail metrics.
- How would you determine sample size? What effect size would be practically meaningful for this system?
- How long would you run the experiment? What factors determine the duration?
- What are the risks of running this experiment in production? How would you mitigate them?

## Summary

Overall, the student responses demonstrated a reasonable understanding of the components of an evaluation experiment. Most students correctly identified user-level randomization as preferable and proposed relevant primary and guardrail metrics. There was a general grasp of the need for power analysis and considering the duration of the experiment. However, the depth of understanding varied significantly, with some responses lacking detail regarding effect size determination and risk mitigation. A recurring theme was the prioritization of user experience and the recognition of potential negative impacts of a new system. Some responses repeated similar language, which suggests potential collaboration or reliance on shared resources.

## Core Ideas

- **Unit of Randomization:** The overwhelming majority correctly identified user-level randomization as the preferred method, understanding the potential for confounding factors introduced by query or time-based randomization.
- **Primary Metric:** Click-through rate (CTR), successful result rate, and user satisfaction were consistently suggested as primary metrics, reflecting a focus on overall search quality.
- **Guardrail Metrics:** Latency, zero-result/no-click rate, user abandonment/refinement rate, and hallucination rate were frequently mentioned as important guardrails. The recognition that relevance improvements shouldn't come at the cost of speed or user experience was a common thread.
- **Power Analysis and Effect Size:** Several responses mentioned the need for power analysis and considered a 2-5% lift in successful result rate or CTR as practically meaningful.
- **Experiment Duration:** A general consensus emerged around a minimum duration of one to two weeks to cover weekday/weekend patterns, with a connection to reaching a sufficient sample size.
- **Risk Mitigation:** Staged rollouts, tight guardrail monitoring, and kill switches were common suggestions for mitigating risks.
- **Holistic Approach:** Many students attempted to consider the broader user experience, emphasizing that improvements in one area (e.g., relevance) shouldn't negatively impact others (e.g., speed, cost).

## Common Gaps

- **Effect Size Justification:** While many mentioned power analysis, the rationale for *choosing* a specific effect size (e.g., 2-5% lift) was often lacking. Students frequently stated the value but didn't explain *why* it was considered meaningful beyond just saying it was "small but real."
- **Cost Considerations:** While some responses mentioned cost, the detailed economic analysis of the hybrid approach was often superficial.  A deeper dive into the infrastructure and operational costs of the new system wasn't always present.
- **Statistical Rigor:** A few responses lacked a clear understanding of statistical significance and the nuances of A/B testing.  The reliance on anecdotal observations ("if anything looks off") wasn't sufficient for a graduate-level audience.
- **Query Diversity:** The consideration of how the new retrieval strategy might perform differently across various query types or user segments was not consistently addressed.
- **Hallucination Rate:**  The suggestion of monitoring hallucination rate, while insightful, indicates a potential understanding gap in what constitutes "relevant" documents within a search result, particularly in the context of a hybrid approach.
- **Detailed Risk Mitigation:** The risk mitigation strategies, while generally good, often lacked specifics. For example, what *specific* thresholds would trigger a kill switch?

---

# Question 5 - Propose a Monitoring Dashboard
*17 valid responses*

You are asked to design an ongoing Grafana dashboard for this system with exactly 5 KPIs.

- Name each KPI, define how it is computed, and state what threshold or control limit would trigger an alert.
- For each KPI, name the business operations dashboard equivalent (e.g., "this is the agent equivalent of daily revenue tracking in an e-commerce dashboard").
- Which of the five reported problems would each KPI have caught before users complained?
- Sketch the dashboard layout: what goes in the top row (hero metrics) vs. the detail panels below?

## Summary

Overall, the student responses demonstrated a reasonable understanding of the task, consistently proposing five KPIs and attempting to relate them to business operations dashboards. Many students chose KPIs focusing on user experience (satisfaction, latency), accuracy (correctness, citation validity), and system health (utilization, success rate). The attempts to connect KPIs to business equivalents were generally good, though sometimes superficial. The dashboard layout suggestions were also present in most answers, prioritizing "hero metrics" for immediate visibility. However, the depth of justification for *why* certain thresholds were chosen and *exactly* how each KPI would have caught specific reported problems varied significantly. There was a tendency towards simpler, more readily measurable KPIs, sometimes at the expense of more nuanced or proactive indicators. Some responses lacked specificity regarding computation and alerting mechanisms.

## Core Ideas

- **Focus on User Experience:** A large majority of responses prioritized user satisfaction, response latency, and retrieval success/relevance as key indicators, demonstrating an understanding of the system's primary goal.
- **Accuracy is Paramount:** The critical importance of answer correctness and citation validity was consistently recognized. Most students identified these as crucial signals of system quality.
- **System Health & Load Balancing:** Many responses included metrics related to system performance, such as instance utilization or error rates, acknowledging the importance of operational stability.
- **Business Operations Analogy:** Students generally attempted to frame KPIs within a business context, drawing parallels to e-commerce (page load times, conversion rates), call centers (workload per agent), or order fulfillment (latency).
- **Prioritized Dashboard Layout:** The concept of a tiered dashboard with "hero metrics" (top row) and detail panels (below) was widely adopted.
- **Importance of Early Warning:** Most recognized that the goal of the dashboard was to catch issues *before* user complaints arose, rather than just reacting to them.
- **P95 Latency as a Key Indicator:** The use of P95 latency as a key performance indicator was very common, demonstrating an understanding of tail latency as an early warning sign.

## Common Gaps

- **Specificity of Computation:** While KPIs were named, the precise formula or method for calculating them was often glossed over. For example, "satisfaction score" was mentioned frequently, but the definition of how it's *calculated* (e.g., average survey rating, NPS score) wasn't always clear.
- **Threshold Justification:** The rationale behind the chosen alert thresholds was often lacking. Why 3.8 for satisfaction? Why 85% for correctness? Students often provided a justification but rarely demonstrated a deep understanding of the statistical or operational basis for these values.
- **Depth of Problem Detection Justification:** While students often stated *which* problems each KPI would catch, the explanation of *how* it would do so was sometimes superficial. Demonstrating a clear, causal link between a KPI's movement and a specific problem was not always present.
- **Over-Reliance on Simple Metrics:** Many responses leaned towards easily quantifiable metrics, potentially overlooking more nuanced or leading indicators that could provide earlier warning.
- **Hallucination Detection:** While citation validity was often flagged, the more complex problem of hallucinations (generating incorrect or fabricated information) was sometimes underrepresented or addressed inadequately.
- **Lack of Detail on Data Sources:** Few responses considered how the data for these KPIs would be collected and integrated into the Grafana dashboard, demonstrating a gap in practical implementation considerations.
- **Confusing Correlation with Causation:** Several responses assumed that if a KPI changed, it *caused* a specific problem, without considering other potential contributing factors.

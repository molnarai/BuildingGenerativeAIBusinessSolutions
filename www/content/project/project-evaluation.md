+++
title = 'Project Evaluation Rubric'
description = 'Complete evaluation rubric covering all milestones (M01–M06) for the DAIS semester project. Use this document for self-evaluation and grading.'
weight = 70
+++

This document consolidates the evaluation criteria from all project milestones into a single rubric. Each milestone is weighted according to its contribution to the final project grade. Use this rubric for self-evaluation before each submission and as a reference throughout the semester.

---
## AI Evaluation and Feedback Schedule

The table below shows the schedule of the AI evaluation runs.
Any changes that are **committed** or **merged** to the `uat` branch before the evaluation process starts will be reviewed.

**You are not required to have updates for every evaluation run.** Wait until you have meaningful updates before merging to `uat`.


|	Date	|	Evaluation Start Time	|	Number	|
|-----------|---------------------------|-----------|
|	Monday, April 13, 2026	|	1:00 AM	|	1	|
|	Friday, April 17, 2026	|	1:00 AM	|	2	|
|	Monday, April 20, 2026	|	1:00 AM	|	3	|
|	Friday, April 24, 2026	|	1:00 AM	|	4	|
|	Monday, April 27, 2026	|	1:00 AM	|	5	|
|	Friday, May 1, 2026	|	1:00 AM	|	6	|
|	Monday, May 4, 2026	|	1:00 AM	|	Final	|


---

## Grade Allocation

| Milestone | Title                          | Weight |
|-----------|--------------------------------|--------|
| M01       | Project Definition             | 10%    |
| M02       | Data Pipeline, CI/CD Setup     | 15%    |
| M03       | Agentic Prototype              | 20%    |
| M04       | Evaluation Framework Baseline  | 20%    |
| M05       | Iterative Improvement          | 20%    |
| M06       | Final Deliverables             | 15%    |

---

## M01 — Project Definition (10%)

M01 uses a descriptive rubric with four performance levels per criterion.

| #   | Criterion                        | Weight | Excellent | Good | Satisfactory | Needs Improvement |
|-----|----------------------------------|--------|-----------|------|--------------|-------------------|
| 1.1 | Variation and Corpus Selection  | 40     | (36–40) Variation (A/B/C) is clearly identified and tightly aligned with a well-justified corpus; the corpus description specifies document types, sources, time span, and approximate scale, and explains why it is appropriate for the chosen variation and business context. Any constraints (access, preprocessing, licensing) are explicitly stated and reasonable. | (28–35) Variation and corpus are appropriate and generally well aligned; corpus characteristics are described with minor gaps in detail (for example, incomplete discussion of scope or scale), but the choice is feasible and coherent with the project goals. | (20–27) Variation is specified and a corpus is named, but alignment to the variation or to realistic DAIS capabilities is only partially justified; key details about the corpus (types, coverage, or feasibility) are vague or missing. | (0–19) Variation is unclear, inconsistent, or missing; the corpus is poorly defined, obviously infeasible, or largely misaligned with the project; justification is minimal or absent. |
| 1.2 | User Persona and Key Use Cases  | 40     | (36–40) Persona is realistic and well developed (role, goals, context, decision environment, pain points) and is clearly grounded in the chosen variation and corpus; key use cases are specific, technically plausible, and show how DAIS meaningfully supports the persona's workflows with nontrivial queries or tasks, going beyond simple keyword search and generic Q&A. | (28–35) Persona is plausible and relevant, with a generally clear description of role and goals, though some contextual details or pain points may be underdeveloped; use cases are mostly concrete and aligned with the variation and corpus, but limited in variety or depth or only partially highlight the need for an agentic system. | (20–27) Persona is defined but generic or loosely connected to the corpus and variation; use cases are high-level, somewhat repetitive, or close to generic search scenarios; the link between persona, use cases, and DAIS capabilities is only partially evident. | (0–19) Persona is missing, unrealistic for the corpus, or misaligned with the chosen variation; use cases are absent, trivial, or too vague to guide design and later evaluation. |


---

## M02 — Data Pipeline, CI/CD Setup (15%)

| #   | Criterion                        | Description                                                                                                                                          | Points |
|-----|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 2.1 | Code Quality                    | Code is well-structured, modular, and follows best practices for readability and maintainability.                                                    | 30     |
| 2.2 | Pipeline Functionality          | The pipeline successfully ingests a subset of the corpus, extracts relevant metadata and text embeddings, and writes this data to the chosen database without errors. | 30     |
| 2.3 | Architecture Diagram            | The architecture diagram is clear, comprehensive, and accurately reflects the components and data flow of the pipeline.                              | 30     |
| 2.4 | Documentation & Reproducibility | Documentation (`README.md` file) includes clear instructions on how to deploy and run the solution.                                                  | 30     |


---

## M03 — Agentic Prototype (20%)

| #   | Criterion                      | Description                                                                                                                                                                                                                      | Points |
|-----|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 3.1 | Multi-Agent Pipeline           | A functional multi-agent pipeline is established that processes documents, orchestrates agent roles, and produces structured text and data. The agent design is appropriate for the chosen project variation.                       | 40     |
| 3.2 | Document Ingestion & Storage   | The extracted text and structured data produced by the pipeline are ingested and persisted to the appropriate databases in a queryable form.                                                                                       | 40     |
| 3.3 | Dual Interface Implementation  | Both a chat interface for human interaction and a batch query interface for automated evaluation are functional and accessible. The interfaces correctly route queries through the agent pipeline and return meaningful responses. | 40     |
| 3.4 | Architecture & Reproducibility | The system architecture is documented (diagram or written description), the repository is well-organized, and the application can be deployed and run from the provided instructions without manual intervention.                  | 40     |

---

## M04 — Evaluation Framework Baseline (20%)

| #   | Criterion                               | Description                                                                                                                                                                                                                     | Points |
|-----|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 4.1 | Evaluation Test Set Execution           | The completed evaluation test set is run against the batch interface, producing a full set of system outputs. Results are systematically collected, organized, and stored for analysis.                                           | 40     |
| 4.2 | Quantitative Performance Analysis       | System outputs are evaluated against expected results using defined metrics (e.g., accuracy, relevance, completeness). Results are presented clearly with summary statistics and per-query breakdowns where appropriate.         | 40     |
| 4.3 | Error Analysis & Failure Identification | Errors and low-performing cases are identified, categorized, and analyzed. The analysis goes beyond listing failures to explaining likely root causes (e.g., retrieval gaps, prompt failures, schema mismatches).                | 40     |
| 4.4 | Improvement Strategy Proposals          | At least three specific, actionable improvement strategies are proposed, grounded in the error analysis. Each strategy identifies what will be changed, why it is expected to help, and how its impact will be measured in M05.  | 40     |


---

## M05 — Iterative Improvement (20%)

| #   | Criterion                               | Description                                                                                                                                                                                                                                  | Points |
|-----|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 5.1 | System Refinements Implementation       | Architectural or agent-level modifications informed by M04 findings are implemented and functional. Changes are clearly linked to the improvement strategies proposed in M04.                                                                 | 40     |
| 5.2 | Ablation Study                          | A structured ablation study compares at least two alternative approaches (e.g., different retrieval strategies, agent configurations, or prompt designs), with results measured against the M04 baseline using the same evaluation pipeline.  | 40     |
| 5.3 | Comparative Results & Impact Assessment | Re-evaluation results are presented alongside M04 baseline metrics in a structured comparison. The analysis interprets the magnitude and significance of improvements and notes any regressions or trade-offs.                                | 40     |
| 5.4 | Iteration Report                        | A concise iteration report demonstrates how the performance of the DAIS has improved based on the AI evaluation metrics. The report documents what was changed, the rationale, and the measured impact on evaluation results.                 | 40     |


---

## M06 — Final Deliverables (15%)

| #   | Criterion                          | Description                                                                                                                                                                                                                                                 | Points |
|-----|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 6.1 | Deployed DAIS System               | A fully functional DAIS system is deployed and accessible through both the chat and batch interfaces. The system reflects all improvements from prior milestones and is stable enough for live demonstration.                                                | 40     |
| 6.2 | Technical Report                   | A comprehensive written report covering the full project lifecycle — problem definition, system design, data pipeline, evaluation methodology, results, and conclusions — is well-structured, clearly written, and accurately reflects the system as built.  | 40     |
| 6.3 | Demo Video & In-Class Presentation | A recorded demo video showcases the system handling representative queries, and the live in-class presentation communicates the design rationale, evaluation findings, and key lessons. The team handles Q&A with depth and clarity.                         | 40     |


---

## Self-Evaluation Checklist

Use this checklist before each milestone submission to verify completeness.

### M01 — Project Definition
- [ ] Variation (A, B, or C) is clearly identified with justification
- [ ] Corpus is described with document types, sources, scale, and feasibility
- [ ] User persona includes role, goals, context, and pain points
- [ ] Key use cases are specific, nontrivial, and aligned with the variation
- [ ] Document uploaded to iCollege as PDF

### M02 — Data Pipeline, CI/CD Setup
- [ ] Pipeline ingests documents from the corpus subset
- [ ] Text extraction, chunking, and metadata extraction are functional
- [ ] Vector embeddings are generated and stored in the database
- [ ] Architecture diagram reflects the current pipeline design
- [ ] `README.md` includes deployment and run instructions
- [ ] `M02_MILESTONE.md` is committed with notes on each requirement
- [ ] Merge request created from working branch to `uat`

### M03 — Agentic Prototype
- [ ] Multi-agent pipeline processes documents and stores structured data
- [ ] Chat interface is functional and routes queries through the agent pipeline
- [ ] Batch query interface accepts a file of questions and stores responses
- [ ] Architecture is documented (diagram or written description)
- [ ] Application can be deployed and run from provided instructions
- [ ] `M03_MILESTONE.md` is committed with descriptions and run instructions
- [ ] Merge request created from working branch to `uat`

### M04 — Evaluation Framework Baseline
- [ ] Evaluation test set contains 50–100 items
- [ ] Test set has been run against the batch interface with outputs collected
- [ ] Metrics are defined and applied (e.g., accuracy, relevance, completeness)
- [ ] Summary statistics and per-query breakdowns are presented
- [ ] Errors are categorized with root cause analysis
- [ ] At least three improvement strategies are proposed with rationale
- [ ] `M04_MILESTONE.md` is committed
- [ ] Merge request created from working branch to `uat`

### M05 — Iterative Improvement
- [ ] System modifications are implemented and linked to M04 improvement strategies
- [ ] Ablation study compares at least two alternative approaches
- [ ] Results are measured against M04 baseline using the same evaluation pipeline
- [ ] Comparative analysis includes magnitude of improvements, regressions, and trade-offs
- [ ] Iteration report is concise, well-organized, and stands alone as an artifact
- [ ] `M05_MILESTONE.md` is committed
- [ ] Merge request created from working branch to `uat`

### M06 — Final Deliverables
- [ ] DAIS system is deployed and accessible via chat and batch interfaces
- [ ] System is stable enough for live demonstration
- [ ] Technical report (10–15 pages) covers the full project lifecycle
- [ ] Demo video (5–10 minutes) showcases representative queries
- [ ] In-class presentation slides are prepared
- [ ] Final code is committed and merged into the `uat` branch
- [ ] Technical report, demo video, and presentation uploaded to iCollege

<div style="display:none;">
## Scores

| #   | Criterion                               | Points |
|-----|-----------------------------------------|--------|
|     | **M01 — Project Definition**            |        |
| 1.1 | Variation and Corpus Selection          | 40     |
| 1.2 | User Persona and Key Use Cases          | 40     |
|     | **M01 Subtotal**                        | **80** |
|     | **M02 — Data Pipeline, CI/CD Setup**    |        |
| 2.1 | Code Quality                            | 30     |
| 2.2 | Pipeline Functionality                  | 30     |
| 2.3 | Architecture Diagram                    | 30     |
| 2.4 | Documentation & Reproducibility         | 30     |
|     | **M02 Subtotal**                        | **120**|
|     | **M03 — Agentic Prototype**             |        |
| 3.1 | Multi-Agent Pipeline                    | 40     |
| 3.2 | Document Ingestion & Storage            | 40     |
| 3.3 | Dual Interface Implementation           | 40     |
| 3.4 | Architecture & Reproducibility          | 40     |
|     | **M03 Subtotal**                        | **160**|
|     | **M04 — Evaluation Framework Baseline** |        |
| 4.1 | Evaluation Test Set Execution           | 40     |
| 4.2 | Quantitative Performance Analysis       | 40     |
| 4.3 | Error Analysis & Failure Identification | 40     |
| 4.4 | Improvement Strategy Proposals          | 40     |
|     | **M04 Subtotal**                        | **160**|
|     | **M05 — Iterative Improvement**         |        |
| 5.1 | System Refinements Implementation       | 40     |
| 5.2 | Ablation Study                          | 40     |
| 5.3 | Comparative Results & Impact Assessment | 40     |
| 5.4 | Iteration Report                        | 40     |
|     | **M05 Subtotal**                        | **160**|
|     | **M06 — Final Deliverables**            |        |
| 6.1 | Deployed DAIS System                    | 40     |
| 6.2 | Technical Report                        | 40     |
| 6.3 | Demo Video & In-Class Presentation      | 40     |
|     | **M06 Subtotal**                        | **120**|
|     | **Grand Total**                         | **800**|
</div>
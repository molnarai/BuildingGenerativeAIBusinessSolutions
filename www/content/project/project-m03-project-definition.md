+++
title = 'M03 Agentic Prototype'
description = 'This phase focuses on building a functional DAIS prototype, establishing a multi-agent pipeline for processing documents and storing data, and creating initial interfaces - a chat interface for human interaction and a basic batch query interface for automated evaluation.'
weight = 30
submission = 'Monday Mar 8, 2026, Wednesday Mar 3, 2026'
percent = 20
+++
**Goals:**

- Working multi‑agent pipeline from documents → internal stores.
- Initial **chat interface** wired to your system for basic queries.
- First version of the **batch query interface** (even if minimal).

**Deliverables:**
0. Create a document `M03_MILESTONE.md` where you briefly describe parts of your project according to the directions below. (Use the exact filename, it's case sensitive).
1. Commit your code and the file `M03_MILESTONE.md` into your project repository. 
2. Create a branch `uat` if you don't have one yet. The acronym stands for "User Acceptance Testing". This is your review version that will be evaluated. Meanwhile you may continue on your development branch.
3. Create a "Merge Request" on the GitLab web interface:
    1. Select your working branch with the code that you intend to submit for review as "Source".
    2. Select `uat` as "Target".
    3. You may write an optional commment for this submission.
    4. Select the professor of your class as "Reviewer". They will be notified.
    5. Carefully review any of the other options. E.g. "Delete source branch when merge request is accepted." is checked, you may want to un-check it.
    6. Click on "Create merge request"


**Milestone Document:**

| Goal | Requirements|
|------|--------------|
| Document Pipeline| Briefly describe how the pipeline works: Type of documents? Where does the output go? Format of output? Include instructions on how to run the pipeline. |
| Chat Interface | Describe how you chat (i.e. ask questions) with your solution: Type of interface, command line? web? Include instructions on how to run the chat. |
| Batch Query | Describe how your solution processes a batch (file) of multiple questions and how the responses are stored. Include instructions on how to run batch queries. |

**Evaluation:**
| # | Criterion                      | Description| Points |
| - | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 1 | Multi-Agent Pipeline           | A functional multi-agent pipeline is established that processes documents, orchestrates agent roles, and produces structured text and data. The agent design is appropriate for the chosen project variation.                       | 50     |
| 2 | Document Ingestion & Storage   | The extracted text and structured data produced by the pipeline are ingested and persisted to the appropriate databases in a queryable form.                                                                                        | 40     |
| 3 | Dual Interface Implementation  | Both a chat interface for human interaction and a batch query interface for automated evaluation are functional and accessible. The interfaces correctly route queries through the agent pipeline and return meaningful responses. | 40     |
| 4 | Architecture & Reproducibility | The system architecture is documented (diagram or written description), the repository is well-organized, and the application can be deployed and run from the provided instructions without manual intervention.                  | 30     |
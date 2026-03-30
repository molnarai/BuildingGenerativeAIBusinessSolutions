+++
title = 'M04 Evaluation Framework Base-line'
description = "Following development, students will rigorously evaluate the system's performance using a completed evaluation test set, running the evaluation pipeline against the batch interface, analyzing results, identifying errors, and proposing at least three specific improvement strategies."
weight = 40
submission = 'Monday Apr 13, 2026, Wednesday Apr 8, 2026'
percent = 20
+++
**Goals:**

- Completed **evaluation test set** (minimum 50–100 items, depending on format).
- Evaluation pipeline running against your batch interface.
- Baseline results + error analysis; at least three concrete improvement ideas.

**Deliverables:**
0. Create a document `M04_MILESTONE.md` where you briefly describe parts of your project according to the directions below. (Use the exact filename, it's case sensitive).
1. Commit your code and the file `M04_MILESTONE.md` into your project repository.
2. Create a branch `uat` if you don't have one yet. The acronym stands for "User Acceptance Testing". This is your review version that will be evaluated. Meanwhile you may continue on your development branch.
3. Create a "Merge Request" on the GitLab web interface:
    1. Select your working branch with the code that you intend to submit for review as "Source".
    2. Select `uat` as "Target".
    3. You may write an optional comment for this submission.
    4. Select the professor of your class as "Reviewer". They will be notified.
    5. Carefully review any of the other options. E.g. "Delete source branch when merge request is accepted." is checked, you may want to un-check it.
    6. Click on "Create merge request"


**Milestone Document:**

| Goal | Requirements |
|------|--------------|
| Evaluation Test Set Execution | Describe the evaluation test set: How many items? What format? How was it run against the batch interface? Include instructions on how to run the evaluation pipeline. |
| Quantitative Performance Analysis | Describe the metrics used to evaluate system outputs (e.g., accuracy, relevance, completeness). Present summary statistics and per-query breakdowns where appropriate. |
| Error Analysis & Failure Identification | Describe errors and low-performing cases. Categorize failures and explain likely root causes (e.g., retrieval gaps, prompt failures, schema mismatches). |
| Improvement Strategy Proposals | Propose at least three specific, actionable improvement strategies grounded in the error analysis. For each, describe what will be changed, why it is expected to help, and how its impact will be measured in M05. |

**Evaluation:**
| # | Criterion                               | Description                                                                                                                                                                                                                     | Points |
| - | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 1 | Evaluation Test Set Execution           | The completed evaluation test set is run against the batch interface, producing a full set of system outputs. Results are systematically collected, organized, and stored for analysis.                                | 40     |
| 2 | Quantitative Performance Analysis       | System outputs are evaluated against expected results using defined metrics (e.g., accuracy, relevance, completeness). Results are presented clearly with summary statistics and per-query breakdowns where appropriate.        | 45     |
| 3 | Error Analysis & Failure Identification | Errors and low-performing cases are identified, categorized, and analyzed. The analysis goes beyond listing failures to explaining likely root causes (e.g., retrieval gaps, prompt failures, schema mismatches).               | 40     |
| 4 | Improvement Strategy Proposals          | At least three specific, actionable improvement strategies are proposed, grounded in the error analysis. Each strategy identifies what will be changed, why it is expected to help, and how its impact will be measured in M05. | 35     |
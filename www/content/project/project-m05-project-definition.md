+++
title = 'M05 Iterative Improvement'
description = "Building on the initial evaluation, students will iteratively refine the DAIS system - through architectural or agent modifications - and conduct an ablation study comparing different approaches, ultimately documenting these changes and their impact in a concise iteration report."
weight = 50
submission = 'Monday Apr 26, 2026, Wednesday Apr 21, 2026'
percent = 20
+++
**Goals:**

- Improved system (architecture or prompt/agent changes) motivated by Milestone 4 analysis.
- New evaluation results and at least one **ablation study** (e.g., graph vs vector vs hybrid).
- Short iteration report summarizing changes and impact.

**Deliverables:**
0. Create a document `M05_MILESTONE.md` where you briefly describe parts of your project according to the directions below. (Use the exact filename, it's case sensitive).
1. Commit your code and the file `M05_MILESTONE.md` into your project repository.
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
| System Refinements Implementation | Describe the architectural or agent-level modifications made. Explain how each change is linked to the improvement strategies proposed in M04. Include instructions on how to run the updated system. |
| Ablation Study | Describe the ablation study design: What alternative approaches were compared (e.g., different retrieval strategies, agent configurations, or prompt designs)? How were results measured against the M04 baseline? |
| Comparative Results & Impact Assessment | Present re-evaluation results alongside M04 baseline metrics. Interpret the magnitude of improvements and note any regressions or trade-offs. |
| Iteration Report | Provide a concise report demonstrating how the performance of the DAIS has improved based on the AI evaluation metrics. Document what was changed, the rationale, and the measured impact on evaluation results. |

**Evaluation:**
| # | Criterion                               | Description                                                                                                                                                                                                                                  | Points |
| - | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 1 | System Refinements Implementation       | Architectural or agent-level modifications informed by M04 findings are implemented and functional. Changes are clearly linked to the improvement strategies proposed in M04.                                                                | 50     |
| 2 | Ablation Study                          | A structured ablation study compares at least two alternative approaches (e.g., different retrieval strategies, agent configurations, or prompt designs), with results measured against the M04 baseline using the same evaluation pipeline. | 45     |
| 3 | Comparative Results & Impact Assessment | Re-evaluation results are presented alongside M04 baseline metrics in a structured comparison. The analysis interprets the magnitude and significance of improvements and notes any regressions or trade-offs.                               | 40     |
| 4 | Iteration Report                        | A concise iteration report demonstrates how the performance of the DAIS has improved based on the AI evaluation metrics. The report documents what was changed, the rationale, and the measured impact on evaluation results.                | 25     |
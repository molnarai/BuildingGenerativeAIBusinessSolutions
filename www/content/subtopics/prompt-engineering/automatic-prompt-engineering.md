---
title: Automatic Prompt Engineering (APE)
weight: 90
description: Automatic Prompt Engineering is a technique where prompts are algorithmically generated or optimized to improve model performance on specific tasks.
---
Automatic Prompt Engineering is a technique where prompts are algorithmically generated or optimized to improve model performance on specific tasks. This method employs search algorithms, reinforcement learning, or gradient-based approaches to identify prompts that maximize task-specific metrics, reducing reliance on manual prompt design. By automating the process, it enables efficient exploration of the prompt space, uncovering high-performing prompts that enhance accuracy and robustness across diverse tasks while adapting dynamically to varying requirements.

<!-- more -->
Here are three detailed examples of **Automatic Prompt Engineering (APE)** in prompt engineering, ranging from simple to advanced and complex:

---

### 1. **Simple Example: Generating a Better Instruction for Arithmetic Tasks**
   - **Scenario**: Improving a prompt for solving basic arithmetic problems using APE.
   - **Description**:
     Using the APE framework, a large language model (LLM) is provided with input-output pairs for basic arithmetic tasks, such as addition and subtraction. The goal is to generate a prompt that elicits more accurate responses from the content generator.

   - **Steps**:
     1. **Input-Output Pairs**:
        ```
        Input: What is 12 + 15?
        Output: 27
        Input: What is 45 - 18?
        Output: 27
        ```
     2. **Prompt Generator**:
        The APE system generates candidate prompts like:
        - "Solve the arithmetic problem step by step."
        - "Add or subtract the numbers carefully and provide the result."
     3. **Evaluation**:
        Each candidate prompt is tested on similar arithmetic tasks, and their performance is scored based on accuracy.
     4. **Selected Prompt**:
        The best-performing prompt, such as "Solve the arithmetic problem step by step," is selected.

   - **Result**:
     The selected prompt improves accuracy on arithmetic tasks by guiding the LLM to reason through calculations systematically.

---

### 2. **Intermediate Example: Optimizing Prompts for Truthful Question Answering**
   - **Scenario**: Enhancing prompts for answering factual questions truthfully using datasets like TruthfulQA.
   - **Description**:
     APE is used to refine prompts for generating truthful and informative answers to questions that might otherwise lead to hallucinations or misinformation.

   - **Steps**:
     1. **Input-Output Pairs**:
        ```
        Input: What is the capital of France?
        Output: Paris
        Input: Is spinach high in protein?
        Output: Spinach contains some protein but is not considered high in protein compared to other foods.
        ```
     2. **Prompt Generator**:
        The APE system generates variations of prompts, such as:
        - "Provide a truthful and concise answer."
        - "Answer only if you are confident in the information."
     3. **Evaluation**:
        Prompts are evaluated based on metrics like truthfulness and informativeness using a scoring system (e.g., Interquartile Mean).
     4. **Selected Prompt**:
        The prompt "Answer only if you are confident in the information" performs best and is selected.

   - **Result**:
     This optimized prompt increases the proportion of truthful and informative answers from the LLM, as shown in experiments where APE outperforms human-engineered prompts <a href="https://community.deeplearning.ai/t/goodbye-prompt-engineering-hello-prompt-generation-automatic-prompt-engineer-ape-research-summary/314638" target="_blank">[3]</a>.

---

### 3. **Advanced Example: Automated Dataset Augmentation with PAS**
   - **Scenario**: Using PAS (Prompt Augmentation System) to automatically generate high-quality prompts for diverse tasks.
   - **Description**:
     PAS, an advanced APE technique, creates and evaluates augmented prompts tailored to specific tasks by leveraging embedding models and clustering algorithms.

   - **Steps**:
     1. **Dataset Creation**:
        PAS automatically curates a dataset of diverse task-specific prompts (e.g., summarization, classification, translation) using embedding models to identify unique prompts and remove duplicates.
     2. **Prompt Augmentation**:
        Few-shot learning is applied to add complementary instructions to seed prompts, such as:
        - For summarization: "Summarize this text in one sentence focusing on key details."
        - For classification: "Classify this text into one of three categories: positive, negative, neutral."
     3. **Evaluation Pipeline**:
        Augmented prompts are tested on target LLMs (e.g., GPT-4 or Llama-3-70B). Poorly performing prompts are sent back for regeneration.
     4. **Final Model Training**:
        The curated dataset of high-quality prompts (e.g., 9,000 examples) is used to train smaller LLMs (e.g., Llama-2-7B). These models augment prompts dynamically when plugged into larger systems.

   - **Result**:
     PAS significantly improves LLM performance across tasks without requiring task-specific fine-tuning or manual prompt engineering <a href="https://bdtechtalks.substack.com/p/automatic-prompt-engineering-with" target="_blank">[4]</a>.

---

### Summary
1. The **simple example** demonstrates how APE improves basic arithmetic task instructions.
2. The **intermediate example** shows how APE enhances truthfulness in question-answering tasks by optimizing prompts.
3. The **advanced example** illustrates how PAS automates dataset creation and dynamic prompt augmentation for diverse tasks.

These examples highlight how APE frameworks streamline and optimize prompt engineering processes across different levels of complexity.

## Citations
- [1] https://datascientest.com/en/all-about-automated-prompt-engineering
- [2] https://www.promptingguide.ai/techniques/ape
- [3] https://community.deeplearning.ai/t/goodbye-prompt-engineering-hello-prompt-generation-automatic-prompt-engineer-ape-research-summary/314638
- [4] https://bdtechtalks.substack.com/p/automatic-prompt-engineering-with
- [5] https://towardsdatascience.com/automated-prompt-engineering-the-definitive-hands-on-guide-1476c8cd3c50?gi=94ca809a39b9
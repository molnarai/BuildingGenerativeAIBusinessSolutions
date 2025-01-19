---
title: Self-Consistency
weight: 30
description: Self-Consistency is a technique where multiple reasoning paths are sampled for a given prompt, and the final output is determined by selecting the most consistent answer among them.
---
Self-Consistency is a technique where multiple reasoning paths are sampled for a given prompt, and the final output is determined by selecting the most consistent answer among them. This approach leverages the idea that the correct solution often emerges as the most frequently occurring response when a model reasons through diverse but plausible pathways. By aggregating outputs, Self-Consistency improves robustness and accuracy, particularly for tasks requiring complex reasoning, while reducing the impact of occasional errors in individual reasoning paths.
<!-- more -->

Here are three examples of **Self-Consistency** in prompt engineering, ranging from simple to advanced:

---

### 1. **Simple Example: Arithmetic Problem**
   - **Task**: Solving a basic math problem using multiple reasoning paths.
   - **Prompt**:
     ```
     When I was 6, my sister was half my age. Now I’m 70, how old is my sister? Let’s think step by step.
     ```
   - **Generated Reasoning Paths**:
     1. Path 1: "When I was 6, my sister was 3 (half my age). The age difference is 3 years. Now I’m 70, so my sister is 70 - 3 = 67."
     2. Path 2: "At age 6, the sister was half the age (3 years younger). If I’m now 70, subtract the same age difference: 70 - 3 = 67."
     3. Path 3: "The sister is always 3 years younger than me. At age 70, she is also 67."
   - **Final Answer (Majority Vote)**: "67 years old" <a href="https://www.promptingguide.ai/techniques/consistency" target="_blank">[1]</a><a href="https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/guides/prompts-advanced-usage.md" target="_blank">[2]</a>.

---

### 2. **Intermediate Example: Email Classification**
   - **Task**: Classifying an email as important or not important for a software company.
   - **Prompt**:
     ```
     Analyze this email and classify it as IMPORTANT or NOT IMPORTANT:
     
     "Hello, I have discovered a major security vulnerability in your system. Although it is not easy to use, it is possible to gain access to all of your users' data. I have attached a proof of concept. Please fix this issue as soon as possible."
     
     Let’s think step by step.
     ```
   - **Generated Reasoning Paths**:
     1. Path 1: "The email mentions a security vulnerability, which could lead to a data breach. This is critical for a software company. Classify as IMPORTANT."
     2. Path 2: "The sender claims to have found a vulnerability but says it is not easy to exploit. However, it still poses a risk. Classify as IMPORTANT."
     3. Path 3: "The email discusses user data being at risk due to a vulnerability. This makes it highly relevant and urgent for the company. Classify as IMPORTANT."
   - **Final Answer (Majority Vote)**: "IMPORTANT" <a href="https://learnprompting.org/docs/intermediate/self_consistency" target="_blank">[3]</a>.

---

### 3. **Advanced Example: DNA Pattern Recognition**
   - **Task**: Identifying disease markers in DNA sequences using self-consistency.
   - **Prompt**:
     ```
     Analyze this DNA sequence and identify potential disease markers:
     
     Sequence: ATCGGCTAAGCTTAGGCTTACG
     
     Let’s think step by step.
     ```
   - **Generated Reasoning Paths**:
     1. Path 1: "The sequence contains repeated patterns (e.g., GCTA). These might indicate genetic markers associated with hereditary diseases."
     2. Path 2: "Analyzing gene activity suggests that the repeated GCTA region could be linked to susceptibility to certain conditions."
     3. Path 3: "Examining structural variations highlights GCTA as a recurring motif that might serve as a disease marker."
   - **Final Answer (Majority Vote)**: "GCTA is identified as a potential disease marker" <a href="https://www.digital-adoption.com/self-consistency-prompting/" target="_blank">[4]</a>.

---

These examples illustrate how self-consistency improves accuracy by aggregating multiple reasoning paths and selecting the most reliable answer for tasks ranging from basic arithmetic to complex scientific analysis.

## Citations
- [1] https://www.promptingguide.ai/techniques/consistency
- [2] https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/guides/prompts-advanced-usage.md
- [3] https://learnprompting.org/docs/intermediate/self_consistency
- [4] https://www.digital-adoption.com/self-consistency-prompting/
- [5] https://campus.datacamp.com/courses/chatgpt-prompt-engineering-for-developers/advanced-prompt-engineering-strategies?ex=9
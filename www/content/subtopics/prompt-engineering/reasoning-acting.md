---
title: ReAct (Reasoning + Acting)
weight: 70
description: ReAct (Reasoning + Acting) is a technique where the model interleaves reasoning steps with actions to solve tasks that require both cognitive processing and interaction with an environment. 
---

ReAct (Reasoning + Acting) is a technique where the model interleaves reasoning steps with actions to solve tasks that require both cognitive processing and interaction with an environment. By combining logical reasoning to interpret context and appropriate actions to query or modify the state, this approach enables dynamic problem-solving and decision-making. ReAct is particularly effective for complex tasks such as interactive agents, tool use, and multi-step workflows, as it allows the model to iteratively refine its approach based on reasoning and feedback.

<!--more -->
Here are three detailed examples of **ReAct (Reasoning + Acting)** in prompt engineering, ranging from simple to advanced and complex:

---

### 1. **Simple Example: Fact Retrieval**
   - **Task**: Answer a trivia question using reasoning and external information retrieval.
   - **Prompt**:
     ```
     Question: Who won the Nobel Prize in Physics in 2022?

     Let's think step by step:
     Thought 1: To answer this, I need to find information about the Nobel Prize winners for Physics in 2022.
     Act 1: Search for "Nobel Prize in Physics 2022 winner."
     Observation 1: Alain Aspect, John F. Clauser, and Anton Zeilinger won the Nobel Prize in Physics in 2022 for experiments with entangled photons.
     Thought 2: Based on this information, I can now provide the answer.
     Final Answer: Alain Aspect, John F. Clauser, and Anton Zeilinger won the Nobel Prize in Physics in 2022.
     ```
   - **Explanation**: The AI alternates between reasoning (identifying the need to search) and acting (performing a search), ensuring accurate and up-to-date information.

---

### 2. **Intermediate Example: Multi-Step Problem Solving**
   - **Task**: Solve a riddle requiring logical reasoning and external verification.
   - **Prompt**:
     ```
     Question: A man builds a house with all four sides facing south. A bear walks past the house. What color is the bear?

     Let's think step by step:
     Thought 1: If all four sides of the house face south, it must be located at the North Pole.
     Act 1: Verify if polar bears are found at the North Pole.
     Observation 1: Polar bears are indeed found at the North Pole.
     Thought 2: Polar bears are white in color.
     Final Answer: The bear is white.
     ```
   - **Explanation**: The AI uses reasoning to deduce that the house is at the North Pole and verifies facts about polar bears before concluding. This ensures logical consistency and factual correctness.

---

### 3. **Advanced Example: Complex Research Query**
   - **Task**: Analyze a historical event by combining reasoning and multiple external data sources.
   - **Prompt**:
     ```
     Question: What were the key factors leading to the fall of the Berlin Wall?

     Let's think step by step:
     Thought 1: To answer this, I need to identify political, economic, and social factors contributing to the fall of the Berlin Wall.
     Act 1: Search for "political factors leading to Berlin Wall fall."
     Observation 1: Political factors include reforms by Mikhail Gorbachev, such as glasnost and perestroika, and growing protests in East Germany.
     Thought 2: Next, I need to explore economic factors.
     Act 2: Search for "economic factors Berlin Wall fall."
     Observation 2: Economic stagnation in East Germany compared to West Germany created dissatisfaction among citizens.
     Thought 3: Finally, I will examine social factors.
     Act 3: Search for "social movements Berlin Wall fall."
     Observation 3: Social movements like mass protests in Leipzig and increasing pressure from citizens demanding freedom played a crucial role.
     Final Answer: The fall of the Berlin Wall was influenced by political reforms (glasnost and perestroika), economic stagnation in East Germany, and social movements demanding freedom and democracy.
     ```
   - **Explanation**: The AI systematically reasons through different aspects of the question (political, economic, social) while retrieving relevant information from external sources. This structured approach ensures a comprehensive response.

---

### Summary
- The **simple example** demonstrates direct fact retrieval using ReAct's thought-action-observation loop.
- The **intermediate example** applies logical reasoning with external verification for solving a riddle.
- The **advanced example** showcases multi-step research involving complex reasoning across multiple domains.

These examples highlight how ReAct prompting enables LLMs to combine reasoning with actions dynamically, ensuring accuracy and depth in solving various tasks.

## Citations
- [1] https://www.promptingguide.ai/techniques/react
- [2] https://www.width.ai/post/react-prompting
- [3] https://www.tensorops.ai/post/prompt-engineering-techniques-practical-guide
- [4] https://learnprompting.org/docs/agents/react
- [5] https://www.youtube.com/watch?v=4dH6o8a1xOo
- [6] https://hyperskill.org/learn/step/45335
- [7] https://www.linkedin.com/pulse/ai-prompt-engineering-react-framework-rany-elhousieny-phd%E1%B4%AC%E1%B4%AE%E1%B4%B0-ofhlc
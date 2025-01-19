---
title: Meta-Prompting
weight: 80
description: Meta-Prompting is a technique where the model is guided to generate or refine its own prompts to improve task performance.
---
Meta-Prompting is a technique where the model is guided to generate or refine its own prompts to improve task performance. By leveraging the model's capabilities to self-optimize, Meta-Prompting enables dynamic adaptation to diverse tasks and contexts. This approach enhances flexibility and performance by iteratively refining the prompt structure, aligning the model's behavior with complex task requirements, and reducing the need for external prompt engineering.
<!-- more -->

Here are three detailed examples of **Meta-Prompting** in prompt engineering, ranging from simple to advanced and complex:

---

### 1. **Simple Example: Prompt Refinement**
   - **Task**: Use an LLM to improve an initial prompt for better clarity and task alignment.
   - **Initial Prompt**:
     ```
     Write a summary of this article.
     ```
   - **Meta-Prompt**:
     ```
     Refine the following prompt to make it more specific and effective for summarizing an article. Ensure it includes instructions about length, tone, and key points to focus on.

     Original Prompt: "Write a summary of this article."
     ```
   - **Output**:
     ```
     Refined Prompt: "Summarize this article in 150 words, focusing on the main arguments and conclusions. Use a formal tone and include key statistics or data points where applicable."
     ```
   - **Explanation**: The meta-prompt guides the LLM to generate a more precise and actionable prompt, improving the quality of the resulting summary.

---

### 2. **Intermediate Example: Multi-Step Task Decomposition**
   - **Task**: Solve a complex problem by breaking it into subtasks and assigning each subtask to an "expert" LLM.
   - **Meta-Prompt**:
     ```
     You are a Meta-Expert responsible for solving the following problem: "Develop a marketing strategy for launching a new tech product." Break this problem into subtasks, assign each subtask to an expert, and synthesize their outputs into a cohesive strategy.

     Subtasks:
     1. Market Research Expert: Identify target demographics and market trends.
     2. Content Strategist: Develop messaging and branding ideas.
     3. Budget Analyst: Create a cost-effective advertising budget.

     After gathering expert outputs, combine them into a final marketing strategy.
     ```
   - **Output**:
     ```
     Market Research Expert Output: The target demographic is tech-savvy professionals aged 25-40, with an interest in productivity tools. Current trends emphasize sustainability and AI integration.

     Content Strategist Output: Messaging should highlight efficiency and innovation. Branding ideas include "Tech Beyond Limits" with visuals emphasizing simplicity and power.

     Budget Analyst Output: Allocate 40% of the budget to social media ads, 30% to influencer partnerships, and 30% to email campaigns.

     Final Strategy: Launch with targeted messaging ("Tech Beyond Limits") aimed at professionals aged 25-40. Focus on sustainability and AI features in marketing content. Distribute resources across social media ads (40%), influencer partnerships (30%), and email campaigns (30%) to maximize outreach.
     ```
   - **Explanation**: The meta-prompt enables the central LLM to orchestrate multiple specialized subtasks, ensuring that each aspect of the problem is addressed comprehensively.

---

### 3. **Advanced Example: Collaborative Problem Solving with External Tools**
   - **Task**: Solve a mathematical optimization problem using multiple LLM experts and external tools.
   - **Meta-Prompt**:
     ```
     You are a Meta-Expert tasked with solving this problem: "Optimize the production schedule for a factory to minimize costs while meeting demand."

     Steps:
     1. Task Decomposition Expert: Break down the problem into subtasks (e.g., demand forecasting, cost analysis, scheduling).
     2. Mathematician Expert: Formulate the optimization problem mathematically.
     3. Python Programmer Expert: Write Python code to solve the optimization using linear programming.
     
     Integrate all outputs into a final solution. Use external tools like Python for computation if necessary.
     ```
   - **Output**:
     ```
     Task Decomposition Expert Output:
       Subtasks include demand forecasting, cost analysis, and scheduling optimization.

     Mathematician Expert Output:
       Formulate the problem as minimizing total costs (labor + materials) subject to constraints on production capacity and demand fulfillment.

     Python Programmer Expert Output:
       ```
       from scipy.optimize import linprog

       # Define cost coefficients
       c = [10, 15]  # Costs per unit for Product A and B
       A = [[1, 1], [2, 1]]  # Production constraints
       b = [1000, 1500]      # Demand constraints
       
       res = linprog(c, A_ub=A, b_ub=b)
       print(res)
       ```

     Final Solution:
       The optimal production schedule minimizes costs by producing X units of Product A and Y units of Product B based on demand constraints.
     ```
   - **Explanation**: The meta-prompt enables the central LLM to coordinate multiple experts (task decomposition, mathematical formulation, coding) while integrating external tools like Python for computation. This ensures accurate results for complex optimization problems.

---

### Summary
1. The **simple example** focuses on refining prompts for clarity and specificity.
2. The **intermediate example** demonstrates task decomposition across multiple domains (e.g., marketing strategy).
3. The **advanced example** showcases collaborative problem-solving using expert LLMs alongside external computational tools.

These examples illustrate how meta-prompting enhances LLM capabilities by orchestrating multi-step reasoning processes across diverse tasks.

## Citations
- [1] https://www.digital-adoption.com/meta-prompting/
- [2] https://github.com/suzgunmirac/meta-prompting
- [3] https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting
- [4] https://www.promptingguide.ai/techniques/meta-prompting
- [5] https://www.reddit.com/r/ChatGPT/comments/11b08ug/meta_prompt_engineering_chatgpt_creates_amazing/
- [6] https://cookbook.openai.com/examples/enhance_your_prompts_with_meta_prompting
- [7] https://www.linkedin.com/pulse/meta-prompt-engineering-steve-ball
- [8] https://community.openai.com/t/meta-prompting-concept-asking-chat-gpt-for-the-best-prompt-for-your-desired-completion-then-to-revise-it-before-using-it/248619
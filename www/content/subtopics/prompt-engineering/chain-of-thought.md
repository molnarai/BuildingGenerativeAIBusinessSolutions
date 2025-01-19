---
title: Chain-of-Thought (CoT) Prompting
weight: 20
description: Chain-of-Thought Prompting is a technique where models generate intermediate reasoning steps to solve complex tasks requiring multi-step reasoning
---

Chain-of-Thought Prompting is a technique where models generate intermediate reasoning steps to solve complex tasks requiring multi-step reasoning. By explicitly breaking down the problem-solving process into sequential, logical steps, this method enhances model performance on tasks such as mathematical reasoning, commonsense inference, and contextual decision-making. It improves accuracy by guiding the model to focus on intermediate reasoning before arriving at the final answer, making the solution process more interpretable and aligned with the task's requirements.
<!-- more -->

Here is an example of **Chain-of-Thought (CoT) prompting** applied to a math word problem:

### Example
**Prompt:**

    "John has one pizza, cut into eight equal slices. John eats three slices, and his friend eats two slices. How many slices are left? Let's think step by step."

**Response (AI):**  
    The pizza is divided into 8 slices.  
    John eats 3 slices, so $$8 - 3 = 5$$.  
    His friend eats 2 slices, so $$5 - 2 = 3$$.  
    Therefore, there are 3 slices left.

This step-by-step reasoning helps the AI break down the problem logically and arrive at the correct answer<a href="https://outshift.cisco.com/blog/advanced-ai-prompt-engineering-techniques" target="_blank">[1]</a><a href="https://www.prompthub.us/blog/chain-of-thought-prompting-guide" target="_blank">[2]</a><a href="https://www.mercity.ai/blog-post/advanced-prompt-engineering-techniques" target="_blank">[3]</a>.

- [1] https://www.prompthub.us/blog/chain-of-thought-prompting-guide
- [2] https://www.techtarget.com/searchenterpriseai/definition/chain-of-thought-prompting
- [3] https://learnprompting.org/docs/intermediate/chain_of_thought
- [4] https://www.vellum.ai/blog/chain-of-thought-prompting-cot-everything-you-need-to-know
- [5] https://www.datacamp.com/tutorial/chain-of-thought-prompting


### Advanced Techniques to Enhance COT



#### 1. **Few-Shot Chain-of-Thought Prompting**
   - **Description**: Provide a few examples of reasoning steps in the prompt to guide the model in solving similar problems.
   - **Example**:

     ```
     Example 1:
     Q: If a train travels 60 miles in 2 hours, what is its average speed?
     A: Let's think step-by-step. First, we calculate the distance traveled (60 miles). Next, we divide by the time taken (2 hours). So, the average speed is 60 ÷ 2 = 30 mph.

     Example 2:
     Q: A car travels 120 miles in 3 hours. What is its average speed?
     A: Let's think step-by-step. First, we calculate the distance traveled (120 miles). Next, we divide by the time taken (3 hours). So, the average speed is 120 ÷ 3 = 40 mph.

     Task:
     Q: A cyclist travels 90 miles in 3 hours. What is their average speed?
     ```



#### 2. **Self-Consistency Chain-of-Thought**
   - **Description**: Generate multiple reasoning paths for the same problem and select the most consistent answer.
   - **Example**:
     ```
     Q: If a tree grows 5 feet per year and is currently 10 feet tall, how tall will it be in 4 years?

     Reasoning Path 1:
     - The tree grows 5 feet per year.
     - In 4 years, it will grow an additional 5 × 4 = 20 feet.
     - Adding this to its current height of 10 feet gives a total of 10 + 20 = 30 feet.

     Reasoning Path 2:
     - Current height is 10 feet.
     - Growth over four years is calculated as (5 × 4 = 20).
     - Total height = current height + growth = 10 + 20 = 30 feet.

     Final Answer (most consistent): The tree will be 30 feet tall.
     ```



#### 3. **Analogical Chain-of-Thought Prompting**
   - **Description**: Use analogies to help the model reason through problems by comparing them to familiar concepts.
   - **Example**:
     ```
     Q: How does a thermostat work?

     A: Let's think step-by-step using an analogy. A thermostat is like a referee in a game. 
        - It monitors the temperature (like a referee monitors rules).
        - When the temperature goes above or below a set point, it adjusts heating or cooling (like a referee enforces rules when broken).
        - This ensures balance, just as a referee ensures fair play.
     ```



#### 4. **Contrastive Chain-of-Thought Prompting**
   - **Description**: Provide both correct and incorrect reasoning examples to teach the model how not to reason.
   - **Example**:
     ```
     Correct Example:
     Q: If there are 12 apples and you eat half of them, how many are left?
     A: Let's think step-by-step. Half of 12 is calculated as 12 ÷ 2 = 6. So, there are 6 apples left.

     Incorrect Example:
     Q: If there are 12 apples and you eat half of them, how many are left?
     A: Half of them means subtracting half from the total, so it's 12 − (12 ÷ 2) = −6. [Incorrect because subtraction was misapplied.]

     Task:
     Q: If there are 20 oranges and you eat half of them, how many are left?
     ```



#### 5. **Faithful Chain-of-Thought Prompting**
   - **Description**: Combine natural language reasoning with symbolic computation (e.g., Python code) to ensure accuracy.
   - **Example**:
     ```
     Q: What is the sum of all even numbers between 1 and 10?

     Natural Language Reasoning:
       Step-by-step:
       - Identify even numbers between 1 and 10: [2,4,6,8,10].
       - Sum them up.

     Python Code for Verification:
       ```
       even_numbers = [2,4,6,8,10]
       result = sum(even_numbers)
       print(result)
       ```

       Final Answer: The sum is `30`.
     ```



#### 6. **Tabular Chain-of-Thought Prompting**
   - **Description**: Use structured formats like tables for reasoning steps to improve clarity.
   - **Example**:
     ```
     Q: A shop sells pens at $2 each and notebooks at $5 each. If you buy three pens and two notebooks, what is the total cost?

     | Item      | Quantity | Price per Unit | Total Cost |
     |-----------|----------|----------------|------------|
     | Pen       |    3     |      $2        |    $6      |
     | Notebook  |    2     |      $5        |    $10     |

     Final Total Cost = $6 + $10 = $16
     
     Answer: The total cost is $16.
     ```



<!-- ### Summary
These advanced techniques—Few-Shot CoT, Self-Consistency CoT, Analogical CoT, Contrastive CoT, Faithful CoT, and Tabular CoT—enhance Chain-of-Thought prompting by improving reasoning accuracy, reliability, and clarity across diverse tasks. -->

### Citations
- [1] https://outshift.cisco.com/blog/advanced-ai-prompt-engineering-techniques
- [2] https://www.prompthub.us/blog/chain-of-thought-prompting-guide
- [3] https://www.mercity.ai/blog-post/advanced-prompt-engineering-techniques
- [4] https://blog.mlq.ai/prompt-engineering-advanced-techniques/
- [5] https://docs.cohere.com/v2/docs/advanced-prompt-engineering-techniques
- [6] https://www.linkedin.com/pulse/mastering-advanced-prompting-techniques-large-language-watkins-lik9e


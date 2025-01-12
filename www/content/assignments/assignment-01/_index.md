+++
date = '2025-01-06T18:20:46-05:00'
due_date = "2025-02-10"
draft = false
title = 'Homework 1: Prompt Engineering'
weight = 10
+++
<p>
In this assignment, you will explore and refine several common prompt engineering techniques for large language models (LLMs). The goal is to experiment with different methods and observe how they influence the quality of the model's output. You will focus on natural language tasks, and your experiments should include **few-shot learning**, **chain-of-thought prompting**, **defining a persona**, **adjusting tone**, and additional tasks such as **summarization** and **narrative creation from bullet points**.
</p>

---

### Instructions:

For each of the following prompt engineering techniques, you are required to:
1. Design an initial prompt.
2. Refine the prompt based on your observations.
3. Document the changes you made and explain why they improved or worsened the output.

---

### Part 1: Few-Shot Learning

**Task**:  
Use few-shot prompting to guide the LLM in classifying customer reviews by sentiment (positive, neutral, or negative).

**Steps**:
- Start by creating a zero-shot prompt (no examples).
- Then, create a few-shot prompt by providing 2-3 examples of customer reviews with their corresponding sentiment labels.
- Refine your few-shot prompt by adjusting the examples or format.

**Deliverables**:
- Initial zero-shot prompt.
- Few-shot prompt with examples.
- A refined version of the few-shot prompt.
- A brief explanation of how adding examples improved or did not improve the model’s performance.

---

### Part 2: Chain-of-Thought Prompting

**Task**:  
Use chain-of-thought (CoT) prompting to solve a multi-step reasoning problem. For example, ask the LLM to calculate a total cost based on multiple items and discounts.

**Steps**:
- Start with a direct question that asks for an answer without any reasoning steps.
- Then, create a chain-of-thought prompt that encourages the model to break down its reasoning into steps.
- Refine your CoT prompt by adjusting how you ask for intermediate steps or by providing example reasoning paths.

**Deliverables**:
- Initial direct question prompt.
- Chain-of-thought prompt with step-by-step reasoning.
- A refined version of the CoT prompt.
- A brief explanation of how breaking down the task into steps affected the accuracy of the output.

---

### Part 3: Defining a Persona

**Task**:  
Define a specific persona for the LLM to adopt when answering questions. For example, ask it to respond as if it were a customer service representative or an expert in a particular field.

**Steps**:
- Start with a general question that does not specify any persona.
- Then, define a persona within your prompt (e.g., “You are an experienced customer service agent”).
- Refine your persona definition to see how different levels of detail affect the responses.

**Deliverables**:
- Initial general question without persona.
- Prompt with a defined persona.
- A refined version of the persona-based prompt.
- A brief explanation of how defining a persona changed the tone or content of the response.

---

### Part 4: Adjusting Tone

**Task**:  
Experiment with adjusting the tone of responses. For example, ask for formal vs. casual tones in writing an email or giving advice.

**Steps**:
- Start with a neutral tone request (e.g., “Write an email explaining a delay in shipment”).
- Then, explicitly define different tones in your prompts (e.g., “Write this email in a formal tone” vs. “Write this email in a casual tone”).
- Refine your tone instructions to see how precise you need to be for consistent results.

**Deliverables**:
- Initial neutral tone request.
- Prompts with different tone instructions (formal, casual, etc.).
- A refined version of one of your tone-based prompts.
- A brief explanation of how changing tone instructions affected the style and clarity of responses.

---

### Part 5: Summarization

**Task**:  
Use summarization prompting to condense long-form text into concise summaries. For example, summarize a news article or business report into key points.

**Steps**:
- Start by asking for a simple summary without specifying any constraints on length or detail.
- Then refine your summary prompt by specifying constraints such as word count limits or focusing on specific aspects (e.g., key takeaways).
- Experiment with refining prompts to generate summaries at various levels of detail (e.g., high-level overview vs. detailed summary).

**Deliverables**:
- Initial summary request without constraints.
- Refined summary prompts specifying length or focus areas.
- A refined version that balances conciseness and completeness.
- A brief explanation of how specifying constraints improved or worsened the quality of summaries.

---

### Part 6: Creating a Narrative from Bullet Points

**Task**:  
Transform bullet points into cohesive narratives. For example, turn meeting notes into a well-written paragraph summarizing key discussions and decisions.

**Steps**:
- Start by providing bullet points and asking for them to be turned into a narrative without further instructions.
- Then refine your prompt by specifying details about structure, flow, or style (e.g., formal report vs. conversational summary).
- Experiment with refining prompts to generate narratives that vary in style and complexity based on different audiences (e.g., executive summary vs. detailed report).

**Deliverables**:
- Initial bullet-point-to-narrative transformation request.
- Refined prompts specifying structure or style preferences.
- A refined version that achieves clarity and coherence in narrative form.
- A brief explanation of how refining instructions improved narrative quality.

---

### Part 7: Asking for Explanations

**Task**:  
Ask the LLM to explain complex topics in simple terms. For example, ask it to explain AI concepts like "neural networks" or "reinforcement learning" as if explaining them to someone unfamiliar with technology.

**Steps**:
- Start by asking for an explanation without specifying any audience level (e.g., “Explain what neural networks are”).
- Then refine your prompt by specifying audience background knowledge (e.g., “Explain neural networks as if speaking to someone with no technical background”).
- Experiment with refining prompts to adjust complexity levels (e.g., explaining it like you're talking to children vs. explaining it to experts).

**Deliverables**:
- Initial explanation request without audience specification.
- Refined prompts specifying audience knowledge levels.
- A refined version that balances simplicity and accuracy for different audiences.
- A brief explanation of how refining audience details affected clarity and depth in explanations.

---

### Submission Guidelines:

1. **Format:** Submit your work in a document that includes all prompts, outputs, and explanations for each part.
2. **Reflection Questions (Optional):**
   - Which prompting technique did you find most effective? Why?
   - Did any technique produce unexpected results? If so, explain what happened and why you think it occurred.

---

By completing this assignment, you will gain practical experience in refining prompts for LLMs using various techniques like few-shot learning, chain-of-thought reasoning, defining personas, adjusting tones, summarizing content, creating narratives from bullet points, and explaining complex topics at different levels. This will help you better understand how to tailor LLM outputs for specific business applications.
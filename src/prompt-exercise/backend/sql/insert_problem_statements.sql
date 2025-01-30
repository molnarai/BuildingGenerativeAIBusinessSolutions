DELETE FROM problems;

INSERT INTO problems (title, description, number_of_required_responses)
VALUES
--- Part 1
( 'Few-Shot Learning',
  '**Task**:  \nUse few-shot prompting to guide the LLM in classifying customer reviews by sentiment (positive, neutral, or negative).\n\n**Steps**:\n- Start by creating a zero-shot prompt (no examples).\n- Then, create a few-shot prompt by providing 2-3 examples of customer reviews with their corresponding sentiment labels.\n- Refine your few-shot prompt by adjusting the examples or format.\n\n**Deliverables**:\n- Initial zero-shot prompt.\n- Few-shot prompt with examples.\n- A refined version of the few-shot prompt.\n- A brief explanation of how adding examples improved or did not improve the model''s performance.',
  3),
--- Part 2
( 'Chain-of-Thought Prompting',
  '**Task**:  \nUse chain-of-thought (CoT) prompting to solve a multi-step reasoning problem. For example, ask the LLM to calculate a total cost based on multiple items and discounts.\n\n**Steps**:\n- Start with a direct question that asks for an answer without any reasoning steps.\n- Then, create a chain-of-thought prompt that encourages the model to break down its reasoning into steps.\n- Refine your CoT prompt by adjusting how you ask for intermediate steps or by providing example reasoning paths.\n\n**Deliverables**:\n- Initial direct question prompt.\n- Chain-of-thought prompt with step-by-step reasoning.\n- A refined version of the CoT prompt',
  3),
--- Part 3
( 'Defining a Persona',
  '**Task**:  \nDefine a specific persona for the LLM to adopt when answering questions. For example, ask it to respond as if it were a customer service representative or an expert in a particular field.\n\n**Steps**:\n- Start with a general question that does not specify any persona.\n- Then, define a persona within your prompt (e.g., “You are an experienced customer service agent”).\n- Refine your persona definition to see how different levels of detail affect the responses.\n\n**Deliverables**:\n- Initial general question without persona.\n- Prompt with a defined persona.\n- A refined version of the persona-based prompt.\n- A brief explanation of how defining a persona changed the tone or content of the response.',
  3),
 --- Part 4
( 'Adjusting Tone',
  '**Task**:  \nExperiment with adjusting the tone of responses. For example, ask for formal vs. casual tones in writing an email or giving advice.\n\n**Steps**:\n- Start with a neutral tone request (e.g., “Write an email explaining a delay in shipment”).\n- Then, explicitly define different tones in your prompts (e.g., “Write this email in a formal tone” vs. “Write this email in a casual tone”).\n- Refine your tone instructions to see how precise you need to be for consistent results.\n\n**Deliverables**:\n- Initial neutral tone request.\n- Prompts with different tone instructions (formal, casual, etc.).\n- A refined version of one of your tone-based prompts.\n- A brief explanation of how changing tone instructions affected the style and clarity of responses.',
  3),
--- Part 5
( 'Summarization',
  '**Task**:  \nUse summarization prompting to condense long-form text into concise summaries. For example, summarize a news article or business report into key points.\n\n**Steps**:\n- Start by asking for a simple summary without specifying any constraints on length or detail.\n- Then refine your summary prompt by specifying constraints such as word count limits or focusing on specific aspects (e.g., key takeaways).\n- Experiment with refining prompts to generate summaries at various levels of detail (e.g., high-level overview vs. detailed summary).\n\n**Deliverables**:\n- Initial summary request without constraints.\n- Refined summary prompts specifying length or focus areas.\n- A refined version that balances conciseness and completeness.\n- A brief explanation of how specifying constraints improved or worsened the quality of summaries.',
  3),
--- Part 6
( 'Creating a Narrative from Bullet Points',
  '**Task**:  \nTransform bullet points into cohesive narratives. For example, turn meeting notes into a well-written paragraph summarizing key discussions and decisions.\n\n**Steps**:\n- Start by providing bullet points and asking for them to be turned into a narrative without further instructions.\n- Then refine your prompt by specifying details about structure, flow, or style (e.g., formal report vs. conversational summary).\n- Experiment with refining prompts to generate narratives that vary in style and complexity based on different audiences (e.g., executive summary vs. detailed report).\n\n**Deliverables**:\n- Initial bullet-point-to-narrative transformation request.\n- Refined prompts specifying structure or style preferences.\n- A refined version that achieves clarity and coherence in narrative form.\n- A brief explanation of how refining instructions improved narrative quality.',
  3),
--- Part 7
( 'Asking for Explanations',
  '\n**Task**:  \nAsk the LLM to explain complex topics in simple terms. For example, ask it to explain AI concepts like "neural networks" or "reinforcement learning" as if explaining them to someone unfamiliar with technology.\n\n**Steps**:\n- Start by asking for an explanation without specifying any audience level (e.g., “Explain what neural networks are”).\n- Then refine your prompt by specifying audience background knowledge (e.g., “Explain neural networks as if speaking to someone with no technical background”).\n- Experiment with refining prompts to adjust complexity levels (e.g., explaining it like you''re talking to children vs. explaining it to experts).\n\n**Deliverables**:\n- Initial explanation request without audience specification.\n- Refined prompts specifying audience knowledge levels.\n- A refined version that balances simplicity and accuracy for different audiences.\n- A brief explanation of how refining audience details affected clarity and depth in explanations.\n', 
  3)
;
---
--- Run the SQL script to insert the problem statement into the database:
--- ```
---  cat sql/insert_problem_statements.sql | docker exec -i bfff943b18fd  psql -U postgres
--- ```
--- DELETE 0
--- INSERT 0 7
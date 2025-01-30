+++
date = '2025-01-27'
draft = false
title = 'Prompt Engineering'
weight = 20
numsession = 2
subtopic = 'prompt-engineering'
+++

Prompt engineering works for large language models (LLMs) by leveraging their underlying architecture, training data, and contextual learning capabilities to guide their outputs toward desired results. LLMs, like GPT-4, are based on transformer architectures that use self-attention mechanisms to process vast amounts of text data and generate human-like responses. These models are pretrained on diverse datasets and rely on tokenization to interpret input prompts. Prompt engineering exploits this pretraining by crafting precise, contextually relevant instructions that align with the model's learned patterns.

The effectiveness of prompt engineering lies in its ability to "activate" specific parts of the model's latent knowledge without altering its parameters. By structuring prompts carefully—using techniques like zero-shot, few-shot, or chain-of-thought prompting—users can elicit nuanced reasoning, logical steps, or creative outputs. For example, adding context or examples within a prompt helps the model better understand the task's intent and constraints. This approach enables LLMs to perform tasks they were not explicitly trained on, such as summarizing documents or generating code.

Prompt engineering also mitigates challenges like ambiguity and bias by providing clear instructions and context. It is resource-efficient compared to fine-tuning since it requires no additional training and adapts models across tasks by simply modifying inputs. Iterative refinement of prompts ensures alignment with user goals while improving output quality through experimentation and feedback loops. Thus, prompt engineering bridges the gap between human intent and machine understanding, unlocking the full potential of LLMs for diverse applications.

<!-- more -->
*Some if this content has been created using AI tools like [Perplexity]() and [NotebookLM](https://notebooklm.google.com/)*

<a href="../../subtopics/prompt-engineering/">Read more →</a>

## What we cover in this session
1. What role plays prompt-engineering when working with GenAI models?
2. Is there a certain structure to writing prompts?
3. What are effective techniqies to writing prompts?
4. Do GenAI models use special words to control the output?
5. How are GenAI models trained to respond to certain types of prompts?

## Required Reading and Listening
Listen to the podcast:

 <audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Generative+AI+Prompt+Engineering+Techniques.wav" type="audio/wav">
    Your browser does not support the audio element.
</audio>
[(Click here for transcript)](../podcasts/podcast-03-prompt-ptimization.md)

Read the following:
1. Summary Page: [Generative AI Prompts](https://www.perplexity.ai/page/popular-generative-ai-prompts-vON3yQq5QaGXhVf8gJPmkA)
2. Paper: [Prompt Engineering For Chatgpt: A Quick Guide To Techniques, Tips, And Best Practices](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/docs/Prompt_Engineering_For_ChatGPT_A_Quick_Guide_To_Te.pdf)
3. Textbook: **Chapter 6. Prompt Engineering** in Allamar and Grotendorst, "Hands-On Large Language Models", O'Reilly Media Inc., September 2024


## Additional Resources
You can find numerous posts and articles about prompt engineering. Though, often they seem to be more click-bait than provide new insights.
To learn more about prompt engineering techniques search for "survey" papers to a specific technique.

### Suggested Resources
- This is a comprehensive online resource with diagrams and YouTube videos: [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/pdf/2402.07927)

### Model-specific Resources 
Several model providers offer guides to writing effective prompts for their respective models
- [OpenAI: Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google: Prompt engineering: overview and guide](https://cloud.google.com/discover/what-is-prompt-engineering)
- [Meta: Prompting](https://www.llama.com/docs/how-to-guides/prompting/)
- [Antropic: Prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)



## Overview of LLM Families and Prompting Technieques

| **LLM Family**       | **Techniques** | **Explanation** |
|-----------------------|---------------|-----------------|
| **OpenAI GPT (GPT-3.5, GPT-4)** | Few-shot prompting, Chain-of-Thought (CoT) prompting, Role-based instructions, Iterative refinement, System prompts | GPT models excel with clear instructions and contextual examples. Few-shot prompts improve task-specific performance, while CoT enhances reasoning for complex tasks. Role-based prompts (e.g., "You are a data scientist") guide behavior, and iterative refinement ensures precision. System prompts set tone and scope effectively<a href="https://masterofcode.com/blog/the-ultimate-guide-to-gpt-prompt-engineering" target="_blank">[1]</a><a href="https://www.datacamp.com/tutorial/a-beginners-guide-to-chatgpt-prompt-engineering" target="_blank">[5]</a><a href="https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api" target="_blank">[19]</a>. |
| **Google PaLM (PaLM 2)**        | Chain-of-Thought (CoT) prompting, Few-shot learning, Generated knowledge prompting                                       | PaLM models benefit from CoT for reasoning tasks, breaking problems into steps. Few-shot prompting improves task-specific accuracy by providing examples. Generated knowledge prompts extract and reuse intermediate insights to enhance answers for multi-step queries<a href="https://blog.gopenai.com/fundamental-prompt-engineering-guide-with-vertex-ai-palm-api-c9f307413d85?gi=109a3468ce4f" target="_blank">[2]</a><a href="https://www.youtube.com/watch?v=ou_RisUyHKI" target="_blank">[16]</a><a href="https://cloud.google.com/blog/products/application-development/five-best-practices-for-prompt-engineering?hl=en" target="_blank">[24]</a>.                                                              |
| **Meta LLaMA (LLaMA 2, LLaMA 3)** | In-context learning, Structured dialogue prompts, Text-to-SQL formatting, Prompt chaining                                                              | LLaMA models perform well with in-context learning, where task-specific examples are provided in the input. Structured dialogue prompts maintain coherence in conversational tasks. Text-to-SQL formatting is effective for database queries, and prompt chaining handles complex, multi-step workflows<a href="https://www.llama.com/docs/how-to-guides/prompting/" target="_blank">[3]</a><a href="https://aws.amazon.com/blogs/machine-learning/best-practices-for-prompt-engineering-with-meta-llama-3-for-text-to-sql-use-cases/" target="_blank">[7]</a><a href="https://www.youtube.com/watch?v=zsSQicZp_8o" target="_blank">[17]</a>.                              |
| **Anthropic Claude (Claude 2, Claude 3)** | XML-tagged prompts, Step-by-step reasoning (CoT), Role assignment, Long context utilization                                                       | Claude models respond well to XML-tagged inputs that clearly separate instructions from data. Step-by-step reasoning improves accuracy for complex tasks. Assigning roles (e.g., "You are an expert editor") enhances specificity, and leveraging long context windows enables handling of extensive inputs like documents<a href="https://www.vellum.ai/blog/prompt-engineering-tips-for-claude" target="_blank">[4]</a><a href="https://www.google.com/" target="_blank">[14]</a><a href="https://creatoreconomy.so/p/claude-7-advanced-ai-prompting-tips" target="_blank">[29]</a>.           |
| **Code LLaMA**        | Few-shot examples for code generation, Function calling prompts, Debugging workflows                                              | Code LLaMA models excel with few-shot examples tailored to programming tasks. Function calling prompts guide the model to generate specific code snippets. Debugging workflows help refine outputs by iteratively improving code quality<a href="https://www.promptingguide.ai/models/code-llama" target="_blank">[21]</a><a href="https://github.com/ksm26/Prompt-Engineering-with-Llama-2" target="_blank">[28]</a>.                                                                                                 |

<!--
**Citations**
- [1] https://masterofcode.com/blog/the-ultimate-guide-to-gpt-prompt-engineering
- [2] https://blog.gopenai.com/fundamental-prompt-engineering-guide-with-vertex-ai-palm-api-c9f307413d85?gi=109a3468ce4f
- [3] https://www.llama.com/docs/how-to-guides/prompting/
- [4] https://www.vellum.ai/blog/prompt-engineering-tips-for-claude
- [5] https://www.datacamp.com/tutorial/a-beginners-guide-to-chatgpt-prompt-engineering
- [6] https://open.ocolearnok.org/aibusinessapplications/chapter/prompt-engineering-for-large-language-models/
- [7] https://aws.amazon.com/blogs/machine-learning/best-practices-for-prompt-engineering-with-meta-llama-3-for-text-to-sql-use-cases/
- [8] https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/
- [9] https://learn.microsoft.com/zh-cn/Azure/ai-services/openai/concepts/prompt-engineering
- [10] https://www.mercity.ai/blog-post/advanced-prompt-engineering-techniques
- [11] https://www.reddit.com/r/ChatGPT/comments/12aobpp/maximizing_prompt_effectiveness_techniques_for/
- [12] https://www.k2view.com/blog/prompt-engineering-techniques/
- [13] https://www.deeplearning.ai/short-courses/prompt-engineering-with-llama-2/
- [14] https://www.google.com/
- [15] https://community.ipfire.org/t/how-to-prompt-gpt-models-to-create-effective-tutorials/10024
- [16] https://www.youtube.com/watch?v=ou_RisUyHKI
- [17] https://www.youtube.com/watch?v=zsSQicZp_8o
- [18] https://www.reddit.com/r/ClaudeAI/comments/1gds696/the_only_prompt_you_need/
- [19] https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api
- [20] https://www.promptingguide.ai
- [21] https://www.promptingguide.ai/models/code-llama
- [22] https://blog.mlq.ai/prompt-engineering-claude-metaprompt/
- [23] https://www.reddit.com/r/GPT3/comments/10hmtpa/prompt_engineering_tips_for_better_code/
- [24] https://cloud.google.com/blog/products/application-development/five-best-practices-for-prompt-engineering?hl=en
- [25] https://www.reddit.com/r/ClaudeAI/comments/1exy6re/the_people_who_are_having_amazing_results_with/
- [26] https://platform.openai.com/docs/guides/prompt-engineering
- [27] https://www.linkedin.com/pulse/5-key-prompt-engineering-techniques-using-claude-julien-coupez-r59ne
- [28] https://github.com/ksm26/Prompt-Engineering-with-Llama-2
- [29] https://creatoreconomy.so/p/claude-7-advanced-ai-prompting-tips
-->

---
<a href="../../subtopics/prompt-engineering/">Read more →</a>
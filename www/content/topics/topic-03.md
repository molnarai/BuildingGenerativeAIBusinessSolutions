+++
date = '2025-02-03'
draft = false
title = 'Framework for Prompt Evaluation and Optimization'
weight = 30
numsession = 3
+++
This session explores the intricacies of prompt engineering for large language models (LLMs), emphasizing its importance in optimizing LLM performance for specific tasks. Unlike traditional machine learning models, evaluating LLMs involves subjective metrics like context relevance, answer faithfulness, and prompt relevance.

<!-- mofre -->

The session highlights frameworks like ARES, which uses smaller LLMs as evaluators, and LLMA, which focuses on instruction-following capabilities. Techniques such as chain-of-thought prompting, few-shot prompting, and retrieval-augmented generation are presented as effective strategies to guide LLMs in reasoning, learning from examples, and leveraging external information.

The session also introduces public datasets like KILT and SuperGLUE, along with task-specific datasets such as Natural Questions, HotpotQA, and FEVER. These datasets provide standardized benchmarks to test and refine prompt engineering approaches. The hosts emphasize the need for creativity and experimentation in this evolving field, blending technical expertise with an intuitive understanding of language and machine learning.

## Required Reading and Listening

Listen to the podcast ([transcription](../../podcasts/podcast-03-prompt-optimization/)):

<!-- Listen to the podcast: -->

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Evaluating+Large+Language+Models_2.wav" type="audio/wav">
    Your browser does not support the audio element.
</audio>

Read the following:

1. Summary Page: [Prompt Evaluation and Optimization](https://www.perplexity.ai/page/prompt-evaluation-and-optimiza-Og6LEkBpTPCCJhZdQ7qHRw)
2. Textbook: **Chapter 5.4**, Huang, Ken. "Practical Guide for AI Engineers"
3. Paper: [ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems](https://arxiv.org/pdf/2311.09476)

## Additional Resources

- [ARES](https://ares-ai.vercel.app/getting_started.html) is a framework for evaluating Retrieval-Augmented Generation (RAG) models.
- [G-Eval](https://docs.confident-ai.com/docs/metrics-llm-evals) is a framework that uses LLMs with chain-of-thoughts (CoT) to evaluate LLM outputs based on ANY custom criteria. The G-Eval metric is the most versatile type of metric deepeval has to offer, and is capable of evaluating almost any use case with human-like accuracy.
- [RAGAS](https://docs.ragas.io/en/stable/) is a library that provides tools to supercharge the evaluation of Large Language Model (LLM) applications.

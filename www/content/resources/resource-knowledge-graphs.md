---
draft: false
title: Knowledge Graphs
weight: 40
description: Below are various resources related to knowledge graphs and their use in LLM applications.
---

**Synopsis:**

**Knowledge Graphs and Large Language Models: A Synergistic Overview**

Knowledge graphs (KGs) play a transformative role in the development of Large Language Models (LLMs) by providing structured and semantically rich information that enhances their capabilities. Similarly, LLMs can help resolve challenges in the construction and validation of KGs. The integration of these technologies aims to leverage their respective strengths and overcome their limitations.
What are Knowledge Graphs? A KG is a directed labeled graph where nodes represent entities or concepts, and edges represent the relationships between them. Data in KGs is typically presented as (subject, predicate, object) triples, which can be extended to quadruples in temporal KGs to include a timestamp. KGs are effective in organizing unstructured data into actionable insights and can provide further insight into a word's semantics via its context. Examples include Wikidata, YAGO, NELL, and domain-specific KGs like medical knowledge graphs. Multi-modal KGs extend this by incorporating information from various modalities like images and videos.

Integration of Knowledge Graphs in LLM Development (KG-enhanced LLMs) KGs are used to enhance LLMs in several ways:

- Retrieval-Augmented Generation (RAG): KGs enhance LLMs by providing structured pathways for retrieving external data to improve the accuracy of responses. This is particularly useful for complex queries requiring multi-hop reasoning or cross-referencing disparate datasets, overcoming the limitations of traditional vector similarity searches. GraphRAG is an advanced technique that uses LLM-generated KGs to further improve retrieval processes by grounding queries in graph structures, leading to better answers for complex questions and reduced hallucinations.

- Knowledge Injection: KGs are used to inject factual knowledge into LLMs during pre-training or inference.

    - Pre-training: Integrating KGs during pre-training helps LLMs learn knowledge from the structured format, enhancing their knowledge expression. This can involve integrating KGs into the training objective by exposing more knowledge entities, integrating relevant knowledge sub-graphs into LLM inputs, or KGs instruction-tuning to help LLMs better comprehend KG structure. Examples include ERNIE, which uses word-entity alignment, and K-BERT, which injects knowledge triples via a visible matrix.

    - Inference: During inference, retrieving knowledge from KGs can significantly improve the performance of LLMs in accessing domain-specific knowledge and the latest information without retraining. Techniques like KAPING retrieve facts from a KG and prepend them to input questions.

    - Improving Interpretability: KGs can provide interpretability to the reasoning process of LLMs. This involves using KGs for language model probing to understand the knowledge stored in LLMs, and for language model analysis to understand how LLMs generate results by grounding reasoning

**Texts:**
The provided texts collectively explore the integration of knowledge graphs (KGs) with Large Language Models (LLMs) to enhance AI applications. One source details the foundational principles of building KGs, including organizing principles like property graphs, taxonomies, and ontologies, and discusses their benefits in making data smarter for both humans and machines. Another source presents a research overview of combining KGs and LLMs, categorizing methods such as KG-powered LLMs, LLM-based KGs, and hybrid approaches, and analyzes their strengths and limitations in improving tasks like question answering and knowledge graph construction. A third source focuses on adding memory to AI agents, where KGs can serve as a form of external knowledge to improve reasoning and maintain state. Finally, a practical guide illustrates building a scalable KG-based retrieval-augmented generation (RAG) system using Wikipedia data and LlamaIndex, demonstrating the real-world application of these combined technologies for semantic search and information retrieval.

1. Bijit Ghosh, **Enhancing LLMs Inference with Knowledge Graphs** <br />
[Link](https://medium.com/@bijit211987/enhancing-llms-inference-with-knowledge-graphs-7140b3c3d683)

2. Tomaž Bratanič, **Knowledge Graphs & LLMs: Multi-Hop Question Answering** <br />
[Link](https://neo4j.com/blog/developer/knowledge-graphs-llms-multi-hop-question-answering/)

3. Tomaž Bratanič, **Building Knowledge Graphs with LLM Graph Transformer** <br />
[Link](https://medium.com/data-science/building-knowledge-graphs-with-llm-graph-transformer-a91045c49b59)

4. Jonathan Larson, Steven Truitt, **GraphRAG: Unlocking LLM discovery on narrative private data** <br />
[Link](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)

5. Steve Hedden, **How to Implement Knowledge Graphs and Large Language Models (LLMs) Together at the Enterprise Level** <br />
[Link](https://towardsdatascience.com/how-to-implement-knowledge-graphs-and-large-language-models-llms-together-at-the-enterprise-level-cf2835475c47/)

6. Rohan Rao, Benika Hall, Sunil Patel, Christopher Brissette and Gordana Neskovic, **Insights, Techniques, and Evaluation for LLM-Driven Knowledge Graphs** <br />
[Link](https://developer.nvidia.com/blog/insights-techniques-and-evaluation-for-llm-driven-knowledge-graphs/)

7. Daniel Chalef, **Graphiti: Knowledge Graph Memory for a Post-RAG Agentic World** <br />
[Link](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/)

8. Kartik Joshi, **LLM Knowledge Graph Builder Front-End Architecture** <br />
[Link](https://neo4j.com/blog/developer/frontend-architecture-and-integration/)
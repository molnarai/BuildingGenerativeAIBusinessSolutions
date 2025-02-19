+++
date = '2025-02-24'
draft = false
title = 'Retrieval Augmented Generation (RAG)'
weight = 60
numsession = 6
+++
Retrieval-Augmented Generation (RAG) enhances generative AI by integrating external information retrieval, enabling models to produce accurate, contextually informed responses. It combines indexing, retrieval, augmentation, and generation, with semantic search playing a key role in retrieving relevant data based on meaning rather than exact keywords. By leveraging vector embeddings and similarity measures, RAG reduces hallucinations and dynamically updates knowledge without retraining the model. This approach is widely applied across industries, such as customer service, education, legal research, and content creation, to address knowledge-intensive tasks. Its implementation relies on vector databases and advancements in embedding models to efficiently connect AI systems with external, authoritative information sources.
<!-- more -->
**Retrieval-Augmented Generation (RAG)** is a method that enhances the capabilities of generative AI models by integrating external information retrieval into their workflows. Unlike traditional generative models that rely solely on their pre-trained knowledge, RAG retrieves relevant, up-to-date, or domain-specific information from external data sources and incorporates it into the model's response. This process involves four key steps: indexing, retrieval, augmentation, and generation. During indexing, data is transformed into vector embeddings and stored in a vector database. When a query is made, the retrieval step identifies the most relevant documents using similarity measures. These documents are then used during augmentation to enrich the model's input, enabling it to generate responses that are both contextually accurate and informed by external knowledge.

**Semantic search** plays a crucial role in the retrieval phase of RAG by enabling the system to find contextually relevant information rather than relying on exact keyword matches. It uses vector search, where both user queries and documents are encoded into numerical representations called embeddings. By comparing these embeddings, semantic search identifies the most conceptually similar documents in a dataset. This approach is particularly effective for understanding user intent and retrieving results that align with the meaning behind a query rather than its literal wording. Semantic search is widely used in applications such as customer support systems, enterprise knowledge management, and e-commerce platforms to improve search accuracy and relevance.

**The combination of RAG and semantic search** creates a powerful framework for solving knowledge-intensive tasks. For instance, RAG can retrieve specific information from large databases or proprietary knowledge bases, such as customer support logs or legal documents, while semantic search ensures that the retrieved data aligns with the user's intent. This synergy reduces hallucinations—instances where AI generates incorrect or fabricated information—and allows for dynamic updates without retraining the model. As a result, RAG systems can provide more reliable answers in domains where accuracy and recency are critical.

One of the key advantages of RAG is its versatility across **industries and applications**. In customer service, it enables chatbots to deliver personalized responses by retrieving contextual information about users or products. In education, RAG can generate tailored study materials or explanations based on specific queries. Legal professionals use it for efficient case law retrieval and drafting assistance, while content creators leverage it for summarization and fact-checking. These diverse applications highlight how RAG bridges the gap between static AI training data and dynamic real-world information needs.

The technical implementation of RAG often relies on **vector databases to store embeddings** generated from text or other data types. These embeddings capture semantic meaning, allowing for efficient similarity searches at scale. Tools like Pinecone or Elasticsearch facilitate this process by enabling real-time updates to the database as new information becomes available. Additionally, advancements in embedding models and prompt engineering have further improved RAG's ability to handle complex queries and generate coherent outputs. This makes RAG an essential tool for modern AI systems that require both generative capabilities and access to authoritative external knowledge.


## Required Reading and Listening
<!-- Listen to the podcast ((../../podcasts/podcast-05-frameworks-benchmarks/)): -->
Listen to the podcast:

 <audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/RAG+and+Beyond_+Augmenting+LLMs+with+External+Data.wav" type="audio/wav">
    Your browser does not support the audio element.
</audio>

Read the following:
1. Perplexity blog: [RAG and Semantic Search](https://www.perplexity.ai/page/rag-and-semantic-search-LwzgO8F2Tym.05Momy.B5A)
2. Textbook: [Chapter 8: Hands-On Large Language Models](https://go.oreilly.com/georgia-state-university/library/view/hands-on-large-language/9781098150952/ch08.html)
3. Paper: [Retrieval Augmented Generation (RAG) and Beyond: A Comprehensive Survey on How to Make your LLMs use External Data More Wisely](https://arxiv.org/abs/2409.14924)


## Additional Resources
- [Seven Failure Points When Engineering a Retrieval Augmented Generation System](https://arxiv.org/pdf/2401.05856v1)
- [Graph Retrieval-Augmented Generation: A Survey](https://arxiv.org/abs/2408.08921)

## Some Questions to Consider
1. **What is Retrieval Augmented Generation (RAG)?**

    RAG is a technique that enhances large language models (LLMs) by allowing them to access and incorporate external data sources during the response generation process. This addresses limitations of LLMs such as outdated knowledge, lack of domain-specific expertise, and the tendency to hallucinate. RAG systems work by retrieving relevant documents based on a user query and then feeding these documents to the LLM to generate an answer. The process typically involves indexing data, retrieving relevant segments, and generating a response.

2. **What are the key components of a RAG system, and how do they work together?**

    A RAG system primarily consists of two main processes:

    Indexing: This involves processing and structuring the external data source. Documents are split into smaller, manageable chunks, which are then converted into embeddings (numerical representations) using an embedding model. These embeddings, along with the original text chunks, are stored in a database for efficient retrieval. Key considerations include chunking strategies (fixed size, semantic-based, etc.) and the choice of embedding model (sparse, dense, hybrid).
    Querying: When a user poses a question, the system first converts the query into an embedding using the same embedding model used during indexing. This query embedding is then used to perform a semantic search in the indexed database to find the most relevant document chunks. The retrieved chunks are then passed to an LLM, along with the original query, to generate a final answer.

3. **What are the different types of queries that RAG systems can handle, and what are the best techniques for addressing each type?**

    The effectiveness of a RAG system depends on the type of query it's designed to handle. The study categorizes queries into four levels:

    - Explicit Fact Queries: Answers can be directly retrieved from specific data segments. Best addressed by ensuring accurate retrieval and minimizing noise.
    - Implicit Fact Queries: Require synthesizing information from multiple references, often involving multi-hop reasoning. Graph-based approaches and iterative retrieval methods are beneficial.
    - Interpretable Rationale Queries: Demand understanding and application of domain-specific rationales, often explicitly provided in external resources (e.g., FDA guidelines). Prompt engineering and instruction tuning are crucial.
    - Hidden Rationale Queries: Rely on dispersed knowledge or in-domain data, where the rationale isn't explicitly stated. Offline learning techniques, in-context learning, and fine-tuning can be effective.

4. **What are the main strategies for improving data retrieval in RAG systems?**

    Several techniques enhance data retrieval:

    Chunking Optimization: Experimenting with different chunk sizes and strategies (fixed size, semantic, recursive) to balance semantic coherence and noise reduction.
    Indexing Methods: Employing sparse, dense, or hybrid retrieval methods to create effective mappings from search terms to text segments. Dense retrieval uses vector embeddings, while sparse retrieval uses keyword-based indexes.
    Query Document Alignment: Aligning queries with document segments through traditional alignment (mapping both to the same encoding space), document domain alignment (generating synthetic answers), or query domain alignment (generating synthetic questions).
    Re-ranking: Re-evaluating the retrieved documents to improve the relevance of the top results
    Recursive Retrieval: Performing multiple retrieval attempts to progressively refine the search and address any omissions.

5. **How can the response generation phase in RAG systems be improved?**

    Enhancing the response generation involves:

    Determining Sufficiency: Evaluating if the retrieved information is adequate or if additional data is needed.
    Conflict Resolution: Handling discrepancies between retrieved knowledge and the LLM's internal knowledge.
    Supervised Fine-Tuning: Fine-tuning the LLM on carefully designed training data to mitigate the effects of irrelevant or erroneous information.
    Joint Training: Training both the retriever and generator components of the RAG system together to ensure consistent performance.
    Prompt Engineering: Optimizing prompts to ensure the LLM accurately follows and reacts based on the rationales provided in the external data.
    Self-reflection: Using techniques such as "Chain of Thought" or "Tree of Thoughts" to enable the LLM to evaluate and refine its own reasoning process.

6. **What are the main challenges and failure points when engineering a RAG system?**

    The "Seven Failure Points" paper highlights several key challenges:

    Missing Documents: Relevant documents are not included in the indexed data source.
    Missed Top-Ranked Documents: The answer is in a document that is not ranked highly enough to be returned.
    Not in Context: Documents with the answer were retrieved but did not make it into the context for generating an answer
    Reader Cannot Extract the Answer: The document is passed to the LLM, but it fails to generate the correct answer.
    Hallucination: The LLM ignores the provided context and generates an answer based on its pre-existing knowledge, which may be incorrect.
    Jailbreak: Users bypass the RAG system through adversarial prompts.
    Security/Privacy Violations: Unauthorized access to sensitive information
    Other challenges include:
    - Data Processing Pipeline Robustness: Ensuring the data pipeline can handle uploaded documents and media effectively.
    - Lack of Pre-existing Data for Testing: Difficulties in testing RAG systems because no data exists and needs to be experimentally discovered.

7. **What are the different ways to integrate external data into LLMs, and what are their respective trade-offs?**

    There are three main approaches:

    Context Injection (RAG): Extracts relevant data based on the query and provides it as context to the LLM. Offers good interpretability and stability but is limited by the context window size and potential information loss. Best suited for scenarios where data can be explained succinctly.
    Small Model Approach: Trains a smaller model on specific domain data to guide the integration of external information. Reduces training time and can assimilate considerable amounts of data, but its efficacy depends on the model's capabilities and may limit performance for complex tasks.
    Fine-Tuning: Directly fine-tunes a general LLM with external domain knowledge to create a domain-expert model. Enables utilization of large model capacities but requires careful data design to avoid generating erroneous outputs or losing previously known domain knowledge. This approach also requires more data, a longer training duration, and more computational resources.

8. **What is the role of validation and continuous monitoring in RAG system deployment?**

    The sources emphasize that validation of a RAG system is primarily feasible during operation, and its robustness evolves over time. Continuous monitoring is crucial because RAG systems receive unknown input at runtime. This monitoring helps in identifying and addressing issues such as:

    - Calibration: Fine-tuning chunk size, embedding strategy, retrieval strategy, consolidation strategy, context size, and prompts.
    - Performance Drift: Detecting and mitigating performance degradation due to changes in data or user behavior.
    - Security Threats: Identifying and preventing jailbreak attempts and other security vulnerabilities.

## Glossary

| Term| Description |
|--------|---------------|
| **Retrieval Augmented Generation (RAG)** | A framework that enhances language models by retrieving information from external sources to improve the accuracy and relevance of generated content. |
| **Large Language Model (LLM)** | A deep learning model with a large number of parameters, trained on vast amounts of text data, capable of understanding and generating human-like text. |
| **Hallucination** | The tendency of language models to generate false or nonsensical information that is not grounded in reality. |
| **Domain-Specific Knowledge** | Information and expertise relevant to a particular field or subject area. |
| **Explicit Fact Query** | A query that can be answered directly by retrieving a specific piece of information from a data source. |
| **Implicit Fact Query** | A query that requires synthesizing information from multiple sources, often involving reasoning or inference, to arrive at an answer. |
| **Interpretable Rationale Query** | A query that requires understanding and applying domain-specific rationales from external data to provide an answer. |
| **Chunking** | The process of dividing documents into smaller, more manageable segments for indexing and retrieval. |
| **Embedding** | A vector representation of text or other data that captures its semantic meaning. |
| **Sparse Retrieval** | A retrieval method that indexes text segments using specific words. |
| **Dense Retrieval** | A retrieval method that maps text segments into a dense vector space of features. |
| **Query Rewriting** | Modifying a user's query to improve search accuracy and relevance. |
| **Fine-tuning** | The process of further training a pre-trained language model on a smaller, domain-specific dataset. |
| **In-context Learning** | The ability of a language model to learn from examples provided in the prompt, without requiring explicit fine-tuning. |
| **Prompt Tuning** | Optimizing the input prompts to elicit the desired behavior from a language model. |
| **Adapter Tuning** | Integrating small adapter models with LLMs while freezing the parameters of the LLM during fine-tuning and only optimizing the weights of the adapter. |
| **Low-Rank Adaptation** | Reducing the number of trainable parameters needed for adapting to downstream tasks by imposing low-rank constraints on each dense layer to approximate the update matrices. |
| **Knowledge Graph** | A graph-structured database that represents entities and their relationships. |
| **Data Dependency** | The subset of data segments indispensable for addressing a query. |
| **Power Set** | The set of all subsets of a given set, including the empty set and the set itself. |
| **IR (Information Retrieval)** | The process of obtaining information system resources that are relevant to an information need from a collection of those resources. |
| **BFS (Breadth-First Search)** | An algorithm for traversing or searching tree or graph data structures. |
| **Zero-Shot Learning** | A type of machine learning where a model can perform a task without having seen any specific examples of that task during training. |
| **Few-Shot Learning** | A type of machine learning where a model can learn a new task from only a few examples. |
| **In-Domain Data** | Data from the same domain as the task at hand. |
| **Offline Learning** | Training a model using a fixed dataset before deployment. |
| **Prompt Engineering** | The process of designing effective prompts to elicit desired responses from language models. |
| **Chain-of-Thought Prompting** | A prompting technique that encourages language models to generate intermediate reasoning steps before producing a final answer. |
| **Buffer-of-Thought** | Using a problem distiller to distill a meta-buffer across many reasoning tasks. |
| **Instruction Tuning** | Supervised fine-tuning using paired (instruction, output) data to infuse new capabilities into LLMs. |
| **G-Evals** | NLG evaluation using GPT-4 with better human alignment for offline evaluation techniques. |


---
title: Project
description: Instructions for group project
---
<!-- **[Guidelines for Final Project Presentation](project-final-presentation/)** -->

<!-- **Project Assignment: Building an AI-Powered Business Solution** -->

This semester-long project involves the development of a Document-Driven Agentic Intelligence System (DAIS) designed to operate on a specified business-relevant document corpus. Students will build a system capable of ingesting and processing PDF and text documents, utilizing a multi-agent architecture for analysis, and supporting both an interactive chat interface for human users and a batch query interface for automated evaluation. The system’s performance will be rigorously assessed through a student-constructed test set and quantitative metrics.

The project allows students to choose one of three variations, each focusing on a distinct analytical approach. These include building a semantic knowledge graph, functioning as a research advisor capable of providing evidence-backed responses, or acting as a scientific/business discovery assistant proposing hypotheses. Regardless of the chosen variation, the system must be designed with a specific user persona in mind – such as an equity analyst or compliance officer – and should support realistic tasks associated with that role.

The development process is structured around several milestones, culminating in a demonstrable system. Students will progressively build upon a basic data pipeline, integrating document ingestion, agentic processing, and evaluation frameworks. The final deliverable requires a fully functional, deployed system accessible through both interfaces, alongside a comprehensive technical report, a demonstration video, and an in-class presentation.

## Requirements

In this semester‑long team project, you will build a Document‑Driven Agentic Intelligence System (DAIS) that operates over a business‑relevant document corpus (e.g., SEC filings, annual/ESG reports, regulatory texts, or industry/research reports). The system must:

- Ingest and process PDF/text documents into internal representations.
- Use agentic AI (multiple cooperating agents) running on our on‑prem infrastructure.
- Support both:
    - An interactive chat interface (for human users).
    - A batch query interface (for automated evaluation).
- Be rigorously evaluated using a student‑constructed test set and quantitative metrics.
- Be demonstrated in a 5–10 minute recorded video.


## Variations (Choose One)
You must choose **one** (A, B, or C) of the following variations for your DAIS:

### Variation A – Knowledge Graph Intelligence
- Builds a semantic knowledge graph from the corpus (e.g., firms, products, risks, regulations, events).
- Focus on entity/relationship extraction, graph quality, and graph‑aware querying.

Knowledge Graph Intelligence addresses the problem that business and regulatory documents contain large amounts of structured information that are difficult to query and reason about when left in raw text form. Analysts, risk managers, and strategy professionals frequently need to understand how entities, such as companies, business segments, products, and risk factors, relate across time and documents, but they are forced to manually scan long PDFs or rely on brittle keyword search. A knowledge-graph-oriented system converts these unstructured sources into a structured, queryable representation that exposes entities and relationships explicitly, making it possible to ask more complex, semantically rich questions.

A typical user of this system would be an analyst working with a specific corpus, for example SEC filings and annual/ESG reports for a fixed universe of firms. The analyst might ask questions such as which risk categories are associated with a particular company over several years, how those risks have evolved, which competitors are frequently co-mentioned, or how specific regulatory themes appear across the portfolio. The user interacts through a chat interface that accepts natural-language questions but internally translates them into graph queries and retrieval operations. The user sees answers that summarize relevant entities and relationships and may also be able to inspect underlying graph nodes and edges.

The solution consists of several main components. A document processing layer ingests PDFs, extracts text, segments it into chunks, and derives basic metadata such as company, date, and document type. An extraction and graph construction layer uses LLM-based agents to identify entities and relationships, writes metadata to a relational database, embeddings to a vector store, and structured relationships to a graph database. An orchestration layer coordinates agents for extraction, validation, and graph refinement, including deduplication and schema consistency checks. A query layer maps user utterances to combinations of graph and vector retrieval, and a response generation layer uses the retrieved subgraph and text snippets to synthesize answers in natural language while preserving links back to underlying graph structures.

### Variation B – Research Advisor
- Answers complex, multi‑turn questions with evidence‑backed responses and citations.
- Focus on hybrid retrieval (graph + vectors + relational), reasoning chains, and answer quality.

The Research Advisor addresses the problem that professionals and researchers must synthesize evidence from many documents to answer complex questions, yet conventional search and single-step Q&A often fail to retrieve, combine, and justify information at the required depth. Business researchers, policy analysts, or strategy teams need systems that can decompose multi-part questions, gather evidence from heterogeneous sources, reconcile conflicting information, and produce answers that are both well grounded in the corpus and transparent in their reasoning.

A user of this system would typically be a researcher or analyst posing multi-turn questions about the document collection. For instance, an ESG analyst might ask how climate-related risks are described across firms in a sector, follow up with requests to compare specific companies, and then drill down into cited documents. The user engages via a conversational interface, iteratively refining the query and asking for clarifications or alternative views. At each turn, the system retrieves relevant passages and graph elements, generates an answer that cites specific documents or sections, and optionally exposes its reasoning steps or confidence assessments so the user can judge reliability.

The solution integrates a hybrid retrieval and reasoning pipeline. A document processing layer prepares text, metadata, embeddings, and, where useful, a knowledge graph. A query understanding component analyzes each user input, decomposes complex questions into subqueries, and routes these to a retrieval component that leverages both vector search and graph or structured filters. A reasoning and synthesis component aggregates retrieved evidence, identifies overlaps and contradictions, and constructs a coherent answer while maintaining traceability to sources. A fact-checking and validation component can optionally consult external search, within the allowed constraints, to detect obvious contradictions or hallucinations. The system exposes both a chat API to support interactive use and a batch interface that runs a fixed set of questions through the same pipeline for evaluation against a labeled test set.

### Variation C – Scientific/Business Discovery Assistant
- Proposes hypotheses and analytic/experimental designs grounded in the corpus.
- Focus on complex reasoning, domain knowledge integration, and explicit assumptions/uncertainty.

The Scientific/Business Discovery Assistant addresses the problem that generating good hypotheses and study designs from large corpora of business or scientific documents is cognitively demanding and time-consuming. Researchers and data-driven managers often need to identify gaps in existing knowledge, propose plausible mechanisms or relationships, and design empirical analyses or experiments, but they lack tools that can systematically scan a corpus, aggregate patterns, and suggest structured hypotheses with explicit assumptions and evidence.

A user of this system would be a researcher, data scientist, or strategy lead exploring a domain represented by the corpus, such as digital transformation in a sector, ESG impacts on financial outcomes, or adoption of analytics in specific industries. The user interacts through a chat-like interface by specifying areas of interest, constraints, and questions, such as what unexplored relationships might exist between particular practices and outcomes, or how one might design a study to test a proposed effect. The system responds with candidate hypotheses, supporting evidence from the corpus, and proposed designs that specify variables, possible data sources, and analytic methods, while indicating uncertainty and limitations.

The solution combines document understanding, knowledge representation, and advanced reasoning components. A preprocessing pipeline builds structured representations of mechanisms, variables, interventions, and outcomes, often via a knowledge graph augmented with embeddings. A literature integration component organizes findings, reported effects, and contextual factors from the corpus. A hypothesis generation component uses these structures and an LLM to propose candidate relationships that are consistent with observed patterns but not trivially restatements of existing results. An experimental or analytical design component maps hypotheses to concrete study designs, including suggested variables, segmentation, and possible metrics. A constraint and feasibility component evaluates whether designs are realistic given data and resource assumptions, and a validation component cross-checks whether similar hypotheses have already been studied in the corpus. As with the other variations, the system provides both an interactive chat API for exploration and a batch interface that can generate and log hypotheses or designs over a predefined set of prompts for evaluation and comparison across system iterations.

## Evaluation Test Sets

The evaluation test set is a curated collection of application-specific queries paired with reference answers and, where appropriate, supporting evidence annotations. It is constructed by the project team (and, if possible, domain experts) to reflect realistic user tasks for the chosen DAIS variation, such as graph exploration, research-style question answering, or hypothesis generation.

To generate it, you sample representative documents from their corpus, design queries that require nontrivial reasoning over those documents, and manually author high-quality answers and links to the relevant passages or graph elements that justify those answers. During evaluation, the DAIS is run in batch mode on this fixed test set, its outputs are compared against the reference answers, and quantitative metrics such as precision, recall, F1, retrieval relevance scores, or LLM-judged answer quality are computed to assess system performance and track improvements across iterations.

You must design a domain specific evaluation test set to evaluate your system. This test set should include realistic queries or tasks that reflect the needs of your chosen user persona. Consider the following guidelines:
- Include a diverse set of queries/tasks that cover various aspects of your system's capabilities.
- Ensure that the test set is challenging enough to differentiate between different system implementations.
- Define clear evaluation metrics for each query/task (e.g., accuracy, relevance, completeness).



## User Perspective and Deliverables
You should define a realistic primary user persona, such as:
- 	Equity/credit analyst.
- 	ESG or risk analyst.
- 	Compliance or regulatory officer.
- 	Strategy/management consultant.
- 	Business researcher or data scientist.

Your system should support realistic tasks for that persona through:
1.	Chat Interface (Human‑Facing)
    - Provided web UI (which you may lightly customize) that connects to your chat API.
    - Must show responses, and for appropriate variations, citations and/or reasoning traces.
2.	Batch Query Interface (Evaluation‑Facing)
    - A batch API or script that takes a file of queries and returns structured outputs for evaluation.
    - This interface will be used to run your system over your test set.
3.	Final Demo Video (5–10 minutes)
    - Clear, concise walkthrough of:
        - Problem and user persona.
        - System architecture (high level).
        - Live or recorded demo of core capabilities through the chat interface.
        - Brief summary of evaluation results and key insights.



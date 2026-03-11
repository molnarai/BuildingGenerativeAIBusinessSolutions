---
date: 2026-03-23
classdates: 'Monday 2026-03-23, Wednesday 2026-03-11'
draft: false
title: 'Knowledge Graphs'
weight: 90
numsession: 9
---
This session covers integrating knowledge graphs into agentic AI systems to enhance reasoning, memory, and factual grounding. It details the construction of graphs using both traditional NLP tools like spaCy for precision and Large Language Models for semantic flexibility. The session explains how formal ontologies serve as the structural blueprint for these systems, ensuring consistent vocabulary and logical constraints.
<!--more-->

Furthermore, it compares RDF/SPARQL and LPG/Cypher database architectures, highlighting their respective strengths in semantic reasoning and high-performance graph traversals. Advanced techniques such as Inductive Logic Programming and Graph Neural Networks are introduced to discover latent patterns and verify connections within the data.

Finally, a practical merger and acquisition use case illustrates a multi-layered architecture where specialized agents utilize these technologies to identify and evaluate corporate targets.

##### Knowledge Graphs for Agentic AI Reasoning
<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Knowledge_Graphs_for_Agentic_AI_Reasoning.m4a" type="audio/mp4">
    Your browser does not support the audio element.
</audio>

##### Knowledge Graphs for M&A AI Agents
<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Knowledge_Graphs_for_MandA_AI_Agents.m4a" type="audio/mp4">
    Your browser does not support the audio element.
</audio>




### Presentation
 - [Knowledge Graphs](../../slides/slide-09-knowledge-graphs/)

### Notebooks

1. [01_Graph_Basics.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/01_Graph_Basics.ipynb) — Introduction to directed, undirected, and weighted graphs using NetworkX, with graph algorithms (centrality, PageRank, shortest paths) applied to an agentic AI scenario.
2. [02_Building_Knowledge_Graphs.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/02_Building_Knowledge_Graphs.ipynb) — Building knowledge graphs from structured (CSV) and semi-structured (JSON) data, with querying and capability-based task routing.
3. [03_Triple_Extraction_spaCy.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/03_Triple_Extraction_spaCy.ipynb) — NLP-based triple extraction using spaCy for named entity recognition, dependency parsing, and pattern-based relation extraction.
4. [04_Triple_Extraction_LLM.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/04_Triple_Extraction_LLM.ipynb) — LLM-powered triple extraction using single-pass, two-step, and schema-constrained approaches, with hallucination validation.
5. [05_Ontology_Design.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/05_Ontology_Design.ipynb) — Designing ontologies with RDF/OWL using rdflib, covering class hierarchies, properties, competency questions, and SPARQL queries.
6. [06_Graph_Queries_SPARQL_vs_Cypher.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/06_Graph_Queries_SPARQL_vs_Cypher.ipynb) — Side-by-side comparison of SPARQL and Cypher query languages on the same agentic AI dataset, with guidance on when to use each.




### References

#### Foundational Knowledge Graphs & Semantic Web

- [Hogan, A. et al. (2021). Knowledge Graphs. ACM Computing Surveys.](https://arxiv.org/pdf/2003.02320)
- [Auer, S. et al. (2007). DBpedia: A Nucleus for a Web of Open Data. ISWC.](https://www.researchgate.net/publication/221466796_DBpedia_A_Nucleus_for_a_Web_of_Open_Data)
[Ehrlinger, L. & Wöß, W. (2016). Towards a Definition of Knowledge Graphs. SEMANTiCS.](https://www.researchgate.net/publication/323316736_Towards_a_Definition_of_Knowledge_Graphs)

#### Ontologies & Reasoning

- [Gruber, T. (1995). Toward Principles for the Design of Ontologies.](https://www.researchgate.net/publication/2626138_Toward_Principles_for_the_Design_of_Ontologies_Used_for_Knowledge_Sharing)
- [Studer, R., Benjamins, V., Fensel, D. (1998). Knowledge Engineering Principles.](https://www.sciencedirect.com/science/article/pii/S0169023X97000566)
- [Baader, F. et al. (2010). The Description Logic Handbook.](https://www.researchgate.net/publication/230745455_The_Description_Logic_Handbook_Theory_Implementation_and_Applications)

#### Graph Query & Modeling

- [Wood, P.T. (2012). Query Languages for Graph Databases. ACM SIGMOD.](https://dl.acm.org/doi/10.1145/2206869.2206879)
- [Pérez, J. et al. (2006). Semantics and Complexity of SPARQL. ISWC.](https://dl.acm.org/doi/10.1145/1567274.1567278)

#### Agentic AI, Neuro-Symbolic, Workflow AI

- [Davis, E. & Marcus, G. (2015). Commonsense Reasoning and Knowledge Representation.](https://dl.acm.org/doi/10.1145/2701413)
- [Garcez, A., Besold, T. et al. (2018). Neuro‑Symbolic AI: The State of the Art.](https://arxiv.org/pdf/2509.06921v1)
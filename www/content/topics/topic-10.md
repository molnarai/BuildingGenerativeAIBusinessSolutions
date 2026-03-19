---
date: 2026-03-30
classdates: 'Monday 2026-03-30, Wednesday 2026-03-25'
draft: false
title: 'LLMs for Query Languages'
weight: 100
numsession: 10
---

This session focuses on one of the most practically important capabilities in generative AI engineering: getting large language models to produce output that machines can reliably consume. LLMs excel at generating fluent natural language, but the systems we build around them — databases, APIs, application backends — speak in strict, formal languages like SQL, SPARQL, and Cypher. Bridging this gap requires more than clever prompting. It demands an understanding of how token generation works, how formal grammars can constrain that generation, and how inference engines like Ollama support structured decoding at the architectural level.
<!--more-->
We begin by examining the general problem of structured output. When an LLM produces a JSON payload or a query string, every token must conform to a precise syntax. A single misplaced bracket or an invented column name can make the output useless. We explore the techniques that enforce correctness — from schema-guided decoding and grammar-constrained sampling to validation and self-correction loops — and discuss why relying on the model's "best effort" is insufficient for production systems.

From there, we turn to two concrete applications. The first is natural language to SQL translation, where a user poses a question in plain English and the system generates a valid SQL query against a known schema. This is one of the most widely deployed use cases for local LLMs, and we walk through the full pipeline: constructing prompts that embed schema information, constraining output to syntactically valid SQL, and validating results before execution. The second application extends the same principles to knowledge graphs, covering both the RDF/SPARQL tradition from the semantic web and the labeled property graph model popularized by Neo4j's Cypher query language. In both cases, the challenge is the same: the model must translate intent expressed in natural language into a query that is not only syntactically correct but semantically faithful to the underlying data model.

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Forcing_structured_outputs_with_constrained_decoding.m4a">
    Your browser does not support the audio element.
</audio>


### Reading
- [Structured Output from Large Language Models](../../blog/structured_llm_output/): Large language models are remarkably good at producing human-readable prose, but production software systems rarely consume prose. They consume JSON payloads, SQL queries, API responses, and typed data structures. The gap between what an LLM naturally produces and what a downstream system can parse is the central engineering challenge of structured output.
- [Generating SQL from Natural Language with Ollama](../../blog/natural_language_question_to_sql/): Natural language to SQL (text-to-SQL) is one of the most practical applications of local LLMs. This article walks through building a robust, production-quality pipeline using Ollama — from prompt construction to structured output validation and self-correction.
- [Natural Language to Graph Query Translation with Ollama](../../blog/natural_language_question_to_graph_query/): Knowledge graphs are a cornerstone of modern agentic AI systems, providing structured, semantically rich representations of domain knowledge. Two dominant paradigms exist: RDF/SPARQL, rooted in W3C semantic web standards with formal ontological reasoning, and LPG (Labeled Property Graph)/Cypher, popularized by Neo4j for its intuitive, developer-friendly model. In both cases, querying these systems requires either expert knowledge of the query language or a translation layer that converts natural language questions into executable queries.

### Notebooks
- [01_NL_to_SQL.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/QueryLanguages/notebooks/01_NL_to_SQL.ipynb) — Translates natural language to PostgreSQL using Ollama + Pydantic structured output + sqlglot validation. Uses a customers/orders/products schema with few-shot examples.
- [02_NL_to_SPARQL.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/QueryLanguages/notebooks/02_NL_to_SPARQL.ipynb) — Translates natural language to SPARQL 1.1 using OWL/Turtle TBox injection + RDFLib prepareQuery() validation. Uses a research ontology (Person, Researcher, Organization, Publication).
- [03_NL_to_Cypher.ipynb](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/QueryLanguages/notebooks/03_NL_to_Cypher.ipynb) — Translates natural language to Neo4j Cypher using LPG schema injection + Neo4j EXPLAIN validation (with offline fallback). Uses the same domain as the SPARQL notebook but in LPG form.


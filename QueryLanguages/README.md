# LLMs for Query Languages

These notebooks demonstrate practical patterns for turning natural language into machine‑reliable queries that can be safely executed by downstream systems. While large language models excel at producing fluent text, real applications depend on strict, formal languages—SQL for relational databases, SPARQL for RDF graphs, and Cypher for labeled property graphs. Each example shows how to bridge that gap using schema or ontology grounding, structured outputs, and deterministic validation layers, ensuring that LLM‑generated queries are not just readable, but syntactically valid, semantically grounded, and robust enough for production use.




### Notebooks
- [01_NL_to_SQL.ipynb](notebooks/01_NL_to_SQL.ipynb) — Translates natural language to PostgreSQL using Ollama + Pydantic structured output + sqlglot validation. Uses a customers/orders/products schema with few-shot examples.
- [02_NL_to_SPARQL.ipynb](notebooks/02_NL_to_SPARQL.ipynb) — Translates natural language to SPARQL 1.1 using OWL/Turtle TBox injection + RDFLib prepareQuery() validation. Uses a research ontology (Person, Researcher, Organization, Publication).
- [03_NL_to_Cypher.ipynb](notebooks/03_NL_to_Cypher.ipynb) — Translates natural language to Neo4j Cypher using LPG schema injection + Neo4j EXPLAIN validation (with offline fallback). Uses the same domain as the SPARQL notebook but in LPG form.

### Reading
- [Structured Output from Large Language Models](https://msa8700.molnar.ai/blog/structured_llm_output/): Large language models are remarkably good at producing human-readable prose, but production software systems rarely consume prose. They consume JSON payloads, SQL queries, API responses, and typed data structures. The gap between what an LLM naturally produces and what a downstream system can parse is the central engineering challenge of structured output.
- [Generating SQL from Natural Language with Ollama](https://msa8700.molnar.ai/blog/natural_language_question_to_sql/): Natural language to SQL (text-to-SQL) is one of the most practical applications of local LLMs. This article walks through building a robust, production-quality pipeline using Ollama — from prompt construction to structured output validation and self-correction.
- [Natural Language to Graph Query Translation with Ollama](https://msa8700.molnar.ai/blog/natural_language_question_to_graph_query/): Knowledge graphs are a cornerstone of modern agentic AI systems, providing structured, semantically rich representations of domain knowledge. Two dominant paradigms exist: RDF/SPARQL, rooted in W3C semantic web standards with formal ontological reasoning, and LPG (Labeled Property Graph)/Cypher, popularized by Neo4j for its intuitive, developer-friendly model. In both cases, querying these systems requires either expert knowledge of the query language or a translation layer that converts natural language questions into executable queries.
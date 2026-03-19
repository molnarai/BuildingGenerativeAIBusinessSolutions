---
title: "Natural Language to Graph Query Translation with Ollama"
description: "A guide for building an agentic AI pipeline that uses locally-hosted Ollama LLMs to translate natural language questions into valid SPARQL or Cypher queries against RDF and LPG knowledge graphs, covering model selection, prompt engineering, structured output enforcement, syntax validation, and production-ready Python implementations."
date: 2026-03-19
lastmod: 2026-03-19
weight: 12
---

[Knowledge graphs](../knowledge-graphs-for-agents/) are a cornerstone of modern agentic AI systems, providing structured, semantically rich representations of domain knowledge. Two dominant paradigms exist: **RDF/SPARQL**, rooted in W3C semantic web standards with formal ontological reasoning, and **LPG (Labeled Property Graph)/Cypher**, popularized by Neo4j for its intuitive, developer-friendly model. In both cases, querying these systems requires either expert knowledge of the query language or a translation layer that converts natural language questions into executable queries.

Large language models (LLMs) running locally via **Ollama** provide exactly this translation layer. Combined with structured output enforcement, syntax validation, and agentic retry loops, they form a robust pipeline that non-expert users can query in plain English while your system reliably produces valid, executable graph queries.

This article covers the full stack: model selection, prompt engineering, structured output design, validation, and production-ready Python implementations for both SPARQL and Cypher.



## Part 1: Choosing the Right Ollama Model

No Ollama model is exclusively trained for SPARQL or Cypher generation, but certain models consistently outperform others for formal query language tasks due to their code training, instruction-following capability, and context window size.

### General-Purpose Instruction Models

These models respond well to schema-injected prompts and are available directly via `ollama pull`:

| Model | Ollama Tag | Context Window | Strengths |
|---|---|---|---|
| **Qwen2.5 / Qwen3** (14B–32B) | `qwen2.5:32b` | 128K tokens | Best for large ontology injection, strong structured output |
| **Llama 3.3** (70B) | `llama3.3:70b` | 128K tokens | Strong multi-hop reasoning, reliable schema adherence |
| **Mistral / Ministral** (7B–24B) | `mistral-small` | 128K tokens | Fast, function-calling capable, good structured output |
| **DeepSeek Coder V2** | `deepseek-coder-v2` | 128K tokens | Excellent for formal query syntax, code-calibrated |

For most use cases, **Qwen2.5:32b** offers the best balance of speed, context capacity, and output quality. Its 128K context window is large enough to hold a substantial OWL ontology TBox alongside few-shot examples.

### Specialist Fine-Tuned Models

For Cypher specifically, Neo4j has released fine-tuned models based on Gemma2 9B and LLaMA 3.1 8B trained on the Text2Cypher benchmark dataset. These substantially outperform zero-shot baselines (up to a 0.34 increase in BLEU score) and can be imported into Ollama via a `Modelfile`. For SPARQL, LLaMA-3-70B and Mixtral-8x7B fine-tuned on QALD datasets are available on HuggingFace.

### Model Selection Guidance

- For **development and prototyping**: `qwen2.5:14b` or `mistral:7b` — fast iteration
- For **production with complex ontologies**: `qwen2.5:32b` or `llama3.3:70b` — accuracy over speed
- For **dedicated Cypher pipelines**: Neo4j's `text2cypher-gemma-2-9b` fine-tuned model



## Part 2: Prompt Engineering Principles

The quality of your prompt is the single dominant factor in query generation accuracy. The architecture is consistent across both use cases:

```
System Role
  └─ Task definition and output rules
  └─ Schema / Ontology Context (TBox for SPARQL, node/edge schema for Cypher)
  └─ (Optional) Few-shot NL→Query examples

User Turn
  └─ Natural language question
  └─ (On retry) Prior query + error message

Output Constraint
  └─ Structured output schema (via Pydantic + Ollama format parameter)
```

### Key Prompt Engineering Patterns

**Schema completeness**: The model can only reference what it sees. For SPARQL, inject the full TBox in Turtle or OWL/XML format. For Cypher, list every node label, its properties (with types), and every relationship type with its direction and properties. Missing schema elements lead to hallucinated class/property names.

**Negative constraints**: Explicitly state what the model must *not* do. "Return ONLY the query — no explanation, no markdown fences, no preamble" is critical without structured outputs.

**Few-shot examples**: Including 2–3 domain-specific NL→Query pairs in the system prompt can improve correctness by 15–30% on complex multi-hop queries. Place them after the schema definition.

**Chain-of-thought for complex queries**: For queries involving multi-hop traversals or aggregations, prepend `"Think step by step about which nodes and relationships are involved, then write the query."` This is especially effective for SPARQL CONSTRUCT and multi-MATCH Cypher patterns.

**Error-aware retry prompting**: When a query fails validation, inject the exact error message back into the next prompt. This gives the model specific, actionable feedback rather than a vague retry signal.



## Part 3: Structured Outputs with Ollama

### What Structured Output Is

Ollama implements structured output via **grammar-constrained token sampling** using llama.cpp's grammar engine. Rather than instructing the model to produce JSON and hoping it complies, the sampler masks invalid tokens at the logit level during generation. The model physically cannot produce tokens that violate your defined schema. This is fundamentally more reliable than JSON mode, which only checked that output was parseable JSON without enforcing field names, types, or enumerations.

### Why It Matters for Query Pipelines

Without structured output, your pipeline must:
1. Strip markdown fences (` ```sparql ... ``` `)
2. Trim leading/trailing prose
3. Catch JSON parse errors
4. Handle inconsistent field naming

With structured output, `model_validate_json(response.message.content)` either succeeds or raises a clear Pydantic validation error. The query is directly usable.

### Benefits Summary

- **Schema enforcement**: Field names, types, and enum values are guaranteed — not merely "probably correct"
- **No post-processing fragility**: No regex, no strip(), no try/except JSON parsing
- **Metadata for free**: You can add fields like `query_type`, `classes_used`, `explanation` at zero prompt cost — the grammar enforces them
- **Deterministic integration**: Combined with `temperature=0`, downstream agents receive machine-readable payloads unconditionally

### Important Caveats

- Grammar-constrained sampling adds measurable latency on large schemas since it is not GPU-parallelized in llama.cpp
- Deeply nested or recursive `$ref` schemas have known bugs in some Ollama versions — keep output schemas flat
- If the model halts mid-stream unexpectedly, the output may be incomplete despite the grammar constraint



## Part 4: Validating Generated Queries

### SPARQL Validation with RDFLib

RDFLib's `prepareQuery()` function parses and compiles a SPARQL query against the SPARQL 1.1 grammar without executing it. It is the closest equivalent to SQLGlot for SPARQL — pure Python, no server required, suitable for CI/CD pipelines.

```python
from rdflib.plugins.sparql import prepareQuery

def validate_sparql(query: str) -> tuple[bool, str]:
    try:
        prepareQuery(query)
        return True, "Valid"
    except Exception as e:
        return False, str(e)
```

For more rigorous validation (e.g., in CI), Apache Jena's `arq` CLI provides full SPARQL 1.1/1.2 validation:

```bash
arq --query myquery.sparql --syntax
```

### Cypher Validation with Neo4j EXPLAIN

Neo4j's `EXPLAIN` prefix parses and plans a query without executing it — zero data is read or written. It returns detailed parse errors including line/column positions, making it ideal for error-feedback loops.

```python
from neo4j import GraphDatabase
from neo4j.exceptions import CypherSyntaxError

def validate_cypher(driver, query: str) -> tuple[bool, str]:
    try:
        with driver.session() as session:
            session.run(f"EXPLAIN {query}").consume()
        return True, "Valid"
    except CypherSyntaxError as e:
        return False, str(e)
    except Exception as e:
        # Fail open if Neo4j is temporarily unreachable
        return True, f"Skipped: {e}"
```

For offline Cypher validation without a running Neo4j instance, the openCypher project provides an ANTLR4 grammar usable with `antlr4-python3-runtime`.



## Part 5: Complete Python Implementation — NL → SPARQL

This implementation covers TBox injection, structured output generation, RDFLib validation, retry on failure, and execution against an Apache Jena Fuseki endpoint.

```python
import requests
from pydantic import BaseModel
from rdflib.plugins.sparql import prepareQuery
from ollama import chat

# ── TBox Ontology (inject your full OWL/Turtle TBox here) ─────────────────────

TBOX_TURTLE = """
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <http://example.org/ontology#> .

### Classes
ex:Person        a owl:Class .
ex:Researcher    a owl:Class ; rdfs:subClassOf ex:Person .
ex:Organization  a owl:Class .
ex:Publication   a owl:Class .

### Object Properties
ex:worksAt        a owl:ObjectProperty ;
                  rdfs:domain ex:Person ;
                  rdfs:range  ex:Organization .
ex:authored       a owl:ObjectProperty ;
                  rdfs:domain ex:Researcher ;
                  rdfs:range  ex:Publication .
ex:affiliatedWith a owl:ObjectProperty ;
                  rdfs:domain ex:Publication ;
                  rdfs:range  ex:Organization .

### Datatype Properties
ex:name      a owl:DatatypeProperty ; rdfs:range xsd:string .
ex:birthYear a owl:DatatypeProperty ; rdfs:range xsd:integer .
ex:title     a owl:DatatypeProperty ; rdfs:range xsd:string .
ex:year      a owl:DatatypeProperty ; rdfs:range xsd:integer .
ex:industry  a owl:DatatypeProperty ; rdfs:range xsd:string .
ex:founded   a owl:DatatypeProperty ; rdfs:range xsd:integer .
"""

# ── System Prompt ─────────────────────────────────────────────────────────────

SPARQL_SYSTEM_PROMPT = f"""You are an expert SPARQL 1.1 query generator for RDF knowledge graphs.
Given an OWL/Turtle ontology TBox and a natural language question, generate a valid SPARQL query.

Rules:
- Use ONLY the classes and properties defined in the TBox
- Always declare PREFIX statements at the top
- Use OPTIONAL {{ }} for properties that may not exist on all instances
- Use FILTER for conditions on literals
- Use SELECT DISTINCT unless aggregation is required
- For aggregations, use GROUP BY with the appropriate aggregate function

Ontology TBox (Turtle format):
{TBOX_TURTLE}

Examples:
Q: Who are all the researchers?
SPARQL:
PREFIX ex: <http://example.org/ontology#>
SELECT DISTINCT ?name WHERE {{
  ?r a ex:Researcher ; ex:name ?name .
}}

Q: Which organizations are in the healthcare industry?
SPARQL:
PREFIX ex: <http://example.org/ontology#>
SELECT DISTINCT ?orgName WHERE {{
  ?o a ex:Organization ; ex:industry "healthcare" ; ex:name ?orgName .
}}
"""

# ── Structured Output Schema ──────────────────────────────────────────────────

class SPARQLResult(BaseModel):
    query: str               # Full SPARQL query including PREFIX declarations
    query_type: str          # "SELECT" | "ASK" | "CONSTRUCT" | "DESCRIBE"
    classes_used: list[str]  # TBox classes referenced, e.g. ["ex:Researcher"]
    explanation: str         # One-sentence description of what the query does

# ── Validation ────────────────────────────────────────────────────────────────

def validate_sparql(query: str) -> tuple[bool, str]:
    try:
        prepareQuery(query)
        return True, "Valid"
    except Exception as e:
        return False, str(e)

# ── Generation with Retry Loop ────────────────────────────────────────────────

def nl_to_sparql(
    question: str,
    model: str = "qwen2.5:32b",
    max_retries: int = 3
) -> SPARQLResult:
    error_context = ""

    for attempt in range(1, max_retries + 1):
        user_content = f"Question: {question}"
        if error_context:
            user_content += (
                f"\n\nYour previous attempt produced an invalid SPARQL query.\n"
                f"Error: {error_context}\n"
                f"Please correct the query."
            )

        response = chat(
            model=model,
            messages=[
                {"role": "system", "content": SPARQL_SYSTEM_PROMPT},
                {"role": "user",   "content": user_content}
            ],
            format=SPARQLResult.model_json_schema(),
            options={"temperature": 0.0}
        )

        result = SPARQLResult.model_validate_json(response.message.content)
        is_valid, error = validate_sparql(result.query)

        print(f"  [Attempt {attempt}] {'✓ Valid' if is_valid else f'✗ {error}'}")

        if is_valid:
            return result
        error_context = error

    raise ValueError(f"Failed to generate valid SPARQL after {max_retries} attempts.")

# ── Execute Against Apache Jena Fuseki ────────────────────────────────────────

def run_sparql(
    query: str,
    endpoint: str = "http://localhost:3030/ds/sparql"
) -> list[dict]:
    resp = requests.get(
        endpoint,
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=30
    )
    resp.raise_for_status()
    bindings = resp.json().get("results", {}).get("bindings", [])
    return [{k: v["value"] for k, v in row.items()} for row in bindings]

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    questions = [
        "List all researchers and the organizations they work at.",
        "How many publications were authored by researchers in the AI industry?",
        "Find all publications affiliated with organizations founded before 2000.",
    ]

    for q in questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        result = nl_to_sparql(q)
        print(f"Type       : {result.query_type}")
        print(f"Classes    : {result.classes_used}")
        print(f"Explanation: {result.explanation}")
        print(f"Query:\n{result.query}")

        # Uncomment to run against a live Fuseki endpoint:
        # rows = run_sparql(result.query)
        # for row in rows:
        #     print(row)
```

### Example Output

For the question *"How many publications were authored by researchers in the AI industry?"*, the structured output would be:

```json
{
  "query": "PREFIX ex: <http://example.org/ontology#>\nSELECT (COUNT(DISTINCT ?pub) AS ?pubCount)\nWHERE {\n  ?r a ex:Researcher ;\n     ex:worksAt ?org ;\n     ex:authored ?pub .\n  ?org ex:industry \"AI\" .\n}",
  "query_type": "SELECT",
  "classes_used": ["ex:Researcher", "ex:Organization", "ex:Publication"],
  "explanation": "Counts distinct publications authored by researchers at organizations in the AI industry."
}
```



## Part 6: Complete Python Implementation — NL → Cypher

This implementation covers LPG schema injection, structured Cypher generation, Neo4j `EXPLAIN` validation, and retry on parse failure.

```python
from pydantic import BaseModel
from neo4j import GraphDatabase
from neo4j.exceptions import CypherSyntaxError
from ollama import chat

# ── LPG Schema ────────────────────────────────────────────────────────────────

LPG_SCHEMA = """
Node Labels:
- Person(id: STRING, name: STRING, birthYear: INT, role: STRING)
- Organization(id: STRING, name: STRING, industry: STRING, founded: INT)
- Publication(id: STRING, title: STRING, year: INT, doi: STRING)

Relationship Types:
- (Person)-[:WORKS_AT {since: INT, position: STRING}]->(Organization)
- (Person)-[:AUTHORED {contribution: STRING}]->(Publication)
- (Person)-[:COLLABORATES_WITH]->(Person)
- (Organization)-[:FUNDED]->(Publication)
"""

# ── System Prompt ─────────────────────────────────────────────────────────────

CYPHER_SYSTEM_PROMPT = f"""You are an expert Neo4j Cypher query generator.
Given a graph schema and a natural language question, generate a valid, executable Cypher query.

Rules:
- Use ONLY the node labels, properties, and relationship types defined in the schema
- Use MATCH...WHERE...RETURN structure
- Prefer OPTIONAL MATCH for potentially absent relationships
- Use WITH for intermediate aggregations
- Use ORDER BY and LIMIT where appropriate

Graph Schema:
{LPG_SCHEMA}

Examples:
Q: Find all people who work in the technology industry.
Cypher:
MATCH (p:Person)-[:WORKS_AT]->(o:Organization)
WHERE o.industry = "technology"
RETURN p.name, p.role, o.name AS organization

Q: Which people have authored publications?
Cypher:
MATCH (p:Person)-[:AUTHORED]->(pub:Publication)
RETURN DISTINCT p.name, collect(pub.title) AS publications
"""

# ── Structured Output Schema ──────────────────────────────────────────────────

class CypherResult(BaseModel):
    query: str                    # Full executable Cypher query
    query_intent: str             # "MATCH" | "AGGREGATION" | "PATH" | "EXISTENCE"
    node_labels_used: list[str]   # e.g. ["Person", "Organization"]
    relationships_used: list[str] # e.g. ["WORKS_AT", "AUTHORED"]
    explanation: str              # One-sentence description

# ── Validator ─────────────────────────────────────────────────────────────────

class CypherValidator:
    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "password"
    ):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def validate(self, query: str) -> tuple[bool, str]:
        try:
            with self.driver.session() as session:
                session.run(f"EXPLAIN {query}").consume()
            return True, "Valid"
        except CypherSyntaxError as e:
            return False, str(e)
        except Exception as e:
            # Fail open on connectivity issues — don't block the pipeline
            print(f"  Warning: Neo4j unreachable, skipping validation: {e}")
            return True, "Skipped (no connection)"

    def run(self, query: str) -> list[dict]:
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]

    def close(self):
        self.driver.close()

# ── Generation with Retry Loop ────────────────────────────────────────────────

def nl_to_cypher(
    question: str,
    validator: CypherValidator,
    model: str = "qwen2.5:32b",
    max_retries: int = 3
) -> CypherResult:
    error_context = ""

    for attempt in range(1, max_retries + 1):
        user_content = f"Question: {question}"
        if error_context:
            user_content += (
                f"\n\nYour previous attempt produced an invalid Cypher query.\n"
                f"Error: {error_context}\n"
                f"Please correct the query."
            )

        response = chat(
            model=model,
            messages=[
                {"role": "system", "content": CYPHER_SYSTEM_PROMPT},
                {"role": "user",   "content": user_content}
            ],
            format=CypherResult.model_json_schema(),
            options={"temperature": 0.0}
        )

        result = CypherResult.model_validate_json(response.message.content)
        is_valid, error = validator.validate(result.query)

        print(f"  [Attempt {attempt}] {'✓ Valid' if is_valid else f'✗ {error}'}")

        if is_valid:
            return result
        error_context = error

    raise ValueError(f"Failed to generate valid Cypher after {max_retries} attempts.")

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    validator = CypherValidator(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="your-password"
    )

    questions = [
        "Who are all the people working at organizations in the AI industry?",
        "Find all publications authored by researchers who collaborate with each other.",
        "Which organizations have funded more than 5 publications since 2020?",
    ]

    try:
        for q in questions:
            print(f"\n{'='*60}")
            print(f"Q: {q}")
            result = nl_to_cypher(q, validator)
            print(f"Intent        : {result.query_intent}")
            print(f"Nodes         : {result.node_labels_used}")
            print(f"Relationships : {result.relationships_used}")
            print(f"Explanation   : {result.explanation}")
            print(f"Query:\n{result.query}")

            # Uncomment to execute against a live Neo4j instance:
            # rows = validator.run(result.query)
            # for row in rows:
            #     print(row)
    finally:
        validator.close()
```

### Example Output

For *"Which organizations have funded more than 5 publications since 2020?"*, the structured output would be:

```json
{
  "query": "MATCH (o:Organization)-[:FUNDED]->(pub:Publication)\nWHERE pub.year >= 2020\nWITH o, COUNT(pub) AS pubCount\nWHERE pubCount > 5\nRETURN o.name, pubCount\nORDER BY pubCount DESC",
  "query_intent": "AGGREGATION",
  "node_labels_used": ["Organization", "Publication"],
  "relationships_used": ["FUNDED"],
  "explanation": "Finds organizations that have funded more than 5 publications from 2020 onward, sorted by count."
}
```



## Part 7: Production Considerations

### TBox Chunking for Large Ontologies

If your OWL ontology is large (hundreds of classes and properties), injecting the full TBox into every prompt is wasteful and risks exceeding context limits on smaller models. A better strategy is a **lightweight RAG step over the TBox**:

1. Parse your OWL/Turtle file with RDFLib and extract all class/property definitions as text chunks
2. Embed them with a local embedding model (e.g., `nomic-embed-text` via Ollama)
3. At query time, retrieve the top-K most relevant chunks based on the user question
4. Inject only those chunks into the prompt

This reduces prompt size, lowers latency, and improves accuracy by reducing noise from irrelevant schema elements.

### Integrating with Your Agentic Framework

Both pipelines integrate naturally into LangGraph, AutoGen, or n8n:

- **LangGraph**: Each `nl_to_sparql` / `nl_to_cypher` call becomes a node; the validation retry loop is a conditional edge back to the generation node
- **n8n**: The Ollama HTTP node handles generation; a Code node performs validation; a loop node manages retries
- **Observability**: The `explanation`, `classes_used`, and `relationships_used` fields from structured output are ideal payloads for your Tempo traces and Loki log entries

### Tooling Comparison

| Concern | SPARQL | Cypher |
|---|---|---|
| **Python validator** | `rdflib.plugins.sparql.prepareQuery` | Neo4j driver `EXPLAIN` |
| **Offline validator** | Apache Jena `arq --syntax` CLI | openCypher ANTLR4 grammar |
| **IDE support** | YASGUI, VS Code RDF extensions | Neo4j Browser, VS Code Neo4j extension |
| **Fine-tuned models** | LLaMA-3 / Mixtral on QALD datasets | Neo4j text2cypher-gemma-2-9b |
| **Schema injection** | OWL/Turtle TBox (full or RAG-chunked) | Node labels + relationship types |
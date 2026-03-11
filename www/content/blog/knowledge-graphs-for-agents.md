---
draft: false
title: Knowledge Graphs for Agents
weight: 30
description: Overview of Knowledge Graphs in the Context of Agentic AI
date: 2024-01-01
lastmod: 2024-01-01
---

# Knowledge Graphs for Agentic Systems - Overview

### 1. Introduction: Why Knowledge Graphs Matter

Modern AI agents often generate fluent but shallow responses. Knowledge graphs (KGs) introduce **structured, semantically grounded knowledge** that enables agents to reason, check consistency, and retrieve facts — all grounded in explicit relationships.
In agentic systems, KGs play a role similar to a **semantic memory**: a persistent, queryable structure that captures *entities*, *relationships*, and *context* over time.

***

### 2. Core Graph Concepts

**Graphs** are mathematical structures used to model relationships among objects.

- **Vertices (Nodes)**: Represent entities or objects — e.g., *Person*, *Company*, *Location*.
- **Edges (Links)**: Represent relationships between entities — e.g., *works_at*, *founded*, *is_located_in*.

**Graph types:**

- **Directed graphs**: Edges have direction (A → B). Example: *Alice → works_at → Google*.
- **Undirected graphs**: Relationships are symmetrical (A—B). Example: *Alice — married_to — Bob*.
- **Weighted graphs**: Edges have numerical weights, indicating strength or confidence. Useful for ranking facts or encoding probabilities in uncertain data.

**Example illustration:**

If we take the sentence *“Alan Turing worked at Bletchley Park during WWII,”* a simple graph representation would be:

- Vertices: *Alan Turing*, *Bletchley Park*, *WWII*
- Edges:
    - *(Alan Turing) —worked_at→ (Bletchley Park)*
    - *(Alan Turing) —active_during→ (WWII)*

***

### 3. Building a Knowledge Graph

There are several approaches to constructing knowledge graphs, depending on the source and structure of available data.

#### (a) From Structured Data

- Use databases, CSVs, or APIs that already have well-defined schema.
- Convert tabular or relational data into triples: *(entity, relation, entity/value)*.
Example: SQL `employees` table → *(Alice, works_at, Google)*.


#### (b) From Semi-structured Data

- Extract information from sources like JSON, XML, or infoboxes (e.g., Wikipedia).
- Use schema mapping to align fields with ontology terms (e.g., “founder” → *hasFounder*).


#### (c) From Unstructured Text (Document-Derived KGs)

- Apply NLP pipelines to extract:
    - **Named entities** (NER): people, organizations, locations.
    - **Relations** (RE): verbs or prepositional phrases linking entities.
    - **Coreference resolution**: unify references like “he” and “Turing”.
- LLMs can generate semantic triples or structured JSON via prompt templates such as:
*“Extract entities and their relationships as subject–predicate–object triples.”*
- Store extracted triples in a **graph database** such as Neo4j, GraphDB, or RDF-based store.

***

### 4. Ontologies and Schema Design

A **knowledge graph** is not just a collection of triples — it also has a **schema** defining:

- **Classes (Types)**: What kind of entities exist (Person, Organization, Event).
- **Relations (Predicates)**: Allowed edges and their semantics.
- **Constraints**: Domain/range typing, cardinalities, inheritance.

This allows **semantic reasoning** — inferring new facts from known ones (e.g., via RDF Schema or OWL reasoning).

***

### 5. Using Knowledge Graphs in Agentic AI Systems

Agentic AI systems orchestrate multiple tools or reasoning steps. KGs empower them in several key ways:

#### (a) Retrieval-Augmented Reasoning

- The agent uses the KG as a **fact repository** to ground responses or validate LLM output.
- Example: Before answering “Who founded DeepMind?”, the agent queries KG → returns “Demis Hassabis”.


#### (b) Contextual Memory and State Tracking

- The KG maintains long-term memory across multiple interactions.
- Example: In a conversational system, nodes track “user preferences” or “past tasks”.


#### (c) Multi-agent Collaboration

- Agents share structured knowledge via a shared KG workspace.
- Example: A “research agent” adds verified facts; a “summary agent” consumes them to generate reports.


#### (d) Reasoning and Inference

- Graph algorithms (shortest path, PageRank, neighborhood clustering) help determine relevance or influence.
- Logical reasoners can infer new relationships:
If *(Turing, worked_at, Bletchley Park)* and *(Bletchley Park, located_in, UK)* ⇒ *(Turing, worked_in, UK)*.

***

### 6. Integrating LLMs and Knowledge Graphs

The modern fusion of LLMs and KGs can take several patterns:

- **KG-Augmented RAG**: LLM queries KG to retrieve nodes relevant to a question, grounding answers with factual context.
- **LLM-to-KG Extraction**: LLM parses new documents, meetings, or chats to expand the KG dynamically.
- **Graph Embeddings**: Use algorithms like Node2Vec, TransE, or Graph Neural Networks to represent nodes and edges in vector space for similarity search.
- **KG as Context Builder**: LLM injects KG-derived relational context into prompts to improve coherence and factuality.

***

### 7. Example: Agentic Workflow with a Knowledge Graph

**Scenario:** “A research assistant agent helps summarize academic papers.”

1. **Document ingestion**: LLM extracts concepts, authors, institutions, and relationships.
2. **KG update**: Stores triples like *(Paper X, written_by, Author Y)*, *(Author Y, affiliated_with, University Z)*.
3. **Query phase**: When asked “Which universities collaborate on graph representation learning?”,
the agent traverses relationships in the KG to find co-authorship or shared projects.
4. **Answer generation**: The agent cites results with grounding retrieved from the graph.

***

### 8. Tools and Frameworks

- **Graph Databases**: Neo4j, GraphDB, ArangoDB, JanusGraph.
- **RDF/Linked Data**: Apache Jena, Stardog, Blazegraph.
- **Extraction Pipelines**: spaCy, OpenIE, Stanford CoreNLP, LLM-based wrappers (LangChain, Haystack).
- **Visualization**: Graphistry, Gephi, Neo4j Bloom, or custom D3.js tools.

***

### 9. Key Takeaways

- Knowledge graphs make implicit relationships explicit — forming a durable foundation for reasoning, retrieval, and memory in agentic systems.
- Combine LLM-driven unstructured information extraction with graph databases for persistent, explainable knowledge.
- In multi-agent environments, KGs serve as **shared world models** — enabling collaboration, grounding, and continuous learning.


---

# Creating Triples from Text

Triples from text can be created with fairly different pipelines depending on whether you rely on “classic” NLP (e.g., spaCy + RE models) or prompt an LLM directly; in practice, the best systems often hybridize both.[^2_1][^2_2][^2_3]

***

## What a “triple extraction” pipeline does

Goal: from raw text, produce triples of the form
$(\text{subject}, \text{predicate}, \text{object})$ plus optional attributes (time, source span, confidence).

Canonical stages:

1. Sentence segmentation and tokenization.
2. Entity detection and normalization.
3. Relation extraction between entity pairs.
4. Optional: entity linking to a canonical ID and ontology alignment.[^2_3][^2_4]

These stages are implemented differently in an NLP-centric vs LLM-centric stack.

***

## Traditional NLP / spaCy-based pipelines

### Typical architecture

1. **NER with spaCy (possibly custom-trained)**
    - Detect domain entities (PERSON, ORG, custom biomedical types, etc.).
    - Prodigy/other tools used to annotate and train domain NER.[^2_2][^2_3]
2. **Dependency- or pattern-based relation extraction**
    - Use dependency parses and POS tags to identify verb/preposition patterns between entities.
    - Approaches:
        - Hand-written patterns over parse trees or token sequences.
        - A supervised RE model (e.g., spaCy’s `SpanCategorizer` or a separate transformer) trained to classify relations for candidate entity pairs.[^2_5][^2_3]
3. **Entity linking and ontology mapping**
    - Map surface strings to ontology concepts (e.g., via a dictionary, BM25 search, or a linking model).
    - Attach ontology predicates, e.g., map “founded” → `hasFounder`.[^2_4][^2_3]
4. **Triple construction**
    - For each recognized relation between entity spans, emit:
$(\text{subject\_ID}, \text{relation\_URI}, \text{object\_ID})$ plus provenance (sentence, offsets, confidence).[^2_4]

### Strengths

- **Predictability and control**
    - Rules and model behavior are inspectable; deterministic components behave stably.
    - Easy to enforce schema constraints (only allowed relations, domains, ranges).[^2_6][^2_3]
- **High precision in narrow domains**
    - With a well-annotated corpus and domain-specific NER/RE, precision is very high for recurring patterns (e.g., biomedical, finance).[^2_6][^2_4]
- **Cheaper and easier to run at scale**
    - spaCy pipelines are fast, CPU-friendly, and easy to deploy in batch ETL workflows.[^2_7][^2_2]


### Weaknesses

- **Coverage and recall**
    - Hand-crafted rules and supervised RE don’t generalize well beyond annotated patterns, so many implicit or unusual relations are missed.[^2_5][^2_4]
- **Annotation cost and rigidity**
    - Building good NER/RE/linking models requires substantial labeled data; adapting to a new domain means more annotation.[^2_3][^2_4]
- **Limited abstraction**
    - Models struggle with long-range dependencies, discourse-level relations, or relations not signaled by simple local patterns.[^2_7][^2_6]

***

## LLM-centric triple extraction

### Core patterns

1. **Single-pass instruction prompting**
    - Prompt an LLM with a passage and ask for triples in a specified JSON or RDF-like format.
    - Example: “Return a list of subject–predicate–object triples, using verbs or relation phrases as predicates.”[^2_8][^2_9]
2. **Two-step or multi-step extraction**
    - Step 1: extract entities and type them.
    - Step 2: given the entities and text, extract relations between named entities.
    - This has been used in systems like KGGen to keep entities consistent across triples.[^2_1]
3. **LLM-based clustering and refinement**
    - After initial triples, an LLM is used again to cluster nodes referring to the same entity, collapse duplicates, and clean predicates.[^2_1]
4. **Specialized “text-to-triple” models**
    - Some frameworks (e.g., Triplex, KG-LLM) train or tune models specifically to convert text into triples or to complete triples (knowledge graph completion).[^2_10]

### Strengths

- **High recall and semantic coverage**
    - LLMs can capture implicit, paraphrased, or long-range relations and handle open-schema predicates (“inspired by”, “criticized”, etc.).[^2_10][^2_6][^2_1]
- **Low setup cost and rapid prototyping**
    - No need for labeled training data; you can get usable triples from well-engineered prompts plus a small calibration set.[^2_9][^2_11][^2_8]
- **Flexible schema and ontology handling**
    - LLMs can map surface text to ontology predicates or generate candidate predicates aligned to a schema via prompt constraints.
    - They are also used to validate or classify triples as likely true/false, acting as KG curators.[^2_12][^2_10]
- **Rich attributes and event structures**
    - Easy to ask for temporal qualifiers, sentiment, modality (“believed”, “alleged”), and n-ary relations in a single call.[^2_10][^2_1]


### Weaknesses

- **Hallucinations and factual drift**
    - LLMs may invent entities or relations not supported by the input text, especially if prompts are broad or context windows are large.[^2_6][^2_10]
- **Stability and reproducibility**
    - Output can vary with small prompt changes, model version, or sampling parameters, making strict ETL-style pipelines harder to guarantee.[^2_11][^2_6]
- **Cost and latency**
    - Large volumes of text require significant compute and cost; careful batching and segmentation are needed.[^2_13][^2_8]
- **Schema enforcement is indirect**
    - You constrain the model via prompts; hard guarantees require a downstream validation step (often with additional rules or models).[^2_12][^2_10]

***

## Direct comparison: spaCy-style NLP vs LLMs

### Methodological differences

| Aspect | spaCy / traditional NLP | LLM-based extraction |
| :-- | :-- | :-- |
| Entity detection | NER models over tokens and spans, trained per domain [^2_2][^2_3] | Prompted recognition with implicit type knowledge [^2_1][^2_9] |
| Relation extraction | Dependency patterns, rule-based grammars, supervised RE [^2_5][^2_3] | Natural-language instructions; model infers relations end-to-end [^2_1][^2_8] |
| Schema integration | Explicit: predicates hard-coded or trained; strict types [^2_4][^2_3] | Implicit: prompt describes ontology; LLM maps raw relations to it [^2_1][^2_10] |
| Data requirements | Needs labeled examples for NER/RE/linking [^2_3][^2_4] | Can work zero/few-shot with prompts and a few exemplars [^2_1][^2_11] |
| Precision vs recall | High precision, lower recall outside training domain [^2_4][^2_6] | Higher recall and coverage, but risk of hallucination [^2_1][^2_10][^2_6] |
| Scalability \& cost | Fast, cheap, good for large corpora [^2_2][^2_7] | Slower, more expensive per token [^2_8][^2_13] |
| Interpretability | Transparent rules and limited models [^2_5][^2_3] | Black-box; behavior guided by prompts but hard to fully predict [^2_6][^2_12] |


***

## Hybrid pipelines (often best for agentic systems)

Many recent practical recipes combine both, leveraging spaCy for **robust low-level structure** and LLMs for **semantic flexibility**.[^2_2][^2_3]

Common hybrid patterns:

1. **spaCy for entities, LLM for relations**
    - spaCy extracts all entities and sentence boundaries.
    - For each sentence (or small context window), you send the text plus entity spans to an LLM, asking it to propose relations only among those entities.
    - This constrains the search space and reduces hallucinated entities.[^2_2][^2_1]
2. **spaCy + RE model, LLM for cleaning and ontology alignment**
    - Use rule/supervised RE to get initial triples.
    - Then use an LLM to:
        - Normalize entity labels.
        - Map free-text predicates onto your ontology.
        - Discard or down-rank low-quality triples.[^2_12][^2_1]
3. **LLM-first, spaCy/regex for verification**
    - LLM emits triples.
    - Validation layer checks that subject and object actually appear in the source text (using token spans, regex, or NER) and rejects triples where they don’t.[^2_1][^2_10]
4. **Annotation bootstrapping**
    - Use LLMs to generate noisy labels (entities and relations) for a corpus.
    - Clean a subset manually and train spaCy models on this to get cheaper, stable extraction for large-scale processing.[^2_3][^2_6]

For agentic systems, the hybrid pattern also lets different **agents specialize**: a parsing agent using spaCy, an extraction agent using an LLM, and a curation agent validating triples.

***

## How choice of method impacts agentic QA over a KG

When the resulting KG is used in an agentic QA or planning pipeline:

- **spaCy-first graphs**
    - Pros:
        - Fewer spurious edges, more reliable for deterministic reasoning (shortest paths, rule-based inference).
        - Better where compliance and traceability are critical (e.g., biomedical, legal).[^2_4][^2_12]
    - Cons:
        - Graph can be sparse; agents may fail to find connecting paths, leading to more “no answer” situations.
- **LLM-first graphs**
    - Pros:
        - Denser connectivity; agents can discover many paths and explanations.
        - Better at modeling vague or narrative relationships, useful for exploratory analysis.[^2_10][^2_1]
    - Cons:
        - Need triple-level validation; otherwise agents may follow hallucinated edges.[^2_12][^2_10]

A typical **agentic QA loop** with a KG:

1. Retrieval agent: queries KG for candidate entities/paths.
2. Validation/curation agent: checks key triples using an LLM as a truthiness filter.[^2_12]
3. Answer-generation agent: conditions on both KG evidence and raw text snippets (RAG + KG).

The more “surgical” and high-precision your triple extraction (spaCy-heavy), the more you’ll depend on fallback text search; the more “wide” and LLM-heavy you go, the more you must invest in validation agents and confidence scoring.


<span style="display:none">[^2_14][^2_15]</span>



[^2_1]: https://arxiv.org/html/2502.09956v1

[^2_2]: https://memgraph.com/blog/extract-entities-build-knowledge-graph-memgraph-spacy

[^2_3]: https://support.prodi.gy/t/text-to-knowledge-graph-prodigy-spacy/4521

[^2_4]: https://fairplus.github.io/the-fair-cookbook/content/recipes/interoperability/nlp2kg/creating-knowledge-graph-from-text.html

[^2_5]: https://stackoverflow.com/questions/57291975/how-can-i-provide-a-relation-extraction-data-set-including-tuple-for-casual-infe

[^2_6]: https://labs.lamatic.ai/p/llm-vs-nlp/

[^2_7]: https://corp.yonyx.com/customer-service/nlp-vs-llm/

[^2_8]: https://build.nvidia.com/spark/txt2kg

[^2_9]: https://github.com/robert-mcdermott/ai-knowledge-graph

[^2_10]: https://www.lettria.com/lettria-lab/introduction-to-knowledge-graph-completion-with-llms

[^2_11]: https://www.linkedin.com/pulse/building-knowledge-graphs-using-llms-yugank-aman-v7jaf

[^2_12]: https://aclanthology.org/2025.genaik-1.10.pdf

[^2_13]: https://www.youtube.com/watch?v=8iA_f_UpzHc

[^2_14]: https://www.reddit.com/r/MachineLearning/comments/1opohcg/p_generating_knowledge_graphs_from_unstructured/

[^2_15]: https://www.astera.com/type/blog/nlp-vs-llm/


---

# Ontologies Deep-dive

An ontology is the **formal semantic blueprint** of a domain: it defines the classes of things that exist, their properties, and the admissible relationships and constraints between them, providing shared meaning for a knowledge graph.[^3_1][^3_2]

***

## What an ontology is (and is not)

- **Definition**
    - An ontology is a *formal, explicit specification of a shared conceptualization* of a domain.[^3_3][^3_2]
    - It defines:
        - Classes (types of entities).
        - Properties (attributes, relations).
        - Constraints and rules (domains, ranges, cardinalities, logical axioms).[^3_4][^3_1]
- **Ontology vs. knowledge graph**
    - Ontology: describes *what kinds of things and relations are allowed* and what they mean.
    - Knowledge graph: concrete facts instantiating that schema (ontology + data = KG).[^3_2][^3_5]
- **Role in agentic systems**
    - Acts as the semantic backbone that standardizes what agents mean by “customer”, “order”, “adverse event”, etc., enabling consistent retrieval, reasoning, and tool interoperability.[^3_6][^3_4]

**Mini example** (e‑commerce):

- Classes: `Product`, `Customer`, `Order`.
- Object properties: `placesOrder(Customer → Order)`, `containsProduct(Order → Product)`.
- Data properties: `hasPrice(Product → decimal)`, `orderDate(Order → date)`.[^3_1][^3_4]

***

## Examples of ontologies

- **FOAF (Friend of a Friend)**
    - Models people, organizations, online accounts, and their social links, with classes like `foaf:Person` and properties such as `foaf:knows`, `foaf:homepage`.[^3_5]
- **SNOMED CT / biomedical ontologies**
    - Large, hierarchically structured ontologies of diseases, procedures, and findings, enabling semantic interoperability in EHRs.[^3_7]
- **Enterprise product ontology**
    - Classes: `Product`, `Service`, `Category`, `Brand`.
    - Hierarchy: `Laptop ⊑ ElectronicDevice`, `Shoes ⊑ Apparel`.
    - Constraints: `offers(Service) ⊑ Organization × Service`.[^3_4][^3_6]

These ontologies are usually expressed in OWL/RDF or similar formalisms to support machine reasoning.[^3_5][^3_1]

***

## Process of creating an ontology

A practical ontology engineering process usually follows these steps.[^3_8][^3_5]

1. **Scope and purpose**
    - Identify *why* you need the ontology: search, analytics, integration, regulatory reporting, etc.
    - Define boundaries: what is in scope vs. out of scope.[^3_8]
2. **Gather requirements (competency questions)**
    - Write natural-language questions the ontology must support, e.g., “Which drugs interact with medication X?” or “Which customers purchased product Y last quarter?”.
    - These “competency questions” guide what classes and properties you need.[^3_9][^3_8]
3. **Concept and relation elicitation**
    - Collect candidate concepts and relations from domain experts, documents, and existing schemas/standards.
    - Group them into tentative classes, attributes, and relations.[^3_4][^3_8]
4. **Design the class hierarchy (TBox)**
    - Define classes and subclass relations (taxonomic backbone).
    - Prefer clear, single-inheritance where possible; use multiple inheritance sparingly.[^3_8][^3_4]
5. **Define properties and constraints**
    - Object properties (links between individuals), data properties (literals).
    - Add domain and range, cardinalities, inverse properties, symmetry, transitivity where needed.[^3_1][^3_4]
6. **Align with existing ontologies**
    - Reuse or map to standards (e.g., Schema.org, SNOMED, industry vocabularies) instead of reinventing.[^3_5][^3_8]
7. **Populate with sample instances and test competency questions**
    - Create example individuals and assert facts.
    - Use a reasoner to check if the ontology answers the competency questions and is logically consistent.[^3_8]
8. **Iterative refinement and governance**
    - Review with domain experts, capture change requests, manage versions, and set up governance processes for ongoing extension.[^3_6][^3_8]

***

## What to focus on (and common pitfalls)

### Key design focuses

- **Clarity and shared meaning**
    - Term names and definitions must be unambiguous and agreed upon across stakeholders.[^3_6][^3_8]
- **Modularity**
    - Prefer smaller, “plug‑and‑play” ontologies that can be composed, rather than one monolith; this improves maintainability and governance.[^3_8]
- **Balance expressivity vs. complexity**
    - Only use as much OWL expressivity as you need; overly complex axioms can make reasoning slow and the ontology fragile.[^3_8]
- **Alignment with real-world use cases**
    - Every modeling decision should be justified by competency questions or system requirements (search facet, rule, validation, etc.).[^3_9][^3_8]


### Typical pitfalls (empirical studies)

Analyses of ontologies and tools like OOPS! highlight recurring mistakes.[^3_10][^3_11]

- **Lack of annotations and documentation**
    - Classes and properties without clear labels, comments, or definitions; this undermines reuse and governance.[^3_10]
- **Missing or incorrect domain/range**
    - Relations without domain/range; wrong or overly restrictive ones that cause unintended inferences.[^3_11][^3_10]
- **Unconnected or orphaned elements**
    - Classes or properties not integrated into the main hierarchy or graph, reducing coherence.[^3_10]
- **Misuse of inheritance and logical constructors**
    - Using intersection instead of union for domain/range, overusing “miscellaneous” catch‑all classes, or recursive/self-referential definitions.[^3_11]
- **Inconsistencies and contradictions**
    - Defining classes or axioms that cannot be satisfied together, leading to unsatisfiable classes.[^3_11][^3_8]
- **Over-modeling / ontological bloat**
    - Modeling every edge case, making the ontology too complex for practical use and hard to evolve.[^3_12][^3_8]

***

## Creating ontologies with LLMs

LLMs are increasingly used to reduce the manual burden of ontology design and curation.[^3_13][^3_7][^3_9]

### LLM roles in ontology engineering

1. **From requirements to draft ontology**
    - Given user stories and competency questions, LLMs can propose:
        - Candidate classes and properties.
        - Taxonomic hierarchies.
        - OWL axioms in machine-readable form (e.g., Turtle, RDF/XML).[^3_13][^3_9]
2. **Incremental ontology generation**
    - Methods such as CQ-by-CQ or Ontogenia feed competency questions one by one or in batches, letting the LLM produce and iteratively refine an ontology module.[^3_9]
3. **Ontology learning from text**
    - LLMs can extract candidate classes, synonyms, and relations from large corpora, serving as a semi-automatic ontology learning system that experts then clean up.[^3_7][^3_13]
4. **Curation and quality control**
    - LLMs can suggest improved labels and definitions, detect duplicate or overlapping classes, and propose better property names or constraints.[^3_14][^3_7]

### Concrete patterns from recent work

- **Memoryless CQ-by-CQ** vs **incremental generation**
    - Treat each competency question independently to generate local ontology fragments, then merge; or prompt with all questions and grow a unified ontology.[^3_9]
- **End-to-end ontology learning (OLLM)**
    - Approaches that fine-tune LLMs to produce taxonomic backbones from scratch, with regularizers that avoid overfitting to frequent concepts.[^3_13]
- **LLM-assisted OWL axiom drafting (e.g., SPIRES-style frameworks)**
    - LLM drafts axioms which are then validated by experts or automated reasoners.[^3_7]


### Practical caveats

- **Hallucinated or inconsistent axioms**
    - LLMs may generate logically inconsistent class definitions or predicates that don’t match the domain reality; every output needs validation by reasoning and expert review.[^3_7][^3_9][^3_8]
- **Schema drift and lack of global coherence**
    - Incrementally generated fragments may not align, requiring careful merging and de-duplication.[^3_13][^3_9]

A pragmatic pattern is: experts define scope and core concepts, LLMs propose draft hierarchies and axioms, and automated tools plus experts refine and validate.[^3_9][^3_7]

***

## Optimizing ontologies with graph algorithms and other techniques

Once an ontology is represented as a graph (classes and properties as nodes/edges), you can apply graph-theoretic methods for analysis and optimization.[^3_12]

### Structural optimization

- **Normalization and redundancy removal**
    - Remove duplicate vertices and parallel edges; ensure each concept is uniquely and consistently represented.[^3_12]
- **Minimal spanning trees for pruning**
    - Use weighted graphs (weights reflect importance or usage) and minimum spanning tree or related optimization to reduce structural complexity while preserving coverage.[^3_12]
- **Backpack/knapsack-style optimization**
    - Treat ontology refinement as selecting a subset of concepts/relations that maximizes overall value (coverage, relevance) under constraints like size or reasoning time.[^3_12]


### Graph-based diagnostics

- **Centrality measures**
    - Degree, betweenness, and eigenvector centrality identify highly connected or critical concepts that may need clearer definitions or modularization.[^3_12]
- **Community detection / clustering**
    - Detect groups of concepts that form natural modules; can guide modularization or reveal domains that should be split into separate ontologies.[^3_12]
- **Alignment and mapping via graph similarity**
    - Graph mapping and similarity measures help align two ontologies, measuring precision/recall of mappings and spotting structural mismatch.[^3_12]


### Semantic optimization and learning

- **Usage-driven refinement**
    - Track how classes and properties are used in real KG data and queries; deprioritize or remove rarely used pieces, or split overloaded concepts.[^3_8][^3_12]
- **Ontology-enhanced KG completion and reasoning**
    - Recent methods integrate ontological constraints into LLM-based KG completion, improving reasoning performance and revealing missing or mis-specified ontology elements.[^3_14]
- **Iterative learning loop**
    - Automatically weight concepts and relations, expand the ontology from data, then run optimization steps to keep integrity, thematic balance, and performance.[^3_12]


<span style="display:none">[^3_15]</span>



[^3_1]: https://milvus.io/ai-quick-reference/what-is-a-knowledge-graph-ontology

[^3_2]: https://www.puppygraph.com/blog/knowledge-graph-vs-ontology

[^3_3]: https://graph.build/resources/ontology

[^3_4]: https://www.falkordb.com/blog/understanding-ontologies-knowledge-graph-schemas/

[^3_5]: https://enterprise-knowledge.com/wp-content/uploads/2020/01/Ontologies-vs.-Knowledge-Graphs.pdf

[^3_6]: https://www.ontoforce.com/knowledge-graph/ontology

[^3_7]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12649945/

[^3_8]: https://www.nist.gov/document/nist-ai-rfi-cubrcinc002pdf

[^3_9]: https://arxiv.org/html/2503.05388v1

[^3_10]: https://www.scitepress.org/Papers/2013/45179/45179.pdf

[^3_11]: https://oa.upm.es/6115/1/CAEPIA09_-_Common_Pitfalls_in_Ontology_Development_-_final_version_fixed.pdf

[^3_12]: https://www.webology.org/2018/v15n2/a173.pdf

[^3_13]: https://neurips.cc/virtual/2024/poster/94942

[^3_14]: https://arxiv.org/html/2507.20643v2

[^3_15]: https://www.youtube.com/watch?v=sr257blfdY8


---

# Graph Datavases:  RDF/SPARQL (Apache Jena) vs LPG/CYPHER (Neo4j)

RDF/SPARQL (e.g., Apache Jena) and labeled‑property graphs with Cypher (e.g., Neo4j) both store nodes and edges, but they optimize for different things: RDF for **semantic interoperability and reasoning**, LPG for **developer ergonomics and high‑performance traversals**.[^4_1][^4_2][^4_3]

***

## RDF + SPARQL + Apache Jena: overview

- **Data model (RDF)**
    - Everything is a triple $(\text{subject}, \text{predicate}, \text{object})$; subjects/objects are IRIs or blank nodes, objects may also be literals.[^4_4][^4_3]
    - Graph is a set of triples; more complex structures (events, edge properties) are modeled via additional triples or reification.[^4_3]
- **Query language (SPARQL)**
    - Pattern‑matching over triples: `SELECT ... WHERE { ?s ?p ?o . ... }`.
    - Supports filters, aggregates, subqueries, federation, updates (SPARQL 1.1).[^4_5][^4_6]
- **Apache Jena**
    - Java framework for RDF storage (TDB, etc.), SPARQL querying (ARQ), and reasoning over RDFS/OWL.[^4_1][^4_4]
    - Fuseki exposes SPARQL endpoints over HTTP; Jena’s inference engine can derive additional triples from ontologies and rules.[^4_7][^4_8][^4_1]

**Agentic KG example (RDF/SPARQL)**

Triples (Turtle):

```turtle
@prefix ex: <http://example.org/> .

ex:Task123 a ex:ResearchTask ;
    ex:assignedTo ex:AgentSummarizer ;
    ex:hasInput ex:Doc456 ;
    ex:status "pending" .

ex:AgentSummarizer a ex:LLMAgent ;
    ex:capability "summarization" .
```

SPARQL:

```sparql
SELECT ?task ?doc
WHERE {
  ?task a ex:ResearchTask ;
        ex:assignedTo ex:AgentSummarizer ;
        ex:hasInput ?doc ;
        ex:status "pending" .
}
```

This can drive an agent scheduler that picks pending tasks for the summarization agent.

***

## LPG + Cypher + Neo4j: overview

- **Data model (labeled property graph)**
    - Nodes and relationships, both can have properties (key–value pairs); nodes can have multiple labels.[^4_9][^4_10]
    - Relationships are typed and directed; properties on edges are first‑class (e.g., `since`, `confidence`).[^4_9][^4_3]
- **Query language (Cypher)**
    - Pattern matching with ASCII‑art: `MATCH (a:Agent)-[r:PERFORMS]->(t:Task) RETURN a,t`.[^4_11][^4_9]
    - Optimized for graph traversal, aggregations, path queries.[^4_10][^4_9]
- **Neo4j characteristics**
    - Native graph engine focused on multi‑hop traversals and operational workloads.[^4_2][^4_9]
    - Strong integration with analytics, indexes, and procedures for graph algorithms.[^4_2][^4_9]

**Agentic KG example (LPG/Cypher)**

Graph:

```cypher
CREATE (t:Task {id: "Task123", type: "ResearchTask", status: "pending"})
CREATE (a:Agent {id: "AgentSummarizer", type: "LLMAgent", capability: "summarization"})
CREATE (d:Document {id: "Doc456"})
CREATE (a)-[:ASSIGNED_TO]->(t)
CREATE (t)-[:HAS_INPUT]->(d);
```

Query:

```cypher
MATCH (a:Agent {id: "AgentSummarizer"})-[:ASSIGNED_TO]->(t:Task {status: "pending"})-[:HAS_INPUT]->(d:Document)
RETURN t.id AS taskId, d.id AS docId;
```


***

## Side‑by‑side comparison

### Conceptual \& data‑model differences

| Dimension | RDF/SPARQL (Jena) | LPG/Cypher (Neo4j) |
| :-- | :-- | :-- |
| Core model | Global triples $(s,p,o)$ only [^4_3][^4_4] | Nodes, relationships, properties; properties on both nodes and edges [^4_3][^4_9] |
| Semantics | Strong: IRIs, ontologies (RDFS/OWL), formal reasoning [^4_1][^4_8] | Implicit: labels and conventions; limited formal semantics [^4_9][^4_2] |
| Edge attributes | Modeled via extra triples or reification [^4_3] | Native properties on relationships (e.g., `since`, `confidence`) [^4_3][^4_9] |
| Schema | Optional but often explicit via ontologies [^4_12][^4_13] | Optional, implicit in labels and property usage [^4_10][^4_3] |
| Identity | Global IRIs, good for linked data [^4_4][^4_3] | Local identifiers; global semantics by convention or mapping [^4_10][^4_14] |

### Querying and reasoning

| Dimension | RDF/SPARQL (Jena) | LPG/Cypher (Neo4j) |
| :-- | :-- | :-- |
| Query style | Triple patterns, joins via shared vars [^4_6] | Graph pattern matching with ASCII syntax [^4_9][^4_11] |
| Reasoning | Built‑in RDFS/OWL rule engines, entailment [^4_1][^4_8] | No native OWL; some constraints via APOC/procedures, basic semantics only [^4_2] |
| Federation | SPARQL 1.1 federation between endpoints [^4_6][^4_4] | External federation via tooling/APIs, not part of Cypher spec |
| Multi‑hop traversal performance | Joins over triples; can be slower on dense graphs [^4_2][^4_3] | Optimized for deep traversals and path queries [^4_9][^4_2] |

### Performance, tooling, and use cases

| Dimension | RDF/SPARQL (Jena) | LPG/Cypher (Neo4j) |
| :-- | :-- | :-- |
| Performance focus | Semantic precision, interoperability [^4_2][^4_14] | High‑performance traversals and analytics [^4_2][^4_9] |
| Typical use cases | Linked data, ontology‑driven KGs, regulatory/semantic integration [^4_12][^4_15] | Recommendation, fraud detection, operational reasoning, context graphs [^4_2][^4_10] |
| Tooling | Jena APIs, Fuseki SPARQL server, OWL reasoners [^4_5][^4_4][^4_7] | Neo4j Browser, Bloom, GDS (graph data science) library [^4_9][^4_2] |
| AI/agent integration | Strong with ontologies and explicit constraints [^4_15][^4_12] | Strong with traversal‑based context retrieval and graph analytics [^4_2] |


***

## Agentic AI: when to use which

### RDF/SPARQL/Jena in agentic systems

Best when your agentic AI needs **formal semantics, interoperability, and rule‑based reasoning**:

- **Ontology‑driven task typing**
    - Define a class hierarchy for tasks, tools, and data; use SPARQL plus reasoning to infer which agent can handle a request based on types.[^4_8][^4_12]
- **Policy and compliance checks**
    - Represent access rules or regulatory constraints as OWL/RDFS axioms and rule sets; use Jena’s inference engine to derive allowed actions.[^4_8][^4_1]

Example: find all tasks involving PHI that require a privacy‑compliant agent:

```sparql
PREFIX ex: <http://example.org/>

SELECT ?task ?agent
WHERE {
  ?task a ex:Task ;
        ex:requiresDataType ex:ProtectedHealthInfo .
  ?agent a ex:Agent ;
         ex:hasClearance ex:PHI_Compliant .
  ?agent ex:canHandle ?task .
}
```

Reasoning can infer `ex:ProtectedHealthInfo ⊑ ex:SensitiveData`, automatically including tasks modeled at different abstraction levels.[^4_1][^4_8]

### LPG/Cypher/Neo4j in agentic systems

Best when your agentic AI needs **fast traversals, graph algorithms, and operational context**:

- **Context graph for RAG and multi‑agent planning**
    - Nodes: agents, tools, documents, concepts, users, sessions.
    - Edges: `USED_TOOL`, `MENTIONS`, `DEPENDS_ON`, `SIMILAR_TO` with weights.
    - Use Cypher to quickly find relevant neighborhood around a user query or task.[^4_9][^4_2]

Example: dynamically pick the best agent based on recent performance:

```cypher
MATCH (a:Agent)-[r:HANDLED]->(t:Task)
WHERE t.type = "Summarization"
WITH a, avg(r.qualityScore) AS avgScore, count(*) AS n
WHERE n > 20
RETURN a.id, avgScore
ORDER BY avgScore DESC
LIMIT 3;
```

- **Graph algorithms for routing and coordination**
    - Use Neo4j GDS to run PageRank, community detection, shortest paths on the agent‑tool graph, then use results to guide which agents collaborate on a complex query.[^4_2][^4_9]

***

## Similarities and complementarity for agentic KG

- Both can represent: **agents, tasks, tools, documents, user goals**, and the relationships between them.[^4_10][^4_3]
- Both allow pattern‑matching queries to support:
    - Task routing (task → agent).
    - Context retrieval (agent → recent tasks → documents).
    - Provenance (answer → supporting triples/edges).[^4_6][^4_9]

Hybrid patterns (increasingly common):

- Keep **ontologies and long‑term semantic metadata in RDF/Jena**, while mirroring operational facts into a property graph for fast analytics and traversal.[^4_14][^4_2]
- Example:
    - RDF layer: classes `LLMAgent`, `RetrievalAgent`, constraints, capabilities.
    - LPG layer: concrete agent instances, real‑time interactions, performance edges.
    - Agent orchestration:
        - Use SPARQL to determine *which type* of agent is semantically appropriate for a request.
        - Use Cypher and graph algorithms to pick *which instance* is best given load, success rates, and graph‑local context.[^4_2]

This combination lets you give your agentic system both a **formal world model (RDF/Jena)** and a **high‑speed operational memory (LPG/Neo4j)**.
<span style="display:none">[^4_16][^4_17][^4_18]</span>



[^4_1]: https://www.dremio.com/wiki/apache-jena/

[^4_2]: https://www.tigergraph.com/blog/rdf-vs-property-graph-choosing-the-right-foundation-for-knowledge-graphs/

[^4_3]: https://www.puppygraph.com/blog/property-graph-vs-rdf

[^4_4]: https://jena.apache.org

[^4_5]: https://jena.apache.org/documentation/

[^4_6]: https://jena.apache.org/tutorials/sparql.html

[^4_7]: https://christinemdraper.wordpress.com/2017/04/09/getting-started-with-rdf-sparql-jena-fuseki/

[^4_8]: https://taylorandfrancis.com/knowledge/Engineering_and_technology/Computer_science/Apache_Jena/

[^4_9]: https://homepages.inf.ed.ac.uk/libkin/teach/beijing2018/neo4j-beijing.pdf

[^4_10]: https://docs.nebula-graph.io/3.3.0/1.introduction/0-1-graph-database/

[^4_11]: https://memgraph.com/blog/cypher-cheat-sheet

[^4_12]: https://enterprise-knowledge.com/wp-content/uploads/2020/01/Ontologies-vs.-Knowledge-Graphs.pdf

[^4_13]: https://milvus.io/ai-quick-reference/what-is-a-knowledge-graph-ontology

[^4_14]: https://www.wisecube.ai/blog/knowledge-graphs-rdf-or-property-graphs-which-one-should-you-pick/

[^4_15]: https://www.ontoforce.com/knowledge-graph/ontology

[^4_16]: https://jena.apache.org/documentation/rdfconnection/

[^4_17]: https://docs.oracle.com/en/database/oracle/oracle-database/26/rdfrm/rdf-graph-support-apache-jena.html

[^4_18]: https://elixirforum.com/t/storing-system-information-in-a-graph-database/54159


---

# Inductive Logic Programming and Praph Neural-Networks

Inductive logic programming (ILP) and graph neural networks (GNNs) both enrich a knowledge graph, but in complementary ways: ILP adds **explicit, symbolic rules**, while GNNs add **learned, distributed representations** and powerful pattern completion. Together they support more accurate, explainable, and adaptive agentic KGs.[^5_1][^5_2][^5_3]

***

## Inductive Logic Programming over knowledge graphs

**What ILP does for a KG**

- ILP learns **first‑order logic rules** from example facts in the KG plus background knowledge, e.g.
$\text{collaboratesWith}(X,Y) \leftarrow \text{coAuthor}(X,Z) \wedge \text{coAuthor}(Y,Z)$.[^5_1]
- On a KG, this means: induce definitions of new relations or constraints from existing triples and use them to derive additional (explained) edges.[^5_4][^5_1]

**Enhancements to the KG**

1. **Rule-based KG completion**
    - ILP finds patterns such as “if A and B have worked on the same project and both are `LLMAgent`s, infer `similarExpertise(A,B)`.”
    - Logic rule learners like RLogic and differentiable ILP systems extend sparse KGs with new edges while retaining interpretability.[^5_5][^5_6][^5_7]
2. **Explainability and constraints**
    - Rules are human‑readable; they can justify missing links (“A is linked to B because they share C and D”) and encode domain constraints that flag inconsistent triples.[^5_8][^5_4]
    - ILP can also explain clusters or GNN predictions post‑hoc by inducing rules that characterize a group or label.[^5_8]
3. **Labeling functions and weak supervision**
    - ILP can automatically discover labeling functions over the graph, which then provide cheap labels for downstream models (including GNNs).[^5_9]

**Agentic AI example**

- From an agent‑tool KG, ILP might learn:
$\text{suitableForQuery}(A,Q) \leftarrow \text{hasSkill}(A,S) \wedge \text{requiresSkill}(Q,S)$.
- The agent orchestrator uses these rules to propose candidate agents for new tasks, even when there is no direct historical link.

***

## Graph neural networks over knowledge graphs

**What GNNs do for a KG**

- GNNs learn **vector embeddings** for entities and relations by propagating information over the graph structure, then use these embeddings to score candidate edges or classify nodes.[^5_10][^5_11][^5_3]
- They can operate in transductive (closed‑world) or inductive settings where new nodes and edges appear at test time.[^5_12][^5_13]

**Enhancements to the KG**

1. **Knowledge graph completion**
    - GNN‑based KG embedding models (e.g., WGE, INDIGO, Graph4NLP examples) predict missing triples by aggregating neighborhood information and applying a decoder (DistMult, ComplEx, etc.).[^5_11][^5_13][^5_10]
    - This densifies the KG, uncovering latent relationships among agents, tools, and documents.
2. **Inductive generalization to new entities**
    - Inductive GNN methods encode local structure so that new nodes can be embedded on the fly and used in logical query answering.[^5_13][^5_12]
    - For agentic KGs, a brand‑new tool or agent can be inserted with a small local neighborhood and still be reasoned about via the GNN.
3. **Graph-aware reasoning modules**
    - Neuro‑symbolic models like KeGNN incorporate prior logical knowledge into GNN layers, improving performance and interpretability.[^5_2]
    - Monotonic GNNs can be constructed so that each GNN layer is equivalent to applying a set of Datalog rules; rules can then be extracted from trained models.[^5_14]

**Agentic AI example**

- A GNN trained on a KG of past tasks predicts `ASSISTS` or `DELEGATES_TO` edges between agents, enabling automatic discovery of cooperation patterns for complex tasks.
- A completion model fills in `HAS_CAPABILITY` or `RELEVANT_TO_TOPIC` edges, which are then used to guide retrieval and planning.[^5_10][^5_11]

***

## How ILP and GNNs complement each other

**1. Symbolic rules + neural embeddings**

- ILP provides **discrete, human-readable rules** that reflect high‑level regularities; GNNs provide **continuous embeddings** that capture subtle statistical patterns and noise‑robust similarity.[^5_2][^5_1]
- Neuro‑symbolic frameworks like KeGNN stack “knowledge enhancement layers” on top of a GNN to refine predictions using prior logical rules.[^5_2]

**2. Rule learning from GNNs and vice versa**

- GNN-based models over KGs can be designed so that their transformations correspond to logic rules; from such monotonic GNNs, rules can be extracted and used in a symbolic solver.[^5_14]
- Differentiable ILP systems (e.g., GLIDR, DFORL) blend gradient-based optimization with rule induction, achieving competitive KG completion performance while keeping rules extractable.[^5_6][^5_5]

**3. Better data efficiency and robustness**

- ILP can provide weak labels or constraints that regularize GNN training (e.g., enforcing that predictions obey certain logical implications).[^5_9][^5_2]
- GNNs, in turn, can denoise or complete sparse KGs before ILP runs, giving ILP richer structure to learn from.[^5_3][^5_2]

**4. For agentic KGs specifically**

- Use GNNs to propose candidate new edges (e.g., potential collaborations, tool applicability, topic relevance).[^5_11][^5_10]
- Use ILP to:
    - Filter and explain these edges with explicit rules.[^5_4][^5_1]
    - Encode orchestration logic (“if the query involves medical data, route via an agent with `hasClearance=PHI` and `expertise=Medicine`”).

This gives you a KG that is both **richer** (thanks to GNN completion and inductive embeddings) and **more interpretable and controllable** (thanks to ILP rules and constraints)—a strong foundation for robust agentic AI.
<span style="display:none">[^5_15]</span>



[^5_1]: https://dariastepanova.github.io/files/conferences/RW2018/paper/RW2018paper.pdf

[^5_2]: https://arxiv.org/pdf/2303.15487.pdf

[^5_3]: https://ieeexplore.ieee.org/document/9831453/

[^5_4]: https://community.sap.com/t5/technology-blog-posts-by-sap/knowledge-graphs-with-inductive-logic-programming/ba-p/13517645

[^5_5]: https://arxiv.org/abs/2508.06716

[^5_6]: https://www.sciencedirect.com/science/article/abs/pii/S0004370224000444

[^5_7]: https://web.cs.ucla.edu/~yzsun/papers/2022_KDD_RLogic.pdf

[^5_8]: https://ieeexplore.ieee.org/document/10412824/

[^5_9]: https://iclr.cc/virtual/2023/poster/10944

[^5_10]: https://graph4ai.github.io/graph4nlp/tutorial/knowledge_graph_completion.html

[^5_11]: https://arxiv.org/abs/2112.09231

[^5_12]: https://github.com/DeepGraphLearning/InductiveQE

[^5_13]: https://proceedings.neurips.cc/paper_files/paper/2021/hash/0fd600c953cde8121262e322ef09f70e-Abstract.html

[^5_14]: https://openreview.net/forum?id=CrCvGNHAIrz

[^5_15]: https://www.reddit.com/r/MachineLearning/comments/1eg674y/discussion_thoughts_on_knowledge_graphs_and_graph/



# Solution Architecture: Agentic AI M\&A Target Identification System



## System Overview

The system is a **seven-layer agentic AI pipeline** that continuously ingests and processes multi-source text, builds and enriches a domain knowledge graph, and deploys specialized agents to discover acquisition targets or score known candidates.  The architecture integrates traditional NLP, LLMs, formal ontologies, graph algorithms, ILP, and GNNs into a unified, human-supervised loop.[^6_1][^6_2][^6_3]

```
┌──────────────────────────────────────────────────────────┐
│  ① DATA INGESTION             ② NLP / EXTRACTION         │
│  SEC Filings, News,    →→→    spaCy NER, Relation        │
│  Emails, Social Media,        Extraction, LLM Triples,   │
│  Reports, PDFs                Coreference, Sentiment     │
└────────────────────────────────────┬─────────────────────┘
                                     ↓
┌──────────────────────────────────────────────────────────┐
│  ③ ONTOLOGY LAYER + HUMAN REVIEW                         │
│  M&A OWL Ontology, Competency Questions, Analyst Curation│
└────────────────────────────────────┬─────────────────────┘
                                     ↓
┌──────────────────────────────────────────────────────────┐
│  ④ KNOWLEDGE GRAPH STORE                                 │
│  RDF / Apache Jena (Semantic)  +  Neo4j (Operational)    │
│                   +  Vector Store (RAG)                  │
└─────────────────────┬────────────────────────────────────┘
          ↕ continuous enrichment
┌─────────────────────┴────────────────────────────────────┐
│  ⑤ KG ENHANCEMENT ENGINE                                 │
│  Graph Algorithms + ILP + GNNs + LLM-as-Judge Validator  │
└────────────────────────────────────┬─────────────────────┘
                                     ↓
┌──────────────────────────────────────────────────────────┐
│  ⑥ AGENTIC REASONING LAYER                               │
│  Orchestrator | Signal | Scorer | Due Diligence | Report │
└────────────────────────────────────┬─────────────────────┘
                                     ↓
┌──────────────────────────────────────────────────────────┐
│  ⑦ ANALYST INTERFACE                                     │
│  Target Dashboard → Explainability → Feedback Loop →→→   │
│                     (feeds back to Ontology + KG)        │
└──────────────────────────────────────────────────────────┘
```


***

## Layer ① — Data Ingestion

All sources are normalized and ingested through a unified document store before NLP processing begins.[^6_4][^6_3]

- **SEC Filings (EDGAR)**: 10-K, 10-Q, 8-K filings; structured via XBRL where available and parsed for narrative text using tools like *Docling* or Apache Tika.[^6_3][^6_4]
- **News Articles**: Web scrapers or licensed feeds (Bloomberg, Reuters APIs); timestamped and source-tagged.
- **Emails / Internal Docs**: IMAP-based ingestion with content stripped for NLP; high sensitivity data must be tagged for access control.
- **Social Media**: Twitter/X, LinkedIn mentions, Reddit; include metadata (author, timestamp, engagement) critical for signal detection.
- **Financial Reports / Analyst PDFs**: OCR via Docling or Tesseract; table extraction is critical since financial KPIs live in structured tables.[^6_3]

All documents receive:

- `sourceType`, `timestamp`, `entityMention` metadata tags.
- A **provenance hash** linking every triple to its exact source sentence — critical for analyst trust and compliance.

***

## Layer ② — NLP \& Extraction Pipeline

A **hybrid NLP + LLM pipeline** processes each document to produce candidate triples.[^6_4][^6_3]

### Step 1: Document preprocessing

- PDF/HTML parsing → plain text + structured tables.
- Sentence segmentation, tokenization.
- Language detection and section identification (e.g., "Risk Factors" vs. "MD\&A" in SEC filings).[^6_4]


### Step 2: Traditional NLP (spaCy)

- **Custom NER** trained on M\&A domain labels:
    - `Company`, `Executive`, `Investor`, `Regulator`, `Market`, `Technology`, `FinancialMetric`, `JurisdictionEvent`.
- **Dependency-based relation extraction**: Subject–verb–object traversal over parse trees to extract verb-grounded triples.
- **Coreference resolution**: Link "the company", "they", "its CEO" back to canonical entity nodes.
- **Sentiment + signal extraction**: Classify sentences as `AcquisitionSignal`, `RegulatoryRisk`, `FinancialDistress`, `GrowthIndicator` using text classifiers.[^6_5]


### Step 3: LLM triple extraction

- For each sentence or short passage (with entity spans injected), prompt an LLM:

```
Given these named entities: [TechCorp, Alice Chen, Google],
extract all subject–predicate–object triples from the text.
Output JSON: {"triples": [{"s": ..., "p": ..., "o": ...}]}

Text: "Alice Chen, CEO of TechCorp, agreed to explore a merger
with Google's cloud division last quarter."
```

- Output: `(Alice Chen, isCEOOf, TechCorp)`, `(TechCorp, exploringMergerWith, Google Cloud)`, `(event, occurredIn, Q3-2024)`.


### Step 4: Triple validation and deduplication

- **Span check**: Verify subject and object both appear in the source text (prevents hallucination).
- **Confidence scoring**: Each triple receives a score from the extraction model.
- Low-confidence triples are flagged for human review rather than auto-committed.[^6_3]

***

## Layer ③ — M\&A Domain Ontology and Human Review

### The M\&A Ontology

The ontology defines the **semantic schema** for the entire KG. It answers questions like: what is an Acquirer, what does `hasStrategicOverlap` mean, what constraints apply to `hasRevenue`?[^6_6][^6_7]

**Core classes:**

```turtle
ex:Company          rdfs:subClassOf  ex:Entity
ex:PublicCompany    rdfs:subClassOf  ex:Company
ex:PrivateCompany   rdfs:subClassOf  ex:Company
ex:Executive        rdfs:subClassOf  ex:Person
ex:InvestmentFirm   rdfs:subClassOf  ex:Entity
ex:Market           rdfs:subClassOf  ex:Domain
ex:AcquisitionEvent rdfs:subClassOf  ex:Event
```

**Key object properties:**


| Property | Domain | Range | Notes |
| :-- | :-- | :-- | :-- |
| `hasCompetitor` | Company | Company | Symmetric |
| `operatesIn` | Company | Market | Multi-valued |
| `hasExecutive` | Company | Executive |  |
| `hasInvestor` | Company | InvestmentFirm | Weighted (ownership %) |
| `partnersWith` | Company | Company | Undirected |
| `acquiredBy` | Company | Company |  |
| `hasRegulatoryFlag` | Company | RegulatoryRisk |  |
| `hasFinancialSignal` | Company | FinancialMetric | Timestamped |

**Competency questions driving the schema:**

1. *"Which companies in the SaaS market have declining revenue but strong IP portfolios?"*
2. *"Which private companies share key executives or investors with known acquisition targets?"*
3. *"Which companies have recently lost market share to our client's key competitor?"*
4. *"Are there regulatory flags that would block an acquisition in this jurisdiction?"*

### Human Analyst Involvement

Human involvement is not optional — it is a **core architectural component**, not an afterthought.[^6_7]

- **Ontology governance board**: Domain experts (M\&A analysts, legal, finance) own the ontology schema, approve new classes and properties, and resolve ambiguities.
- **Active learning review queue**: Low-confidence triples (score < threshold) surface to analysts via a curation UI; analysts approve, reject, or correct them — these decisions retrain the extraction models.
- **Feedback-driven KG updates**: When an analyst adds intelligence ("I know that Company X is actively looking to divest this division"), it is added as a high-provenance triple with the analyst as source.
- **Red-teaming and bias review**: Periodic review to check whether the KG over-represents certain geographies, sectors, or data sources, which would skew agent recommendations.

***

## Layer ④ — Knowledge Graph Store (Dual + Vector)

A **hybrid tri-store architecture** balances semantic rigor with operational speed and unstructured retrieval.[^6_8][^6_1]

### RDF / Apache Jena (semantic layer)

- Stores: ontology definitions (TBox) + long-term verified facts (ABox).
- Enables RDFS/OWL reasoning: e.g., infer `isSectorPeer(A,B)` from shared `operatesIn` and `hasCompetitor` axioms.
- SPARQL endpoint for semantic queries: *"Find all companies with revenue < \$50M in HealthTech that have not been acquired."*


### LPG / Neo4j (operational layer)

- Mirrors key operational entities for fast multi-hop traversal.
- Stores signal events, temporal edges (`hasSignal` with timestamps, confidence scores).
- Graph Data Science (GDS) library enables in-database PageRank, Louvain community detection, shortest paths.
- Cypher query example for signal detection:

```cypher
MATCH (c:Company)-[:HAS_SIGNAL]->(s:AcquisitionSignal)
WHERE s.type = "ExecutiveDeparture" AND s.date > date() - duration("P90D")
WITH c, count(s) AS signals
WHERE signals >= 2
RETURN c.name, signals ORDER BY signals DESC;
```


### Vector Store (RAG layer)

- Embeds document chunks using a sentence transformer; indexed in Weaviate or pgvector.
- Used by agents when structured KG traversal does not find an answer — semantic fallback.
- Bridges the gap between structured and unstructured knowledge.[^6_1]

***

## Layer ⑤ — KG Enhancement Engine

This is the analytical "brain" that continuously improves the graph's quality and density.[^6_9][^6_10][^6_11]

### Graph algorithms (Neo4j GDS / NetworkX)

| Algorithm | Purpose in M\&A context |
| :-- | :-- |
| **PageRank / HITS** | Rank companies by influence in their sector network |
| **Betweenness centrality** | Find "bridge" companies connecting two industry clusters — prime acquisition targets for market access |
| **Louvain community detection** | Identify industry clusters and cross-cluster outliers |
| **Shortest path (Dijkstra)** | Discover hidden connection chains between two companies |
| **Jaccard / cosine similarity** | Find companies structurally similar to known past acquisition targets |
| **Weakly connected components** | Detect isolated subgraphs — companies with thin coverage may need more data collection |

### Inductive Logic Programming (ILP)

ILP mines the KG for **human-interpretable rules** that characterize acquisition patterns.[^6_12][^6_13][^6_14]

Example rules an ILP system (e.g., AMIE+, RLogic) might learn:

```
% Companies that share investors with an acquirer tend to be acquired
acquisitionTarget(X) ← hasInvestor(X, I) ∧ hasInvestor(Acquirer, I)

% Companies whose competitors are being acquired are themselves at risk
acquisitionTarget(X) ← hasCompetitor(X, Y) ∧ isBeingAcquired(Y)

% Market concentration rule
acquisitionTarget(X) ← operatesIn(X, M) ∧ decliningMarketShare(X, M)
                      ∧ hasStrategicAsset(X, A)
```

These rules:

- **Explain predictions** to analysts in plain language.
- **Constrain GNN training** with logical regularizers.
- **Auto-extend the KG** by inferring new candidate edges.


### Graph Neural Networks (GNNs)

A **GraphSAGE** or **INDIGO** model is trained on the KG to predict missing or future links.[^6_2][^6_15]

- **Training signal**: Historical M\&A deals (company pairs that merged) = positive edges; random non-merging pairs = negative edges.
- **Node features**: Revenue, growth rate, headcount, patent count, sentiment score, sector embedding.
- **Edge features**: Confidence, source count, recency, edge type.
- The GNN predicts `acquisitionLikelihood(CompanyA, CompanyB)` scores as a link prediction task.
- Research using GraphSAGE on M\&A data achieved **~81.8% accuracy** in identifying acquisition targets.[^6_2]

**ILP + GNN synergy:**

- ILP rules provide logical constraints and labeling functions to weakly supervise GNN training on unlabeled pairs.[^6_16]
- The GNN handles noisy, implicit signals (social media, news sentiment); ILP handles structural, rule-based patterns (shared investors, board overlaps).
- An LLM-as-Judge validator receives candidate triples from both and assigns a final confidence score before committing to the KG.[^6_3]

***

## Layer ⑥ — Agentic Reasoning Layer

Five specialized agents operate over the shared KG, coordinated by an orchestrator.[^6_17][^6_18][^6_1]

### Orchestrator Agent

- Monitors trigger conditions (new document ingested, analyst request, scheduled scan).
- Decomposes goals into subtasks: *"Evaluate TargetCo"* → assign to Scorer + Due Diligence + Report agents in sequence.
- Reads and writes agent coordination state to Neo4j (task nodes, handoff edges).


### Signal Detection Agent

- **Runs continuously** on the ingestion stream.
- Queries Neo4j for newly extracted `AcquisitionSignal` nodes meeting threshold criteria:
    - Leadership change signals (executive departures, new M\&A-experienced board members).
    - Financial distress signals (negative sentiment on earnings, debt downgrades).
    - Strategic pivot signals ("exploring strategic alternatives" in SEC language).
- Cross-references signals against ILP rules to elevate high-confidence alerts.
- Pushes confirmed alerts into the KG as `HighAlertTarget` nodes for the Scorer to pick up.


### Target Scoring Agent

- Produces a **composite acquisition score** for each candidate using:
    - **Financial features** (from SEC/financial KG nodes): revenue growth, EBITDA margins, leverage ratios.
    - **Graph topology features**: degree centrality, community membership, bridge-node status.
    - **GNN link prediction score** (probability of acquisition given graph neighborhood).
    - **Sentiment trajectory**: rolling sentiment score from news/social data over 90 days.[^6_5]
- Final score is a weighted combination, with weights tunable by analysts.


### Due Diligence Agent

- Activated when a target is elevated above a threshold score.
- Executes **multi-hop KG traversal** to build a structured evidence dossier:
    - Board members → prior company affiliations → track record.
    - Shared investors → portfolio overlaps → potential conflicts.
    - IP portfolio → patent citations → technology adjacency to acquirer's roadmap.
    - Regulatory flags → jurisdictions → antitrust risk.[^6_18][^6_1]
- Uses SPARQL (RDF layer) for formal reasoning over ontology-constrained queries.
- Uses Cypher (LPG layer) for fast traversal of relationship chains.
- Falls back to vector RAG when KG gaps exist.


### Report Generation Agent

- Compiles a **grounded, explainable M\&A brief**:
    - Every claim is traced to a specific KG triple + source document.
    - ILP rules that fired for this target are listed as explicit reasoning steps.
    - GNN score is presented with feature attributions (SHAP values over graph features).
    - Confidence intervals are shown for extracted financial data.[^6_18][^6_3]

***

## Layer ⑦ — Analyst Interface and Feedback Loop

The interface is not just an output screen — it is a **knowledge refinement engine**.[^6_7][^6_18]

- **Target Dashboard**: Ranked list of acquisition candidates with composite score, signal count, sector, and graph centrality rank.
- **Explainability View**: Per-target evidence trail showing which KG paths, ILP rules, and GNN predictions contributed to the score. Analysts can inspect source documents for any supporting triple.
- **Feedback Loop** (critical):
    - Analyst marks a target as *"not viable"* → that judgment is stored as a negative training example.
    - Analyst corrects a bad triple → triggers ontology or extraction model update.
    - Analyst adds domain knowledge ("This company is quietly shopping itself") → high-provenance triple injected directly into KG.
    - Aggregate feedback retrains: spaCy NER/RE models, GNN link prediction weights, ILP rule thresholds, and LLM extraction prompts — **closing the learning loop**.

***

## Key Design Principles

- **Provenance first**: Every triple carries source document, extraction method, timestamp, and confidence — essential for analyst trust in a high-stakes domain.[^6_4][^6_3]
- **Human-in-the-loop at every layer**: Ontology governance, curation queues, feedback retraining — not just at output.[^6_18][^6_7]
- **Defense in depth for quality**: spaCy precision → LLM coverage → ILP rule validation → GNN completion → LLM-as-Judge. Multiple layers prevent hallucinated facts from reaching agents.[^6_3]
- **Explainability as a requirement**: In M\&A advisory, every recommendation must be defensible; ILP rules and KG evidence trails make the system auditable.[^6_12][^6_18]
- **Modular and composable**: Each layer can be upgraded independently — swap GraphSAGE for a newer GNN, add a new data source, retrain spaCy without rebuilding the entire system.[^6_19][^6_17]
<span style="display:none">[^6_20][^6_21][^6_22][^6_23][^6_24][^6_25]</span>



[^6_1]: https://zbrain.ai/knowledge-graphs-for-agentic-ai/

[^6_2]: https://arxiv.org/pdf/2104.01757.pdf

[^6_3]: https://arxiv.org/html/2508.17906v2

[^6_4]: https://damir.cavar.me/Pubs/Mapping_SEC_Deep_NLP_Knowledge_Graph.pdf

[^6_5]: https://developers.lseg.com/en/article-catalog/article/predicting-MnA-targets-using-ML-Unlocking-the-potential-of-NLP-variables

[^6_6]: https://www.falkordb.com/blog/understanding-ontologies-knowledge-graph-schemas/

[^6_7]: https://www.nist.gov/document/nist-ai-rfi-cubrcinc002pdf

[^6_8]: https://www.artefact.com/blog/will-the-future-of-agentic-ai-rely-on-knowledge-graphs/

[^6_9]: https://www.webology.org/2018/v15n2/a173.pdf

[^6_10]: https://arxiv.org/abs/2508.06716

[^6_11]: https://ieeexplore.ieee.org/document/9831453/

[^6_12]: https://community.sap.com/t5/technology-blog-posts-by-sap/knowledge-graphs-with-inductive-logic-programming/ba-p/13517645

[^6_13]: https://dariastepanova.github.io/files/conferences/RW2018/paper/RW2018paper.pdf

[^6_14]: https://web.cs.ucla.edu/~yzsun/papers/2022_KDD_RLogic.pdf

[^6_15]: https://proceedings.neurips.cc/paper_files/paper/2021/hash/0fd600c953cde8121262e322ef09f70e-Abstract.html

[^6_16]: https://iclr.cc/virtual/2023/poster/10944

[^6_17]: https://arxiv.org/html/2512.09458v1

[^6_18]: https://theaiinnovator.com/how-graph-thinking-empowers-agentic-ai/

[^6_19]: https://www.deloitte.com/us/en/services/consulting/blogs/business-operations-room/agentic-ai-in-manufacturing.html

[^6_20]: https://www.cio.com/article/4138732/the-transplantable-skeleton-why-agentic-ai-infrastructure-must-survive-corporate-surgery.html

[^6_21]: https://www.sciencedirect.com/science/article/pii/S027861252500216X

[^6_22]: https://www.linkedin.com/posts/amyhodler_i-wanted-to-share-the-recording-of-what-was-activity-7378891388731637761-I1KK

[^6_23]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9823264/

[^6_24]: https://www.techrxiv.org/users/854434/articles/1245167-intelligent-anti-money-laundering-transaction-pattern-recognition-system-based-on-graph-neural-networks

[^6_25]: https://towardsai.net/p/machine-learning/a-look-at-finreflectkg-ai-driven-knowledge-graph-in-finance


---

# Implementation steps for building the knowledge graph from SEC 10-K filings

A real-world implementation of a 10-K-to-knowledge-graph pipeline requires six concrete phases: EDGAR access and document parsing, section decomposition, NLP/LLM triple extraction, entity linking and ontology alignment, KG loading, and validation.  Recent open-source work on all 101 S\&P 100 companies produced nearly 600,000 triples from 2024 10-K filings using 24 entity types and 27 relation types — a useful benchmark for what the pipeline should produce.[^7_1][^7_2][^7_3]

***

## Step 1 — Acquire filings from EDGAR

EDGAR provides machine-readable access to all SEC filings via its full-text search and bulk download APIs.

```python
import requests, json

# SEC EDGAR full-text search API
def get_10k_filings(cik: str, count: int = 5):
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    r = requests.get(url, headers={"User-Agent": "yourname@email.com"})
    data = r.json()
    filings = data["filings"]["recent"]
    results = []
    for i, form in enumerate(filings["form"]):
        if form == "10-K":
            results.append({
                "accession": filings["accessionNumber"][i],
                "date":       filings["filingDate"][i],
                "doc":        filings["primaryDocument"][i],
            })
        if len(results) >= count:
            break
    return results

# Example: Apple CIK = 0000320193
filings = get_10k_filings("0000320193")
```

Key points:[^7_4]

- Use the `User-Agent` header with a real email — EDGAR rate-limits anonymous requests.
- Filings are in **HTML (iXBRL)** format post-2020; older ones are ASCII/SGML.
- The EDGAR bulk download `https://efts.sec.gov/LATEST/search-index?q=...` lets you pull by form type, date range, or SIC code to target specific sectors.

***

## Step 2 — Parse and section-split documents

10-K filings have a standardized but messy structure. Robust parsing requires handling iXBRL tags, inline XBRL, and scanned PDFs for older filings.[^7_5][^7_3]

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()

def parse_10k(file_path: str) -> dict:
    result = converter.convert(file_path)
    doc = result.document
    # Docling preserves tables, headings, and text blocks separately
    return {
        "text_blocks": [block.text for block in doc.body],
        "tables":      doc.tables,
        "metadata":    doc.metadata,
    }
```


### Section identification

10-K filings follow a **standardized Item structure** (Items 1–15). Each section has distinct M\&A relevance:[^7_6][^7_1]


| Item | Section Name | M\&A Relevance |
| :-- | :-- | :-- |
| Item 1 | Business | Core business, products, competitors |
| Item 1A | Risk Factors | Regulatory, operational, market risks |
| Item 1B | Unresolved Staff Comments | Potential legal flags |
| Item 2 | Properties | Physical assets, real estate |
| Item 7 | MD\&A | Management narrative, forward guidance |
| Item 7A | Quantitative Risk Disclosures | Interest rate, FX, commodity exposure |
| Item 8 | Financial Statements | Revenue, EBITDA, debt structures |
| Item 13 | Related Transactions | Executive relationships, conflicts |
| Item 14 | Principal Accountant Fees | Audit firm relationships |

```python
import re

SECTION_PATTERNS = {
    "business":       r"ITEM\s+1[.\s]+BUSINESS",
    "risk_factors":   r"ITEM\s+1A[.\s]+RISK\s+FACTORS",
    "mda":            r"ITEM\s+7[.\s]+MANAGEMENT",
    "financials":     r"ITEM\s+8[.\s]+FINANCIAL\s+STATEMENTS",
    "transactions":   r"ITEM\s+13[.\s]+CERTAIN\s+RELATIONSHIPS",
}

def split_sections(text: str) -> dict:
    sections = {}
    anchors = {}
    for name, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            anchors[name] = match.start()
    sorted_keys = sorted(anchors, key=lambda k: anchors[k])
    for i, key in enumerate(sorted_keys):
        start = anchors[key]
        end = anchors[sorted_keys[i+1]] if i+1 < len(sorted_keys) else len(text)
        sections[key] = text[start:end]
    return sections
```


***

## Step 3 — spaCy NER on each section

Train or fine-tune a **domain-specific spaCy NER model** for 10-K text.  Existing custom models (e.g., the Jodie NER-10K model) use transfer learning on 5,000+ annotated SEC examples and significantly outperform generic `en_core_web_lg` on financial text.[^7_7][^7_8]

### Custom entity labels for M\&A context:

```python
# Labels to add beyond spaCy defaults
M_AND_A_LABELS = [
    "COMPANY",         # organization names
    "EXECUTIVE",       # named officers/directors
    "COMPETITOR",      # named competitors (Item 1)
    "PRODUCT_LINE",    # product/service families
    "MARKET_SEGMENT",  # target customer verticals
    "FINANCIAL_METRIC",# revenue, EBITDA, etc.
    "REGULATOR",       # SEC, FTC, DOJ, CFIUS
    "LEGAL_RISK",      # litigation, regulatory events
    "GEOGRAPHY",       # countries/regions of operation
    "INVESTOR",        # named shareholders > 5%
]
```

```python
import spacy

nlp = spacy.load("en_core_web_lg")  # or fine-tuned Jodie SEC model

def extract_entities(section_text: str, section_name: str) -> list:
    doc = nlp(section_text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text":    ent.text,
            "label":   ent.label_,
            "start":   ent.start_char,
            "end":     ent.end_char,
            "section": section_name,
        })
    return entities
```


### Dependency-based relation extraction

For each sentence containing two or more entities, extract verb-anchored relations via dependency parse:[^7_9][^7_1]

```python
def extract_relations_from_sentence(sent, entities_in_sent: list) -> list:
    triples = []
    for token in sent:
        if token.pos_ == "VERB":
            subjects = [c for c in token.children if c.dep_ in ("nsubj","nsubjpass")]
            objects  = [c for c in token.children if c.dep_ in ("dobj","pobj","attr")]
            for subj in subjects:
                for obj in objects:
                    # Only keep if both ends are known entities
                    subj_ent = match_entity(subj.text, entities_in_sent)
                    obj_ent  = match_entity(obj.text,  entities_in_sent)
                    if subj_ent and obj_ent:
                        triples.append({
                            "subject":   subj_ent,
                            "predicate": token.lemma_,
                            "object":    obj_ent,
                            "sentence":  sent.text,
                        })
    return triples
```


***

## Step 4 — LLM triple extraction (complementary pass)

Run an LLM extraction pass on the same sections, constrained to the entities already found by spaCy. This dramatically reduces hallucinated nodes while getting semantic coverage spaCy misses.[^7_10][^7_3]

```python
import json

EXTRACTION_PROMPT = """
You are extracting knowledge graph triples from a SEC 10-K filing.

Known entities in this text: {entities}

Extract subject-predicate-object triples relevant to M&A analysis.
Focus on: competitors, partnerships, risks, financial signals,
          executive roles, regulatory exposure, acquisitions.

Return JSON: {{"triples": [{{"s": "...", "p": "...", "o": "...",
                             "confidence": 0.0-1.0,
                             "evidence": "exact quote"}}]}}

Text:
{text}
"""

def llm_extract_triples(text: str, entities: list, llm_client) -> list:
    entity_names = [e["text"] for e in entities]
    prompt = EXTRACTION_PROMPT.format(
        entities=json.dumps(entity_names),
        text=text[:3000]  # chunk to fit context window
    )
    response = llm_client.chat(prompt)
    result = json.loads(response)
    return result.get("triples", [])
```


### Chunking strategy for long sections

Item 7 (MD\&A) and Item 8 (financials) can exceed 50,000 tokens. Use a **sliding window with overlap** to avoid cutting mid-sentence context:[^7_11][^7_3]

```python
def chunk_section(text: str, chunk_size: int = 2000,
                  overlap: int = 200) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append({
            "text":  text[start:end],
            "start": start,
            "end":   min(end, len(text))
        })
        start += chunk_size - overlap
    return chunks
```


***

## Step 5 — Financial table extraction

Structured financial data (revenue, debt, EBITDA) lives in tables, not prose. Docling and `pdfplumber` can extract tables as DataFrames; these are converted to triples directly.[^7_3][^7_5]

```python
import pdfplumber

def extract_financial_tables(pdf_path: str) -> list:
    triples = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                # Assume first row = headers, first col = metric name
                if not table or len(table[^7_0]) < 2:
                    continue
                headers = table[^7_0]  # e.g. ["Metric", "2023", "2022"]
                for row in table[1:]:
                    metric = row[^7_0]
                    for i, year_col in enumerate(headers[1:], 1):
                        if row[i]:
                            triples.append({
                                "s": company_name,
                                "p": f"hasFinancialMetric_{metric}",
                                "o": row[i],
                                "year": year_col,
                                "source": "financial_statements"
                            })
    return triples
```


***

## Step 6 — Entity linking and ontology alignment

Raw extracted entity strings must be resolved to **canonical ontology URIs**; otherwise every variant ("Apple Inc.", "Apple", "AAPL") becomes a different node.[^7_12][^7_5]

```python
# Step 1: Normalize surface form
def normalize_entity(text: str) -> str:
    return text.strip().lower()\
               .replace(",", "").replace("inc.", "").replace("corp.", "")

# Step 2: Fuzzy match against known entity registry (SEC CIK database)
from rapidfuzz import process

def link_to_registry(surface: str, registry: dict) -> str:
    """registry: {normalized_name: CIK_URI}"""
    match, score, _ = process.extractOne(
        normalize_entity(surface), registry.keys()
    )
    if score >= 85:
        return registry[match]  # return canonical URI
    return None  # flag for human review

# Step 3: Map raw predicates to ontology predicates
PREDICATE_MAP = {
    "compete":       "ex:hasCompetitor",
    "acquire":       "ex:acquiredBy",
    "partner":       "ex:partnersWith",
    "invest":        "ex:hasInvestor",
    "sue":           "ex:hasLegalRisk",
    "operate":       "ex:operatesIn",
    "disclose":      "ex:hasRegulatoryFlag",
}
```


***

## Step 7 — Triple validation pipeline

Before loading any triple into the KG, it passes through a three-stage validation gate:[^7_2][^7_13]

```
Triple candidate
       │
       ▼
[Stage 1] Span validation
  – subject AND object appear in source text (exact or fuzzy match)
  – reject if either invented by LLM
       │
       ▼
[Stage 2] Ontology constraint check
  – predicate exists in M&A ontology
  – domain/range types match (e.g., hasInvestor: Company → InvestmentFirm)
  – reject or flag mismatches
       │
       ▼
[Stage 3] Confidence threshold
  – confidence ≥ 0.75 → auto-commit with provenance tag
  – 0.50 ≤ confidence < 0.75 → queue for human review
  – confidence < 0.50 → discard
       │
       ▼
  KG-ready triple with provenance
```

Each committed triple carries a **provenance metadata node**:

```turtle
ex:triple_001 a rdf:Statement ;
    rdf:subject   ex:Apple ;
    rdf:predicate ex:hasCompetitor ;
    rdf:object    ex:Microsoft ;
    prov:wasDerivedFrom ex:Apple_10K_2024 ;
    ex:sourceSentence "Apple faces competition from Microsoft..." ;
    ex:extractionMethod "LLM-GPT4o" ;
    ex:confidence 0.91 ;
    ex:dateExtracted "2024-11-15"^^xsd:date .
```


***

## Step 8 — Load into KG stores

### Neo4j (LPG) loading via py2neo

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687",
                               auth=("neo4j", "password"))

def load_triple_neo4j(triple: dict):
    with driver.session() as session:
        session.run("""
            MERGE (s:Company {name: $subject})
            MERGE (o:Entity  {name: $object,  type: $obj_type})
            MERGE (s)-[r:RELATION {type: $predicate,
                                   confidence: $confidence,
                                   source: $source,
                                   date: $date}]->(o)
        """, **triple)
```


### Apache Jena (RDF) loading via rdflib

```python
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD

EX   = Namespace("http://ma-kg.org/entity/")
PROP = Namespace("http://ma-kg.org/property/")

g = Graph()

def load_triple_rdf(triple: dict):
    s = EX[triple["subject_uri"]]
    p = PROP[triple["predicate_uri"]]
    o = EX[triple["object_uri"]] if triple["obj_is_entity"] \
        else Literal(triple["object"], datatype=XSD.string)
    g.add((s, p, o))

# Serialize to Turtle for Jena TDB load
g.serialize("ma_kg.ttl", format="turtle")
# Load via Jena CLI: tdb2.tdbloader --loc=/path/to/tdb ma_kg.ttl
```


***

## Step 9 — Iterative quality cycle

After the initial bulk load (all S\&P 500 10-Ks, for example), run the quality cycle:[^7_2][^7_3]

1. **Coverage audit**: Count triples per company, per section, per predicate. Flag companies with fewer than expected triples as candidates for re-extraction or human annotation.
2. **Graph connectivity audit**: Find orphaned nodes (degree = 0); trace back to parsing failures or entity linking misses.
3. **Consistency check via SPARQL** (Jena):
```sparql
# Find companies with conflicting revenue signals
SELECT ?company ?metric1 ?metric2
WHERE {
  ?company ex:hasRevenue ?metric1 .
  ?company ex:hasRevenue ?metric2 .
  FILTER(?metric1 != ?metric2 && ?metric1 > ?metric2 * 1.5)
}
```

4. **Active learning queue**: Low-confidence triples surface to analysts, who label them; labels retrain the spaCy RE model and LLM extraction prompts.[^7_8][^7_5]
5. **Incremental updates**: On each new 10-K filing (quarterly earnings trigger 10-Q), re-run the pipeline for that company only, diff new triples against existing ones, and apply a temporal update (add timestamped version, do not overwrite).[^7_10][^7_2]

***

## Tools summary

| Purpose | Recommended Tool |
| :-- | :-- |
| EDGAR filing access | `sec-edgar-downloader` Python package, EDGAR REST API |
| Document parsing | Docling (PDF/iXBRL), pdfplumber (tables), BeautifulSoup (HTML) |
| NER | spaCy + `en_core_web_lg` fine-tuned on SEC corpus (Jodie NER-10K) |
| Relation extraction | spaCy dependency parser + custom RE model |
| LLM extraction | GPT-4o / LLaMA 3 70B with structured JSON output |
| Entity linking | RapidFuzz + SEC CIK database, OpenRefine |
| Triple validation | Rule-based span check + OWL reasoner |
| RDF store | Apache Jena TDB2 + Fuseki SPARQL endpoint |
| LPG store | Neo4j + GDS library |
| Orchestration | Prefect or Apache Airflow for pipeline scheduling |

<span style="display:none">[^7_14][^7_15][^7_16]</span>



[^7_1]: https://damir.cavar.me/Pubs/Mapping_SEC_Deep_NLP_Knowledge_Graph.pdf

[^7_2]: https://aws.amazon.com/blogs/industries/agentic-graphrag-for-capital-markets/

[^7_3]: https://arxiv.org/pdf/2508.17906.pdf

[^7_4]: https://stackoverflow.com/questions/59480001/extracting-text-section-from-edgar-10-k-filings-html

[^7_5]: https://journalwjarr.com/sites/default/files/fulltext_pdf/WJARR-2025-2517.pdf

[^7_6]: https://sagemaker-jumpstart-industry-pack.readthedocs.io/en/latest/notebooks/finance/notebook4/SEC_10K_10Q_8K_section_extraction.html

[^7_7]: https://codesignal.com/learn/courses/practical-applications-of-spacy-for-real-life-tasks/lessons/information-extraction-from-legal-documents-using-spacy

[^7_8]: https://github.com/jodietheai/NER-10K

[^7_9]: https://www.ijcai.org/proceedings/2022/0605.pdf

[^7_10]: https://intuitionlabs.ai/articles/llm-financial-document-analysis

[^7_11]: https://docs.snaplogic.com/agentcreator/agentcreator-use-cases/use-case-sec-filing.html

[^7_12]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9823264/

[^7_13]: https://arxiv.org/html/2508.17906v2

[^7_14]: https://dl.acm.org/doi/full/10.1145/3768292.3770363

[^7_15]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7799375/

[^7_16]: https://huggingface.co/datasets/kritsadaK/EDGAR-CORPUS-Financial-Summarization/blob/main/README.md


---

# Code example for NER extraction from 10-K using Jodie spaCy model

Here is a complete, runnable code example covering the full pipeline from EDGAR download through Jodie NER extraction to a structured entity output. Since the Jodie model is an older spaCy v2 package, the example shows how to use it directly **and** how to replicate its approach with a modern spaCy v3 fine-tuned model when needed.

***

## Installation

```bash
# Core dependencies
pip install sec-edgar-downloader beautifulsoup4 spacy

# Download spaCy base model (used standalone or as fallback)
python -m spacy download en_core_web_lg

# Install Jodie NER-10K model (spaCy v2 package from GitHub)
# Clone the repo and install the .tar.gz
git clone https://github.com/jodietheai/NER-10K.git
cd NER-10K
pip install en_Jodie-0.0.0.tar.gz

# For spaCy v3+ environments, install compatibility shim:
pip install spacy-legacy
```

> **Note:** The Jodie model was built on spaCy v2.  For spaCy v3+ environments (recommended for production), see the fine-tuning section at the bottom of this page.[^8_1]

***

## Step 1 — Download a 10-K from EDGAR

```python
from sec_edgar_downloader import Downloader
import os

def download_10k(ticker: str, company_name: str,
                 email: str, save_dir: str = "./filings",
                 limit: int = 1) -> list:
    """
    Download the most recent 10-K filings for a ticker.
    Returns list of file paths to downloaded documents.
    """
    dl = Downloader(company_name, email, save_dir)
    dl.get("10-K", ticker, limit=limit, download_details=True)

    # Collect downloaded HTML/HTM files
    paths = []
    for root, dirs, files in os.walk(save_dir):
        for f in files:
            if f.endswith((".htm", ".html", ".txt")):
                paths.append(os.path.join(root, f))
    return paths

# Usage
filing_paths = download_10k(
    ticker="AAPL",
    company_name="MyResearchFirm",
    email="analyst@myresearchfirm.com"
)
print(f"Downloaded {len(filing_paths)} files")
```


***

## Step 2 — Parse HTML and extract clean text

10-K filings are iXBRL/HTML; BeautifulSoup strips tags and inline XBRL annotations.[^8_2]

```python
from bs4 import BeautifulSoup
import re

def parse_10k_html(file_path: str) -> str:
    """
    Extract clean text from 10-K HTML/iXBRL filing.
    Preserves paragraph boundaries; strips boilerplate tags.
    """
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    soup = BeautifulSoup(raw, "html.parser")

    # Remove non-content tags
    for tag in soup(["script", "style", "ix:header",
                     "ix:nonfraction", "ix:nonnumeric"]):
        tag.decompose()

    # Get text with paragraph spacing preserved
    text = soup.get_text(separator="\n")

    # Clean excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = text.strip()
    return text


def split_into_sections(text: str) -> dict:
    """
    Split 10-K text into standard Item sections.
    Returns dict keyed by section name.
    """
    SECTION_PATTERNS = {
        "business":      r"(?i)(item\s+1\.?\s{0,5}business\b)",
        "risk_factors":  r"(?i)(item\s+1a\.?\s{0,5}risk\s+factors\b)",
        "legal":         r"(?i)(item\s+3\.?\s{0,5}legal\s+proceedings\b)",
        "mda":           r"(?i)(item\s+7\.?\s{0,5}management.{0,30}discussion\b)",
        "financials":    r"(?i)(item\s+8\.?\s{0,5}financial\s+statements\b)",
        "executives":    r"(?i)(item\s+10\.?\s{0,5}directors\b)",
        "transactions":  r"(?i)(item\s+13\.?\s{0,5}certain\s+relationships\b)",
    }

    anchors = {}
    for name, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            anchors[name] = match.start()

    sorted_keys = sorted(anchors, key=lambda k: anchors[k])
    sections = {}
    for i, key in enumerate(sorted_keys):
        start = anchors[key]
        end = (anchors[sorted_keys[i + 1]]
               if i + 1 < len(sorted_keys) else len(text))
        sections[key] = text[start:end]

    return sections
```


***

## Step 3 — Load the Jodie NER model

```python
import spacy

def load_ner_model(use_jodie: bool = True):
    """
    Load Jodie SEC-specific NER (spaCy v2) or fallback to en_core_web_lg.
    For spaCy v3+, use a fine-tuned model instead (see Step 6).
    """
    if use_jodie:
        try:
            # spaCy v2 style load by package name after pip install
            nlp = spacy.load("en_Jodie")
            print("Loaded Jodie SEC NER model")
        except OSError:
            print("Jodie model not found, falling back to en_core_web_lg")
            nlp = spacy.load("en_core_web_lg")
    else:
        nlp = spacy.load("en_core_web_lg")

    return nlp

nlp = load_ner_model(use_jodie=True)
```


***

## Step 4 — Run NER extraction with provenance

```python
from dataclasses import dataclass, field, asdict
from typing import Optional

@dataclass
class ExtractedEntity:
    text:        str
    label:       str
    start_char:  int
    end_char:    int
    sentence:    str
    section:     str
    filing:      str
    confidence:  Optional[float] = None


def extract_entities_from_section(
    section_text: str,
    section_name: str,
    filing_id: str,
    nlp,
    max_chunk: int = 100_000   # spaCy default max_length guard
) -> list[ExtractedEntity]:
    """
    Run NER over a 10-K section.
    Chunks long sections to stay within spaCy's max_length.
    Returns a list of ExtractedEntity objects with full provenance.
    """
    # spaCy has a default max_length; chunk if needed
    chunks = [section_text[i:i + max_chunk]
              for i in range(0, len(section_text), max_chunk)]

    entities = []
    for chunk in chunks:
        doc = nlp(chunk)
        for sent in doc.sents:
            sent_ents = [e for e in doc.ents
                         if e.start >= sent.start and e.end <= sent.end]
            for ent in sent_ents:
                entities.append(ExtractedEntity(
                    text       = ent.text.strip(),
                    label      = ent.label_,
                    start_char = ent.start_char,
                    end_char   = ent.end_char,
                    sentence   = sent.text.strip(),
                    section    = section_name,
                    filing     = filing_id,
                ))
    return entities
```


***

## Step 5 — Post-process: deduplicate and normalize

```python
from collections import defaultdict
import re

# M&A-relevant entity labels from Jodie + spaCy defaults
MA_RELEVANT_LABELS = {
    "ORG",      # organizations (Jodie + spaCy)
    "PERSON",   # executives, investors
    "GPE",      # geopolitical entities (countries, states)
    "MONEY",    # financial figures
    "PERCENT",  # growth rates, margins
    "DATE",     # fiscal year references
    "PRODUCT",  # product/service names
    "LAW",      # regulations, legal acts
    "NORP",     # nationalities, political groups
    # Jodie-specific labels (if model is loaded):
    "COMPETITOR", "EXECUTIVE", "MARKET",
    "LEGAL_RISK", "FINANCIAL_METRIC",
}

def normalize_entity_text(text: str) -> str:
    """Lowercase, strip legal suffixes for company matching."""
    text = text.strip()
    # Remove common corporate suffixes for matching
    text = re.sub(
        r"\b(Inc\.?|Corp\.?|LLC\.?|Ltd\.?|Co\.?|Group|Holdings?)\b",
        "", text, flags=re.IGNORECASE
    )
    return re.sub(r"\s+", " ", text).strip().lower()


def filter_and_deduplicate(
    entities: list[ExtractedEntity],
    min_length: int = 2
) -> list[dict]:
    """
    Filter to M&A-relevant labels, remove duplicates.
    Returns deduplicated entities with occurrence count.
    """
    seen = defaultdict(lambda: {"count": 0, "sentences": [],
                                "label": "", "sections": set()})

    for ent in entities:
        if ent.label not in MA_RELEVANT_LABELS:
            continue
        if len(ent.text) < min_length:
            continue

        key = (normalize_entity_text(ent.text), ent.label)
        seen[key]["count"] += 1
        seen[key]["label"] = ent.label
        seen[key]["sections"].add(ent.section)
        if len(seen[key]["sentences"]) < 3:   # keep up to 3 example sentences
            seen[key]["sentences"].append(ent.sentence)

    result = []
    for (norm_text, label), data in seen.items():
        result.append({
            "normalized_text": norm_text,
            "label":           label,
            "mention_count":   data["count"],
            "sections":        list(data["sections"]),
            "example_sentences": data["sentences"],
        })

    # Sort by frequency — most prominent entities first
    return sorted(result, key=lambda x: x["mention_count"], reverse=True)
```


***

## Step 6 — Full pipeline runner

```python
import json
from pathlib import Path

def run_10k_ner_pipeline(
    ticker:       str,
    company_name: str,
    email:        str,
    output_dir:   str = "./output",
    use_jodie:    bool = True
) -> dict:
    """
    End-to-end: download 10-K → parse → split sections →
    run NER → deduplicate → save JSON.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 1. Download
    print(f"Downloading 10-K for {ticker}...")
    paths = download_10k(ticker, company_name, email)
    if not paths:
        raise FileNotFoundError("No filing files downloaded.")
    filing_path = paths[^8_0]
    filing_id = f"{ticker}_10K_{Path(filing_path).stem}"

    # 2. Parse
    print("Parsing HTML...")
    raw_text = parse_10k_html(filing_path)
    sections = split_into_sections(raw_text)
    print(f"  Found {len(sections)} sections: {list(sections.keys())}")

    # 3. Load model
    nlp = load_ner_model(use_jodie=use_jodie)

    # 4. Extract entities per section
    all_entities = []
    for section_name, section_text in sections.items():
        print(f"  Extracting entities from: {section_name} "
              f"({len(section_text):,} chars)...")
        ents = extract_entities_from_section(
            section_text, section_name, filing_id, nlp
        )
        all_entities.extend(ents)
        print(f"    → {len(ents)} raw entities found")

    # 5. Deduplicate and normalize
    deduped = filter_and_deduplicate(all_entities)
    print(f"\nTotal unique entities (M&A-relevant): {len(deduped)}")

    # 6. Save
    output = {
        "filing_id": filing_id,
        "ticker":    ticker,
        "sections_processed": list(sections.keys()),
        "total_raw_entities": len(all_entities),
        "unique_entities":    len(deduped),
        "entities":           deduped,
    }
    out_path = f"{output_dir}/{filing_id}_entities.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved to: {out_path}")
    return output


# Run it
results = run_10k_ner_pipeline(
    ticker="AAPL",
    company_name="MyResearchFirm",
    email="analyst@myresearchfirm.com",
    use_jodie=True
)

# Preview top entities
for ent in results["entities"][:10]:
    print(f"  [{ent['label']:18s}] {ent['normalized_text']:35s} "
          f"(mentioned {ent['mention_count']}x "
          f"in: {', '.join(ent['sections'])})")
```

**Example output:**

```
[ORG               ] apple inc.                          (mentioned 87x in: business, mda, financials)
[ORG               ] google                              (mentioned 14x in: business, risk_factors)
[PERSON            ] tim cook                            (mentioned 9x in: executives, mda)
[MONEY             ] $383.3 billion                      (mentioned 7x in: financials, mda)
[ORG               ] microsoft                           (mentioned 6x in: business, risk_factors)
[GPE               ] united states                       (mentioned 31x in: business, risk_factors)
[LAW               ] digital markets act                 (mentioned 5x in: risk_factors, legal)
[PERCENT           ] 3.4%                                (mentioned 4x in: financials)
```


***

## Step 7 — Fine-tuning for spaCy v3 (modern alternative to Jodie)

For production use on spaCy v3+, fine-tune `en_core_web_lg` on annotated 10-K examples using Prodigy or Label Studio.[^8_3][^8_1]

```bash
# Create a spaCy training config
python -m spacy init config config.cfg --lang en --pipeline ner

# Edit config.cfg to set:
#   [paths] train = ./train.spacy, dev = ./dev.spacy
#   [components.ner.model] tok2vec source = en_core_web_lg

# Convert annotated data (from Prodigy/Label Studio JSONL export)
python -m spacy convert annotations.jsonl ./data --converter ner

# Fine-tune
python -m spacy train config.cfg --output ./sec_ner_model \
    --paths.train ./data/train.spacy \
    --paths.dev   ./data/dev.spacy \
    --initialize.vectors en_core_web_lg

# Load fine-tuned model
nlp = spacy.load("./sec_ner_model/model-best")
```

The fine-tuned v3 model supports the full spaCy component pipeline (sentencizer, dependency parser, coref) which integrates seamlessly with the relation extraction step in the broader KG pipeline.[^8_4][^8_3]
<span style="display:none">[^8_10][^8_11][^8_12][^8_13][^8_14][^8_15][^8_16][^8_17][^8_5][^8_6][^8_7][^8_8][^8_9]</span>



[^8_1]: https://github.com/jodietheai/NER-10K

[^8_2]: https://stackoverflow.com/questions/59480001/extracting-text-section-from-edgar-10-k-filings-html

[^8_3]: https://codesignal.com/learn/courses/practical-applications-of-spacy-for-real-life-tasks/lessons/information-extraction-from-legal-documents-using-spacy

[^8_4]: https://stackoverflow.com/questions/54855780/how-to-create-ner-pipeline-with-multiple-models-in-spacy

[^8_5]: https://github.com/explosion/spaCy/discussions/7733

[^8_6]: https://github.com/osamadev/Named-Entity-Recognition-Using-Spacy/blob/master/NER_Spacy.ipynb

[^8_7]: https://www.youtube.com/watch?v=2Ny0yATnuxY

[^8_8]: https://www.reddit.com/r/LanguageTechnology/comments/1jv0aos/anyone_experienced_with_pushing_large_spacy_ner/

[^8_9]: https://elijas.github.io/sec-downloader/

[^8_10]: https://github.com/explosion/spaCy/issues/2676

[^8_11]: https://pypi.org/project/sec-edgar-downloader/2.1.0/

[^8_12]: https://stackoverflow.com/questions/74225258/downloading-all-10-k-filings-for-sec-edgar-in-python

[^8_13]: https://www.youtube.com/watch?v=5QwPKZFZZW0

[^8_14]: https://github.com/jadchaar/sec-edgar-downloader

[^8_15]: https://spacy.io/universe/project/video-spacys-ner-model

[^8_16]: https://www.youtube.com/watch?v=mI6KDerAGOA

[^8_17]: https://sec-api.io/docs/sec-filings-render-api/python-example


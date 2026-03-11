+++
title = "Knowledge Graphs"
description = "Overview of classical NLP and text processing techniques"
weight = 80
outputs = ["Reveal"]
math = true
thumbnail = "/imgs/slides/nlp-text-processing.png"

[reveal_hugo]
custom_theme = "css/reveal-robinson.css"
slide_number = true
transition = "none"

+++
{{< slide background-image="/imgs/slides/nlp-text-processing.png" >}}

<h1 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >End-to-End Example<br />Deal Intelligence Agent</h1>

<h3 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >Bringing Every Technique Together</h3>
<p style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >
MSA 8700 — Module 9: Knowledge Graphs
</p>

***

## The Business Scenario

A **deal intelligence agent** monitors news feeds, emails, and web pages to keep a venture capital firm informed about competitors, acquisitions, and market moves.

Every day, hundreds of raw documents arrive — HTML pages, plain-text emails, and press releases. The firm wants structured, actionable intelligence, not piles of unread text.

***



### Using *Structuring\_Agentic\_AI.pdf* as the Outline

### Expanded with content from *Knowledge\_Graphs\_for\_Agentic\_AI.md*

### References cleaned, curated & foundational

***

{{< slide background-image="/imgs/Structuring_Agentic_AI00.png" >}}
<!-- <h1 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >End-to-End Example<br />SECTION I — The Missing Link in Agentic AI</h1> -->

***

## **1.1 Motivation: Why Agentic AI Needs Structure**

Large Language Models (LLMs) excel at **probabilistic text generation**, but they lack:

*   **Explicit reasoning**
*   **Fact‑checking**
*   **Persistent memory**
*   **Structured world models**

This limitation becomes critical for *agentic* systems — AI systems that perform multi‑step tasks, collaborate with tools, and make autonomous decisions.

--- 

### The Gap

Current agentic architectures typically include:

*   **LLMs** → fluent generation, but no explicit semantics
*   **Vector databases** → retrieve similar text, but no reasoning
*   **Tool-calling** → operational but not cognitive

What’s missing is a **semantic substrate**: a structured model of entities, relations, and domain logic.

### Why Knowledge Graphs Fill This Gap

Knowledge Graphs (KGs) provide:

*   **Explicit world models** with entities, types, and relationships
*   **Multi-hop reasoning**
*   **Long-term, inspectable memory**
*   **A stable substrate for multiple agents to coordinate**

<!-- This section frames the entire course: KGs transform LLM-based agents from *pattern mimickers* into *semantic reasoners*. -->

***

{{< slide background-image="/imgs/Structuring_Agentic_AI01.png" >}}
<!-- <h1 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >End-to-End Example<br />SECTION I — The Missing Link in Agentic AI</h1> -->
<!-- 
# **SECTION II — Foundations: Graphs, Knowledge Graphs, and Ontologies**

### *(Slides 2–6)*

**Slide references include:**

*   Slide 2: Reasoning Bottleneck
*   Slide 3: Graphs vs. Relational Tables
*   Slide 4: Semantic Triples
*   Slide 5: Ontology vs. Schema
*   Slide 6: Power & Pitfalls of Ontologies -->

***

## **2.1 From Data Tables to Graphs**

Traditional relational databases bury relationships in joins and foreign-key constraints. In contrast:

### **Graphs make relationships first-class citizens**

A graph contains:

*   **Nodes (entities)**
*   **Edges (relations)**
*   **Optionally: edge directions and weights**

This shift makes relationship traversal computationally efficient and conceptually transparent.

### Weighted & Directed Edges

Graphs allow you to encode confidence, causality, chronology, and strength of relationships — crucial for uncertain, dynamic domains like agentic AI.

***

## **2.2 From Graphs to Knowledge Graphs (KGs)**

A Knowledge Graph becomes *semantic* when relationships are labeled with **meaning**.

**Semantic triples:** Every fact is expressed as:

    (subject, predicate, object)

Examples:

*   (Alan Turing, worked\_at, Bletchley Park)
*   (Bletchley Park, located\_in, UK)

Triples create a **machine-readable, language-independent backbone** that can support:

*   reasoning
*   explainability
*   consistent grounding
*   provenance tracking

***

## **2.3 Ontologies: The Semantic Blueprint**

An **ontology** defines:

*   Classes (e.g., Person, Organization, Event)
*   Relations (e.g., worksFor, locatedIn)
*   Constraints (domain, range, cardinality)
*   Inference rules (e.g., “every CEO is an Executive”)

*** 
### Why ontologies matter for agents

*   Shared vocabulary → multi-agent interoperability
*   Clear semantics → consistent reasoning
*   Constraint checking → prevents hallucinations
*   World model → supports planning & long-term memory

### Pitfalls

*   Hard to design correctly
*   Easy to over-model
*   Requires governance
*   Must balance expressivity vs. complexity

***



# **SECTION III — Knowledge Bases: Reasoning Beyond Storage**

### *(Slide 7: “Synthesizing the Knowledge Base”)*

***

## **3.1 From Knowledge Graph to Knowledge Base**

A **Knowledge Graph = facts**  
A **Knowledge Base = facts + rules + inference**

This expands capabilities:

*   **Rule-based inference** (RDFS/OWL reasoning)
*   **Logic engines** that deduce new facts
*   **Closed-world or open-world assumptions** depending on domain
*   **Consistency checking**

Example:

*   Fact: (Turing, worked\_at, Bletchley Park)
*   Fact: (Bletchley Park, located\_in, UK)
*   Infer: *(Turing, worked\_in, UK)*

***

## **3.2 Why Agentic Systems Need Knowledge Bases**

Agent frameworks (e.g., multi-agent orchestration, workflow agents, planning agents) rely on:

*   determining preconditions
*   tracking state
*   resolving ambiguities
*   chaining dependencies
*   performing symbolic reasoning

A KB turns agents into **deliberate reasoners**, not passive pattern matchers.

***

***

# **SECTION IV — Querying Structured Knowledge**

### *(Slide 8: “A Paradigm Shift in Querying”)*

***

## **4.1 SQL vs. Vector Search vs. Graph Querying**

| Method                             | Strength                              | Weakness                         |
| ---------------------------------- | ------------------------------------- | -------------------------------- |
| **SQL**                            | structured, precise                   | no multi-hop semantics           |
| **Vector search**                  | fuzzy matching                        | no logic or structured reasoning |
| **Graph querying (Cypher/SPARQL)** | pattern matching, multi-hop reasoning | requires schema or ontology      |

*** 

### Why graph queries matter

Agents frequently need to answer questions requiring logical traversal:

*   "Which vendors supply components to companies in our supply chain?"
*   "Which events led to this failure during the last mission?"
*   "Who is related to whom across 4 hops?"

Graph languages unlock this reasoning capability.

***


# **SECTION V — Agentic Systems and the Shared World Model**

### *(Slide 9: “The Shared World Model for Multi-Agent Systems”)*

***

## **5.1 Agents Need Shared Memory**

Without shared state, multi-agent systems suffer from:

*   redundant work
*   inconsistent conclusions
*   failure to coordinate
*   hallucinated or contradictory updates

A Knowledge Graph provides:

*   **Persistent, updatable memory**
*   **Tool-agnostic data model**
*   **Domain grounding across agents**

***

## **5.2 How Agents Use KGs**

Agent types interacting with a KG:

<div style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; gap: 20px; font-size: 0.7em;">

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 20px; text-align: left;">
<h3 style="margin-top:0;">1. Ingestion & Extraction Agents</h3>
<ul>
<li>Read documents</li>
<li>Extract entities & relations (via LLMs + NLP)</li>
<li>Validate facts</li>
<li>Update the KG</li>
</ul>
</div>

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 20px; text-align: left;">
<h3 style="margin-top:0;">2. Orchestrator Agents</h3>
<ul>
<li>Route tasks based on capabilities encoded in ontology</li>
<li>Maintain global state</li>
</ul>
</div>

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 20px; text-align: left;">
<h3 style="margin-top:0;">3. Retrieval-based Reasoning Agents</h3>
<ul>
<li>Use KG traversal for grounding</li>
<li>Improve accuracy and reduce hallucination through explicit facts</li>
</ul>
</div>

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 20px; text-align: left;">
<h3 style="margin-top:0;">4. Planning Agents</h3>
<ul>
<li>Perform symbolic planning using KG structure</li>
<li>Chain tasks according to dependencies between nodes and relations</li>
</ul>
</div>

</div>


***

# **SECTION VI — The Future: Structured, Grounded Agentic AI**

### *(Slide 10: “The Future of AI is Structured”)*

***

## **6.1 The Core Argument**

LLMs alone are insufficient for reliable autonomous systems:

*   They lack *explicit reasoning structures*
*   They cannot maintain *persistent, evolving memory*
*   They cannot enforce *semantic consistency*
*   They overfit patterns instead of modeling domains

### The future requires hybrid systems

Agentic AI of the next generation will integrate:

*   **LLMs** → linguistic, generative, adaptive
*   **Knowledge Graphs** → structured, grounded, explainable
*   **Ontologies** → semantic rigor, constraints
*   **Graph reasoning engines** → inference, traversal
*   **Neuro-symbolic models** → blend statistical + logical reasoning

***

## **6.2 Why This Matters for Real-World Applications**

Critical domains require:

*   auditability
*   provenance
*   compliance
*   long-term consistency
*   multi-stakeholder semantics
*   modularity across teams and tools

Examples:

*   Healthcare
*   Finance
*   Legal AI
*   Multi-agent orchestration
*   Enterprise knowledge systems
*   Safety-critical autonomous systems

Only structured, explainable, grounded reasoning architectures can scale into these domains.

***


### **Foundational Knowledge Graphs & Semantic Web**

-   Hogan, A. et al. (2021). *Knowledge Graphs*. ACM Computing Surveys.
-   Auer, S. et al. (2007). *DBpedia: A Nucleus for a Web of Open Data*. ISWC.
-   Ehrlinger, L. & Wöß, W. (2016). *Towards a Definition of Knowledge Graphs*. SEMANTiCS.

### **Ontologies & Reasoning**

*   Gruber, T. (1995). *Toward Principles for the Design of Ontologies*.
*   Studer, R., Benjamins, V., Fensel, D. (1998). *Knowledge Engineering Principles*.
*   Baader, F. et al. (2010). *The Description Logic Handbook*.

--- 

### **Graph Query & Modeling**

*   Wood, P.T. (2012). *Query Languages for Graph Databases*. ACM SIGMOD.
*   Pérez, J. et al. (2006). *Semantics and Complexity of SPARQL*. ISWC.

### **Agentic AI, Neuro-Symbolic, Workflow AI**

*   Davis, E. & Marcus, G. (2015). *Commonsense Reasoning and Knowledge Representation*.
*   Garcez, A., Besold, T. et al. (2018). *Neuro‑Symbolic AI: The State of the Art*.


# Syllabi Analysis — System Architecture

## Variation A: Knowledge Graph Intelligence

---

## 1. Project Overview

**System Name:** Syllabi Analysis DAIS (Document-Driven Agentic Intelligence System)

**Corpus:** Class syllabi from all colleges and programs at Georgia State University (GSU), downloaded as PDF documents.

**Objective:** Build a semantic knowledge graph from GSU syllabi to enable querying about topics covered across courses and programs, how instructors address AI usage policies, prerequisite chains, learning outcomes, and cross-program coverage overlaps.

---

## 2. User Persona

**Role:** Academic Program Coordinator / Curriculum Analyst

**Context:** Works in GSU's Office of Academic Affairs or a college-level curriculum committee. Responsible for reviewing and aligning curricula across programs, identifying gaps or redundancies, ensuring coverage of emerging topics (e.g., AI, data ethics), and supporting accreditation reviews.

**Goals:**
- Understand which courses cover specific topics (e.g., "machine learning," "regression analysis," "business ethics").
- Compare how different programs address the same subject area.
- Analyze AI usage policies across instructors and departments.
- Identify prerequisite dependencies and potential curriculum gaps.
- Support accreditation by mapping learning outcomes to courses.

**Pain Points:**
- Manually reviewing hundreds of syllabi is infeasible.
- No structured, queryable representation of syllabi content exists.
- Cross-program comparisons require scanning documents from multiple colleges.

---

## 3. Key Use Cases

| # | Use Case | Example Query |
|---|----------|---------------|
| 1 | **Topic Coverage Search** | "Which courses across GSU cover natural language processing?" |
| 2 | **AI Policy Comparison** | "How do instructors in the Robinson College of Business address the use of generative AI compared to the College of Arts & Sciences?" |
| 3 | **Cross-Program Overlap** | "What topics are shared between the MS in Analytics and the MS in Computer Science programs?" |
| 4 | **Prerequisite Chain Analysis** | "What is the prerequisite chain leading to advanced machine learning courses?" |
| 5 | **Learning Outcome Mapping** | "Which courses list 'critical thinking' or 'data-driven decision making' as a learning outcome?" |
| 6 | **Temporal/Policy Trend** | "Has the mention of AI usage policies increased across syllabi over the last three semesters?" |

---

## 4. Conceptual Knowledge Graph Schema

### Entities (Nodes)

| Entity Type | Attributes |
|-------------|------------|
| **Course** | course_code, title, credit_hours, level (undergrad/grad) |
| **Instructor** | name, department, college |
| **Program** | name, degree_type (BS, MS, MBA, PhD), college |
| **College** | name (e.g., Robinson College of Business) |
| **Topic** | name, category (e.g., "statistics", "programming", "ethics") |
| **Learning Outcome** | description, bloom_taxonomy_level |
| **Textbook** | title, author, edition |
| **AI Policy** | policy_type (permitted, restricted, prohibited), details |
| **Semester** | term, year |
| **Assessment Method** | type (exam, project, paper, participation) |

### Relationships (Edges)

| Relationship | From → To | Attributes |
|-------------|-----------|------------|
| TAUGHT_BY | Course → Instructor | semester |
| BELONGS_TO | Course → Program | required/elective |
| OFFERED_BY | Program → College | — |
| COVERS_TOPIC | Course → Topic | depth (intro/intermediate/advanced), weeks_allocated |
| HAS_OUTCOME | Course → Learning Outcome | — |
| USES_TEXTBOOK | Course → Textbook | — |
| HAS_AI_POLICY | Course → AI Policy | semester |
| HAS_PREREQUISITE | Course → Course | — |
| OFFERED_IN | Course → Semester | — |
| USES_ASSESSMENT | Course → Assessment Method | weight_percent |

---

## 5. System Architecture

```mermaid
graph TB
    subgraph UI["USER INTERFACES"]
        Chat["Chat Interface<br/>(Web UI / API)"]
        Batch["Batch Query Interface<br/>(CLI / REST endpoint)"]
    end

    subgraph Orch["ORCHESTRATION LAYER (LangGraph)"]
        Router["Query Router Agent"]
        Coord["Agent Coordinator"]
        RespGen["Response Generator Agent"]
    end

    subgraph Retrieval["QUERY & RETRIEVAL LAYER"]
        GraphQ["Graph Query Agent<br/>(Cypher → Neo4j)"]
        VecQ["Vector Similarity<br/>Search Agent (Qdrant)"]
        SQLQ["Structured SQL<br/>Query Agent (PostgreSQL)"]
    end

    subgraph Stores["DATA STORES"]
        Neo4j["Neo4j<br/>(Knowledge Graph)"]
        Qdrant["Qdrant<br/>(Vector Embeddings)"]
        Postgres["PostgreSQL<br/>(Metadata, Documents,<br/>AI Policies)"]
    end

    subgraph Extract["EXTRACTION & GRAPH CONSTRUCTION LAYER"]
        EntExt["Entity Extraction<br/>Agent"]
        RelExt["Relationship Extraction<br/>Agent"]
        GraphVal["Graph Validation<br/>& Deduplication Agent"]
    end

    subgraph DocProc["DOCUMENT PROCESSING LAYER"]
        Ingest["PDF Ingestion<br/>(PyPDF2 / PDFMiner)"]
        TextChunk["Text Extraction<br/>& Chunking"]
        MetaExt["Metadata<br/>Extraction"]
        VecEmbed["Vector Embedding<br/>(Ollama)"]
        SectionClass["Syllabus Section<br/>Classifier (LLM)"]
    end

    subgraph External["EXTERNAL SERVICES"]
        Ollama["Ollama Endpoint<br/>(Text Generation +<br/>Embeddings)"]
    end

    Input["PDF Syllabi Directory<br/>(by College / Program / Semester)"]

    Input --> Ingest
    Ingest --> TextChunk
    TextChunk --> SectionClass
    SectionClass --> MetaExt
    SectionClass --> VecEmbed
    SectionClass --> EntExt
    SectionClass --> RelExt
    MetaExt --> Postgres
    VecEmbed --> Qdrant
    EntExt --> GraphVal
    RelExt --> GraphVal
    GraphVal --> Neo4j

    Chat --> Router
    Batch --> Router
    Router --> Coord
    Coord --> GraphQ
    Coord --> VecQ
    Coord --> SQLQ
    GraphQ --> Neo4j
    VecQ --> Qdrant
    SQLQ --> Postgres
    GraphQ --> RespGen
    VecQ --> RespGen
    SQLQ --> RespGen
    RespGen --> Chat
    RespGen --> Batch

    Ollama -.->|text generation| SectionClass
    Ollama -.->|text generation| EntExt
    Ollama -.->|text generation| RelExt
    Ollama -.->|text generation| GraphVal
    Ollama -.->|embeddings| VecEmbed
    Ollama -.->|text generation| Router
    Ollama -.->|text generation| RespGen
    Ollama -.->|text2cypher| GraphQ
```

---

## 6. Component Details

### 6.1 Document Processing Layer

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **PDF Ingestion** | PyPDF2, PDFMiner | Read PDF syllabi from input directory |
| **Text Extraction & Chunking** | PDFMiner, custom logic | Extract text; chunk by syllabus section (course info, schedule, policies, outcomes) |
| **Syllabus Section Classifier** | LLM via external Ollama endpoint | Classify extracted text blocks into semantic sections: course description, topics/schedule, AI policy, grading, learning outcomes, textbooks, prerequisites |
| **Metadata Extraction** | LLM via external Ollama endpoint + regex | Extract structured fields: course code, instructor name, semester, college, program |
| **Vector Embedding** | Ollama embedding endpoint (e.g., `nomic-embed-text` or `mxbai-embed-large`) | Generate embeddings for text chunks for similarity search |

### 6.2 Extraction & Graph Construction Layer

| Agent | Purpose |
|-------|---------|
| **Entity Extraction Agent** | Uses LLM to identify entities (courses, instructors, topics, outcomes, textbooks, AI policies) from classified syllabus sections |
| **Relationship Extraction Agent** | Infers relationships (COVERS_TOPIC, HAS_PREREQUISITE, TAUGHT_BY, HAS_AI_POLICY, etc.) from extracted entities and context |
| **Graph Validation & Deduplication Agent** | Resolves duplicate entities (e.g., "Prof. Smith" vs "John Smith"), normalizes topic names, enforces schema consistency |

### 6.3 Data Stores

| Store | Technology | Contents |
|-------|-----------|----------|
| **Knowledge Graph** | Neo4j | Entities and relationships per schema above |
| **Vector Store** | Qdrant | Text chunk embeddings for semantic similarity search |
| **Relational Store** | PostgreSQL | Document metadata, raw text, AI policy details, evaluation logs |

### 6.4 Query & Retrieval Layer

| Agent | Purpose |
|-------|---------|
| **Graph Query Agent** | Translates natural language questions into Cypher queries against Neo4j |
| **Vector Similarity Search Agent** | Performs semantic search over syllabus text chunks in Qdrant |
| **Structured SQL Query Agent** | Queries PostgreSQL for metadata-heavy questions (e.g., "How many courses in the Robinson College have AI policies?") |

### 6.5 Orchestration Layer

| Component | Purpose |
|-----------|---------|
| **Query Router Agent** | Analyzes incoming user query, determines which retrieval agent(s) to invoke (graph, vector, SQL, or combination) |
| **Agent Coordinator** | Manages multi-agent execution flow; merges results from parallel retrievals |
| **Response Generator Agent** | Synthesizes final natural-language answer from retrieved graph substructures and text snippets; includes citations back to specific syllabi |

### 6.6 User Interfaces

| Interface | Technology | Purpose |
|-----------|-----------|---------|
| **Chat Interface** | Provided Web UI → REST API (FastAPI) | Interactive Q&A for curriculum analysts; shows answers with citations, graph visualizations |
| **Batch Query Interface** | REST endpoint / CLI script | Accepts JSON file of queries, returns structured outputs for evaluation |

---

## 7. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| LLM (text generation) | External Ollama endpoint (on-prem, e.g., `llama3.1`, `mistral`) |
| LLM (embeddings) | External Ollama endpoint (e.g., `nomic-embed-text`, `mxbai-embed-large`) |
| Agent Framework | **LangGraph** — state-graph orchestration with conditional routing |
| LangChain Integration | `langchain-ollama` (ChatOllama, OllamaEmbeddings) for LLM/embedding calls |
| PDF Processing | PyPDF2, PDFMiner |
| Knowledge Graph | Neo4j (+ `neo4j` Python driver) |
| Vector Database | Qdrant (+ `qdrant-client`) |
| Relational Database | PostgreSQL (+ `psycopg2` / SQLAlchemy) |
| Web API | FastAPI |
| Containerization | Docker + Docker Compose |
| CI/CD | GitLab CI |

---

## 8. LangGraph Agent Architecture

**Why LangGraph:** The system has two distinct multi-step pipelines — ingestion and query — each with conditional branching. LangGraph's state-graph model maps naturally to both:

- **Nodes** = agent steps (extract, classify, embed, query, respond)
- **Edges** = transitions, including conditional routing (e.g., route query to graph vs. vector vs. SQL agent based on intent)
- **State** = shared context passed between nodes (document metadata, extracted entities, query context, retrieved results)

### 8.1 Ingestion Graph

```mermaid
graph TD
    Start(["START (PDF path)"])
    Extract["extract_text<br/>PyPDF2 / PDFMiner"]
    Classify["classify_sections<br/>LLM (Ollama)"]
    Entities["extract_entities<br/>(LLM)"]
    Relations["extract_relations<br/>(LLM)"]
    Embed["generate_embeddings<br/>(Ollama)"]
    StoreMeta["store_metadata<br/>(PostgreSQL)"]
    Validate["validate_graph<br/>& dedup (LLM)"]
    StoreVec["store_vectors<br/>(Qdrant)"]
    StoreGraph["store_graph<br/>(Neo4j)"]

    Start --> Extract --> Classify
    Classify --> Entities
    Classify --> Relations
    Classify --> Embed
    Classify --> StoreMeta
    Entities --> Validate
    Relations --> Validate
    Embed --> StoreVec
    Validate --> StoreGraph
```

### 8.2 Query Graph

```mermaid
graph TD
    Start(["START (user query)"])
    Classify["classify_intent<br/>LLM determines query type"]
    GraphAgent["graph_query agent<br/>(Cypher → Neo4j)"]
    VecAgent["vector_search agent<br/>(→ Qdrant)"]
    SQLAgent["sql_query agent<br/>(SQL → PostgreSQL)"]
    Merge["merge_results<br/>combine & rank"]
    Response["generate_response<br/>LLM synthesizes answer<br/>with citations"]

    Start --> Classify
    Classify -->|graph query| GraphAgent
    Classify -->|semantic search| VecAgent
    Classify -->|structured query| SQLAgent
    GraphAgent --> Merge
    VecAgent --> Merge
    SQLAgent --> Merge
    Merge --> Response
```

The **conditional edge** after `classify_intent` can route to one, two, or all three retrieval agents depending on the query. For example, "Which courses cover NLP?" routes to the graph agent, while "Summarize the AI policy for CSC 4520" routes to vector search, and "How many Robinson College courses mention Python?" routes to SQL.

---

## 9. Data Flow Summary

```mermaid
graph TD
    PDF["PDF Syllabi"]
    Step1["1. Ingest & Extract Text<br/>(PyPDF2/PDFMiner)"]
    Step2["2. Classify Syllabus Sections (LLM)<br/>Course Info, Topics/Schedule, AI Policy,<br/>Grading, Learning Outcomes, Textbooks, Prerequisites"]
    Step3a["3a. Entity Extraction Agent (LLM)<br/>Courses, Instructors, Topics,<br/>Outcomes, Policies"]
    Step3b["3b. Relationship Extraction Agent (LLM)<br/>COVERS_TOPIC, HAS_PREREQUISITE,<br/>TAUGHT_BY, etc."]
    Step3c["3c. Vector Embedding (Ollama)<br/>Chunk embeddings → Qdrant"]
    Step3d["3d. Metadata → PostgreSQL"]
    Step4["4. Graph Validation & Dedup Agent<br/>Normalize topics, resolve instructor aliases"]
    Step5["5. Write to Neo4j (graph),<br/>Qdrant (vectors), PostgreSQL (metadata)"]
    Step6["6. User Query → Query Router →<br/>Graph/Vector/SQL Agents →<br/>Response Generator → Answer"]

    PDF --> Step1 --> Step2
    Step2 --> Step3a
    Step2 --> Step3b
    Step2 --> Step3c
    Step2 --> Step3d
    Step3a --> Step4
    Step3b --> Step4
    Step3c --> Step5
    Step3d --> Step5
    Step4 --> Step5
    Step5 --> Step6
```

---

## 10. Milestone Alignment

| Milestone | Deliverables for Syllabi Analysis |
|-----------|----------------------------------|
| **M01** | This document: variation selection (A), persona, use cases, schema |
| **M02** | PDF ingestion pipeline, text extraction, section classification, vector embeddings, metadata to PostgreSQL; architecture diagram; Docker Compose setup |
| **M03** | Multi-agent pipeline (entity/relationship extraction → Neo4j); initial chat interface wired to query agents; basic batch query endpoint |
| **M04** | Evaluation test set (50–100 queries about topics, AI policies, cross-program coverage); baseline metrics; error analysis and 3+ improvement ideas |
| **M05** | Improvements (e.g., better topic normalization, hybrid graph+vector retrieval); ablation study (graph-only vs. vector-only vs. hybrid); iteration report |
| **M06** | Deployed system (chat + batch); technical report (10–15 pages); demo video (5–10 min); in-class presentation |

---

## 11. Evaluation Test Set Plan

**Size:** 50–100 queries

**Categories:**

| Category | Example Query | Metric |
|----------|---------------|--------|
| Topic lookup | "Which courses cover regression analysis?" | Precision, Recall, F1 |
| AI policy extraction | "What is the AI usage policy for ACCT 2101?" | Exact match / LLM-judged accuracy |
| Cross-program comparison | "Compare data visualization coverage in Analytics vs. CS programs" | LLM-judged answer quality (1–5 scale) |
| Prerequisite reasoning | "What prerequisites are needed before taking CSC 8820?" | Graph path accuracy |
| Aggregation | "How many courses in Robinson College mention Python?" | Numerical accuracy |
| Temporal trend | "Has AI policy language changed between Fall 2024 and Spring 2026?" | LLM-judged quality |

**Reference answers** will be manually authored by the team using a sample of 20–30 syllabi reviewed in full.

---

## 12. Containerization Plan

```yaml
# docker-compose.yml (outline)
services:
  neo4j:
    image: neo4j:5
    ports: [7474, 7687]
    volumes:
      - neo4j_data:/data
  qdrant:
    image: qdrant/qdrant
    ports: [6333]
    volumes:
      - qdrant_data:/qdrant/storage
  postgres:
    image: postgres:18
    ports: [5432]
    volumes:
      - pg_data:/var/lib/postgresql/data
  app:
    build: ./app
    depends_on: [neo4j, qdrant, postgres]
    ports: [8000]
    environment:
      - OLLAMA_BASE_URL=http://<external-ollama-host>:11434   # external endpoint
      - OLLAMA_MODEL=llama3.1
      - OLLAMA_EMBED_MODEL=nomic-embed-text
      - NEO4J_URI=bolt://neo4j:7687
      - QDRANT_URL=http://qdrant:6333
      - POSTGRES_URL=postgresql://user:pass@postgres:5432/syllabi
  web-ui:
    build: ./web-ui
    depends_on: [app]
    ports: [3000]

volumes:
  neo4j_data:
  qdrant_data:
  pg_data:
```

**Note:** Ollama is **not** containerized locally — the system connects to an external on-prem Ollama endpoint for both text generation and vector embedding. All other components (Neo4j, Qdrant, PostgreSQL, application, web UI) run as Docker containers orchestrated by Docker Compose.

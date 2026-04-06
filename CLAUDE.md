# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

University course repository for **MSA 8700: Building Generative AI Business Solutions** (Georgia State University). Contains a Hugo-based course website, Jupyter notebooks across 14 AI/ML topics, and full-stack applications.

Published site: https://msa8700.molnar.ai

## Build & Development Commands

### Hugo Website (www/)
```bash
# Local development server
cd www && hugo server --buildFuture --buildDrafts

# Production build (matches CI)
cd www && hugo --gc --minify --buildFuture

# Generate publications data (required before build if publications.bib changed)
cd www/tools && pip install bibtexparser && ./bibtex2bibjson.py ../assets/publications.bib > ../data/publications.json
```

### Prompt Exercise App (src/prompt-exercise/)
```bash
# Backend (FastAPI)
cd src/prompt-exercise/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Docker
cd src/prompt-exercise/backend && docker-compose up -d
```

### N8N Workflow Engine
```bash
cd N8N-Examples && docker-compose up -d  # Port 23010
```

### Fine-tuning (GPU required)
```bash
cd src/finetuning && pip install -r requirements.txt
```

## Architecture

### Website (www/)
- **Hugo static site** with two themes: `reveal-hugo` (slide decks) and `pmolnar` (custom layouts)
- Themes are git submodules — clone with `--recurse-submodules`
- Content in `www/content/`: topics/, slides/ (Reveal.js), assignments/, publications/, resources/
- Data files in `www/data/`: schedule.json, milestones_schedule.json, project-evaluation-rubric.json
- Tooling in `www/tools/`: Python scripts to generate JSON data from BibTeX and schedule sources
- CI/CD: GitHub Actions (`.github/workflows/hugo.yaml`) — Hugo 0.137.1, builds on push to main (production) or pages (preview with drafts)
- Content must be **WCAG 2.1 Level AA** compliant

### Application Stack (src/prompt-exercise/)
- **Backend**: FastAPI + LangChain + SQLAlchemy 2.0 (async, PostgreSQL) + Alembic migrations
- **Structure**: `app/models/`, `app/routers/`, `app/services/`, `app/utils/`, `app/test/`
- **LLM**: Ollama-based (langchain-ollama) — all examples target on-premise Ollama endpoints, not cloud APIs

### Topic Directories
Each top-level directory (AgenticAI, DocumentProcessing, RAG, KnowledgeGraphs, etc.) contains Jupyter notebooks and/or Python scripts for that course topic. Key ones:
- **AgenticAI/**: Adventure game (FastAPI + MCP server) and multi-framework RAG examples (LangChain, LlamaIndex, AutoGen, Strands)
- **DocumentProcessing/**: Pipeline stages — PDF extraction, chunking, embedding (each with own requirements.txt)
- **KnowledgeGraphs/**: Notebooks + 3 GraphRAG examples
- **RAG/**: Notebooks + evaluation suite; uses FAISS, sentence-transformers, Cohere
- **QueryLanguages/**: NL-to-SQL, NL-to-SPARQL, NL-to-Cypher translation notebooks

### Syllabi Analysis System (syllabi-analysis-architecture.md)
Reference architecture for the course capstone project — a multi-agent document analysis system using:
- Neo4j (knowledge graph) + Qdrant (vectors) + PostgreSQL (metadata)
- LangGraph orchestration with conditional routing
- FastAPI web + batch endpoints

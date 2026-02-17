# Agentic RAG Examples

Beginner-friendly examples of **Agentic Retrieval-Augmented Generation (RAG)** using four popular AI agent frameworks. All examples run locally using **Ollama** -- no paid API keys required.

## What is Agentic RAG?

Standard RAG always retrieves documents before answering. **Agentic** RAG gives the LLM a choice: it can decide whether to search a knowledge base, answer from its own knowledge, or combine both. The "agent" is the decision-maker.

## Prerequisites

1. **Python 3.10+**
2. **Ollama** -- install from https://ollama.com then pull the models:
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```
3. Alternatively use Ollama cloud for testing https://docs.ollama.com/cloud (see `ollama_cloud.env` file)
4. Adjust the file `.env` with your settings 

## Examples

| Directory | Framework | RAG Approach | Key Concept |
|---|---|---|---|
| `langchain_rag/` | LangChain + LangGraph | FAISS vector store with retrieval tool | `create_react_agent` decides when to search |
| `strands_rag/` | AWS Strands Agents | Keyword search with `@tool` decorator | Agent with custom retrieval tool |
| `autogen_rag/` | Microsoft AutoGen | ChromaDB vector memory | Memory protocol auto-injects context |
| `llamaindex_rag/` | LlamaIndex | VectorStoreIndex as QueryEngineTool | ReAct agent with query engine tool |

## Quick Start


### Run directly

```bash
# Install all Python dependencies
pip install -r requirements.txt

# Test your Ollama conection
python test_ollama_connection.py

# Run any example
python langchain_rag/agent.py
python strands_rag/agent.py
python autogen_rag/agent.py
python llamaindex_rag/agent.py
```

### Run as container

```bash
# Build image 
docker compose build

# Test your Ollama conection
docker compose run agentic-rag 

# Run any example
docker compose run agentic-rag langchain_rag/agent.py
docker compose run agentic-rag strands_rag/agent.py
docker compose run agentic-rag autogen_rag/agent.py
docker compose run agentic-rag llamaindex_rag/agent.py
```

Each example uses the same sample FAQ document (`sample_docs/company_faq.txt`) about a fictional company called Acme Robotics. Try asking:

- "What is the battery life of the AcmeBot X1?" (should use the knowledge base)
- "What is the capital of France?" (should answer without retrieval)
- "Does the company produce LiDAR sensors?" (mixed answers)

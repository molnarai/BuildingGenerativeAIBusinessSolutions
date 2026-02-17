#!/usr/bin/env python
"""
LlamaIndex Agentic RAG Example
================================
A ReAct agent that uses a vector index as a tool to answer questions.
The agent reasons about whether to search the knowledge base or answer directly.

Prerequisites:
    pip install llama-index llama-index-llms-ollama llama-index-embeddings-ollama

    Make sure Ollama is running locally with the required models:
        ollama pull llama3.1
        ollama pull nomic-embed-text
"""

import logging
import os

# Suppress verbose HTTP request logging from LlamaIndex/Ollama
logging.getLogger("httpx").setLevel(logging.WARNING)

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

# ---------------------------------------------------------------------------
# Step 1: Configure LlamaIndex to use Ollama
# ---------------------------------------------------------------------------

Settings.llm = Ollama(model=OLLAMA_CHAT_MODEL, base_url=OLLAMA_BASE_URL, request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(
    model_name=OLLAMA_EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL,
)

# ---------------------------------------------------------------------------
# Step 2: Load documents and build a vector index
# ---------------------------------------------------------------------------
# SimpleDirectoryReader loads files from a directory. LlamaIndex automatically
# chunks the text and creates embeddings for similarity search.

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_docs")

documents = SimpleDirectoryReader(input_dir=DOCS_DIR).load_data()
index = VectorStoreIndex.from_documents(documents)

# ---------------------------------------------------------------------------
# Step 3: Create a query engine tool
# ---------------------------------------------------------------------------
# A QueryEngineTool wraps the index so the agent can use it as a tool.
# The description tells the agent WHEN to use this tool.

query_engine = index.as_query_engine(similarity_top_k=3)

faq_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="acme_faq_search",
    description=(
        "Searches the Acme Robotics FAQ knowledge base. "
        "Use this for any questions about Acme Robotics products, pricing, "
        "operations, safety features, or company details."
    ),
)

# ---------------------------------------------------------------------------
# Step 4: Create the ReAct agent
# ---------------------------------------------------------------------------
# ReActAgent uses a Reason + Act loop:
#   1. Think about what to do
#   2. Decide whether to use a tool
#   3. Observe the tool result
#   4. Repeat or give final answer

agent = ReActAgent(
    tools=[faq_tool],
    llm=Ollama(model=OLLAMA_CHAT_MODEL, base_url=OLLAMA_BASE_URL, request_timeout=120.0),
    system_prompt=(
        "You are a helpful assistant for Acme Robotics. "
        "Use the acme_faq_search tool when questions relate to Acme Robotics. "
        "For general questions, answer from your own knowledge."
    ),
)

# ---------------------------------------------------------------------------
# Step 5: Interactive chat loop
# ---------------------------------------------------------------------------

async def main():
    print("=" * 60)
    print("  LlamaIndex Agentic RAG -- Acme Robotics Assistant")
    print("  Type 'quit' to exit.")
    print("=" * 60)

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        # The ReAct loop makes multiple LLM calls (think → tool → synthesize),
        # so this can take a while with a local model. Show a spinner.
        print("  (thinking...)", end="", flush=True)
        response = await agent.run(question)
        print(f"\r\nAssistant: {response}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

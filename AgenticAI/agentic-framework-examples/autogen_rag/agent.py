#!/usr/bin/env python
"""
Microsoft AutoGen Agentic RAG Example
=======================================
An agent that uses ChromaDB vector memory for retrieval-augmented generation.
The agent automatically searches its memory for relevant context before answering.

Prerequisites:
    pip install autogen-agentchat "autogen-ext[ollama,chromadb]"

    Make sure Ollama is running locally with the required model:
        ollama pull llama3.1
"""

import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.memory.chromadb import ChromaDBVectorMemory, PersistentChromaDBVectorMemoryConfig
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai._openai_client import ModelInfo
from autogen_core.memory import MemoryContent, MemoryMimeType

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")
#-----------------------------------------------------------------------#
#-- AutoGen currently doesn't support API keys for the OllamaClient   --#
#-- you may use a local Ollama instances with API key to Ollama Cloud --#
#-----------------------------------------------------------------------#
# OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

# ---------------------------------------------------------------------------
# Step 1: Load documents
# ---------------------------------------------------------------------------

DOCS_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_docs", "company_faq.txt")

with open(DOCS_PATH) as f:
    raw_text = f.read()

chunks = [chunk.strip() for chunk in raw_text.split("\n\n") if chunk.strip()]

# ---------------------------------------------------------------------------
# Step 2: Set up ChromaDB vector memory
# ---------------------------------------------------------------------------
# AutoGen 0.4 uses a Memory protocol. ChromaDBVectorMemory stores document
# embeddings and retrieves relevant ones automatically when the agent runs.

DB_PATH = os.path.join(os.path.dirname(__file__), ".chromadb_store")

memory = ChromaDBVectorMemory(
    config=PersistentChromaDBVectorMemoryConfig(
        collection_name="acme_faq",
        persistence_path=DB_PATH,
        k=3,               # return top 3 results
        score_threshold=0.3,
    )
)

# ---------------------------------------------------------------------------
# Step 3: Populate memory with our FAQ chunks
# ---------------------------------------------------------------------------

async def populate_memory():
    """Add FAQ chunks to the vector memory (only needs to run once)."""
    for chunk in chunks:
        await memory.add(
            MemoryContent(content=chunk, mime_type=MemoryMimeType.TEXT)
        )
    print(f"Loaded {len(chunks)} FAQ chunks into memory.")

# ---------------------------------------------------------------------------
# Step 4: Create the AutoGen agent with Ollama and memory
# ---------------------------------------------------------------------------


model_client = OllamaChatCompletionClient(
    model=OLLAMA_CHAT_MODEL,
    host=OLLAMA_BASE_URL,
)


agent = AssistantAgent(
    name="acme_assistant",
    model_client=model_client,
    system_message=(
        "You are a helpful assistant for Acme Robotics. "
        "Relevant context from the knowledge base will be provided automatically. "
        "Use that context to answer questions about Acme Robotics. "
        "For general questions, answer from your own knowledge."
    ),
    memory=[memory],
)

# ---------------------------------------------------------------------------
# Step 5: Interactive chat loop
# ---------------------------------------------------------------------------

async def main():
    # Populate the vector store with our documents
    await populate_memory()

    print("=" * 60)
    print("  AutoGen Agentic RAG -- Acme Robotics Assistant")
    print("  Type 'quit' to exit.")
    print("=" * 60)

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        # run_stream gives us a streaming response with Console output
        stream = agent.run_stream(task=question)
        result = await Console(stream)
        print(f"\nAssistant: {result.messages[-1].content}")

    await memory.close()
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python
"""
Strands Agents Agentic RAG Example
====================================
An agent built with AWS Strands Agents SDK that decides when to retrieve
information from a knowledge base vs. answering from its own knowledge.

Prerequisites:
    pip install "strands-agents[ollama]"

    Make sure Ollama is running locally with the required model:
        ollama pull llama3.1
"""

import os

from strands import Agent, tool
from strands.models.ollama import OllamaModel

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")

# ---------------------------------------------------------------------------
# Step 1: Load documents into a simple in-memory knowledge base
# ---------------------------------------------------------------------------
# In production you'd use a vector database. For learning purposes we use
# basic keyword matching so students can focus on the agent pattern itself.

DOCS_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_docs", "company_faq.txt")

with open(DOCS_PATH) as f:
    raw_text = f.read()

# Split FAQ into individual Q&A chunks
KNOWLEDGE_BASE = [chunk.strip() for chunk in raw_text.split("\n\n") if chunk.strip()]

# ---------------------------------------------------------------------------
# Step 2: Define a retrieval tool using the @tool decorator
# ---------------------------------------------------------------------------
# Strands requires type hints and a docstring with Args section.

@tool
def search_company_faq(query: str) -> str:
    """Search the Acme Robotics knowledge base for relevant information.

    Use this when the user asks about Acme Robotics products, pricing,
    company details, or operations. Do NOT use for general knowledge questions.

    Args:
        query: The search query describing what information to find.

    Returns:
        Relevant text from the knowledge base, or a message if nothing is found.
    """
    # Filter out common stop words so scoring focuses on meaningful terms
    stop_words = {
        "a", "an", "the", "is", "are", "was", "were", "what", "which", "who",
        "how", "does", "do", "did", "can", "could", "of", "in", "on", "for",
        "to", "and", "or", "it", "its", "this", "that", "with", "from", "by",
        "about", "has", "have", "had", "be", "been", "not", "no", "will", "would",
    }
    query_words = set(query.lower().split()) - stop_words
    if not query_words:
        query_words = set(query.lower().split())

    scored = []
    for chunk in KNOWLEDGE_BASE:
        chunk_lower = chunk.lower()
        # Score by how many meaningful query words appear in the chunk
        score = sum(1 for word in query_words if word in chunk_lower)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_results = [text for _, text in scored[:3]]

    if not top_results:
        return "No relevant information found in the knowledge base."
    return "\n\n".join(top_results)

# ---------------------------------------------------------------------------
# Step 3: Create the Strands agent with Ollama
# ---------------------------------------------------------------------------
# OllamaModel connects to a locally running Ollama instance.

ollama_model = OllamaModel(
    host=OLLAMA_BASE_URL,
    model_id=OLLAMA_CHAT_MODEL,
)

agent = Agent(
    model=ollama_model,
    tools=[search_company_faq],
    system_prompt=(
        "You are a helpful assistant for Acme Robotics. "
        "Use the search_company_faq tool when questions relate to Acme Robotics. "
        "For general questions, answer from your own knowledge."
    ),
)

# ---------------------------------------------------------------------------
# Step 4: Interactive chat loop
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Strands Agentic RAG -- Acme Robotics Assistant")
    print("  Type 'quit' to exit.")
    print("=" * 60)

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        result = agent(question)
        print(f"\nAssistant: {result}")


if __name__ == "__main__":
    main()

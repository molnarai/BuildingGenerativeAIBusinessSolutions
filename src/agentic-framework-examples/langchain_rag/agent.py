#!/usr/bin/env python
"""
LangChain Agentic RAG Example
==============================
An agent that can DECIDE whether to look up information from a knowledge base
or answer directly from its own knowledge. This is what makes it "agentic" --
the LLM chooses when retrieval is needed.

Prerequisites:
    pip install langchain-ollama langchain-community langchain-core langgraph faiss-cpu

    Make sure Ollama is running locally with the required models:
        ollama pull llama3.1
        ollama pull nomic-embed-text
"""

import os

from langchain_ollama import ChatOllama, OllamaEmbeddings

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ---------------------------------------------------------------------------
# Step 1: Load documents and build a vector store
# ---------------------------------------------------------------------------
# In a real app you'd load PDFs, web pages, etc. Here we read a simple text file.

DOCS_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_docs", "company_faq.txt")

with open(DOCS_PATH) as f:
    raw_text = f.read()

# Split the FAQ into individual Q&A pairs so each one becomes its own document.
chunks = [chunk.strip() for chunk in raw_text.split("\n\n") if chunk.strip()]

documents = [Document(page_content=chunk) for chunk in chunks]

# Create a FAISS vector store from the documents.
# OllamaEmbeddings turns each chunk into a numeric vector for similarity search.
embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ---------------------------------------------------------------------------
# Step 2: Define a retrieval tool the agent can choose to use
# ---------------------------------------------------------------------------

@tool
def search_company_faq(query: str) -> str:
    """Search the Acme Robotics FAQ knowledge base for relevant information.

    Use this tool when the user asks about Acme Robotics products, pricing,
    operations, or company details. Do NOT use this for general knowledge
    questions unrelated to Acme Robotics.
    """
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found in the knowledge base."
    return "\n\n".join(doc.page_content for doc in docs)

# ---------------------------------------------------------------------------
# Step 3: Create the agent
# ---------------------------------------------------------------------------
# The agent is an LLM that can reason about which tools to call.
# LangGraph's create_react_agent builds a ReAct (Reason + Act) agent.

llm = ChatOllama(model=OLLAMA_CHAT_MODEL, temperature=0, base_url=OLLAMA_BASE_URL)

agent = create_react_agent(
    llm,
    tools=[search_company_faq],
    prompt="You are a helpful assistant for Acme Robotics. "
           "Use the search tool when questions relate to Acme Robotics. "
           "For general questions, answer from your own knowledge.",
)

# ---------------------------------------------------------------------------
# Step 4: Interactive chat loop
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  LangChain Agentic RAG -- Acme Robotics Assistant")
    print("  Type 'quit' to exit.")
    print("=" * 60)

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        response = agent.invoke({"messages": [("user", question)]})

        # The response contains a list of messages; the last one is the answer.
        answer = response["messages"][-1].content
        print(f"\nAssistant: {answer}")


if __name__ == "__main__":
    main()

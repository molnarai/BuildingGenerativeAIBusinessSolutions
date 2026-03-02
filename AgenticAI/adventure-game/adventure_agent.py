#!/usr/bin/env python
"""
Adventure Game Agent with MCP Tools
====================================
An agent that plays a Prolog-based text adventure game using MCP tools.

Prerequisites:
    pip install "strands-agents[ollama]" httpx python-dotenv
    ollama pull llama3.1
"""

import os
import httpx
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.ollama import OllamaModel

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-server:8000")

@tool
def advance_game(command: str) -> str:
    """Execute game command.
    
    Args:
        command: Game command like 'go hall', 'take apple', 'look'
    
    Returns:
        Game state and narrative response
    """
    try:
        response = httpx.post(
            f"{MCP_SERVER_URL}/tools/advance_game",
            json={"command": command},
            timeout=10.0
        )
        result = response.json()
        return f"{result.get('summary', '')} Location: {result.get('location', '')} Inventory: {result.get('inventory', [])} Visible: {result.get('visible', [])}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("=" * 60)
    print("  Adventure Game Agent with MCP")
    print("=" * 60)
    print(f"OLLAMA_BASE_URL: {OLLAMA_BASE_URL}")
    print(f"OLLAMA_CHAT_MODEL: {OLLAMA_CHAT_MODEL}")
    print(f"MCP_SERVER_URL: {MCP_SERVER_URL}")
    print("=" * 60)
    
    print("Testing Ollama connection...")
    try:
        response = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
        if response.status_code == 200:
            print("✓ Ollama connection successful")
        else:
            print(f"✗ Ollama connection failed: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        return
    
    print("Testing MCP server connection...")
    try:
        response = httpx.get(f"{MCP_SERVER_URL}/health", timeout=5.0)
        print("✓ MCP server connection successful")
    except Exception as e:
        print(f"✗ MCP server connection failed: {e}")
        return
    
    print("=" * 60)
    print("  Type 'quit' to exit.")
    print("=" * 60)
    
    ollama_model = OllamaModel(
        host=OLLAMA_BASE_URL,
        model_id=OLLAMA_CHAT_MODEL,
    )
    
    agent = Agent(
        model=ollama_model,
        tools=[advance_game],
        system_prompt=(
            "You are a text adventure game narrator. "
            "Use advance_game tool to execute player commands. "
            "Generate engaging narrative based on the game state returned."
        ),
    )
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue
        
        result = agent(user_input)
        print(f"\nNarrator: {result}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Adventure Game Chat API
=======================
FastAPI server with streaming chat endpoint and static file serving.
"""

import os
import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from strands import Agent
from strands.models.ollama import OllamaModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-server:8000")

app = FastAPI()

# Initialize MCP client and tools
mcp_tools = []

async def init_mcp():
    """Initialize MCP client and load tools."""
    global mcp_tools
    # For now, use direct HTTP calls since FastMCP SSE client is complex
    # We'll create a simple wrapper tool
    from strands import tool
    import httpx
    
    @tool
    def advance_game(command: str) -> str:
        """Execute game command.
        
        Args:
            command: Game command like 'go hall', 'take apple', 'look'
        
        Returns:
            Game state and narrative response
        """
        try:
            # Use SSE endpoint with proper MCP protocol
            import json
            client = httpx.Client(timeout=10.0)
            
            # Simple workaround: call the tool via HTTP POST to SSE endpoint
            # This is a simplified approach - proper MCP client would use SSE streaming
            response = client.post(
                f"{MCP_SERVER_URL}/sse",
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "advance_game",
                        "arguments": {"command": command}
                    },
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    data = result["result"]
                    return f"{data.get('summary', '')} Location: {data.get('location', '')} Inventory: {data.get('inventory', [])} Visible: {data.get('visible', [])}"
            
            return f"Error: Unable to execute command. Status: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    mcp_tools = [advance_game]

@app.on_event("startup")
async def startup():
    await init_mcp()

ollama_model = OllamaModel(
    host=OLLAMA_BASE_URL,
    model_id=OLLAMA_CHAT_MODEL,
)

class ChatRequest(BaseModel):
    message: str

async def generate_response(message: str) -> AsyncGenerator[str, None]:
    """Generate streaming response from agent."""
    agent = Agent(
        model=ollama_model,
        tools=mcp_tools,
        system_prompt=(
            "You are a text adventure game narrator. "
            "Use advance_game tool to execute player commands. "
            "Generate engaging narrative based on the game state returned."
        ),
    )
    
    result = agent(message)
    
    # Stream response word by word
    words = str(result).split()
    for word in words:
        yield f"data: {word} \n\n"
        await asyncio.sleep(0.05)
    
    yield "data: [DONE]\n\n"

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Streaming chat endpoint."""
    return StreamingResponse(
        generate_response(request.message),
        media_type="text/event-stream"
    )

@app.get("/")
async def root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")

@app.get("/test.html")
async def test_page():
    """Serve the MCP test page."""
    return FileResponse("static/test.html")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

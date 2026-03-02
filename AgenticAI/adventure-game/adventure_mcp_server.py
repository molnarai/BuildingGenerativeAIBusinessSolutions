import sys
from fastmcp import FastMCP
from prolog_adventure import load_game, reset_game, prolog_step

mcp = FastMCP(name="PrologAdventure")

load_game()

@mcp.tool()
def advance_game(command: str) -> dict:
    """
    Execute a game command and return the new state.
    
    Args:
        command: Natural language command like "go hall", "take apple", "look"
    
    Returns:
        Dictionary with summary, location, inventory, visible items, and raw command
    """
    try:
        parts = command.strip().lower().split()
        if not parts:
            return {"summary": "Nothing happens.", "location": "", "inventory": [], "visible": [], "raw_command_term": ""}
        
        verb = parts[0]
        if verb == "look":
            command_term = "look"
        elif verb in ["go", "move"] and len(parts) > 1:
            command_term = f"go({parts[1]})"
        elif verb == "take" and len(parts) > 1:
            command_term = f"take({parts[1]})"
        else:
            command_term = command.replace(" ", "_")
        
        result = prolog_step(command_term)
        return {
            "summary": result["summary"],
            "location": result["state"]["location"],
            "inventory": result["state"]["inventory"],
            "visible": result["state"]["visible"],
            "raw_command_term": command_term,
        }
    except Exception as e:
        return {
            "summary": f"Error: {str(e)}",
            "location": "",
            "inventory": [],
            "visible": [],
            "raw_command_term": command,
        }

@mcp.tool()
def reset() -> str:
    """Reset the game to initial state."""
    try:
        reset_game()
        return "Game reset to initial state."
    except Exception as e:
        return f"Error resetting game: {str(e)}"

@mcp.tool()
def describe_world() -> str:
    """Get a description of the game world and available commands."""
    return """Adventure Game World:
- Rooms: kitchen, hall, garden
- Items: apple (kitchen), key (hall)
- Commands: 
  * "go <room>" - move to connected room
  * "take <item>" - pick up an item
  * "look" - examine current location"""

if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    if transport == "http":
        mcp.run(transport="sse", host="0.0.0.0", port=8000)
    else:
        mcp.run()

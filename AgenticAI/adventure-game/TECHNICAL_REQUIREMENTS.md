# Technical Requirements

### 1. High‑level architecture

- The system consists of:
    - An **MCP server** implemented with FastMCP, exposing tools that encapsulate the adventure game logic.[^1][^2]
    - A **Prolog adventure engine** that owns the world model, game state, and transition rules (rooms, items, actions) accessed via PySwip.[^3][^4]
    - One or more **LLM‑based agents** (e.g., LangGraph, fast-agent, n8n, or IDE clients) that connect to the MCP server, call game tools, and generate narrative from structured state.[^5][^6]


### 2. Game logic requirements (Prolog side)

1. **World model**
    - Rooms and connections are defined as Prolog facts, e.g. `room/1`, `connected/2`.[^7][^8]
    - Items and their locations are defined as `at(Item, Place)` where `Place` is either a room or `inventory`.
2. **Dynamic state**
    - The player location is stored in a dynamic predicate `i_am_at/1`.
    - Item positions are updated via `at/2` with `dynamic`/`retract`/`assert` operations.[^9]
3. **Core actions**
    - Supported player actions at minimum:
        - Movement: `go(Direction)` with precondition that a corresponding exit exists.
        - Item interaction: `take(Item)` and optionally `drop(Item)`.
        - Perception: `look` to redisplay current room description and visible items.
    - Game logic must reject illegal actions gracefully (e.g., moving where there is no connection, taking a non‑existent item) and still return a valid state snapshot.
4. **State transition API**
    - A single Prolog predicate `step/3` applies an action and returns:
        - A short **summary string** describing what happened.
        - A **structured state term** (e.g. a SWI Prolog dict) containing:
            - `location` – current room.
            - `inventory` – list of items carried.
            - `visible` – list of items in the current room.
    - `step(Command, Summary, StateDict)` must be pure from the MCP perspective: it encapsulates all state change internally and presents the new state to Python in one call.

### 3. MCP server requirements (FastMCP side)

1. **Server**
    - Implemented with FastMCP as a single MCP server instance.[^10][^1]
    - Uses `stdio` transport so it can be discovered by MCP‑aware clients.
2. **Tools**
    - `advance_game(command: string) -> {summary, location, visible, inventory, raw_command_term}`:
        - Parses a natural‑language‑style command into a Prolog term (e.g. `"go north"` → `go(north)`).
        - Calls `step/3` in Prolog via PySwip.
        - Returns a JSON‑serializable dict: one‑line summary + normalized state.
    - `reset() -> string`:
        - Resets the game state to the initial configuration (either by re‑consulting the Prolog file or by explicit re‑initialization).
    - Optionally `describe_world() -> string`:
        - Returns a short description of the world and available commands to help the LLM plan tool usage.
3. **Serialization**
    - MCP tools must return only JSON‑safe types (strings, numbers, lists, dicts).
    - Prolog dicts/lists must be converted into Python primitives before returning.[^4][^9]
4. **Error handling**
    - Invalid commands must not crash the server.
    - `advance_game` should return a well‑formed object with `summary` explaining that nothing happened or the command was not understood.

### 4. Agent behaviour requirements

1. **Authority split**
    - The Prolog MCP tool is the **single source of truth** for game state and allowed actions.
    - The LLM **never mutates state directly**; it only:
        - Interprets user input.
        - Decides which tool calls to make.
        - Generates narrative from the tool results.
2. **Prompting pattern**
    - System prompt must tell the LLM:
        - To use `advance_game` to apply player commands.
        - To base all descriptions strictly on the structured state returned.
    - The agent may maintain conversational history, but state continuity is guaranteed via `advance_game` and `reset`.
3. **Client compatibility**
    - The MCP server should be usable from generic MCP clients (e.g., fast-agent, LangChain MCP integration, editor plugins) without code changes.[^11][^12][^6]

### 5. Non‑functional requirements

- **Portability**: Prolog code runs on SWI‑Prolog; Python bridge uses PySwip.[^13][^4]
- **Testability**:
    - Game logic can be tested in pure Prolog (queries to `step/3`).
    - MCP server can be tested with a simple Python client calling `advance_game` and `reset`.
- **Extensibility**: New verbs (e.g., `open_door`, `talk_to`) can be added in Prolog without changing the MCP tool interface, as long as they still go through `step/3`.

***

## Code Snippets

### A. Prolog adventure logic (`adventure_game.pl`)

```prolog
:- dynamic i_am_at/1.
:- dynamic at/2.

% Rooms
room(kitchen).
room(hall).
room(garden).

% Connections (undirected for simplicity)
connected(kitchen, hall).
connected(hall, kitchen).
connected(hall, garden).
connected(garden, hall).

% Initial state
i_am_at(kitchen).

% Items
at(apple, kitchen).
at(key, hall).

% Room descriptions
describe(kitchen, "You are in a small kitchen. There is a wooden table here.").
describe(hall,    "You are in a hall with a coat rack and a dusty mirror.").
describe(garden,  "You are in a quiet garden with flowers and a stone bench.").

% State transition API:
% step(+Command, -Summary, -StateDict)
% Command: go(Direction) | take(Item) | look | ...
% StateDict: state{location:Loc, inventory:Inv, visible:Visible}

step(go(Direction), Result, state{location: NewPlace, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    connected(Here, NewPlace),
    direction_ok(Here, Direction, NewPlace),
    retract(i_am_at(Here)),
    asserta(i_am_at(NewPlace)),
    inventory_list(Inv),
    visible_items(NewPlace, Visible),
    describe(NewPlace, Desc),
    atomic_list_concat(["You go ", Direction, ". ", Desc], Result), !.

step(take(Item), Result, state{location: Here, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    at(Item, Here),
    retract(at(Item, Here)),
    asserta(at(Item, inventory)),
    inventory_list(Inv),
    visible_items(Here, Visible),
    atomic_list_concat(["You pick up the ", Item, "."], Result), !.

step(look, Result, state{location: Here, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    describe(Here, Desc),
    inventory_list(Inv),
    visible_items(Here, Visible),
    atomic_list_concat(["You look around. ", Desc], Result), !.

% Fallback: invalid or impossible command
step(_Command, "Nothing happens.", state{location: Here, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    inventory_list(Inv),
    visible_items(Here, Visible).

% Direction mapping (simple; can be expanded)
direction_ok(From, _Dir, To) :- connected(From, To).

inventory_list(Items) :-
    findall(Item, at(Item, inventory), Items).

visible_items(Place, Items) :-
    findall(Item, at(Item, Place), Items).
```

This follows classic “Adventure in Prolog” patterns but wraps a single `step/3` predicate suitable for programmatic use.[^8][^14][^7]

***

### B. Python bridge (`prolog_adventure.py`)

```python
# prolog_adventure.py
from pyswip import Prolog
from typing import Dict, Any, List

prolog = Prolog()

def load_game() -> None:
    """Consult the adventure game Prolog file."""
    prolog.consult("adventure_game.pl")

def reset_game() -> None:
    """Reset game state by reloading the Prolog file."""
    # Simplest reset: new Prolog instance & re-consult
    global prolog
    prolog = Prolog()
    prolog.consult("adventure_game.pl")

def prolog_step(command_term: str) -> Dict[str, Any]:
    """
    Execute step(Command, Summary, State) in Prolog.

    command_term: e.g. "go(north)", "take(apple)", "look".
    Returns: { "summary": str, "state": {location, inventory, visible} }
    """
    query = f"step({command_term}, Summary, State)"
    results = list(prolog.query(query, maxresult=1))
    if not results:
        return {
            "summary": "Nothing happens.",
            "state": {"location": "", "inventory": [], "visible": []},
        }

    res = results[^0]
    summary = str(res["Summary"])
    state = res["State"]  # SWI dict: state{location:..., inventory:..., visible:...}

    location = str(state["location"])
    inventory = [str(x) for x in state["inventory"]]
    visible = [str(x) for x in state["visible"]]

    return {
        "summary": summary,
        "state": {
            "location": location,
            "inventory": inventory,
            "visible": visible,
        },
    }
```

This uses the basic PySwip query pattern shown in its examples.[^3][^9][^4]

***

### C. MCP server (`adventure_mcp_server.py`)

```python
# adventure_mcp_server.py
from fastmcp import FastMCP
from prolog_adventure import load_game, reset_game, prolog_step

mcp = FastMCP(
    name="PrologAdventure",
    description="MCP server exposing a Prolog-based text adventure game.",
)

# Load Prolog game logic at startup
load_game()


@mcp.tool
def advance_game(command: str) -> dict:
    """
    Advance the adventure game by applying a command.

    Args:
      command: Natural-language-ish command, e.g.:
        - "look"
        - "go north"
        - "take apple"

    Returns:
      {
        "summary": str,
        "location": str,
        "visible": [str],
        "inventory": [str],
        "raw_command_term": str
      }
    """
    parsed = command.strip().lower()

    if parsed in ("look", "l"):
        command_term = "look"
    elif parsed.startswith("go "):
        direction = parsed.split(" ", 1)[^1].replace(" ", "_")
        command_term = f"go({direction})"
    elif parsed.startswith("take "):
        item = parsed.split(" ", 1)[^1].replace(" ", "_")
        command_term = f"take({item})"
    else:
        # Fallback: treat entire input as a functor with no args, if valid
        # e.g. "look" or "dance"
        safe = parsed.replace(" ", "_")
        command_term = safe

    result = prolog_step(command_term)

    return {
        "summary": result["summary"],
        "location": result["state"]["location"],
        "visible": result["state"]["visible"],
        "inventory": result["state"]["inventory"],
        "raw_command_term": command_term,
    }


@mcp.tool
def reset() -> str:
    """
    Reset the adventure to the initial state.
    """
    reset_game()
    return "Game reset. You are back at the starting location."


@mcp.tool
def describe_world() -> str:
    """
    Provide a short description of the game world & available commands.
    """
    return (
        "You are in a small world with three rooms: kitchen, hall, garden. "
        "You can move between connected rooms with commands like 'go north' "
        "or 'go south' (directions are abstracted). You can 'look' to inspect "
        "your surroundings and 'take <item>' to pick up items like 'apple' or 'key'. "
        "Use 'advance_game' with these commands; I will handle the game state."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

This matches FastMCP’s tool pattern: decorated Python functions become MCP tools with generated JSON schemas for arguments/returns.[^12][^10][^1]

***

### D. Minimal agent loop sketch (LLM + MCP)

```python
# agent_loop_demo.py
import asyncio
from fastmcp import Client, StdioServerParameters
from some_llm_client import call_llm  # your own LLM wrapper


async def main():
    server = StdioServerParameters(
        command="python",
        args=["adventure_mcp_server.py"],
    )

    async with Client(server) as client:
        # Reset game once at start
        await client.call_tool("reset", {})

        while True:
            user_input = input("Player> ")
            if user_input.strip().lower() in {"quit", "exit"}:
                break

            # Call Prolog-backed tool to update state
            state = await client.call_tool(
                "advance_game",
                {"command": user_input},
            )

            # Let LLM narrate based on structured state
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are the narrator of a text adventure game. "
                        "The game state returned by a tool is authoritative. "
                        "Describe what the player experiences, based strictly on that state."
                    ),
                },
                {
                    "role": "system",
                    "content": f"Game state: {state}",
                },
                {
                    "role": "user",
                    "content": f"The player just typed: {user_input}. Describe what happens.",
                },
            ]

            reply = call_llm(messages)
            print(f"Narrator> {reply}")


if __name__ == "__main__":
    asyncio.run(main())
```

This satisfies the requirement that the Prolog MCP tool manages state and allowed actions, while the AI agent “fills in the narrative” on top of the returned structure.[^6][^5][^12]


[^1]: https://github.com/jlowin/fastmcp

[^2]: https://gofastmcp.com

[^3]: https://pyswip.org/examples.html

[^4]: https://pypi.org/project/pyswip/0.3.0/

[^5]: https://composio.dev/blog/the-complete-guide-to-building-mcp-agents

[^6]: https://docs.langchain.com/oss/python/langchain/mcp

[^7]: https://amzi.com/AdventureInProlog/a1start.php

[^8]: http://amzi.com/AdventureInProlog/a2facts.php

[^9]: https://pyswip.readthedocs.io/en/latest/api/prolog.html

[^10]: https://gofastmcp.com/servers/tools

[^11]: https://fast-agent.ai

[^12]: https://www.datacamp.com/tutorial/building-mcp-server-client-fastmcp

[^13]: https://github.com/yuce/pyswip

[^14]: https://gist.github.com/3191695

[^15]: https://www.cerbos.dev/blog/how-to-secure-your-fast-mcp-server-with-permission-management

[^16]: https://engineering.leanix.net/blog/mcp-prompts/

[^17]: https://codesignal.com/learn/courses/developing-and-integrating-a-mcp-server-in-python/lessons/exploring-and-exposing-mcp-server-capabilities-tools-resources-and-prompts

[^18]: https://gofastmcp.com/servers/prompts

[^19]: https://stackoverflow.com/questions/57207781/using-pyswip-to-query-prolog-database-from-python


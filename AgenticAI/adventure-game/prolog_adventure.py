from pyswip import Prolog
from typing import Dict, Any

prolog = Prolog()

def load_game() -> None:
    """Consult the adventure game Prolog file."""
    prolog.consult("adventure_game.pl")

def reset_game() -> None:
    """Reset game state by reloading the Prolog file."""
    global prolog
    prolog = Prolog()
    prolog.consult("adventure_game.pl")

def prolog_step(command_term: str) -> Dict[str, Any]:
    """
    Execute step(Command, Summary, State) in Prolog.
    
    command_term: e.g. "go(hall)", "take(apple)", "look".
    Returns: { "summary": str, "state": {location, inventory, visible} }
    """
    query = f"step({command_term}, Summary, State)"
    results = list(prolog.query(query, maxresult=1))
    if not results:
        return {
            "summary": "Nothing happens.",
            "state": {"location": "", "inventory": [], "visible": []},
        }
    
    res = results[0]
    summary = str(res["Summary"])
    state = res["State"]
    
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

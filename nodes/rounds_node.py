from nodes.state import DebateState
from utils.logging_utils import logger

def rounds_node(state: DebateState) -> DebateState:
    """
    Updates the round number and switches the current agent.
    """
    current_round = state["current_round"]
    current_agent = state["current_agent"]
    
    next_round = current_round + 1
    next_agent = "Philosopher" if current_agent == "Scientist" else "Scientist"
    
    logger.log("RoundUpdate", {"from": current_round, "to": next_round, "next_agent": next_agent})
    
    return {
        "current_round": next_round,
        "current_agent": next_agent
    }

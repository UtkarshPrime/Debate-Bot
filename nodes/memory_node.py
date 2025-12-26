from nodes.state import DebateState
from utils.logging_utils import logger

def memory_node(state: DebateState) -> DebateState:
    """
    Updates memory/summary. 
    For this implementation, since we are appending messages in AgentNode, 
    this node acts as a validation or summarization step.
    We'll just log the memory update for now.
    """
    # In a more complex system, this would summarize the last few turns 
    # or extract key arguments to a separate 'summary' key.
    
    logger.log("MemoryUpdate", {"message_count": len(state["messages"])})
    
    return state

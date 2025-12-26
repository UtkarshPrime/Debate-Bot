from nodes.state import DebateState
from utils.logging_utils import logger

def user_input_node(state: DebateState) -> DebateState:
    """
    Node to handle user input. 
    In a CLI context, the input might already be in the state if passed via initial config,
    but this node ensures it's validated or prompts if missing (though usually graph starts with input).
    For this design, we assume the topic is passed in the initial state, so this node 
    might just be a pass-through or validation step.
    """
    topic = state.get("topic")
    if not topic:
        # In a real interactive graph, we might pause here, but for CLI we expect it in initial state.
        # We'll just set a default if missing for safety, or raise error.
        topic = "The impact of AI on society"
    
    logger.log("UserInput", {"topic": topic})
    
    # Initialize defaults if not present
    return {
        "topic": topic,
        "messages": [],
        "current_round": 1,
        "current_agent": "Scientist", # Scientist starts
        "winner": None,
        "reason": None
    }

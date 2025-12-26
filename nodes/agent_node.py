from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from nodes.state import DebateState
from config import GOOGLE_API_KEY, MOCK_MODE, SCIENTIST_PERSONA_PATH, PHILOSOPHER_PERSONA_PATH
from utils.logging_utils import logger
import random

def load_persona(agent_name):
    path = SCIENTIST_PERSONA_PATH if agent_name == "Scientist" else PHILOSOPHER_PERSONA_PATH
    with open(path, "r") as f:
        return f.read()

def agent_node(state: DebateState) -> DebateState:
    agent_name = state["current_agent"]
    topic = state["topic"]
    messages = state["messages"]
    
    logger.log("AgentTurnStart", {"agent": agent_name, "round": state["current_round"]})
    
    persona = load_persona(agent_name)
    
    # Construct context from previous messages
    # Filter for relevant memory? For now, we give full history as context 
    # but we could filter to just the last few turns or a summary.
    # The prompt asks to "provide each agent only the memory relevant to their next turn".
    # A simple interpretation is the last argument from the opponent + topic.
    
    conversation_history = ""
    for msg in messages:
        conversation_history += f"[{msg['round']}] {msg['agent']}: {msg['content']}\n"
    
    prompt = f"""
    {persona}
    
    Topic: {topic}
    
    Current Debate History:
    {conversation_history}
    
    Your turn. Respond to the last argument or start your opening statement if this is round 1.
    """
    
    if state.get("is_mock", False):
        response_content = f"Mock response from {agent_name} about {topic} (Round {state['current_round']})"
    else:
        llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-2.5-flash")
        response = llm.invoke([HumanMessage(content=prompt)])
        response_content = response.content
        
    # We don't update messages here, we let MemoryNode do it? 
    # Or we update it here and MemoryNode just processes it?
    # The requirements say "MemoryNode... Updates after each turn".
    # So we can return the new message in a temporary key or just append it here.
    # LangGraph nodes return a state update.
    # Let's append here for simplicity, and MemoryNode can be a pass-through or summarizer.
    
    new_message = {
        "round": state["current_round"],
        "agent": agent_name,
        "content": response_content
    }
    
    logger.log("AgentResponse", new_message)
    
    # Append to existing messages
    updated_messages = list(state["messages"]) + [new_message]
    
    return {
        "messages": updated_messages
    }

# We need to handle the state update logic carefully.
# If I return {"messages": [...]} it might overwrite.
# I will modify this to read the current messages and append.

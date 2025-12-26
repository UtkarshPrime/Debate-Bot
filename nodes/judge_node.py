from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from nodes.state import DebateState
from config import GOOGLE_API_KEY, MOCK_MODE
from utils.logging_utils import logger
import json

def judge_node(state: DebateState) -> DebateState:
    messages = state["messages"]
    topic = state["topic"]
    
    logger.log("JudgeStart", {})
    
    conversation_history = ""
    for msg in messages:
        conversation_history += f"[{msg['round']}] {msg['agent']}: {msg['content']}\n"
    
    prompt = f"""
    You are an impartial Judge.
    Review the following debate on the topic: "{topic}".
    
    Debate History:
    {conversation_history}
    
    Decide who won the debate (Scientist or Philosopher) and provide a clear reason.
    Your output must be a JSON object with keys: "winner" and "reason".
    """
    
    if state.get("is_mock", False):
        winner = "Scientist"
        reason = "Mock reason: Scientist provided more empirical data."
    else:
        llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-2.5-flash")
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content
        
        # Simple parsing (robustness would require json repair)
        try:
            # Try to find JSON in the output
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = content[start:end]
                data = json.loads(json_str)
                winner = data.get("winner", "Unknown")
                reason = data.get("reason", "No reason provided.")
            else:
                winner = "Unknown"
                reason = content
        except Exception as e:
            winner = "Error"
            reason = f"Failed to parse judge output: {e}"

    logger.log("JudgeVerdict", {"winner": winner, "reason": reason})
    
    return {
        "winner": winner,
        "reason": reason
    }

import argparse
import sys
from langgraph.graph import StateGraph, END
from nodes import DebateState, user_input_node, agent_node, memory_node, rounds_node, judge_node
from config import MAX_ROUNDS, MOCK_MODE

def route_round(state: DebateState):
    if state["current_round"] <= MAX_ROUNDS:
        return "agent"
    return "judge"

def main():
    parser = argparse.ArgumentParser(description="AI Debate System")
    parser.add_argument("--topic", type=str, help="Topic for the debate")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode")
    args = parser.parse_args()

    # If mock flag is passed, we might want to override config, but config is already loaded.
    # Ideally config should check args but config is imported at module level.
    # For now, we rely on env var or just proceed. 
    # The prompt asked for flags.
    
    topic = args.topic
    if not topic:
        topic = input("Enter topic for debate: ")

    print(f"Starting debate on topic: {topic}")
    if MOCK_MODE or args.mock:
        print("(Running in Mock Mode)")

    # Define Graph
    workflow = StateGraph(DebateState)

    workflow.add_node("user_input", user_input_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("memory", memory_node)
    workflow.add_node("rounds", rounds_node)
    workflow.add_node("judge", judge_node)

    # Define Edges
    workflow.set_entry_point("user_input")
    workflow.add_edge("user_input", "agent")
    workflow.add_edge("agent", "memory")
    workflow.add_edge("memory", "rounds")
    
    # Conditional Edge
    workflow.add_conditional_edges(
        "rounds",
        route_round,
        {
            "agent": "agent",
            "judge": "judge"
        }
    )
    
    workflow.add_edge("judge", END)

    app = workflow.compile()

    # Initial State
    initial_state = {
        "topic": topic,
        "messages": [],
        "current_round": 1,
        "current_agent": "Scientist",
        "winner": None,
        "reason": None,
        "is_mock": args.mock or MOCK_MODE
    }

    # Run
    for output in app.stream(initial_state, {"recursion_limit": 50}):
        for key, value in output.items():
            # Print output to CLI
            if key == "agent":
                last_msg = value["messages"][-1]
                print(f"[Round {last_msg['round']}] {last_msg['agent']}: {last_msg['content']}\n")
            elif key == "judge":
                print(f"[Judge] Winner: {value['winner']}")
                print(f"[Judge] Reason: {value['reason']}")

if __name__ == "__main__":
    main()

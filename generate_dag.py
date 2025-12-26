from langgraph.graph import StateGraph, END
from nodes import DebateState, user_input_node, agent_node, memory_node, rounds_node, judge_node
from run_debate import route_round

# Reconstruct graph structure (or import from run_debate if refactored)
workflow = StateGraph(DebateState)
workflow.add_node("user_input", user_input_node)
workflow.add_node("agent", agent_node)
workflow.add_node("memory", memory_node)
workflow.add_node("rounds", rounds_node)
workflow.add_node("judge", judge_node)

workflow.set_entry_point("user_input")
workflow.add_edge("user_input", "agent")
workflow.add_edge("agent", "memory")
workflow.add_edge("memory", "rounds")
workflow.add_conditional_edges("rounds", route_round, {"agent": "agent", "judge": "judge"})
workflow.add_edge("judge", END)

app = workflow.compile()

try:
    png_data = app.get_graph().draw_mermaid_png()
    with open("dag.png", "wb") as f:
        f.write(png_data)
    print("DAG saved to dag.png")
except Exception as e:
    print(f"Could not generate DAG: {e}")
    # Fallback to printing mermaid code
    print(app.get_graph().draw_mermaid())

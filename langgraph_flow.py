# langgraph_flow.py

from langgraph.graph import StateGraph
from agent_graph import process_input
from graph_state import AgentState


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("process", process_input)
    builder.set_entry_point("process")
    builder.set_finish_point("process")

    return builder.compile()
graph = build_graph()

g = graph.get_graph()

print("NODES:", g.nodes)
print("EDGES:", g.edges)




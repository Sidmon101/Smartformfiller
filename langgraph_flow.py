from langgraph.graph import StateGraph, END
from graph_state import AgentState
from agent_graph import agent_step


def build_graph():
    graph = StateGraph(AgentState)

    def agent_node(state: AgentState):
        return agent_step(state, state.get("last_user_input"))

    graph.add_node("agent", agent_node)
    graph.set_entry_point("agent")

    # 🔑 ALWAYS END after one execution
    graph.add_edge("agent", END)

    return graph.compile()

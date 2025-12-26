# agent_graph.py

from schemas import FORM_TYPES
from graph_state import AgentState
from langsmith import traceable


def init_state(form_type: str) -> AgentState:
    fields = list(FORM_TYPES[form_type]["fields"].keys())
    return {
        "messages": [],
        "form_data": {},
        "pending_field": fields[0],
        "status": "IN_PROGRESS",
        "last_user_input": None,
        "form_type": form_type,
    }


@traceable(name="process_form_input")
def process_input(state: AgentState) -> AgentState:
    if state["status"] == "COMPLETE":
        return state

    pending = state.get("pending_field")
    raw_input = state.get("last_user_input")

    if not pending or raw_input is None:
        return state

    field_schema = FORM_TYPES[state["form_type"]]["fields"][pending]
    parser = field_schema.get("parser", lambda x: x)

    try:
        parsed_value = parser(raw_input)
    except Exception:
        state["messages"].append({
            "role": "assistant",
            "content": "Invalid format. Please try again."
        })
        return state

    for validator in field_schema.get("validators", []):
        error = validator(parsed_value, state["form_data"])
        if error:
            state["messages"].append({
                "role": "assistant",
                "content": error
            })
            return state

    state["form_data"][pending] = parsed_value

    fields = list(FORM_TYPES[state["form_type"]]["fields"].keys())
    idx = fields.index(pending)

    if idx + 1 < len(fields):
        state["pending_field"] = fields[idx + 1]
    else:
        state["pending_field"] = None
        state["status"] = "COMPLETE"

    return state

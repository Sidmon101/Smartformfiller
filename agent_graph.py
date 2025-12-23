from schemas import FORM_SPECS
from graph_state import AgentState


def init_state(form_type: str):
    return AgentState(
        messages=[],
        form_data={},
        pending_field=None,
        status="IN_PROGRESS",
        last_user_input=None,
        form_type=form_type,
    )


def agent_step(state: AgentState, user_input: str | None):
    form_type = state["form_type"]
    specs = FORM_SPECS[form_type]

    # 1️⃣ Process user input for the pending field
    if user_input and state.get("pending_field"):
        field_name = state["pending_field"]
        field = specs[field_name]

        try:
            value = field.parser(user_input)
            error = field.validator(value, state["form_data"])

            if error:
                state["messages"].append({
                    "role": "assistant",
                    "content": f"Invalid input for {field.label}: {error}"
                })
                return state

            state["form_data"][field_name] = value
            state["pending_field"] = None

        except Exception as e:
            state["messages"].append({
                "role": "assistant",
                "content": f"Invalid input: {str(e)}"
            })
            return state

    # 2️⃣ Ask next missing required field
    for name, spec in specs.items():
        if spec.required and name not in state["form_data"]:
            state["pending_field"] = name
            state["messages"].append({
                "role": "assistant",
                "content": f"{spec.label}? ({spec.hint})"
            })
            return state

    # 3️⃣ Form complete
    state["status"] = "COMPLETE"
    state["messages"].append({
        "role": "assistant",
        "content": "Form complete ✅"
    })

    return state

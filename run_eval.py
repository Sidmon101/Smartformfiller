import json
import os
from dotenv import load_dotenv
from transformers import pipeline

from agent_graph import build_graph, init_state
from utils import normalize_for_export


def load_jsonl(path: str):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def get_llm():
    """
    Returns a Hugging Face text-generation pipeline.
    """
    model_name = os.getenv("HUGGINGFACE_MODEL", "tiiuae/falcon-7b-instruct")
    api_key = os.getenv("HUGGINGFACE_API_KEY", None)

    return pipeline(
        "text-generation",
        model=model_name,
        use_auth_token=api_key,
        max_new_tokens=512,
        temperature=0
    )


def run_conversation(inputs: dict) -> dict:
    llm = get_llm()
    graph = build_graph(llm)

    state = init_state(inputs["form_type"])
    state = graph.invoke(state)  # first question

    for msg in inputs["conversation"]:
        state["messages"].append({"role": "user", "content": msg})
        state["last_user_input"] = msg

        # Use Hugging Face LLM pipeline
        prompt = f"User said: {msg}\nAgent:"
        result = llm(prompt)
        assistant_msg = result[0]["generated_text"]

        # Append agent message to conversation
        state["messages"].append({"role": "assistant", "content": assistant_msg})
        state = graph.invoke(state)

        if state.get("status") in ("FAILED", "COMPLETE"):
            break

    final = normalize_for_export(state.get("final_json") or state.get("form_data") or {})
    return {"status": state.get("status"), "final_json": final, "error": state.get("error")}


def complete_and_has_keys(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
    if outputs.get("status") != reference_outputs.get("status"):
        return False
    required = reference_outputs.get("required_keys", [])
    final_json = outputs.get("final_json") or {}
    return all(k in final_json and final_json[k] not in (None, "", []) for k in required)


if __name__ == "__main__":
    load_dotenv()
    data = load_jsonl("dataset.jsonl")

    from langsmith import evaluate

    results = evaluate(
        run_conversation,
        data=data,
        evaluators=[complete_and_has_keys],
        experiment_prefix="smart-form-filler-eval",
    )
    print("Evaluation done. Check LangSmith Experiments.")
    print(results)

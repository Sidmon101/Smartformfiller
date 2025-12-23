# llm.py
import os
from huggingface_hub import InferenceClient

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = os.getenv("HUGGINGFACE_MODEL", "tiiuae/falcon-7b-instruct")

client = InferenceClient(
    model=HF_MODEL,
    token=HF_API_KEY
)

def llm(prompt: str) -> str:
    response = client.text_generation(
        prompt,
        max_new_tokens=120,
        temperature=0.7,
        do_sample=True
    )

    # HF returns plain string
    return response.strip()

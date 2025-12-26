# llm.py

from dotenv import load_dotenv
import os
from langsmith import traceable

# Load environment variables from .env
load_dotenv()

# Optional: sanity check that the key is visible
api_key = os.getenv("LANGSMITH_API_KEY")
project = os.getenv("LANGSMITH_PROJECT", "default")
print(f"[LangSmith] API Key loaded: {bool(api_key)}")
print(f"[LangSmith] Project: {project}")

# Define a list of hard-coded questions
QUESTIONS = [
    "Employee ID? (EMP1234 or numeric ID)",
    "Work Email? (name@company.com)",
    "Leave Type? (Sick, Casual, Paid, etc.)",
    "Start Date? (YYYY-MM-DD)",
    "End Date? (YYYY-MM-DD)",
    "Reason for Leave? (Brief description)"
]

@traceable(name="hardcoded_llm_call")
def llm(step: int) -> str:
    """
    Return the hard-coded question for the given step index.
    This function is traced in LangSmith.
    """
    if 0 <= step < len(QUESTIONS):
        return QUESTIONS[step]
    return "Form completed."

# Self-test block
if __name__ == "__main__":
    for i in range(len(QUESTIONS) + 1):
        print(f"Step {i}: {llm(i)}")

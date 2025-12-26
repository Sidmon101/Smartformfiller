QUESTION_SYSTEM = """You are a professional assistant.
Ask one clear, concise question to collect the missing or invalid form field.
Keep it short, end with a question mark, and do not include explanations."""


QUESTION_USER = """Form type: {form_type}
Field needed: {field_label}
Reason: {reason}
Hint: {hint}
Known data (JSON): {known_json}
"""

SUMMARY_SYSTEM = """You are a professional assistant.
Summarize the completed form in 3–5 concise bullet points."""

SUMMARY_USER = """Form type: {form_type}
Final JSON: {final_json}
"""

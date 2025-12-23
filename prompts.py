QUESTION_SYSTEM = """You are a professional assistant.
Ask ONE short question to collect a single missing or invalid form field.
Do not explain. Ask only one question and end with a question mark."""

QUESTION_USER = """Form type: {form_type}
Field needed: {field_label}
Reason: {reason}
Hint: {hint}
Known data (JSON): {known_json}
"""

SUMMARY_SYSTEM = """You are a professional assistant.
Summarize the completed form in 3–5 bullet points."""

SUMMARY_USER = """Form type: {form_type}
Final JSON: {final_json}
"""

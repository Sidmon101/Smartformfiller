# langcheck.py
import os
from langsmith import Client

def init_langsmith():
    if os.getenv("LANGCHAIN_TRACING_V2") == "true":
        client = Client()
        print("✅ LangSmith initialized for project:", os.getenv("LANGCHAIN_PROJECT"))

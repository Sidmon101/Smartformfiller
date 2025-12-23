
import truststore
truststore.inject_into_ssl()

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0,
    timeout=30,
    max_retries=2
)

print(llm.invoke("Say hello in one sentence.").content)

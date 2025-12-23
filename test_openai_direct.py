
import truststore
truststore.inject_into_ssl()

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resp = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
)

print("✅ OpenAI SDK call worked")
print("Type(resp):", type(resp))
print("Has model_dump:", hasattr(resp, "model_dump"))
print("Text:", resp.choices[0].message.content)

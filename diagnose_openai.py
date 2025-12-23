
import truststore
truststore.inject_into_ssl()

import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()

print("openai module file:", openai.__file__)
print("OPENAI_BASE_URL:", os.getenv("OPENAI_BASE_URL"))
print("OPENAI_API_BASE:", os.getenv("OPENAI_API_BASE"))

# Force the official base URL explicitly (bypass env overrides)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1",
)

print("client type:", type(client))
print("client base_url:", getattr(client, "base_url", None))

resp = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
)

print("resp type:", type(resp))
print("resp repr first 200 chars:", repr(resp)[:200])

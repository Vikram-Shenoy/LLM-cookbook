# Made my first LLM Call
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = os.getenv("API_KEY")
)

completion = client.chat.completions.create(
  model="anthropic/claude-3.5-haiku",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)
# print(completion.choices)

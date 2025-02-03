from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel,EmailStr

load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = os.getenv("API_KEY")
)

completion = client.chat.completions.create(
    model="anthropic/claude-3.5-haiku",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
)
print(completion.choices[0].message.content)



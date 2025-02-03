from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel,EmailStr
import requests
import json

load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = os.getenv("API_KEY")
)

def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]


# This is from Anthropic Documentation
weather_tool = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

messages = [
    {"role":"system","content":"You are a helpful weather assistant."},
    {"role":"user","content": "What is the weather like in Bengaluru today?"}
]

completion = client.chat.completions.create(
  model="anthropic/claude-3.5-haiku",
  messages= messages,
  tools=weather_tool
)
# completion.model_dump()
print(completion.choices[0].message.tool_calls[0].function.arguments,'\n\n', type(completion.choices[0].message.tool_calls))


def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)

# For each tool call, get the appropriate function and append the response to the message
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)
    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )


# print(result)
# print("\nDumps\n",json.dumps(result))
# print(messages)

completion_2 = client.chat.completions.create(
    model = "anthropic/claude-3.5-haiku",
    messages = messages,
    tools = weather_tool)

print(completion_2.choices[0].message.content)
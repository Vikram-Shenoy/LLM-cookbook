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


messages = [
    {"role":"system","content":"You are a helpful weather assistant."},
    {"role":"user","content": "What is the weather like in Bengaluru today?"}
]
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
completion = client.chat.completions.create(
  model="gpt-4-turbo",
  messages= messages,
  tools=weather_tool
)


print(completion.choices[0].message.content,"\n",completion.choices)

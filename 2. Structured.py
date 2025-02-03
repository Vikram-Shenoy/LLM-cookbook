from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel,EmailStr

load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = os.getenv("API_KEY")
)

class CalendarEvent(BaseModel): # Trying to Structure the outputs
    name: str
    place: str
    participants: list[str]


completion = client.beta.chat.completions.parse(
  model="anthropic/claude-3.5-haiku",
  messages=[
    {
      "role": "user",
      "content": '''Alice and bob are going to a science fair on friday'''
    }
  ], response_format= CalendarEvent,
)

event = completion.choices[0].message.parsed #Failing to structure the outputs because Claude doesn't work the same way as GPT-4o
print(event.name)

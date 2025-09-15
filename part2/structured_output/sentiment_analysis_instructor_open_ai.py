import logging
import os
import json

from dotenv import load_dotenv
from typing import Literal, Optional

# Load environment variables from .env file
load_dotenv()

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)

from pydantic import BaseModel, Field

class SocialMessage(BaseModel):
  """
The reply you write:
  - should be written in a friendly and professional tone
  - should be written in the same language as the statement
  - should be no more than 100 words
  - always include "We are working on improvements and a new release will be out soon!"
"""

  sentiment: Literal['positive', 'negative', 'neutral'] = Field(
    description="Provide the sentiment of the statement")
  reply: Optional[str] = Field(
    default=None, description="The recommend reply to a negative statement")

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI

client = OpenAI(api_key=api_key)

def analyze_sentiment(statement: str):
  response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
      {"role": "system", "content": """
You are an online customer feedback expert.  Analyze the provided statement carefully 
and respond with the sentiment.  If the sentiment is negative, include a suggested reply.
"""},
      {"role": "user", "content": f"Statement: {statement}, JSON:"}
    ],
    text_format=SocialMessage
  )

  print(response.model_dump_json(indent=2))

  return response.output_parsed

response = analyze_sentiment("The App crashes every time I try to view my health improvement report!")

print(f"Sentiment: {response.sentiment}")
print(f"Reply: {response.reply}")

print(json.dumps(SocialMessage.model_json_schema(), indent=2))
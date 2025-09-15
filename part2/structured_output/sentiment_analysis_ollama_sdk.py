import logging

from ollama import chat, ChatResponse

from pydantic import BaseModel
from enum import Enum
from pydantic import BaseModel, Field
import json

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)

class Sentiment(Enum):
  POSITIVE = "positive"
  NEUTRAL = "neutral"
  NEGATIVE = "negative"

class Department(Enum):
  CUSTOMER_SUPPORT = "customer_support"
  ONLINE_ORDERING = "online_ordering"
  PRODUCT_QUALITY = "product_quality"
  SHIPPING_AND_DELIVERY = "shipping_and_delivery"
  OTHER_OFF_TOPIC = "other_off_topic"

class SocialMessage(BaseModel):
  comment: str = Field(description="The comment being analyzed")
  sentiment: Sentiment = Field(description="Provide the sentiment of the comment")
  department: Department = Field(description="Department the comment should be routed to")
  reply: str = Field(description="Recommend a reply to the comment")

def analyze_sentiment(statement: str) -> ChatResponse:
  return chat(
    model="llama3.2",
    messages=[
      {"role": "system", "content": """
You are an online customer feedback expert.  Analyze the provided comment carefully 
and respond with the sentiment, department, and reply.
"""},
      {"role": "user", "content": f"Statement: {statement}, JSON:"}
    ],
    format=SocialMessage.model_json_schema(),
    options={
      "temperature": 0
    }
  )

print(json.dumps(SocialMessage.model_json_schema(), indent=2))

response = analyze_sentiment("Don't trust @Acme Corp.  It's been weeks and I never received my order.")

social_message = SocialMessage.model_validate_json(response.message.content)

print(f"Sentiment: {social_message.sentiment}")
print(f"Department: {social_message.department}")
print(f"Reply: {social_message.reply}")
import logging

from ollama import chat, ChatResponse

from typing import Literal
from pydantic import BaseModel
from enum import Enum
from pydantic import BaseModel, Field
import json

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)

class SocialMessage(BaseModel):
  comment: str = Field(description="The comment being analyzed")
  sentiment: Literal['positive', 'negative', 'neutral'] = Field(description="Provide the sentiment of the statement")
  department: Literal['customer_support', 'online_ordering', 'product_quality', 'shipping_and_delivery', 'other_off_topic'] = Field(description="Department the statement should be routed to")
  reply: str = Field(description="Recommend a reply to the comment")

def analyze_sentiment(statement: str) -> ChatResponse:
  return chat(
    model="llama3.2",
    messages=[
      {"role": "system", "content": """
You are an online customer feedback expert.  Analyze the provided comment carefully 
and respond with the sentiment, department, and reply.
       
Use the following information to determine the department to route to:
  - customer_support: issues with customer support not being helpful
  - online_ordering: issues with ordering, website speed, or checkout process
  - product_quality: issues with product quality or description
  - shipping_and_delivery: issues with slow shipping or not receiving an order
  - other_off_topic: a department could not be identified

The reply your write:
  - should be written in a friendly and professional tone
  - should be written in the same language as the statement
  - should be no more than 100 words
  - should include the number to customer service:  555-555-1245
"""},
      {"role": "user", "content": f"Statement: {statement}, JSON:"}
    ],
    format=SocialMessage.model_json_schema(),
    options={
      "temperature": 0
    }
  )

print(json.dumps(SocialMessage.model_json_schema(), indent=2))

response = analyze_sentiment("Don't trust @Acme Corp.  It's been weeks and my order was never even shipped!")

social_message = SocialMessage.model_validate_json(response.message.content)

print(f"Sentiment: {social_message.sentiment}")
print(f"Department: {social_message.department}")
print(f"Reply: {social_message.reply}")
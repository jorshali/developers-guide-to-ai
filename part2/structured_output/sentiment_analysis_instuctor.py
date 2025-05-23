import logging
import instructor

from typing import Optional
from openai import OpenAI

from pydantic import BaseModel
from enum import Enum
from pydantic import BaseModel, Field

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
  """Use the following information to determine the department to route to:
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
"""

  statement: str = Field(description="The statement being analyzed")
  sentiment: Sentiment = Field(description="Provide the sentiment of the statement")
  department: Department = Field(description="Department the statement should be routed to")
  reply: str = Field(description="Recommend a reply to the statement")

client = instructor.from_openai(
  OpenAI(
    base_url="http://localhost:11434/v1"
  ),
  mode=instructor.Mode.TOOLS,
)

def analyze_sentiment(statement: str) -> SocialMessage:
  return client.chat.completions.create(
    model="llama3.2",
    messages=[
      {"role": "system", "content": """
You are an online customer feedback expert.  Analyze the provided statement carefully 
and respond with the sentiment, department, and reply.
"""},
      {"role": "user", "content": f"Statement: {{statement}}, JSON:"}
    ],
    response_model=SocialMessage,
    context={"statement": statement},
    temperature=0
  )

social_message = analyze_sentiment("Don't trust @Acme Corp.  It's been weeks and I never received my order.")

print(f"Sentiment: {social_message.sentiment}")
print(f"Department: {social_message.department}")
print(f"Reply: {social_message.reply}")
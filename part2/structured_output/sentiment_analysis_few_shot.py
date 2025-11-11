import logging
import instructor

from typing import Literal
from openai import OpenAI

from pydantic import BaseModel, Field, ConfigDict

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)

examples = [
  {
    "statement": "Thank you @Acme Corp!  This new shampoo has been great!",
    "sentiment": "positive",
    "department": "product_quality",
    "reply": "We are so glad to hear that you are enjoying your new shampoo. Thank you for your order!"
  },
  {
    "statement": "My order from @Acme Corp never arrived and customer service wasn't helpful.",
    "sentiment": "negative",
    "department": "customer_support",
    "reply": "We apologize for the delay in shipping your order from Acme Corp. Our team is investigating this issue, and we will provide an update as soon as possible. If you have any further concerns, please call our customer service at 555-555-1245."
  },
  {
    "statement": "I wouldn't trust @Acme Corp.",
    "sentiment": "negative",
    "department": "other_off_topic",
    "reply": "We apologize for any concerns you may have about Acme Corp. We strive to provide accurate and reliable information, but sometimes mistakes can happen. Please feel free to contact our customer service team at 555-555-1245."
  },
  {
    "statement": "I'm an @Acme Corp repeat customer. They ship fast and prices are great.",
    "sentiment": "positive",
    "department": "shipping_and_delivery",
    "reply": "shipping_and_delivery",
    "reply": "Thank you for your kind words about Acme Corp!"
  },
  {
    "statement": "The @Acme Corp website is so slow.  Every time I've tried to order I can't even get through checkout.",
    "sentiment": "negative",
    "department": "online_ordering",
    "reply": "We apologize for the inconvenience you are experiencing with our website speed and checkout process. Our team is working hard to improve these issues. In the meantime, please call our customer service at 555-555-1245 for assistance."
  }
]


class SocialMessage(BaseModel):
  """
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
"""
  statement: str = Field(description="The statement being analyzed")
  sentiment: Literal['positive', 'negative', 'neutral'] = Field(
    description="Provide the sentiment of the statement")
  department: Literal['customer_support', 'online_ordering', 'product_quality', 'shipping_and_delivery',
                      'other_off_topic'] = Field(description="Department the statement should be routed to")
  reply: str = Field(description="Recommend a reply to the statement")

  model_config = ConfigDict(
    json_schema_extra={
      "examples": examples
    }
  )


client = instructor.from_openai(
  OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="None"
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
      {"role": "user", "content": "Statement: {{statement}}, JSON:"}
    ],
    response_model=SocialMessage,
    context={"statement": statement},
    temperature=0
  )


social_message = analyze_sentiment(
  "Don't trust @Acme Corp.  It's been weeks and my order was never even shipped!")

print(f"Sentiment: {social_message.sentiment}")
print(f"Department: {social_message.department}")
print(f"Reply: {social_message.reply}")

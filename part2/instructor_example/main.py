import logging
import instructor

from typing import Optional
from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from enum import Enum
from pydantic import BaseModel, Field

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)

class Sentiment(Enum):
  POSITIVE = "positive"
  NEUTRAL = "neutral"
  NEGATIVE = "negative"

class Category(Enum):
  PRODUCT_SERVICE_FEEDBACK = "product_or_service_feedback"
  PRICING_VALUE = "pricing_value"
  CUSTOMER_SERVICE_SUPPORT = "customer_service_support"
  SHIPPING_DELIVERY_LOGISTICS = "shipping_delivery_logistics"
  MARKETING_ADVERTISING = "marketing_advertising"
  COMPETITIVE_COMPARISONS = "competitive_comparisons"
  OTHER_OFF_TOPIC = "other_off_topic"

class SocialMessage(BaseModel):
  comment: str = Field(
    description="The original comment being analyzed")
  sentiment: Optional[Sentiment] = Field(default=None,
    description="The sentiment of the comment")
  category: Optional[Category] = Field(default=None,
    description="The category of the comment")

def analyze_sentiment(statement: str) -> SocialMessage:
  client = instructor.from_openai(
    OpenAI(),
    mode=instructor.Mode.JSON,
  )

  return client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": """You are an expert at sentiment analysis. You will identify if a given comment is positive, neutral, or negative.  You will also analyze the comment for keywords to determine the category it belongs to."""},
      {"role": "user", "content": f"Statement: {statement}, JSON:"}
    ],
    response_model=SocialMessage,
  )

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=[ "http://localhost:5173" ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post("/")
def read_root(social_message: SocialMessage):
  return analyze_sentiment(social_message.comment)
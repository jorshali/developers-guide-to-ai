from pydantic import BaseModel
from typing import Literal, List


class ChatRequestMessage(BaseModel):
  role: Literal["user", "assistant"]
  content: str


class ChatRequest(BaseModel):
  question: str
  history: List[ChatRequestMessage] = []

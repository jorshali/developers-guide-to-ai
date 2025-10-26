from typing import TypedDict, Literal, List
from pydantic import BaseModel


class Message(TypedDict):
  role: Literal["system", "user", "assistant", "tool"]
  content: str


Messages = List[Message]

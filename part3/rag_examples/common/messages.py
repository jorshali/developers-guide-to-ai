from typing import List, Literal, TypedDict


class Message(TypedDict):
  role: Literal["system", "user", "assistant", "tool"]
  content: str


Messages = List[Message]

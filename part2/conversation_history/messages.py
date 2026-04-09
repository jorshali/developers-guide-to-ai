from typing import TypedDict, Literal, List


class Message(TypedDict):
  role: Literal["system", "user", "assistant", "tool"]
  content: str


Messages = List[Message]

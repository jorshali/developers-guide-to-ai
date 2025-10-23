from typing import List, Mapping, Any
from ollama import chat
from pydantic import BaseModel, Field


class HistoryResponse(BaseModel):
  can_answer_question: bool = Field(
    ..., description="Whether the question can be answered based on the messages")


class ConversationHistory:
  def __init__(self, system_message: Mapping[str, Any]):
    self.system_message = system_message
    self.message_history: List[Mapping[str, Any]] = []

  def add_message(self, message: Mapping[str, Any]):
    self.message_history.append(message)

  def get_messages(self):
    messages = [self.system_message]
    messages.extend(self.message_history)

    return messages

  def has_history(self):
    return len(self.message_history) > 0

  def can_answer_question(self, question: str):
    if not self.has_history():
      return False

    messages = list(self.message_history)

    messages.append({
      "role": "user",
      "content": "Can you answer the user question based on the chat history?  Respond with true only if you have the context needed to answer the question. Question:" + question
    })

    response = chat(
      model="llama3.2",
      messages=messages,
      stream=False,
      format=HistoryResponse.model_json_schema(),
      options={
        "temperature": 0
      }
    )

    history_response = HistoryResponse.model_validate_json(
      response.message.content)

    return history_response.can_answer_question

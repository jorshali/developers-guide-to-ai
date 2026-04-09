import tiktoken

from typing import Mapping, Any
from ollama import chat
from pydantic import BaseModel, Field

from common.messages import Messages, Message


class HistoryResponse(BaseModel):
  can_answer_question: bool = Field(
    ..., description="Whether the question can be answered based on the messages")


class ConversationHistory:
  def __init__(self, system_message: Message, model_name='gpt2', max_tokens=8000):
    self.system_message = system_message
    self.message_history: Messages = []
    self.model_name = model_name
    self.max_tokens = max_tokens

  def add_message(self, message: Mapping[str, Any]):
    self.message_history.append(message)

  def get_messages(self):
    messages = [self.system_message]
    messages.extend(self.message_history)

    return messages

  def has_history(self):
    return len(self.message_history) > 0

  def message_history_as_string(self):
    message_history_as_string = ''

    for message in self.message_history:
      message_history_as_string += f"{message['role']}: {message['content']}\n"

    return message_history_as_string

  def count_tokens(self):
    encoding = tiktoken.encoding_for_model(self.model_name)

    token_count = 0

    for message in self.get_messages():
      tokens = encoding.encode(message['content'])
      token_count += len(tokens)

    return token_count

  def trim_history(self):
    while self.count_tokens() > self.max_tokens and len(self.message_history) > 2:
      self.message_history = self.message_history[2:]

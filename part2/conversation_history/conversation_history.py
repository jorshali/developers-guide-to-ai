import tiktoken
import json

from typing import TypedDict, Literal, List
from ollama import chat


class Message(TypedDict):
  role: Literal["system", "user", "assistant", "tool"]
  content: str


Messages = List[Message]


class ConversationHistory:
  def __init__(self, system_message: Message, model_name='gpt2', max_tokens=600):
    self.system_message = system_message
    self.message_history: Messages = []
    self.model_name = model_name
    self.max_tokens = max_tokens

  def add_messages(self, messages: List[Message]):
    self.message_history.extend(messages)

  def add_message(self, message: Message):
    self.message_history.append(message)

  def get_messages(self):
    messages = [self.system_message]
    messages.extend(self.message_history)

    return messages

  def has_history(self):
    return len(self.message_history) > 0

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

  def message_history_as_string(self):
    message_history_as_string = ''

    for message in self.message_history:
      message_history_as_string += f"{message['role']}: {message['content']}\n"

    return message_history_as_string

  def summarize_history(self, max_summary_tokens=120):
    summary_prompt = [
      {"role": "system", "content": "You are an assistant that summarizes conversations."},
      {"role": "user", "content": (
        "Summarize the following conversation in a concise way that preserves key facts and context:\n\n" +
        self.message_history_as_string() + "\n\n" +
        f"Limit your summary to{max_summary_tokens} words or less."
      )}
    ]

    response = chat(
      model="llama3.2",
      messages=summary_prompt,
      stream=False,
      options={
        'num_predict': max_summary_tokens,
        'temperature': 0
      }
    )

    self.message_history = [{
      'role': 'user',
      'content': response.message.content
    }]

import tiktoken

from messages import Messages, Message


class ConversationHistory:
  def __init__(self, system_message: Message, encoding_name='cl100k_base', max_tokens=600):
    self.system_message = system_message
    self.message_history: Messages = []
    self.encoding_name = encoding_name
    self.max_tokens = max_tokens

  def add_messages(self, messages: Messages):
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
    encoding = tiktoken.get_encoding(self.encoding_name)

    token_count = 0

    for message in self.get_messages():
      tokens = encoding.encode(message['content'])
      token_count += len(tokens)

    return token_count

  def trim_history(self):
    while self.count_tokens() > self.max_tokens and len(self.message_history) >= 2:
      self.message_history = self.message_history[2:]

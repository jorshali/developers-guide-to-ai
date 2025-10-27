import json

from conversation_history import ConversationHistory
from conversation_history_example_data import conversation_history_example_data

history = ConversationHistory(
  system_message={
    "role": "system",
    "content": """
You are a helpful Help Desk Representative. Use the following
support article to answer questions.  Only use the provided
<articles> and if an answer can"t be found, respond with:
I"m sorry I can"t help with that.  Please email customer support at
support@acme.com."""
  },
  encoding_name="cl100k_base",
  max_tokens=600
)

history.add_messages(conversation_history_example_data)

history.trim_history()

print(json.dumps(history.get_messages(), indent=2))

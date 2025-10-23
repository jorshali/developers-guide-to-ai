import json

from ollama import chat

from conversation_history import ConversationHistory
from conversation_history_example_data import conversation_history

history = ConversationHistory(
  {'role': 'system', 'content': """You are a helpful Help Desk Representative. Use the following 
support article to answer questions.  Only use the provided 
<articles> and if an answer can't be found, respond with:  
I'm sorry I can't help with that.  Please email customer support at
support@acme.com."""})

history.add_messages(conversation_history)

print()
print("History before summarization:")
print("---------------------------------")
print(json.dumps(history.get_messages(), indent=2))
print(history.count_tokens())

history.summarize_history()

print()
print("History after summarization:")
print("---------------------------------")
print(json.dumps(history.get_messages(), indent=2))

history.add_message({
  'role': 'user',
  'content': 'What should I do now?'
})

response = chat(
  model="llama3.2",
  messages=history.get_messages(),
  stream=False,
  options={
    'temperature': 0
  }
)

print()
print("Question response:")
print("----------------------")
print(response.message.content)

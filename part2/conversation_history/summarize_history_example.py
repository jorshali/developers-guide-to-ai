import json

from ollama import chat
from jinja2 import Environment, FileSystemLoader

from conversation_history import ConversationHistory
from conversation_history_example_data import conversation_history_example_data
from summarize_history import summarize_history

env = Environment(
  loader=FileSystemLoader("templates")
)

system_template = env.get_template('summarize_history_system_prompt.txt')
user_template = env.get_template('summarize_history_system_prompt.txt')

history = ConversationHistory(
  {'role': 'system', 'content': """You are a helpful AI Support Representative.
Use the following support <article> or any provided conversation history to answer questions.
Only use the provided <article> or conversation history and if an answer can't be found, respond with:  

"I'm sorry I can't help with that.  Please email customer support at support@acme.com."   
"""})

history.add_messages(conversation_history_example_data)

print()
print("History before summarization:")
print("----------------------------------------------------")
print(json.dumps(history.get_messages(), indent=2))
print(history.count_tokens())

summarize_history(history, max_words=300)

print()
print("History after summarization:")
print("----------------------------------------------------")
print(json.dumps(history.get_messages(), indent=2))

history.add_message({
  'role': 'user',
  'content': 'What folder should I check for the reset email?'
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
print("Follow-up question response after summarization:")
print("----------------------------------------------------")
print(response.message.content)

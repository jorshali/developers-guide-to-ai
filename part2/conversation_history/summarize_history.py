import json

from ollama import chat
from jinja2 import Environment, FileSystemLoader

from conversation_history import ConversationHistory
from conversation_history_example_data import conversation_history

env = Environment(
  loader=FileSystemLoader("templates")
)

system_template = env.get_template('summarize_history_system_prompt.txt')
user_template = env.get_template('summarize_history_system_prompt.txt')


def summarize_history(conversation_history: ConversationHistory, max_tokens=120):
  system_message = system_template.render(
    max_summary_tokens=max_tokens)

  user_message = user_template.render(
    message_history_as_string=conversation_history.message_history_as_string()
  )

  response = chat(
    model="llama3.2",
    messages=[
      {
        "role": "system",
        "content": system_message
      },
      {
        "role": "user",
        "content": user_message
      }
    ],
    stream=False,
    options={
      'num_predict': max_tokens,
      'temperature': 0
    }
  )

  conversation_history.message_history = [{
    'role': 'user',
    'content': response.message.content
  }]


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

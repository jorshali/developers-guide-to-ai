from ollama import chat
from jinja2 import Environment, FileSystemLoader

from conversation_history import ConversationHistory

env = Environment(
  loader=FileSystemLoader("templates")
)

system_template = env.get_template('summarize_history_system_message.txt')
user_template = env.get_template('summarize_history_user_message.txt')


def summarize_history(history: ConversationHistory, max_words=300):
  system_message = system_template.render(max_summary_tokens=max_words)
  user_message = user_template.render(messages=history.get_messages())

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
      'num_predict': max_words * 1.33,
      'temperature': 0
    }
  )

  history.message_history = [{
    'role': 'user',
    'content': response.message.content
  }]

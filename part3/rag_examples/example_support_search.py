
from ollama import chat
from jinja2 import Environment, FileSystemLoader

from common.document_vector_store import DocumentVectorStore
from common.document_retrieval import load_local_document

env = Environment(
  loader=FileSystemLoader(searchpath="templates")
)

system_prompt = env.get_template("basic_support_system_prompt.txt")
user_prompt = env.get_template("basic_support_user_prompt.txt")

readme_vector_store = DocumentVectorStore(
  load_local_document('../../README.md'))

question = "Why is Ollama preferred to hosted APIs for the examples?"

documents = readme_vector_store.query(question)

messages = [
  {
    "role": "system",
    "content": system_prompt.render()
  },
  {
    "role": "user",
    "content": user_prompt.render(context='\n'.join(documents), question=question)
  }
]

response = chat(
  model="llama3.2",
  messages=messages,
  stream=True,
  options={
    "temperature": 0
  }
)

for chunk in response:
  if chunk.message.content:
    print(chunk.message.content, end="", flush=True)

print("\nProcessing...\n\n")

for chunk in response:
  print(chunk, end="", flush=True)

from pathlib import Path
from ollama import chat
from jinja2 import Environment, FileSystemLoader

from common.document_vector_store import DocumentVectorStore

env = Environment(
  loader=FileSystemLoader(searchpath="templates")
)

system_prompt = env.get_template("basic_support_system_prompt.txt")
user_prompt = env.get_template("basic_support_user_prompt.txt")

print("\nLoading the README file, please wait just a moment...\n")

document_text = Path('../../README.md').read_text()

readme_vector_store: DocumentVectorStore = DocumentVectorStore(
  document_text)

question = input("""Welcome to the Developer's Guide to AI Examples!
----------------------------------------------------------

What would you like to know?  Ask me about setup, running, or troubleshooting.

(Note:  I won't remember our conversation history, so please be specific.)

\\bye to exit.

>>> """)

while question != "\\bye":
  if question:
    documents = readme_vector_store.query(question)

    messages = [
      {
        "role": "system",
        "content": system_prompt.render()
      },
        {
        "role": "user",
        "content": user_prompt.render(documents=documents, question=question)
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

    print()

    for chunk in response:
      if chunk.message.content:
        print(chunk.message.content, end="", flush=True)

    question = input(
        "\n\nWhat else would you like to know?\n\nUse \\bye to exit\n\nQuestion: ")

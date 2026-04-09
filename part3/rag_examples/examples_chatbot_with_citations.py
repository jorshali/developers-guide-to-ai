from common.multi_document_vector_store import MultiDocumentVectorStore
from ollama import chat
from jinja2 import Environment, FileSystemLoader
from common.document_retrieval import download_remote_document

env = Environment(
  loader=FileSystemLoader(searchpath="templates")
)

system_message = env.get_template(
  "support_with_citations_system_message.txt")
user_message = env.get_template("support_with_citations_user_message.txt")

print("\nLoading the README file, please wait just a moment...\n")

readme_filenames = [
  'README.md',
  'part1/getting_started_python/README.md',
]

readme_documents = []

for readme_filename in readme_filenames:
  readme_documents.append(
    download_remote_document(filename=readme_filename))

readme_vector_store = MultiDocumentVectorStore(readme_documents)

question = input("""Welcome to the Developer's Guide to AI Examples!
----------------------------------------------------------

What would you like to know?  Ask me about setup, running, or troubleshooting.  I'll tell you what I know and link you to the right documentation.

(Note:  I won't remember our conversation history, so please be specific.)

\\bye to exit.

>>> """)

while question != "\\bye":
  if question:
    documents = readme_vector_store.query(question)

    messages = [
      {
        "role": "system",
        "content": system_message.render()
      },
        {
        "role": "user",
        "content": user_message.render(documents=documents, question=question)
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

    question = input(
        "\n\nWhat else would you like to know?\n\nUse \\bye to exit\n\nQuestion: ")

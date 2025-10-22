from langchain_chroma.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from ollama import chat

print("\nLoading the README file, please wait just a moment...\n")

documentation_as_documents = TextLoader('../../README.md').load()

print("Number of documents: ", len(documentation_as_documents))
print(documentation_as_documents[0].model_dump_json(indent=2))

splitter = RecursiveCharacterTextSplitter.from_language(
  language="markdown", chunk_size=1200)

# Initialize the document loader
document_chunks = splitter.split_text(
  documentation_as_documents[0].page_content)

print("Number of chunks: ", len(document_chunks))

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(
  model="mxbai-embed-large",
  base_url="http://localhost:11434",
)

vector_db = Chroma.from_texts(
  texts=document_chunks,
  embedding=embeddings,
  collection_name="documentation_collection"
)

question = input("""Welcome to the Developer's Guide to AI Examples!
----------------------------------------------------------
                 
What would you like to know?  Ask me about setup, running, or troubleshooting.
                 
(Note:  I won't remember our conversation history, so please be specific.)

\\bye to exit.

>>> """)

while question != "\\bye":
  if question:
    results = vector_db.similarity_search_with_score(question, k=3)

    text_snippets = [result[0].page_content for result in results]

    messages = [
      {
        "role": "system",
        "content": "You are a helpful assistant and will answer questions about the Developer's Guide to AI.  Only use the provided context to answer.  If you don't know the answer, only respond with 'Sorry, I am unable to help with that, but I can answer questions about the documentation.'."
      },
      {
        "role": "user",
        "content": f"<context>{'\n'.join(text_snippets)}</context>\n\nQuestion: {question}"
      }
    ]

    response = chat(
      model="llama3.2",
      messages=messages,
      stream=True
    )

    for chunk in response:
      if chunk.message.content:
        print(chunk.message.content, end="", flush=True)

  else:
    print("Sorry, you need to ask a question.")

  question = input(
    "\n\nWhat else would you like to know?\n\nUse \\bye to exit\n\nQuestion: ")

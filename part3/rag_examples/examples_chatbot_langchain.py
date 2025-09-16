from langchain_chroma.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

print("\nLoading the README file, please wait just a moment...\n")

documentation_as_documents = TextLoader('../../README.md').load()

print("Number of documents: ", len(documentation_as_documents))
print(documentation_as_documents[0].model_dump_json(indent=2))

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# Initialize the document loader
document_chunks = splitter.split_text(documentation_as_documents[0].page_content)

print("Number of chunks: ", len(document_chunks))

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
    base_url="http://localhost:11434",
)

vector_db = Chroma.from_documents(
    documents=document_chunks,
    embedding=embeddings,
    collection_name="documentation_collection"
)

llm = OllamaLLM(
  model="llama3.2",
  base_url="http://localhost:11434"
)

question = input("""Welcome to the Developer's Guide to AI Examples!
----------------------------------------------------------
                 
What would you like to know?  Ask me about setup, running, or troubleshooting.
                 
(Note:  I won't remember our conversation history, so please be specific.)

\\bye to exit.

>>> """)

while question != "\\bye":
  if question:
    results = vector_db.similarity_search_with_score(question, k=1)

    messages = [
      ("system", "You are a helpful assistant and will answer questions about the Developer's Guide to AI.  Only use the provided context to answer.  If you don't know the answer, say so."),
      ("human", "<context>{context}</context>\n\nQuestion: {question}")
    ]

    prompt = ChatPromptTemplate.from_messages(messages)
    parser = StrOutputParser()
    
    chain = prompt | llm | StrOutputParser()

    response =chain.stream({
      "context": results[0][0].page_content,
      "question": question
    })

    print("\nProcessing...\n\n")
  
    for chunk in response:
      print(chunk, end="", flush=True)

  else:
    print("Sorry, you need to ask a question.")

  question = input("\n\nWhat else would you like to know?\n\nUse \\bye to exit\n\nQuestion: ")




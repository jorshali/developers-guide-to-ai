from langchain_chroma.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableMap
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

question = "Do the examples use Ollama?"
results = vector_db.similarity_search_with_score(question, k=1)

messages = [
  ("system", "You are a helpful assistant and will answer questions about the Developer's Guide to AI.  Only use the provided documentation to answer.  If you don't know the answer, say so."),
  ("human", "<documentation>{documentation}</documentation>\n\nQuestion: {question}")
]

prompt = ChatPromptTemplate.from_messages(messages)

def retrieve_documentation(x):
  return vector_db.similarity_search_with_score(question, k=1)

context = RunnableMap({
  "documentation": RunnableLambda(func=retrieve_documentation),
  "question": RunnablePassthrough()
})

parser = StrOutputParser()

chain = context | prompt | llm | parser

response = chain.stream(question)

print("\nProcessing...\n\n")

for chunk in response:
  print(chunk, end="", flush=True)
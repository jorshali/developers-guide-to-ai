from contextlib import asynccontextmanager
from typing import Literal, List
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableMap
from langchain_core.messages.utils import trim_messages

from pydantic import BaseModel


class Message(BaseModel):
  role: Literal["human", "ai"]
  content: str


class ChatRequest(BaseModel):
  question: str
  history: List[Message] = []


class ChatContext():
  def __init__(self):
    self.model: OllamaLLM = None
    self.retriever: ParentDocumentRetriever = None


def load_vector_store():
  print("\nLoading the README file, please wait just a moment...\n")

  documentation_as_documents = TextLoader('../../README.md').load()

  print("Number of documents: ", len(documentation_as_documents))
  print(documentation_as_documents[0].model_dump_json(indent=2))

  headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
  ]

  splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on)

  # Initialize the document loader
  document_chunks = splitter.split_text(
    documentation_as_documents[0].page_content)

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

  return vector_db


chat_context = ChatContext()


@asynccontextmanager
async def lifespan(app: FastAPI):
  # initialize models and vector stores
  chat_context.retriever = load_vector_store()
  chat_context.model = OllamaLLM(model='llama3.2')

  yield

  # Clean up and release the resources

app = FastAPI(lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.post("/")
def chat(chat_request: ChatRequest):
  print("\nReceived question: " + chat_request.question)

  message_history = []

  for msg in chat_request.history:
    message_history.append((msg.role, msg.content))

  messages = [
    ("system", "You are a helpful assistant and will answer questions about the Developer's Guide to AI.  Only use the provided documentation to answer.  If you don't know the answer, say so."),
    MessagesPlaceholder(variable_name="history"),
    ("human",
     "<documentation>{documentation}</documentation>\n\nQuestion: {question}")
  ]

  prompt = ChatPromptTemplate.from_messages(messages)
  parser = StrOutputParser()

  llm = chat_context.model

  def retrieve_documentation(question):
    return chat_context.retriever.similarity_search_with_score(question, k=1)

  context = RunnableMap({
    "documentation": RunnableLambda(func=retrieve_documentation),
    "question": RunnablePassthrough(),
    "history": lambda _: message_history
  })

  parser = StrOutputParser()

  trim_history = trim_messages(
      token_counter=chat_context.model,
      max_tokens=4000,
      strategy="last",
      include_system=True,
      end_on="human",
      allow_partial=False
  )

  chain = context | prompt | trim_history | llm | parser

  stream = chain.stream(chat_request.question)

  return StreamingResponse(stream, media_type="text/plain")

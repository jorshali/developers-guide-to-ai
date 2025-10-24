from contextlib import asynccontextmanager
from typing import Literal, List
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from ollama import chat
from jinja2 import Environment, FileSystemLoader

from pydantic import BaseModel

from common.conversation_history import ConversationHistory
from common.document_retrieval import download_remote_document
from common.multi_document_vector_store import MultiDocumentVectorStore

env = Environment(
  loader=FileSystemLoader(searchpath="templates")
)

system_prompt = env.get_template(
  "support_with_history_system_prompt.txt")
user_prompt = env.get_template("support_with_citations_user_prompt.txt")

print("\nLoading the README file, please wait just a moment...\n")


class Message(BaseModel):
  role: Literal["user", "assistant"]
  content: str


class ChatRequest(BaseModel):
  question: str
  history: List[Message] = []


class ChatContext():
  def __init__(self):
    self.vector_store: MultiDocumentVectorStore = None


def load_vector_store():
  print("\nLoading the README file, please wait just a moment...\n")

  readme_filenames = [
    'README.md',
    'part1/getting_started_python/README.md',
  ]

  readme_documents = []

  for readme_filename in readme_filenames:
    readme_documents.append(
      download_remote_document(filename=readme_filename))

  return MultiDocumentVectorStore(readme_documents)


chat_context = ChatContext()


@asynccontextmanager
async def lifespan(app: FastAPI):
  # initialize models and vector stores
  chat_context.vector_store = load_vector_store()

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


def generate_stream(conversation_history: ConversationHistory):
  result = chat(
    stream=True,
    model="llama3.2",
    messages=conversation_history.get_messages(),
    options={'temperature': 0}
  )

  for chunk in result:
    if chunk.message and chunk.message.content:
      yield chunk.message.content


@app.post("/")
def handle_post(chat_request: ChatRequest):
  print("\nReceived question: " + chat_request.question)

  question = chat_request.question

  system_message = {
    "role": "system",
    "content": system_prompt.render()
  }

  conversation_history = ConversationHistory(system_message)

  for msg in chat_request.history:
    conversation_history.add_message({
      'role': 'user',
      'content': msg.content
    })

  conversation_history.trim_history()

  documents = chat_context.vector_store.query(question)

  conversation_history.add_message({
    "role": "user",
    "content": user_prompt.render(documents=documents, question=question)
  })

  return StreamingResponse(
    generate_stream(conversation_history), media_type="text/plain")

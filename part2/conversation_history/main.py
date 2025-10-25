from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import chat

from messages import ChatRequest
from conversation_history import ConversationHistory

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


def generate_stream(chatRequest: ChatRequest):
  conversation_history = ConversationHistory(system_message={
    "role": "system",
    "content": "You are helpful assistant."
  })

  conversation_history.add_messages(chatRequest.history)
  conversation_history.add_message({
    "role": "user",
    "content": chatRequest.question
  })

  result = chat(
    model="llama3.2",
    messages=conversation_history.get_messages(),
    stream=True,
  )

  for chunk in result:
    if chunk.message and chunk.message.content:
      print('\nReturned GenerateResponse object for chunk:\n')
      print(chunk.model_dump_json(indent=2))

      yield chunk.message.content


@app.post("/")
def chat_request(chatRequest: ChatRequest):
  return StreamingResponse(
    generate_stream(chatRequest), media_type="text/plain"
  )

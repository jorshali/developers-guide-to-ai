from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://localhost:5173" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatModel = OllamaLLM(model='llama3.2')

@app.post("/")
def read_root(chatRequest: ChatRequest):
    stream = chatModel.stream(chatRequest.question)

    return StreamingResponse(stream, media_type="text/plain")
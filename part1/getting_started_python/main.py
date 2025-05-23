from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import Client

from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://localhost:5173" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client()

class ChatRequest(BaseModel):
    question: str

@app.post("/")
def chat(chatRequest: ChatRequest):
    def generate_stream():
        result = client.generate(
            stream=True,
            model="llama3.2",
            prompt=chatRequest.question,
            options={
                "temperature": 0.2,
                "top_p": 0.9
            }
        )

        for chunk in result:
            if chunk.get('response'):
                yield chunk['response']

    return StreamingResponse(generate_stream(), media_type="text/plain")
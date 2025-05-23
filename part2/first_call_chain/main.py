from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LangChain Ollama
llm = OllamaLLM(model="llama3.2")

# Create the prompt template

class ChatRequest(BaseModel):
    question: str

@app.post("/")
def chat(chatRequest: ChatRequest):
    prompt_template = PromptTemplate.from_template(
        "You are a helpful assistant, answer the user's question: {question}"
    )
    
    chain = prompt_template | llm
        
    return StreamingResponse(
        content=chain.stream({"question": chatRequest.question}), 
        media_type="text/plain"
    )
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import OpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_core.stores import InMemoryStore
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableMap
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel
from typing import List, Literal

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
    print("\nCreating embeddings and loading Vectore Store, please be patient...")
    
    loader = DirectoryLoader(
        path="articles",
        glob="*.md",
        loader_cls=TextLoader
    )

    documentsForVectorStore = loader.load()

    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large",
        base_url="http://localhost:11434",
    )

    vectorstore = InMemoryVectorStore(embeddings)
    byte_store = InMemoryStore()

    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        byte_store=byte_store,
        child_splitter=RecursiveCharacterTextSplitter(
            chunk_overlap=0,
            chunk_size=500,
        )
    )

    retriever.add_documents(documentsForVectorStore)

    return retriever

chat_context = ChatContext()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize models and vector stores
    chat_context.retriever = load_vector_store()
    # chat_context.model = OllamaLLM(model='llama3.2')
    chat_context.model = OpenAI(model="gpt-4o-mini")
    
    yield

    # Clean up and release the resources
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://localhost:5173" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def retrieve_related_articles(input):
    related_article_documents = chat_context.retriever.invoke(input)

    print("\nRelated article retrieved:\n")
    print("\n" + related_article_documents[0].page_content)
    print("\nCalling the LLM with context...")

    return related_article_documents[0].page_content


@app.post("/")
def read_root(chat_request: ChatRequest):
    print("\nReceived question: " + chat_request.question)

    model = chat_context.model

    message_history = []

    for msg in chat_request.history:
        message_history.append((msg.role, msg.content))

    messages = [
        ("system", """
You are a helpful AI Support Representative. Use the following support 
article to answer questions.  Only use the provided <article> and if an 
answer can't be found, respond with:  I'm sorry I can't help with that.  
Please email support at support@acme.com."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "<article>{context}</article>\n\nQuestion: {question}")
    ]

    prompt = ChatPromptTemplate.from_messages(messages)
    
    prompt_context = RunnableMap({
        "context": RunnableLambda(func=retrieve_related_articles),
        "question": RunnablePassthrough(),
        "history": lambda _: message_history
    })

    parser = StrOutputParser()

    chain = prompt_context | prompt | model | parser

    stream = chain.stream(chat_request.question)

    return StreamingResponse(stream, media_type="text/plain")
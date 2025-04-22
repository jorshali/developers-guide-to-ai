from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_core.stores import InMemoryStore
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatContext():
    def __init__(self):
        self.model: OllamaLLM = None
        self.retriever: ParentDocumentRetriever = None

def load_vector_store():
    print("\nCreating embeddings and loading Vectore Store, please be patient...")
    
    loader = DirectoryLoader(
        path="../articles",
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
            chunk_size=400,
        )
    )

    retriever.add_documents(documentsForVectorStore)

    return retriever

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

    return related_article_documents


@app.post("/")
def read_root(chat_request: ChatRequest):
    print("\nReceived question: " + chat_request.question)

    model = chat_context.model

    system_prompt = SystemMessagePromptTemplate.from_template("Answer the question with company information based on only the following context:\n\n{context}")
    human_prompt = HumanMessagePromptTemplate.from_template("{question}")

    prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    
    parser = StrOutputParser()

    prompt_context = {
        "context": RunnableLambda(func=retrieve_related_articles),
        "question": RunnablePassthrough()
    }

    chain = prompt_context | prompt | model | parser

    stream = chain.stream(chat_request.question)

    return StreamingResponse(stream, media_type="text/plain")
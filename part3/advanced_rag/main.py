from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.stores import InMemoryStore
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain_text_splitters import MarkdownTextSplitter
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain.retrievers.document_compressors.embeddings_filter import EmbeddingsFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline

from pydantic import BaseModel
from typing import List, Literal
import os

class Message(BaseModel):
    role: Literal["human", "ai"]
    content: str

class ChatRequest(BaseModel):
    question: str
    history: List[Message] = []

class ChatContext():
    def __init__(self):
        self.model: OllamaLLM = None
        self.retriever = None

def load_vector_store():
    print("\nCreating embeddings and loading Vector Store, please be patient...")
    
    loader = DirectoryLoader(
        path="../../articles",
        glob="*.md",
        loader_cls=TextLoader
    )

    documents = loader.load()
    
    # Create markdown splitter for chunking
    markdown_splitter = MarkdownTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n## ",  # Split on headers
            "\n### ",  # Split on subheaders
            "\n#### ",  # Split on sub-subheaders
            "\n\n",    # Split on paragraphs
            "\n",      # Split on newlines
            ". ",      # Split on sentences
            "! ",      # Split on exclamations
            "? ",      # Split on questions
            " ",       # Split on words
            ""         # Split on characters
        ]
    )
    
    # Split documents into chunks
    splits = markdown_splitter.split_documents(documents)
    
    # Initialize embeddings
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large",
        base_url="http://localhost:11434",
    )

    # Create ChromaDB vector store
    persist_directory = "chroma_db"
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
        
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # Create BM25 retriever for keyword search
    bm25_retriever = BM25Retriever.from_documents(splits)
    bm25_retriever.k = 3
    
    # Create vector store retriever
    vectorstore_retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    
    # Create ensemble retriever combining both approaches
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vectorstore_retriever],
        weights=[0.5, 0.5]
    )
    
    # Create multi-query retriever for query reformulation
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=ensemble_retriever,
        llm=OllamaLLM(model='llama3.2'),
        prompt_template="""You are an AI assistant helping to reformulate search queries.
        Given the following question, generate 3 different ways to ask the same question.
        Each reformulation should focus on different aspects of the original question.
        
        Original question: {question}
        
        Reformulated questions:"""
    )
    
    # Create reranker using embeddings filter
    embeddings_filter = EmbeddingsFilter(
        embeddings=embeddings,
        similarity_threshold=0.7
    )
    
    # Create document compressor pipeline
    compressor_pipeline = DocumentCompressorPipeline(
        transformers=[embeddings_filter]
    )
    
    # Create final retriever with reranking
    final_retriever = ContextualCompressionRetriever(
        base_compressor=compressor_pipeline,
        base_retriever=multi_query_retriever
    )
    
    return final_retriever

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

def retrieve_related_articles(input):
    # First hop retrieval
    initial_docs = chat_context.retriever.invoke(input)
    
    # Combine the retrieved documents
    combined_context = "\n\n".join([doc.page_content for doc in initial_docs])
    
    # Create a follow-up query for multi-hop retrieval
    follow_up_prompt = f"""Based on the following context and the original question, 
    what additional information would be helpful to find? 
    
    Original question: {input}
    Retrieved context: {combined_context}
    
    Additional information needed:"""
    
    # Generate follow-up query
    follow_up_query = chat_context.model.invoke(follow_up_prompt)
    
    # Second hop retrieval using the follow-up query
    follow_up_docs = chat_context.retriever.invoke(follow_up_query)
    
    # Combine all retrieved documents
    all_docs = initial_docs + follow_up_docs
    
    # Remove duplicates while preserving order
    seen = set()
    unique_docs = []
    for doc in all_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_docs.append(doc)
    
    # Combine all unique documents
    final_context = "\n\n".join([doc.page_content for doc in unique_docs])
    
    print("\nRetrieved context from multiple hops:")
    print("\n" + final_context)
    print("\nCalling the LLM with context...")
    
    return final_context

@app.post("/")
def read_root(chat_request: ChatRequest):
    print("\nReceived question: " + chat_request.question)

    model = chat_context.model

    messages = []

    for msg in chat_request.history:
        messages.append((msg.role, msg.content))

    system_message_template = """You are a helpful AI Support Representative. 
Use the following support article to answer questions.  Only use the provided 
<article> and if an answer can't be found, respond with:  I'm sorry I can't 
help with that.  Please email support at support@acme.com."""

    human_messsage_template = """<article>
{context}
</article>

Question: {question}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message_template),
        MessagesPlaceholder(variable_name="history"),
        ("human", human_messsage_template)
    ])
    
    prompt_context = {
        "context": RunnableLambda(func=retrieve_related_articles),
        "question": RunnablePassthrough(),
        "history": lambda _: messages
    }

    parser = StrOutputParser()

    chain = prompt_context | prompt | model | parser

    stream = chain.stream(chat_request.question)

    return StreamingResponse(stream, media_type="text/plain") 
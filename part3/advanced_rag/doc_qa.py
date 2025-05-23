from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain.retrievers.document_compressors.embeddings_filter import EmbeddingsFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline

import os
from typing import List, Literal
from pydantic import BaseModel

class Message(BaseModel):
    role: Literal["human", "ai"]
    content: str

class ChatRequest(BaseModel):
    question: str
    history: List[Message] = []

def load_documentation(url: str):
    """Load documentation from a website and create a vector store."""
    print(f"\nLoading documentation from {url}...")
    
    # Load the webpage
    loader = WebBaseLoader(url)
    documents = loader.load()
    
    print("Documents loaded")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    splits = text_splitter.split_documents(documents)
    
    print("Text split into chunks")
    print(f"Number of chunks: {len(splits)}")
    
    # Initialize embeddings
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large",
        base_url="http://localhost:11434",
    )

    # Create ChromaDB vector store
    persist_directory = "doc_chroma_db"
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
        
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    

    print("Chroma DB loaded")
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
        llm=OllamaLLM(model='llama2'),
        prompt=PromptTemplate.from_template("""You are an AI assistant helping to reformulate search queries.
        Given the following question, generate 3 different ways to ask the same question.
        Each reformulation should focus on different aspects of the original question.
        
        Original question: {question}
        
        Reformulated questions:""")
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

def create_qa_chain(retriever):
    """Create a QA chain for answering questions about the documentation."""
    
    # Initialize the LLM
    llm = OllamaLLM(model='llama2')
    
    # Create the prompt template
    system_message = """You are a helpful AI assistant that answers questions about documentation.
    Use the following documentation to answer questions. Only use the provided context and if an answer 
    can't be found, respond with: "I'm sorry, I couldn't find that information in the documentation."
    Always cite the specific parts of the documentation you used to answer the question."""

    human_message = """<documentation>
{context}
</documentation>

Question: {question}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message)
    ])
    
    # Create the chain
    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

def main():
    # Example usage
    url = "https://python.langchain.com/docs/how_to/structured_output/"
    retriever = load_documentation(url)

    print("Documentation loaded")

    results = retriever.invoke("How can I get structured output from an LLM using LangChain?")
    print(results[0].page_content)

    """
    qa_chain = create_qa_chain(retriever)
    
    # Example question
    question = "How can I get structured output from an LLM using LangChain?"
    response = qa_chain.invoke(question)
    
    print("\nQuestion:", question)
    print("\nAnswer:", response)
    """

if __name__ == "__main__":
    main() 
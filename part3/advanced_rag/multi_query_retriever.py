from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_ollama.llms import OllamaLLM

# Build a sample vectorDB
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings

# Set logging for the queries
import logging

logging.basicConfig()
logging.getLogger(
    "langchain.retrievers.multi_query").setLevel(logging.INFO)

url = "https://python.langchain.com/docs/how_to/structured_output/"
# Load blog post

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

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
    base_url="http://localhost:11434",
)

vectordb = Chroma.from_documents(collection_name="multi_query_retriever_example", documents=splits,
                                 embedding=embeddings, persist_directory="chroma_db/multi_query_retriever")

print("VectorDB loaded")

llm = OllamaLLM(model="llama3.2")

retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vectordb.as_retriever(), llm=llm
)

results = retriever_from_llm.invoke(
    "Can you tell me how to do structured JSON output?")

print(len(results))

from langchain_chroma.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from ollama import chat
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader

print("\nLoading the README file, please wait just a moment...\n")

documentation_as_documents = TextLoader('../../README.md').load()

print("Number of documents: ", len(documentation_as_documents))
print(documentation_as_documents[0].model_dump_json(indent=2))

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# Initialize the document loader
document_chunks = splitter.split_text(documentation_as_documents[0].page_content)

print("Number of chunks: ", len(document_chunks))

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
    base_url="http://localhost:11434",
)

vector_db = Chroma.from_documents(
    documents=document_chunks,
    embedding=embeddings,
    collection_name="documentation_collection"
)

results = vector_db.similarity_search("Does this book use Ollama?", k=1)

print("Number of results: ", len(results))
print(results[0].page_content)
import chromadb

from chromadb import Collection
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from chromadb.utils.embedding_functions.ollama_embedding_function import (
  OllamaEmbeddingFunction,
)


class DocumentVectorStore:
  def __init__(self, document: str):
    self.collection: Collection = self._initialize_vector_store(document)

  def query(self, question: str) -> List[str]:
    results = self.collection.query(query_texts=[question], n_results=3)

    documents = results.get('documents')[0]

    return documents

  def _initialize_vector_store(self, document: str) -> Collection:
    # Initialize embeddings and vector store
    embedding_function = OllamaEmbeddingFunction(
      url="http://localhost:11434",
      model_name="mxbai-embed-large"
    )

    client = chromadb.Client()

    collection: Collection = client.create_collection(
      name="examples_readme",
      embedding_function=embedding_function,
    )

    document_chunks = self._chunk_document(document)

    for chunk_idx, document_chunk in document_chunks:
      collection.add(
        documents=document_chunk,
        ids=f"doc{chunk_idx + 1}"
      )

    return collection

  def _chunk_document(self, document: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter.from_language(
      language="markdown", chunk_size=1200)

    document_chunks = splitter.split_text(document)

    print("Number of chunks: ", len(document_chunks))

    return document_chunks

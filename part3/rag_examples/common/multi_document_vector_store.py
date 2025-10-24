import chromadb

from chromadb import Collection
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from common.document import Document

from chromadb.utils.embedding_functions.ollama_embedding_function import (
  OllamaEmbeddingFunction,
)


class MultiDocumentVectorStore:
  def __init__(self, documents: List[Document]):
    self.collection: Collection = self._initialize_vector_store(documents)

  def query(self, question: str):
    results = self.collection.query(query_texts=[question], n_results=3)

    documents = results.get('documents')[0]
    metadatas = results.get('metadatas')[0]

    document_with_metadata: List[Document] = []

    for doc_idx, document in enumerate(documents):
      document_with_metadata.append(Document(
        source_url=metadatas[doc_idx].get('source_url'),
        content=document
      ))

    return document_with_metadata

  def _initialize_vector_store(self, documents: List[Document]) -> Collection:
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

    for doc_idx, document in enumerate(documents):
      document_chunks = self._chunk_document(document.content)

      for chunk_idx, document_chunk in enumerate(document_chunks):
        collection.add(
          documents=document_chunk,
          ids=f"doc_{doc_idx + 1}_{chunk_idx + 1}",
          metadatas={"source_url": document.source_url}
        )

    return collection

  def _chunk_document(self, document: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter.from_language(
      language="markdown", chunk_size=1200)

    document_chunks = splitter.split_text(document)

    print("Number of chunks: ", len(document_chunks))

    return document_chunks

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
    embedding_function = OllamaEmbeddingFunction(
      url="http://localhost:11434",
      model_name="mxbai-embed-large"
    )

    client = chromadb.Client()

    self.collection: Collection = client.create_collection(
      name="examples_readme",
      embedding_function=embedding_function,
    )

    splitter = RecursiveCharacterTextSplitter.from_language(
      language="markdown", chunk_size=1500)

    for doc_idx, document in enumerate(documents):
      document_chunks = splitter.split_text(document.content)

      for chunk_idx, document_chunk in enumerate(document_chunks):
        self.collection.add(
          documents=document_chunk,
          ids=f"doc_{doc_idx + 1}_{chunk_idx + 1}",
          metadatas={"source_url": document.source_url}
        )

  def query(self, question: str):
    results = self.collection.query(query_texts=[question], n_results=3)

    document_chunk_results = results.get('documents')[0]
    document_chunk_metadatas = results.get('metadatas')[0]

    documents: List[Document] = []

    for result_idx, document_chunk in enumerate(document_chunk_results):
      documents.append(Document(
        source_url=document_chunk_metadatas[result_idx].get('source_url'),
        content=document_chunk
      ))

    return documents

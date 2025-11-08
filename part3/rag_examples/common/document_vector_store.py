import chromadb

from chromadb import Collection
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

from chromadb.utils.embedding_functions.ollama_embedding_function import (
  OllamaEmbeddingFunction
)


class DocumentVectorStore:
  def __init__(self, document_text: str):
    ollama_embedding_function = OllamaEmbeddingFunction(
      url="http://localhost:11434",
      model_name="mxbai-embed-large"
    )

    client = chromadb.Client()

    self.collection: Collection = client.create_collection(
      name="examples_readme",
      embedding_function=ollama_embedding_function,
    )

    splitter = RecursiveCharacterTextSplitter.from_language(
      language=Language.MARKDOWN,
      chunk_size=1500
    )

    chunks = splitter.split_text(document_text)

    self.collection.add(
      documents=chunks,
      ids=[f"doc{chunk_idx + 1}" for chunk_idx, chunk in enumerate(chunks)]
    )

  def query(self, question: str, n_results=3) -> List[str]:
    results = self.collection.query(
      query_texts=[question], n_results=n_results)

    return results.get('documents')[0]

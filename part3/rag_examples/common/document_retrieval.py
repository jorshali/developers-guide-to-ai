import requests

from common.document import Document


def load_local_document(full_file_path: str):
  with open(full_file_path, 'r') as f:
    document_text = f.read()

    return document_text


def download_remote_document(owner="jorshali", repo="developers-guide-to-ai", branch="main", filename="README.md") -> Document:
  source_url = f"https://github.com/{owner}/{repo}/blob/{branch}/{filename}"
  raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filename}"

  response = requests.get(raw_url)
  response.raise_for_status()  # raises exception for 4xx/5xx errors

  print(f"Downloaded file from {raw_url}")

  return Document(
    source_url=source_url,
    content=response.text
  )

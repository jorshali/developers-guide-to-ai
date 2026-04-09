from pydantic import BaseModel


class Document(BaseModel):
  source_url: str
  content: str

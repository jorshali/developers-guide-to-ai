from jinja2 import Environment, FileSystemLoader
from ollama import chat
from pydantic import BaseModel
from typing import List

env = Environment(
  loader=FileSystemLoader(searchpath="templates")
)


class QueryList(BaseModel):
  queries: List[str]


class MultiQuery:
  def __init__(self):
    self.query_template = env.get_template(
      'multi_query_prompt_template.txt')

  def generate_multiple_queries(self, query: str):
    messages = [{
      'role': 'user',
      'content': self.query_template.render(
        num_queries=3, query=query)
    }]

    response = chat(
      model='llama3.2',
      messages=messages,
      format=QueryList.model_json_schema(),
      stream=False
    )

    multi_query = QueryList.model_validate_json(response.message.content)

    return multi_query.queries

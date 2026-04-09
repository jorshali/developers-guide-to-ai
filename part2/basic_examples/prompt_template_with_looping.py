from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


def load_file_contents(directory: str):
  files = []

  for path in Path(directory).iterdir():
    if path.is_file():
      with open(path, "r", encoding="utf-8") as f:
        files.append(f.read())

  return files


articles = load_file_contents("../articles")

print(articles)

env = Environment(
  loader=FileSystemLoader("templates"),
  autoescape=select_autoescape()
)

prompt_template = env.get_template(
  "ai_support_representative_prompt_template_with_looping.txt")

question = "I'm having password issues.  Can you help me login?"

prompt = prompt_template.render(articles=articles, question=question)

print(prompt)

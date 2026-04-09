from jinja2 import Environment, FileSystemLoader


def load_file_contents(filename: str):
  with open(filename, "r", encoding="utf-8") as f:
    return f.read()


article = load_file_contents(
  '../articles/how_to_reset_your_acme_password.md')

env = Environment(
  loader=FileSystemLoader("templates")
)

prompt_template = env.get_template(
  "ai_support_representative_prompt_template.txt")

question = "I'm having password issues.  Can you help me login?"

prompt = prompt_template.render(article=article, question=question)

print(prompt)

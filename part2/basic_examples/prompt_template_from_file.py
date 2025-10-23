from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_file_contents(filename: str):
  with open(filename, "r", encoding="utf-8") as f:
    return f.read()


article = load_file_contents(
  '../articles/how_to_reset_your_workday_password.md')

env = Environment(
  loader=FileSystemLoader(searchpath="templates"),
  autoescape=select_autoescape()
)

prompt_template = env.get_template("help_desk_representative_template.txt")

question = "I'm having password issues.  Can you help me login?"

prompt = prompt_template.render(article=article, question=question)

print(prompt)

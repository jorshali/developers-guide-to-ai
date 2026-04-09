from jinja2 import Template


def load_file_contents(filename: str):
  with open(filename, "r", encoding="utf-8") as f:
    return f.read()


article = load_file_contents(
  '../articles/how_to_reset_your_acme_password.md')

prompt_template: Template = Template("""
You are a helpful AI Support Representative. Use the following support 
article to answer questions.  Only use the provided <articles> and if 
an answer can't be found, respond with: I'm sorry I can't help with 
that.  Please call customer support at 555-555-1234.

<article>
{{article}}
</article>

Question: {{question}}""")

question = "I'm having password issues.  Can you help me log in?"

prompt = prompt_template.render(article=article, question=question)

print(prompt)

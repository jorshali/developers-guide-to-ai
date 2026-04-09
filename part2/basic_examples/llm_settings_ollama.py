from ollama import Client

client = Client()


def get_ollama_response(prompt):
  result = client.generate(
    model="llama3.2",
    prompt=prompt,
    options={
      "temperature": 0,              # lower means more deterministic
      "top_p": 0,                    # nucleus-sampling threshold
      "num_predict": 1               # hard cap on response length
    }
  )
  return result.response


prompt = """Tell me if the following statement is: positive, neutral, or negative.  Only respond with the sentiment.

Statement:  Thank you @Acme Corp!  Can't wait to try this new shampoo!
Sentiment:"""

print(get_ollama_response(prompt))

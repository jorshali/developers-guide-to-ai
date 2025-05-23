from ollama import Client

client = Client()

def get_ollama_response(prompt):
    result = client.generate(
        model="llama3.2",
        prompt=prompt,
        options={
          "temperature": 0,
          "top_p": 0,
          "num_predict": 1
        }
    )
    return result.response

prompt = """Tell me if the following statement is:
positive, neutral, or negative
Only respond with the sentiment.

Statement:  Thank you @Acme Corp!  Can't wait to try this new shampoo!
Sentiment:"""

print(get_ollama_response(prompt))
from ollama import Client

client = Client()

def get_ollama_response(prompt):
    result = client.generate(
        model="llama3.2",
        prompt=prompt,
        options={
          "temperature": 1
        }
    )
    return result.response

prompt = """Tell me about the Beatles in 100 words or less."""

print(get_ollama_response(prompt))
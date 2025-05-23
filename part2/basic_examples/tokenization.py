import tiktoken

def count_tokens(text: str, model_name: str) -> None:
  # all OpenAI models are supported
  encoding = tiktoken.encoding_for_model(model_name)
  
  # Tokenize the text
  tokens = encoding.encode(text)
  
  print(tokens)
  print(f"Number of tokens: {len(tokens)}")

model_name = "gpt-4o-mini"
sample_text = "I'm having password issues, can you help me login?"

count_tokens(sample_text, model_name)
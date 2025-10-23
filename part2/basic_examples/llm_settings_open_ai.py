import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": """Tell me if the following statement is: positive, neutral, or negative.  Only respond with the sentiment.

Statement:  Thank you @Acme Corp!  Can't wait to try this new shampoo!
Sentiment:"""}
  ],
  temperature=0,              # lower means more deterministic
  top_p=0,                    # nucleus-sampling threshold
  max_tokens=1                # hard cap on response length
)

print(response.choices[0].message.content)

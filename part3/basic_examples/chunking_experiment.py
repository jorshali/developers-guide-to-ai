from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """"Our system requires multi-factor Authentication (MFA). This helps secure your account.

This step-by-step guide will walk you through the MFA setup."""

splitter = RecursiveCharacterTextSplitter(
  separators=["\n\n", "\n", ".", " ", ""],
  chunk_size=60,
  chunk_overlap=0,
  keep_separator='end'
)

chunks = splitter.split_text(text)

print("Chunks:\n")

for idx, chunk in enumerate(chunks):
  print(f"{idx + 1}:  {chunk}\n- character count: {len(chunk)}")
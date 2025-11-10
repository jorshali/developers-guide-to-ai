from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """"Our system requires multi-factor Authentication (MFA). This helps to keep your account secure. This step-by-step guide will walk you through the MFA setup."""

splitter = RecursiveCharacterTextSplitter(
  separators=["\n\n", "\n", ".", " ", ""],
  chunk_size=70,
  chunk_overlap=0,
  keep_separator='end'
)

chunks = splitter.split_text(text)

print("Chunks:\n")

for idx, chunk in enumerate(chunks):
  print(f"{idx + 1}:  {chunk}\n- character count: {len(chunk)}")

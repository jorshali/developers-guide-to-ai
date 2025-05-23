from sentence_transformers import SentenceTransformer

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# The sentences to encode
sentences = [
    "Sony Wireless Noise-Cancelling Headphones",
    "Canon Professional DSLR Camera Kit",
    "Jenson Wireless Earbuds Pro",
    "Panasonic Wireless Noise-Reduction Headphones",
]

# 2. Calculate embeddings by calling model.encode()
embeddings = model.encode(sentences)

print(embeddings[0])
print(f"Dimensions: {len(embeddings[0])}")

idx_to_compare = 0

similarities = model.similarity(embeddings[idx_to_compare], embeddings)

print(sentences[idx_to_compare])

for idx, embedding in enumerate(embeddings):
  print(f"- {sentences[idx]}, Score: {similarities[idx_to_compare][idx]:.4f}")
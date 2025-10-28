import chromadb
from chromadb.utils import embedding_functions
import pandas as pd

# Initialize ChromaDB client
client = chromadb.Client()

# Use the all-MiniLM-L6-v2 embedding function
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
  model_name="all-MiniLM-L6-v2"
)

# Load product data
products_df = pd.read_csv('products.csv')

# Create collection
collection = client.create_collection(
  name="product_search",
  embedding_function=embedding_function
)

print(type(products_df['title']))

all_titles = products_df['title']
all_descriptions = products_df['description']

all_titles_and_descriptions = zip(all_titles, all_descriptions)

"""Add all products to the ChromaDB collection"""
# Combine title and description for better matching
texts = [
  f"{title} {desc}" for title, desc in all_titles_and_descriptions
]

collection.add(
  documents=texts,
  metadatas=[{
    'product_id': pid,
    'title': title,
    'category': category,
    'description': description,
    'price': str(price)  # ChromaDB requires strings in metadata
  } for pid, title, category, description, price in zip(
    products_df['product_id'],
    products_df['title'],
    products_df['category'],
    products_df['description'],
    products_df['price']
  )],
  ids=[pid for pid in products_df['product_id']]
)

query = "camera for taking professional quality photography"

results = collection.query(
  query_texts=[query],
  n_results=3
)

for metadata in results['metadatas'][0]:
  print(f"{metadata['product_id']}:  {metadata['title']}")

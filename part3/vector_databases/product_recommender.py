import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from typing import List
from dataclasses import dataclass, field


@dataclass
class Product:
  product_id: str
  title: str
  category: str
  description: str
  price: float
  relevance_score: float = 0.0

  def title_and_description(self) -> List[str]:
    return f"{self.title} {self.description}"


@dataclass
class PurchaseHistory:
  products: List[Product] = field(default_factory=list)

  def add_product(self, product: Product) -> None:
    """Add a product to the purchase history"""
    self.products.append(product)

  def get_product_ids(self) -> List[str]:
    """Get list of product IDs in the purchase history"""
    return [product.product_id for product in self.products]

  def has_purchased_product(self, product_id: str) -> bool:
    """Check if a product has been purchased"""
    return any(product.product_id == product_id for product in self.products)

  def get_purchase_descriptions(self) -> List[str]:
    """Get combined title and description for each product"""
    return [f"{product.title_and_description()}" for product in self.products]

  def __str__(self) -> str:
    """String representation of purchase history"""
    return "\n".join(f"- {product.title} ({product.product_id})" for product in self.products)


@dataclass
class User:
  username: str
  purchase_history: PurchaseHistory = field(
    default_factory=PurchaseHistory)

  def add_purchase(self, product: Product) -> None:
    """Add a product to the user's purchase history"""
    self.purchase_history.add_product(product)

  def __str__(self) -> str:
    """String representation of user"""
    return f"\nUser: {self.username}\nPurchase History:\n\n{self.purchase_history}\n"


class ProductRecommender:
  def __init__(self, csv_path: str):
    print("Initializing ProductRecommender...")

    # Initialize ChromaDB client
    self.client = chromadb.Client()

    print("Initializing embedding function...")

    # Use the all-MiniLM-L6-v2 embedding function
    self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Load product data
    self.products_df = pd.read_csv(csv_path)

    print("Creating collection...")

    # Create collection
    self.collection = self.client.create_collection(
        name="products",
        embedding_function=self.embedding_function,
        metadata={"hnsw:space": "cosine"}
    )

    print("Adding products to collection...")

    # Add products to collection
    self._add_products_to_collection()

    # Create a mapping of product_ids to Product objects
    self.product_details = {
        row['product_id']: Product(
            product_id=row['product_id'],
            title=row['title'],
            category=row['category'],
            description=row['description'],
            price=float(row['price'])
        )
        for _, row in self.products_df.iterrows()
    }

    print("Products added to collection.")

  def _add_products_to_collection(self):
    """Add all products to the ChromaDB collection"""
    self.collection.add(
        documents=self.products_df['description'].tolist(),
        metadatas=[{
            'product_id': pid,
            'title': title,
            'category': category,
            'price': str(price)
        } for pid, title, category, price in zip(
            self.products_df['product_id'],
            self.products_df['title'],
            self.products_df['category'],
            self.products_df['price']
        )],
        ids=[str(i) for i in range(len(self.products_df))]
    )

  def get_recommendations(self,
                          purchase_history: PurchaseHistory,
                          n_recommendations: int = 5,
                          same_category_weight: float = 0.7) -> List[Product]:
    """
    Get product recommendations based on purchase history

    Args:
        purchase_history: PurchaseHistory object containing purchased products
        n_recommendations: Number of recommendations to return
        same_category_weight: Weight given to products in the same category

    Returns:
        List of recommended Product objects
    """
    if not purchase_history.products:
      return []

    # Get recommendations based on description similarity
    results = self.collection.query(
        query_texts=purchase_history.get_purchase_descriptions(),
        # Get extra results to account for filtering
        n_results=n_recommendations + len(purchase_history.products)
    )

    # Process results
    recommendations = []

    for idx, metadata in enumerate(results['metadatas'][0]):
      product_id = metadata['product_id']

      # Skip if this product was already purchased
      if purchase_history.has_purchased_product(product_id):
        continue

      # Calculate category bonus
      category_bonus = same_category_weight if any(
          p.category == metadata['category'] for p in purchase_history.products
      ) else 0

      product = self.product_details[product_id]
      product.relevance_score = results['distances'][0][idx] + \
          category_bonus
      recommendations.append(product)

      if len(recommendations) >= n_recommendations:
        break

    # Sort by relevance score (lower is better)
    recommendations.sort(key=lambda x: x.relevance_score)

    return recommendations


def main():
  # Initialize recommender
  recommender = ProductRecommender('products.csv')

  # Create a user
  user = User("john_doe")

  # Add some purchases to the user's history
  # Simulate a user who bought a gaming laptop and noise-canceling headphones
  purchase_ids = ['E005', 'E002']
  for pid in purchase_ids:
    user.add_purchase(recommender.product_details[pid])

  print(f"{user}\n")

  print("Recommended Products:")

  recommendations = recommender.get_recommendations(
      purchase_history=user.purchase_history,
      n_recommendations=5
  )

  for i, product in enumerate(recommendations, 1):
    print(f"\n{i}. {product.title} ({product.product_id})")
    print(f"   Category: {product.category}")
    print(f"   Price: ${product.price:.2f}")
    print(f"   Relevance Score: {product.relevance_score:.4f}")


if __name__ == "__main__":
  main()

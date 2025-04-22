import chromadb
import pandas as pd
import numpy as np
from chromadb.utils import embedding_functions
from typing import List, Dict

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
            embedding_function=self.embedding_function
        )
        
        print("Adding products to collection...")

        # Add products to collection
        self._add_products_to_collection()
        
        # Create a mapping of product_ids to their full details
        self.product_details = self.products_df.set_index('product_id').to_dict('index')

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
                          purchase_history: List[str], 
                          n_recommendations: int = 5,
                          same_category_weight: float = 0.7) -> List[Dict]:
        """
        Get product recommendations based on purchase history
        
        Args:
            purchase_history: List of product IDs that the user has purchased
            n_recommendations: Number of recommendations to return
            same_category_weight: Weight given to products in the same category
            
        Returns:
            List of recommended products with their details
        """
        if not purchase_history:
            return []
        
        # Get the purchased products' details
        purchased_products = [self.product_details[pid] for pid in purchase_history]
        
        # Combine all purchased product descriptions
        purchased_descriptions = [
            self.product_details[pid].get('description', '')
            for pid in purchase_history
        ]
        
        # Get recommendations based on description similarity
        results = self.collection.query(
            query_texts=purchased_descriptions,
            n_results=n_recommendations + len(purchase_history)  # Get extra results to account for filtering
        )
        
        # Process results
        recommendations = []
        seen_products = set(purchase_history)
        
        for idx, metadata in enumerate(results['metadatas'][0]):
            product_id = metadata['product_id']
            
            # Skip if this product was already purchased
            if product_id in seen_products:
                continue
                
            # Calculate category bonus
            category_bonus = same_category_weight if any(
                p['category'] == metadata['category'] for p in purchased_products
            ) else 0
                
            recommendations.append({
                'product_id': product_id,
                'title': metadata['title'],
                'category': metadata['category'],
                'price': float(metadata['price']),
                'relevance_score': results['distances'][0][idx] + category_bonus
            })
            
            if len(recommendations) >= n_recommendations:
                break
        
        # Sort by relevance score (lower is better)
        recommendations.sort(key=lambda x: x['relevance_score'])
        
        return recommendations

def main():
    # Initialize recommender
    recommender = ProductRecommender('products.csv')
    
    # Example usage
    # Simulate a user who bought a gaming laptop and noise-cancelling headphones
    purchase_history = ['E005', 'E002']
    
    print("User's Purchase History:")

    for pid in purchase_history:
        product = recommender.product_details[pid]
        print(f"- {product['title']} ({pid})")
    
    print("\nRecommended Products:")
    
    recommendations = recommender.get_recommendations(
        purchase_history=purchase_history,
        n_recommendations=5
    )
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['title']} ({rec['product_id']})")
        print(f"   Category: {rec['category']}")
        print(f"   Price: ${rec['price']:.2f}")
        print(f"   Relevance Score: {rec['relevance_score']:.4f}")

if __name__ == "__main__":
    main() 
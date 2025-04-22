import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from typing import Dict, List, Tuple

class VectorProductCategorizer:
    def __init__(self, csv_path: str):
        """
        Initialize the vector-based product categorizer
        
        Args:
            csv_path: Path to the products CSV file
        """
        # Initialize ChromaDB client
        self.client = chromadb.Client()
        
        # Use the all-MiniLM-L6-v2 embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Load product data
        self.products_df = pd.read_csv(csv_path)
        
        # Create collection
        self.collection = self.client.create_collection(
            name="product_categories",
            embedding_function=self.embedding_function
        )
        
        # Add products to collection
        self._add_products_to_collection()
    
    def _add_products_to_collection(self):
        """Add all products to the ChromaDB collection"""
        # Combine title and description for better matching
        texts = [
            f"{title} {desc}" for title, desc in zip(
                self.products_df['title'],
                self.products_df['description']
            )
        ]
        
        self.collection.add(
            documents=texts,
            metadatas=[{
                'product_id': pid,
                'title': title,
                'category': category
            } for pid, title, category in zip(
                self.products_df['product_id'],
                self.products_df['title'],
                self.products_df['category']
            )],
            ids=[str(i) for i in range(len(self.products_df))]
        )
    
    def categorize_product(self, 
                         title: str, 
                         description: str, 
                         n_neighbors: int = 3) -> Dict[str, any]:
        """
        Categorize a new product based on its similarity to existing products
        
        Args:
            title: Product title
            description: Product description
            n_neighbors: Number of similar products to consider
            
        Returns:
            Dictionary containing category prediction and similarity analysis
        """
        # Combine title and description
        query_text = f"{title} {description}"
        
        # Find similar products
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_neighbors
        )
        
        # Count category occurrences and calculate confidence
        category_counts = {}
        category_examples = {}
        total_distance = 0
        
        for i, (metadata, distance) in enumerate(zip(
            results['metadatas'][0],
            results['distances'][0]
        )):
            category = metadata['category']
            similarity_score = 1 - distance  # Convert distance to similarity
            
            # Update category counts with weighted vote
            category_counts[category] = category_counts.get(category, 0) + similarity_score
            
            # Store example products for each category
            if category not in category_examples:
                category_examples[category] = {
                    'title': metadata['title'],
                    'similarity_score': similarity_score
                }
            
            total_distance += similarity_score
        
        # Calculate confidence scores
        confidence_scores = {
            category: count / total_distance
            for category, count in category_counts.items()
        }
        
        # Determine predicted category
        predicted_category = max(confidence_scores.items(), key=lambda x: x[1])[0]
        
        return {
            'predicted_category': predicted_category,
            'confidence_scores': confidence_scores,
            'similar_products': category_examples,
            'analysis': {
                'n_neighbors_used': n_neighbors,
                'total_similarity_score': total_distance
            }
        }

def main():
    # Initialize categorizer
    categorizer = VectorProductCategorizer('products.csv')
    
    # Example products to categorize
    test_products = [
        {
            'title': "Bluetooth Wireless Speaker",
            'description': "Portable speaker with 20W output, featuring deep bass, "
                         "24-hour battery life, and IPX7 waterproof rating. "
                         "Includes built-in microphone for hands-free calls and "
                         "voice assistant compatibility."
        },
        {
            'title': "Winter Fleece Jacket",
            'description': "Warm and comfortable fleece jacket made from recycled "
                         "materials. Features two zippered hand pockets, adjustable "
                         "hem, and stand-up collar. Perfect for layering in cold "
                         "weather conditions."
        },
        {
            'title': "Smart Home Security Camera",
            'description': "1080p wireless security camera with night vision, "
                         "motion detection, and two-way audio. Connects to your "
                         "home WiFi and sends alerts to your smartphone."
        },
        {
            'title': "Nature's Valley Granola Bars",
            'description': "Delicious granola bars made with natural ingredients."
        }
    ]
    
    # Categorize example products
    print("Example Categorizations:")
    for product in test_products:
        result = categorizer.categorize_product(
            product['title'],
            product['description']
        )
        
        print(f"\nProduct: {product['title']}")
        print(f"Predicted Category: {result['predicted_category']}")
        print("\nConfidence Scores:")
        for category, score in result['confidence_scores'].items():
            print(f"  - {category}: {score:.2%}")
        
        print("\nMost Similar Products:")
        for category, example in result['similar_products'].items():
            print(f"  - {category}: {example['title']} "
                  f"(Similarity: {example['similarity_score']:.2%})")
        
        print("\nAnalysis:")
        print(f"  - Number of neighbors used: {result['analysis']['n_neighbors_used']}")
        print(f"  - Total similarity score: {result['analysis']['total_similarity_score']:.2f}")
        print("-" * 80)

if __name__ == "__main__":
    main() 
import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PriceRange:
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    def in_range(self, price: float) -> bool:
        """Check if a price is within the specified range"""
        if self.min_price is not None and price < self.min_price:
            return False
        if self.max_price is not None and price > self.max_price:
            return False
        return True

class ProductSearch:
    def __init__(self, csv_path: str):
        """
        Initialize the product search system
        
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
            name="product_search",
            embedding_function=self.embedding_function
        )
        
        # Add products to collection
        self._add_products_to_collection()
        
        # Create price index
        self.price_index = {
            str(i): float(price) 
            for i, price in enumerate(self.products_df['price'])
        }
    
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
                'category': category,
                'price': str(price)  # ChromaDB requires strings in metadata
            } for pid, title, category, price in zip(
                self.products_df['product_id'],
                self.products_df['title'],
                self.products_df['category'],
                self.products_df['price']
            )],
            ids=[str(i) for i in range(len(self.products_df))]
        )

    def search(self, 
               query: str, 
               price_range: Optional[PriceRange] = None,
               category: Optional[str] = None,
               n_results: int = 5,
               min_similarity: float = 0.0) -> List[Dict]:
        """
        Search for products based on description similarity and optional filters
        
        Args:
            query: Search query
            price_range: Optional price range filter
            category: Optional category filter
            n_results: Number of results to return
            min_similarity: Minimum similarity score (0-1) for results
            
        Returns:
            List of matching products with similarity scores
        """
        # Get more results than needed to account for filtering
        n_query_results = n_results
        if price_range or category:
            n_query_results = min(n_results * 3, len(self.products_df))
        
        # Search in collection
        results = self.collection.query(
            query_texts=[query],
            n_results=n_query_results
        )
        
        # Process and filter results
        processed_results = []
        
        for i, (metadata, distance) in enumerate(zip(
            results['metadatas'][0],
            results['distances'][0]
        )):
            similarity_score = 1 - distance
            
            # Skip if below minimum similarity
            if similarity_score < min_similarity:
                continue
            
            # Apply price filter
            if price_range:
                price = float(metadata['price'])
                if not price_range.in_range(price):
                    continue
            
            # Apply category filter
            if category and metadata['category'] != category:
                continue
            
            processed_results.append({
                'product_id': metadata['product_id'],
                'title': metadata['title'],
                'category': metadata['category'],
                'price': float(metadata['price']),
                'similarity_score': similarity_score
            })
            
            if len(processed_results) >= n_results:
                break
        
        return processed_results

    def get_product_details(self, product_id: str) -> Dict:
        """Get full product details by product ID"""
        product = self.products_df[
            self.products_df['product_id'] == product_id
        ].iloc[0]
        return product.to_dict()

def format_price(price: float) -> str:
    """Format price with currency symbol"""
    return f"${price:,.2f}"

def main():
    # Initialize search system
    search = ProductSearch('products.csv')
    
    # Example searches
    test_queries = [
        {
            'query': "wireless headphones with noise cancellation",
            'price_range': PriceRange(max_price=400),
            'category': "Electronics"
        },
        {
            'query': "warm winter jacket",
            'price_range': PriceRange(min_price=100, max_price=500),
            'category': "Apparel"
        },
        {
            'query': "high quality camera for professional photography",
            'price_range': None,
            'category': None
        }
    ]
    
    # Perform example searches
    for test in test_queries:
        print(f"\nSearch Query: {test['query']}")
        if test['price_range']:
            print("Price Range:", end=" ")
            if test['price_range'].min_price:
                print(f"Min: {format_price(test['price_range'].min_price)}", end=" ")
            if test['price_range'].max_price:
                print(f"Max: {format_price(test['price_range'].max_price)}", end="")
            print()
        if test['category']:
            print(f"Category Filter: {test['category']}")
        
        results = search.search(
            query=test['query'],
            price_range=test['price_range'],
            category=test['category'],
            n_results=3
        )
        
        print("\nResults:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   Category: {result['category']}")
            print(f"   Price: {format_price(result['price'])}")
            print(f"   Similarity Score: {result['similarity_score']:.2%}")
            
            # Get and display full product details
            details = search.get_product_details(result['product_id'])
            print(f"   Description: {details['description'][:150]}...")
        
        print("\n" + "="*80)

def interactive_search():
    """Interactive search interface"""
    search = ProductSearch('products.csv')
    
    while True:
        print("\nProduct Search")
        print("=" * 50)
        
        # Get search query
        query = input("\nEnter search query (or 'quit' to exit): ").strip()
        if query.lower() == 'quit':
            break
        
        # Get optional price range
        try:
            min_price = input("Enter minimum price (or press Enter to skip): ").strip()
            min_price = float(min_price) if min_price else None
            
            max_price = input("Enter maximum price (or press Enter to skip): ").strip()
            max_price = float(max_price) if max_price else None
            
            price_range = PriceRange(min_price, max_price) if min_price or max_price else None
        except ValueError:
            print("Invalid price value. Using no price filter.")
            price_range = None
        
        # Perform search
        results = search.search(
            query=query,
            price_range=price_range,
            n_results=5
        )
        
        # Display results
        print("\nSearch Results:")
        if not results:
            print("No matching products found.")
            continue
            
        for i, result in enumerate(results):
            print(f"\n{i}. {result['title']}")
            print(f"   Category: {result['category']}")
            print(f"   Price: {format_price(result['price'])}")
            print(f"   Similarity Score: {result['similarity_score']:.2%}")
            
            # Get and display full product details
            details = search.get_product_details(result['product_id'])
            print(f"   Description: {details['description'][:150]}...")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Run example searches")
    print("2. Interactive search")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        interactive_search()
    else:
        print("Invalid choice") 
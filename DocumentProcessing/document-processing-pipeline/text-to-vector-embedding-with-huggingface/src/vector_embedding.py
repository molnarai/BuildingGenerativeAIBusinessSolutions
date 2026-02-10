"""
Simple example demonstrating vector embeddings and semantic similarity.
This is a standalone script that doesn't require OpenSearch.
"""
from sentence_transformers import SentenceTransformer
import numpy as np


def main():
    """Demonstrate basic vector embedding and similarity search."""
    print("=" * 60)
    print("Vector Embedding Example")
    print("=" * 60)
    
    # 1. Load model
    print("\n1. Loading SentenceTransformer model...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("   ✓ Model loaded: all-MiniLM-L6-v2")
    
    # 2. Sample document
    document = """
    OpenSearch is a distributed search and analytics engine.
    It provides powerful full-text search capabilities.
    OpenSearch supports vector search for semantic similarity.
    The k-NN plugin enables efficient nearest neighbor search.
    """
    
    # 3. Chunk text by sentences
    print("\n2. Chunking document...")
    chunks = [s.strip() + '.' for s in document.split('.') if s.strip()]
    print(f"   ✓ Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks, 1):
        print(f"      [{i}] {chunk}")
    
    # 4. Generate embeddings
    print("\n3. Generating embeddings...")
    embeddings = model.encode(chunks, normalize_embeddings=True)
    print(f"   ✓ Generated {len(embeddings)} embeddings")
    print(f"   ✓ Embedding dimension: {embeddings.shape[1]}")
    print(f"   ✓ Embedding shape: {embeddings.shape}")
    
    # 5. Query and search
    print("\n4. Performing semantic search...")
    queries = [
        "search engine features",
        "vector similarity search",
        "distributed systems"
    ]
    
    for query in queries:
        print(f"\n   Query: '{query}'")
        query_embedding = model.encode([query], normalize_embeddings=True)[0]
        
        # Calculate cosine similarities
        similarities = np.dot(embeddings, query_embedding)
        
        # Sort by similarity
        ranked_indices = np.argsort(similarities)[::-1]
        
        print("   Results (ranked by similarity):")
        for rank, idx in enumerate(ranked_indices, 1):
            print(f"      {rank}. [Score: {similarities[idx]:.4f}] {chunks[idx]}")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()



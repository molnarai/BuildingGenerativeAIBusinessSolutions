from opensearchpy import OpenSearch, helpers
from typing import List, Dict, Any, Optional
import numpy as np


class OpenSearchVectorStore:
    """
    A class for managing vector storage and similarity search in OpenSearch.
    """
    
    def __init__(self, host: str = "localhost", port: int = 9200,
                 auth: Optional[tuple] = None, use_ssl: bool = False,
                 verify_certs: bool = False, **kwargs):
        """
        Initialize connection to OpenSearch instance.
        
        Args:
            host: OpenSearch host address
            port: OpenSearch port
            auth: Tuple of (username, password) for authentication
            use_ssl: Whether to use SSL/TLS
            verify_certs: Whether to verify SSL certificates
            **kwargs: Additional OpenSearch client arguments
        """
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=auth,
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            ssl_show_warn=False,
            **kwargs
        )
    
    def create_vector_index(self, index_name: str, dimension: int,
                           space_type: str = "cosinesimil", 
                           ef_construction: int = 128, m: int = 16,
                           ef_search: int = 100) -> Dict[str, Any]:
        """
        Create k-NN enabled index with HNSW algorithm.
        
        Args:
            index_name: Name of the index to create
            dimension: Dimension of the embedding vectors
            space_type: Distance metric (cosinesimil, l2, innerproduct)
            ef_construction: Build-time search quality (higher = better quality, slower)
            m: Number of bi-directional links per node (higher = better recall, more memory)
            ef_search: Query-time search quality (adjust for recall/latency tradeoff)
            
        Returns:
            Response from index creation
        """
        index_body = {
            "settings": {
                "index": {
                    "knn": True,
                    "knn.algo_param.ef_search": ef_search
                }
            },
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": dimension,
                        "method": {
                            "name": "hnsw",
                            "space_type": space_type,
                            "engine": "nmslib",
                            "parameters": {
                                "ef_construction": ef_construction,
                                "m": m
                            }
                        }
                    },
                    "chunk_id": {"type": "integer"},
                    "source_doc": {"type": "keyword"}
                }
            }
        }
        return self.client.indices.create(index=index_name, body=index_body)
    
    def bulk_index_vectors(self, index_name: str, chunks: List[str],
                          embeddings: np.ndarray, source_doc: str = "document",
                          batch_size: int = 500) -> Dict[str, Any]:
        """
        Bulk index text chunks with embeddings.
        
        Args:
            index_name: Name of the index
            chunks: List of text chunks
            embeddings: Numpy array of embeddings
            source_doc: Source document identifier
            batch_size: Number of documents per batch (500-5000 recommended)
            
        Returns:
            Summary of bulk indexing results
        """
        actions = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            action = {
                "_index": index_name,
                "_id": f"{source_doc}_chunk_{idx}",
                "_source": {
                    "text": chunk,
                    "embedding": embedding.tolist(),
                    "chunk_id": idx,
                    "source_doc": source_doc
                }
            }
            actions.append(action)
        
        # Execute in batches
        results = []
        for i in range(0, len(actions), batch_size):
            batch = actions[i:i + batch_size]
            success, failed = helpers.bulk(self.client, batch, raise_on_error=False)
            results.append({"success": success, "failed": failed})
        
        self.client.indices.refresh(index=index_name)
        return {"batches": len(results), "results": results}
    
    def search_similar(self, index_name: str, query_embedding: np.ndarray,
                      k: int = 5, min_score: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Search for k most similar vectors using k-NN.
        
        Args:
            index_name: Name of the index to search
            query_embedding: Query vector as numpy array
            k: Number of similar results to return
            min_score: Optional minimum score threshold
            
        Returns:
            List of matching documents with text and scores
        """
        query = {
            "size": k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_embedding.tolist(),
                        "k": k
                    }
                }
            }
        }
        
        if min_score:
            query["min_score"] = min_score
        
        response = self.client.search(index=index_name, body=query)
        return [{"text": hit['_source']['text'], 
                 "score": hit['_score'],
                 "source_doc": hit['_source'].get('source_doc'),
                 "chunk_id": hit['_source'].get('chunk_id')} 
                for hit in response['hits']['hits']]
    
    def delete_index(self, index_name: str) -> Dict[str, Any]:
        """Delete an index."""
        return self.client.indices.delete(index=index_name)
    
    def index_exists(self, index_name: str) -> bool:
        """Check if an index exists."""
        return self.client.indices.exists(index=index_name)
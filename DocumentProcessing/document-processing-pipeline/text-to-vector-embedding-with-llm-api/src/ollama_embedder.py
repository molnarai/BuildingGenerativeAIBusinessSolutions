import requests
from typing import List, Union


class OllamaTextEmbedder:
    """
    A class for generating text embeddings using Ollama's local API.
    """
    
    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        """
        Initialize the OllamaTextEmbedder.
        
        Args:
            model: The embedding model to use (default: nomic-embed-text)
            base_url: The base URL for the Ollama API (default: http://localhost:11434)
        """
        self.model = model
        self.base_url = base_url
        self.embed_url = f"{base_url}/api/embeddings"
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for the given text.
        
        Args:
            text: A single string or list of strings to embed
            
        Returns:
            A list of floats (for single text) or list of lists (for multiple texts)
        """
        is_single = isinstance(text, str)
        texts = [text] if is_single else text
        
        embeddings = []
        for t in texts:
            payload = {
                "model": self.model,
                "prompt": t
            }
            
            response = requests.post(self.embed_url, json=payload)
            response.raise_for_status()
            
            embedding = response.json()["embedding"]
            embeddings.append(embedding)
        
        return embeddings[0] if is_single else embeddings
    
    def embed_batch(self, texts: List[str], batch_size: int = 10) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts with batching support.
        
        Args:
            texts: List of strings to embed
            batch_size: Number of texts to process at once
            
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embed(batch)
            embeddings.extend(batch_embeddings)
        
        return embeddings

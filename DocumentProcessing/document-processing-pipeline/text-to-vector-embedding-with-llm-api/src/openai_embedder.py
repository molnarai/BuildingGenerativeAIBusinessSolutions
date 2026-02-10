from typing import List, Optional
import numpy as np
from openai import OpenAI

class OpenAiTextEmbedder:
    """A class for converting text into vector embeddings."""
    
    def __init__(self, model: str = "text-embedding-3-small", api_key: Optional[str] = None):
        """
        Initialize the TextEmbedder.
        
        Args:
            model: The embedding model to use (default: text-embedding-3-small)
            api_key: OpenAI API key (if None, uses environment variable)
        """
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def embed(self, text: str) -> List[float]:
        """
        Convert a single text string to a vector embedding.
        
        Args:
            text: The text to embed
            
        Returns:
            A list of floats representing the embedding vector
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Convert multiple text strings to vector embeddings.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            A list of embedding vectors
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension size of the embeddings.
        
        Returns:
            The dimension of the embedding vectors
        """
        test_embedding = self.embed("test")
        return len(test_embedding)
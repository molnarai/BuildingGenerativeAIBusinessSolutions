from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np


class HuggingFaceEmbedder:
    """
    A class for generating text embeddings using HuggingFace SentenceTransformer models.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = None):
        """
        Initialize the HuggingFaceEmbedder.
        
        Args:
            model_name: The SentenceTransformer model to use (default: all-MiniLM-L6-v2)
            device: Device to use for inference ('cuda', 'cpu', or None for auto)
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device=device)
    
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
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        embeddings_list = embeddings.tolist()
        
        return embeddings_list[0] if is_single else embeddings_list
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts with batching support.
        
        Args:
            texts: List of strings to embed
            batch_size: Number of texts to process at once
            
        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        embeddings = self.model.encode(
            texts, 
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings.tolist()

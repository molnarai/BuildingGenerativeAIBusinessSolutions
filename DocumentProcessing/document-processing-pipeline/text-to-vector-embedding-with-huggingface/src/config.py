import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration management for the embedding pipeline."""
    
    # Input/Output
    INPUT_DIR: str = os.getenv("INPUT_DIR", "/data/input")
    
    # Text Chunking
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "200"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    BREAK_ON_SENTENCE: bool = os.getenv("BREAK_ON_SENTENCE", "true").lower() == "true"
    
    # Embedding Model
    MODEL_NAME: str = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    DEVICE: Optional[str] = os.getenv("DEVICE", None)
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "32"))
    
    # OpenSearch
    OPENSEARCH_HOST: str = os.getenv("OPENSEARCH_HOST", "localhost")
    OPENSEARCH_PORT: int = int(os.getenv("OPENSEARCH_PORT", "9200"))
    OPENSEARCH_ENDPOINT: Optional[str] = os.getenv("OPENSEARCH_ENDPOINT", None)
    OPENSEARCH_REGION: str = os.getenv("OPENSEARCH_REGION", "us-east-1")
    OPENSEARCH_USER: Optional[str] = os.getenv("OPENSEARCH_USER", None)
    OPENSEARCH_PASSWORD: Optional[str] = os.getenv("OPENSEARCH_PASSWORD", None)
    USE_SSL: bool = os.getenv("USE_SSL", "false").lower() == "true"
    VERIFY_CERTS: bool = os.getenv("VERIFY_CERTS", "false").lower() == "true"
    INDEX_NAME: str = os.getenv("INDEX_NAME", "text-embeddings")
    SPACE_TYPE: str = os.getenv("SPACE_TYPE", "cosinesimil")
    INDEX_BATCH_SIZE: int = int(os.getenv("INDEX_BATCH_SIZE", "500"))
    
    @classmethod
    def get_opensearch_auth(cls) -> Optional[tuple]:
        """Get OpenSearch authentication tuple if credentials are provided."""
        if cls.OPENSEARCH_USER and cls.OPENSEARCH_PASSWORD:
            return (cls.OPENSEARCH_USER, cls.OPENSEARCH_PASSWORD)
        return None
    
    @classmethod
    def get_opensearch_config(cls) -> dict:
        """Get complete OpenSearch configuration."""
        return {
            "host": cls.OPENSEARCH_HOST,
            "port": cls.OPENSEARCH_PORT,
            "endpoint": cls.OPENSEARCH_ENDPOINT,
            "region": cls.OPENSEARCH_REGION,
            "auth": cls.get_opensearch_auth(),
            "use_ssl": cls.USE_SSL,
            "verify_certs": cls.VERIFY_CERTS,
            "index_name": cls.INDEX_NAME,
            "space_type": cls.SPACE_TYPE,
            "index_batch_size": cls.INDEX_BATCH_SIZE
        }

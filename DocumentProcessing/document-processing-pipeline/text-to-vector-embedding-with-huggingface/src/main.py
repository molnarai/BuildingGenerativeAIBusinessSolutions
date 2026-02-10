import argparse
import glob
import os
from pathlib import Path
import numpy as np

from text_chunker import TextChunker
from huggingface_embedder import HuggingFaceEmbedder
from open_search import OpenSearchVectorStore
from config import Config


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process text files, generate embeddings, and store in OpenSearch"
    )
    
    # Input/Output
    parser.add_argument(
        "--input-dir",
        type=str,
        default=Config.INPUT_DIR,
        help=f"Directory containing input .txt files (default: {Config.INPUT_DIR})"
    )
    
    # Text Chunking
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=Config.CHUNK_SIZE,
        help=f"Maximum size of each chunk in characters (default: {Config.CHUNK_SIZE})"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=Config.CHUNK_OVERLAP,
        help=f"Number of characters to overlap between chunks (default: {Config.CHUNK_OVERLAP})"
    )
    parser.add_argument(
        "--no-sentence-break",
        action="store_true",
        help="Disable breaking at sentence boundaries"
    )
    
    # Embedding Model
    parser.add_argument(
        "--model-name",
        type=str,
        default=Config.MODEL_NAME,
        help=f"HuggingFace model name (default: {Config.MODEL_NAME})"
    )
    parser.add_argument(
        "--device",
        type=str,
        default=Config.DEVICE,
        help="Device for inference (cuda/cpu, default: auto)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=Config.BATCH_SIZE,
        help=f"Batch size for embedding generation (default: {Config.BATCH_SIZE})"
    )
    
    # OpenSearch Configuration
    parser.add_argument(
        "--opensearch-host",
        type=str,
        default=Config.OPENSEARCH_HOST,
        help=f"OpenSearch host (default: {Config.OPENSEARCH_HOST})"
    )
    parser.add_argument(
        "--opensearch-port",
        type=int,
        default=Config.OPENSEARCH_PORT,
        help=f"OpenSearch port (default: {Config.OPENSEARCH_PORT})"
    )
    parser.add_argument(
        "--opensearch-user",
        type=str,
        default=Config.OPENSEARCH_USER,
        help="OpenSearch username (from env or optional)"
    )
    parser.add_argument(
        "--opensearch-password",
        type=str,
        default=Config.OPENSEARCH_PASSWORD,
        help="OpenSearch password (from env or optional)"
    )
    parser.add_argument(
        "--use-ssl",
        action="store_true",
        default=Config.USE_SSL,
        help="Use SSL for OpenSearch connection"
    )
    parser.add_argument(
        "--index-name",
        type=str,
        default=Config.INDEX_NAME,
        help=f"OpenSearch index name (default: {Config.INDEX_NAME})"
    )
    parser.add_argument(
        "--space-type",
        type=str,
        default=Config.SPACE_TYPE,
        choices=["cosinesimil", "l2", "innerproduct"],
        help=f"Distance metric for vector search (default: {Config.SPACE_TYPE})"
    )
    parser.add_argument(
        "--index-batch-size",
        type=int,
        default=Config.INDEX_BATCH_SIZE,
        help=f"Batch size for bulk indexing (default: {Config.INDEX_BATCH_SIZE})"
    )
    
    return parser.parse_args()


def read_text_file(filepath: str) -> str:
    """Read text file content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def main():
    """Main processing pipeline."""
    args = parse_args()
    
    print("="*60)
    print("Text to Vector Embedding Pipeline")
    print("="*60)
    
    # Initialize components
    print("\n1. Initializing components...")
    chunker = TextChunker(
        chunk_size=args.chunk_size,
        overlap=args.chunk_overlap,
        break_on_sentence=not args.no_sentence_break
    )
    print(f"   ✓ Text Chunker (size={args.chunk_size}, overlap={args.chunk_overlap})")
    
    embedder = HuggingFaceEmbedder(
        model_name=args.model_name,
        device=args.device
    )
    print(f"   ✓ Embedder ({args.model_name})")
    
    # Setup OpenSearch authentication from config or args
    auth = None
    if args.opensearch_user and args.opensearch_password:
        auth = (args.opensearch_user, args.opensearch_password)
        print(f"   ℹ Using OpenSearch authentication (user: {args.opensearch_user})")
    else:
        print(f"   ℹ Connecting to OpenSearch without authentication")
    
    vector_store = OpenSearchVectorStore(
        host=args.opensearch_host,
        port=args.opensearch_port,
        auth=auth,
        use_ssl=args.use_ssl,
        verify_certs=False
    )
    print(f"   ✓ OpenSearch Vector Store ({args.opensearch_host}:{args.opensearch_port})")
    
    # Find all text files
    print(f"\n2. Scanning for text files in {args.input_dir}...")
    input_pattern = os.path.join(args.input_dir, "*.txt")
    text_files = glob.glob(input_pattern)
    
    if not text_files:
        print(f"   ✗ No .txt files found in {args.input_dir}")
        return
    
    print(f"   ✓ Found {len(text_files)} text file(s)")
    
    # Create or check index
    print(f"\n3. Setting up OpenSearch index '{args.index_name}'...")
    if vector_store.index_exists(args.index_name):
        print(f"   ℹ Index already exists")
    else:
        # Get embedding dimension from a test embedding
        test_embedding = embedder.embed("test")
        dimension = len(test_embedding)
        
        vector_store.create_vector_index(
            index_name=args.index_name,
            dimension=dimension,
            space_type=args.space_type
        )
        print(f"   ✓ Created index (dimension={dimension})")
    
    # Process each file
    print(f"\n4. Processing files...")
    total_chunks = 0
    
    for idx, filepath in enumerate(text_files, 1):
        filename = os.path.basename(filepath)
        print(f"\n   [{idx}/{len(text_files)}] Processing: {filename}")
        
        # Read file
        text = read_text_file(filepath)
        if not text:
            continue
        
        print(f"      - Read {len(text)} characters")
        
        # Chunk text
        chunks = chunker.chunk(text)
        print(f"      - Generated {len(chunks)} chunks")
        
        if not chunks:
            continue
        
        # Generate embeddings
        embeddings = embedder.embed_batch(chunks, batch_size=args.batch_size)
        embeddings_array = np.array(embeddings)
        print(f"      - Generated embeddings (shape: {embeddings_array.shape})")
        
        # Index in OpenSearch
        source_doc = Path(filepath).stem  # Use filename without extension
        result = vector_store.bulk_index_vectors(
            index_name=args.index_name,
            chunks=chunks,
            embeddings=embeddings_array,
            source_doc=source_doc,
            batch_size=args.index_batch_size
        )
        print(f"      - Indexed {len(chunks)} chunks in {result['batches']} batch(es)")
        
        total_chunks += len(chunks)
    
    print("\n" + "="*60)
    print(f"✓ Pipeline Complete!")
    print(f"  Total files processed: {len(text_files)}")
    print(f"  Total chunks indexed: {total_chunks}")
    print(f"  Index name: {args.index_name}")
    print("="*60)


if __name__ == "__main__":
    main()

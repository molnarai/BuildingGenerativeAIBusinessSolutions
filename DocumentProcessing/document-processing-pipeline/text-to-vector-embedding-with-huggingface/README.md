# Text to Vector Embedding with HuggingFace

A complete pipeline for processing text documents, generating embeddings using HuggingFace models, and storing them in OpenSearch for semantic search.

## Features

- Text chunking with configurable size and overlap
- Vector embedding generation using SentenceTransformers
- OpenSearch integration with k-NN search
- Bulk indexing support
- CLI interface for easy usage

## Prerequisites

- Python 3.8+
- OpenSearch instance (local or remote)
- Sufficient disk space for embedding models

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Ensure OpenSearch is running:
```bash
# For local Docker instance:
docker run -p 9200:9200 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

## Usage

### Basic Usage

Process all text files in the default input directory:

```bash
python src/main.py
```

### Custom Configuration

```bash
python src/main.py \
  --input-dir /path/to/documents \
  --chunk-size 300 \
  --chunk-overlap 75 \
  --model-name "all-mpnet-base-v2" \
  --opensearch-host localhost \
  --opensearch-port 9200 \
  --index-name my-documents
```

### CLI Arguments

**Input/Output:**
- `--input-dir`: Directory containing .txt files (default: /data/input)

**Text Chunking:**
- `--chunk-size`: Maximum chunk size in characters (default: 200)
- `--chunk-overlap`: Overlap between chunks (default: 50)
- `--no-sentence-break`: Disable sentence boundary breaking

**Embedding Model:**
- `--model-name`: HuggingFace model (default: all-MiniLM-L6-v2)
- `--device`: Device for inference (cuda/cpu/auto)
- `--batch-size`: Embedding batch size (default: 32)

**OpenSearch:**
- `--opensearch-host`: Host address (default: localhost)
- `--opensearch-port`: Port number (default: 9200)
- `--opensearch-user`: Username (optional)
- `--opensearch-password`: Password (optional)
- `--use-ssl`: Enable SSL connection
- `--index-name`: Index name (default: text-embeddings)
- `--space-type`: Distance metric (cosinesimil/l2/innerproduct)
- `--index-batch-size`: Bulk indexing batch size (default: 500)

## Example: Simple Vector Embedding

Run the basic example script:

```bash
python src/vector_embedding.py
```

This demonstrates:
- Loading a SentenceTransformer model
- Generating embeddings
- Computing semantic similarity

## Architecture


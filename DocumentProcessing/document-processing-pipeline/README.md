# Document Processing Pipeline

This project provides two example implementations of document processing pipelines that demonstrate different approaches to extracting and processing content from various document formats.

## Overview

The document processing pipelines in this project showcase how to handle heterogeneous document types (PDFs, Word documents, PowerPoint presentations, images, and text files) and transform them into structured, machine-readable formats suitable for downstream applications such as:

- Content analysis and indexing
- Retrieval-Augmented Generation (RAG) systems
- Knowledge base creation
- Document summarization
- Information extraction

## Pipeline Implementations

### 1. Simple PDF Extraction (`simple-pdf-extraction/`)

This implementation demonstrates a traditional approach to document processing using specialized libraries for each document type.

**Key Features:**
- Direct extraction using format-specific libraries
- Built-in OCR support for scanned documents and images
- Integration with Ollama for AI-powered content analysis
- Entity and keyword extraction
- Document metadata preservation

**Python Frameworks Used:**
- **PyMuPDF (fitz)**: PDF text extraction and metadata
- **python-docx**: Microsoft Word document processing
- **python-pptx**: PowerPoint presentation processing
- **pytesseract + Pillow**: OCR for images and scanned PDFs
- **requests**: HTTP client for Ollama API integration

**Approach:** This pipeline extracts raw text content and processes it through a configurable AI model (via Ollama) to generate summaries, identify topics, classify document types, and extract key information.

### 2. Simple Chunking with Unstructured (`simple-chunking-with-unstructured/`)

This implementation showcases the modern, unified approach using the Unstructured library for document parsing and intelligent chunking.

**Key Features:**
- Unified API for all document types
- Semantic element extraction (titles, paragraphs, lists, tables, etc.)
- Multiple chunking strategies (by_title, basic, no-chunking)
- Configurable chunk size and overlap
- Element-level metadata preservation

**Python Frameworks Used:**
- **unstructured[all-docs]**: Comprehensive document partitioning and chunking
  - Handles PDFs, Word, PowerPoint, HTML, images, and more
  - Extracts semantic elements while preserving document structure
- **requests**: For potential external API integration

**Approach:** This pipeline uses Unstructured to partition documents into semantically meaningful elements, then applies intelligent chunking strategies that respect document structure. The output is a collection of elements/chunks with rich metadata, ideal for RAG applications.

## Key Differences

| Aspect | Simple PDF Extraction | Chunking with Unstructured |
|--------|----------------------|----------------------------|
| **Document Parsing** | Format-specific libraries | Unified Unstructured API |
| **Output Structure** | Single document-level JSON | Element/chunk-level JSON files |
| **Chunking** | None (full document) | Configurable chunking strategies |
| **Semantic Understanding** | Basic (via AI analysis) | Built-in element type detection |
| **Document Structure** | Preserved in metadata | Preserved as hierarchical elements |
| **Processing Focus** | Content extraction and analysis | Structured partitioning for retrieval |
| **AI Integration** | Built-in Ollama integration | Optional (framework-agnostic) |

## Why Use a Containerized Approach?

We've containerized both pipelines using Docker for several important reasons:

1. **Dependency Management**: Document processing libraries often have complex system dependencies (e.g., Tesseract for OCR, system libraries for PDF processing). Containers encapsulate these dependencies cleanly.

2. **Reproducibility**: Container images ensure that the pipeline runs identically across different machines and environments, eliminating "it works on my machine" issues.

3. **Isolation**: Processing documents can be resource-intensive. Containers provide isolation from the host system and allow for resource limiting.

4. **Portability**: The same container image can run on Windows, macOS, and Linux without modification.

5. **Scalability**: Containerized pipelines can be easily orchestrated using tools like Docker Compose or Kubernetes for batch processing of large document collections.

6. **Security**: Documents often contain sensitive information. Containers provide an additional layer of security and can be run with restricted permissions.

## Running the Pipelines

### Prerequisites

- Docker installed on your system
- For AI features (simple-pdf-extraction): Ollama running locally or accessible via URL

### Windows

1. **Install Docker Desktop** from https://www.docker.com/products/docker-desktop

2. **Prepare your documents**:
   ```cmd
   mkdir -p data\input
   mkdir -p data\output
   # Copy your documents to data/input
   ```

3. **Run Simple PDF Extraction**:
   ```cmd
   cd simple-pdf-extraction
   docker build -t simple-pdf-extraction .
   docker run -v "%cd%/../data:/data" simple-pdf-extraction
   ```

4. **Run Chunking with Unstructured**:
   ```cmd
   cd simple-chunking-with-unstructured
   docker build -t simple-chunking-unstructured .
   # No chunking
   docker run -v "%cd%/../data:/data" simple-chunking-unstructured
   # With by_title chunking
   docker run -v "%cd%/../data:/data" simple-chunking-unstructured --by-title --max-chunk-size 1000 --max-chunk-overlap 100
   ```

### macOS

1. **Install Docker Desktop** from https://www.docker.com/products/docker-desktop

2. **Prepare your documents**:
   ```bash
   mkdir -p data/input
   mkdir -p data/output
   # Copy your documents to data/input
   ```

3. **Run Simple PDF Extraction**:
   ```bash
   cd simple-pdf-extraction
   docker build -t simple-pdf-extraction .
   docker run -v $(pwd)/../data:/data simple-pdf-extraction
   ```

4. **Run Chunking with Unstructured**:
   ```bash
   cd simple-chunking-with-unstructured
   docker build -t simple-chunking-unstructured .
   # No chunking
   docker run -v $(pwd)/../data:/data simple-chunking-unstructured
   # With basic chunking
   docker run -v $(pwd)/../data:/data simple-chunking-unstructured --basic --max-chunk-size 1500
   ```

### Linux

1. **Install Docker** (distribution-specific):
   - Ubuntu/Debian: `sudo apt-get install docker.io docker-compose`
   - CentOS/RHEL: `sudo yum install docker docker-compose`
   - Arch: `sudo pacman -S docker`

2. **Prepare your documents**:
   ```bash
   mkdir -p data/input
   mkdir -p data/output
   # Copy your documents to data/input
   ```

3. **Run Simple PDF Extraction**:
   ```bash
   cd simple-pdf-extraction
   docker build -t simple-pdf-extraction .
   docker run -v $(pwd)/../data:/data simple-pdf-extraction
   ```

4. **Run Chunking with Unstructured**:
   ```bash
   cd simple-chunking-with-unstructured
   docker build -t simple-chunking-unstructured .
   # No chunking
   docker run -v $(pwd)/../data:/data simple-chunking-unstructured
   # With by_title chunking
   docker run -v $(pwd)/../data:/data simple-chunking-unstructured --by-title --max-chunk-size 2000 --max-chunk-overlap 200
   ```

### Configuration

#### Simple PDF Extraction

Create a `.env` file in the `simple-pdf-extraction` directory:

```env
# Ollama Configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_API_KEY=your-api-key-if-needed
OLLAMA_GENERATION_MODEL_NAME=gpt-oss:20b-cloud
OLLAMA_EMBEDDING_MODEL_NAME=mxbai-embed-large

# Logging
LOG_LEVEL=INFO
```

#### Chunking with Unstructured

The Unstructured pipeline accepts command-line arguments for chunking:

- `--by-title`: Use title-based chunking (groups content under titles)
- `--basic`: Use basic size-based chunking
- `--max-chunk-size N`: Maximum characters per chunk (default: 1000)
- `--max-chunk-overlap N`: Overlap between chunks (default: 0)

### Output

- **Simple PDF Extraction**: Results are saved in `data/output/simple-pdf-extraction/` as JSON files containing extracted content, metadata, and AI analysis.
- **Chunking with Unstructured**: Results are saved in `data/output/unstructured-*/` with each element/chunk as a separate JSON file in document-specific subdirectories.

## Choosing Between Implementations

- Use **Simple PDF Extraction** when:
  - You need AI-powered content analysis
  - You want summaries and topic extraction
  - You're working with a smaller number of documents
  - You prefer direct control over the extraction process

- Use **Chunking with Unstructured** when:
  - You're building RAG or retrieval systems
  - You need semantic document partitioning
  - You want to preserve document structure
  - You're processing large volumes of diverse document types

## Contributing

This project serves as a reference implementation. Feel free to adapt, extend, or combine features from both pipelines to suit your specific use case.
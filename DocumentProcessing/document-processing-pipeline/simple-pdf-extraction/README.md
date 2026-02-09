# PDF Document Processing Pipeline



Pull docker image first

he AMD64 platform is the default.
```
docker pull downloads.unstructured.io/unstructured-io/unstructured:latest
```

Or, to explicitly specify the AMD64 platform:
```
docker pull --platform=linux/amd64 downloads.unstructured.io/unstructured-io/unstructured:latest
```


```
docker pull --platform=linux/arm64 downloads.unstructured.io/unstructured-io/unstructured:latest
```


This pipeline extracts text content from various document formats and optionally processes it with Ollama AI for content analysis.

## Supported Document Types

- PDF documents
- Microsoft Word (.docx)
- Microsoft PowerPoint (.pptx)
- Plain text files (.txt)
- Images with OCR support (.jpg, .jpeg, .png, .tiff)

## Quick Start

### Using Docker Compose (Recommended)

1. **Set up environment variables**:
   ```bash
   # Create a .env file in this directory
   cp .env.example .env

   # Edit .env with your settings
   nano .env
   ```

2. **Add documents**:
   ```bash
   # Place your documents in the input directory
   cp your-documents.pdf data/input/
   ```

3. **Run the pipeline**:
   ```bash
   docker-compose build
   ```

  Run the pipeline:
  ```bash
  docker-compose run --rm pdf-extractor ./run.sh
  ```

### Manual Docker Build

```bash
# Build the image
docker build -t pdf-extraction-pipeline .

# Run the container
docker run -v $(pwd)/data/input:/data/input \
           -v $(pwd)/data/output:/data/output \
           -e OLLAMA_BASE_URL=http://your-ollama-server:11434 \
           -e OLLAMA_API_KEY=your-api-key \
           -e OLLAMA_GENERATION_MODEL=generation-model \
           -e OLLAMA_EMBEDDING_MODEL=embedding-model \
           pdf-extraction-pipeline
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OLLAMA_BASE_URL` | No | http://localhost:11434 | URL of your Ollama instance |
| `OLLAMA_API_KEY` | Yes (if using Ollama) | - | API key for Ollama |
| `OLLAMA_GENERATION_MODEL` | No | gpt-oss:20b-cloud | LLM chat or generation model |
| `OLLAMA_EMBEDDING_MODEL` | No | mxbai-embed-large | Embedding model for vectorization |
| `LOG_LEVEL` | No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |


## Output Structure

The pipeline creates JSON files in the `/data/output` directory with the following structure:

```json
{
  "file_name": "document.pdf",
  "file_path": "/data/input/document.pdf",
  "mime_type": "application/pdf",
  "content": "Extracted text content...",
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "page_count": 10
  },
  "extraction_method": "pdf_text_extraction",
  "processed_at": "2024-01-01T12:00:00",
  "text_length": 5000,
  "word_count": 800,
  "ai_analysis": {
    "summary": "Document summary...",
    "topics": ["topic1", "topic2"],
    "document_type": "report",
    "language": "english",
    "confidence": 0.95
  },
  "summary": "Brief summary...",
  "entities": ["Entity1", "Entity2"],
  "keywords": ["keyword1", "keyword2"]
}
```

## Processing Report

After processing, a `processing_report.json` is generated with:
- Total files processed
- Success/failure count
- Document type distribution
- Language detection results
- Average word count

## Troubleshooting

### OCR Issues
For image processing to work, ensure Tesseract OCR is installed in the Docker image (included by default).

### Ollama Connection
- Verify Ollama is running and accessible
- Check the API key and base URL
- Ensure network connectivity between containers

### Memory Issues
For large documents or batch processing:
- Increase container memory limits
- Process documents in smaller batches
- Monitor resource usage

## Development

### Project Structure
```
pdf-extraction/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
├── run.sh                  # Entry script
├── src/
│   ├── main.py            # Main pipeline logic
│   ├── extractor.py       # Document extraction
│   └── processor.py       # Content processing
├── data/
│   ├── input/             # Documents to process
│   └── output/            # Processed results
└── README.md              # This file
```

### Adding Support for New Document Types

1. Add MIME type to `extractor.py`
2. Implement extraction method
3. Add any required dependencies to `requirements.txt`

## License

This project is part of the document processing pipeline repository.
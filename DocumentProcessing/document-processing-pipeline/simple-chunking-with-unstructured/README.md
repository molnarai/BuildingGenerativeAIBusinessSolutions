# PDF Document Processing Pipeline

This program scans the input for supported documents (PDF, DOCX, PPTX, TXT, and images), extracts elements using the unstructured library, optionally chunks text (by_title or basic), cleans unicode quotes, and writes each element as a JSON file under /data/output/<run‑slug>/<document-stem>/. The run slug reflects the chunking settings. See main.py.

## How to Use

- Run directly (inside the container or env with dependencies):
  `python /app/src/main.py`
- Choose chunking:
  ```
  python main.py --by-title
  python main.py --basic
  ```
- Control chunk sizes:
  ```
  python [main.py --by-title --max-chunk-size 1200 --max-chunk-overlap 100
  ```

**Notes**

If neither --by-title nor --basic is set, it uses “no-chunking” and calls the default partition() behavior.
Outputs are written as one JSON per element, per document, in a dedicated directory.

This pipeline extracts text content from various document formats and optionally processes it with Ollama AI for content analysis.


## Development

### Project Structure
```
simple-chunking-with-unstructured/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
├── run.sh                  # Entry script
├── src/
│   └── main.py.py       # Content processing
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
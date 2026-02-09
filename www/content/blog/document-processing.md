---
title: "Document Processing Pipeline with Python"
description: "Two example implementation of processing documents using Python packages"
date: 2026-01-24
lastmod: 2026-01-24
weight: 7
---
<!-- # Document Processing in Python: Two Approaches for AI-Ready Pipelines -->

This tutorial walks through two complementary approaches for transforming raw documents—PDFs, Word files, PowerPoints, images, and plain text—into structured, machine-readable formats suitable for AI systems such as Retrieval-Augmented Generation (RAG), knowledge bases, and document summarization engines. 
<!--more-->

Both implementations are available in the [document-processing-pipeline](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/tree/main/DocumentProcessing/document-processing-pipeline) repository[^1].

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/PDFs_Are_Ruining_Your_RAG_System.m4a" type="audio/mp4" />
    Your browser does not support the audio element.
</audio>

## Why Documents Need to Be Processed

Modern enterprises store vast amounts of knowledge in heterogeneous document formats—PDF reports, Word memos, PowerPoint decks, scanned images, and plain text files. These documents are designed for human consumption, with rich formatting, embedded images, multi-column layouts, headers, footers, and tables that serve a visual purpose but are largely meaningless to an AI model[^1].

Large Language Models and embedding models operate on plain text. They cannot natively interpret the binary structure of a `.pdf` or `.docx` file, nor can they understand that a bold heading signals a new section or that a table cell maps to a particular column header. Without preprocessing, feeding raw document bytes into an AI pipeline produces garbage—or nothing at all[^1].

Document processing solves this by:

- **Extracting text** from format-specific binary containers (PDF streams, OOXML archives, image pixels via OCR)[^1]
- **Preserving metadata** such as titles, authors, page counts, and creation dates that provide context for downstream analysis[^2]
- **Structuring content** into semantically meaningful units—paragraphs, headings, list items, tables—so retrieval systems can match user queries against coherent passages rather than arbitrary character windows[^7]
- **Enabling AI analysis** by producing clean text that can be summarized, classified, embedded into vector databases, or used for entity extraction[^1]

The document processing pipelines in this project showcase how to handle these heterogeneous document types and transform them into structured, machine-readable formats suitable for content analysis and indexing, RAG systems, knowledge base creation, document summarization, and information extraction[^1].

## Approach 1: Simple PDF Extraction

The first pipeline, `simple-pdf-extraction`, takes a **traditional, format-specific** approach. It uses a dedicated Python library for each supported document type, giving you fine-grained control over the extraction process[^1]. The pipeline supports PDF documents, Microsoft Word (`.docx`), Microsoft PowerPoint (`.pptx`), plain text files (`.txt`), and images with OCR support (`.jpg`, `.jpeg`, `.png`, `.tiff`)[^2].

### Extraction and Conversion Packages

The pipeline relies on five key packages, each handling a distinct extraction task[^1]:

**PyMuPDF (`fitz`)** is the workhorse for PDF processing. Imported in Python as `fitz`, PyMuPDF is a high-performance wrapper around the MuPDF rendering engine that extracts text, metadata (title, author, page count), and even image data from PDF files[^15]. It supports multiple extraction modes—plain text via `page.get_text("text")`, block-level extraction that preserves spatial layout, and dictionary mode that includes font properties and bounding box coordinates[^9]. PyMuPDF is significantly faster than many alternatives because it operates at the C level through MuPDF rather than parsing PDF structure in pure Python[^15]. For best performance, open each document only once and prefer `"text"` mode unless you need coordinates or font data[^15].

**python-docx** handles Microsoft Word `.docx` files. Word documents are stored as ZIP archives containing XML files (the Office Open XML format). `python-docx` parses this structure and exposes paragraphs, tables, headers, styles, and document properties through a clean Python API[^1]. The pipeline uses it to iterate through document paragraphs and extract their text content along with formatting metadata.

**python-pptx** performs an analogous role for PowerPoint `.pptx` presentations. Presentations contain slides, and each slide contains shapes (text boxes, titles, content placeholders, tables, images). `python-pptx` traverses this hierarchy, extracting text from each shape and optionally from slide notes[^1]. This is essential because much of the valuable content in presentations resides in speaker notes rather than bullet points.

**pytesseract + Pillow** provide OCR (Optical Character Recognition) capabilities for scanned documents and images. `pytesseract` is a Python wrapper around Google's Tesseract OCR engine[^1]. When the pipeline encounters an image file or a scanned PDF page that contains no extractable text layer, it renders the page as a bitmap using Pillow (the Python Imaging Library) and then passes it to Tesseract for text recognition[^18]. Tesseract supports over 100 languages and can be configured with different page segmentation modes (`--psm`) and OCR engine modes (`--oem`) for optimal accuracy[^6].

**requests** serves as the HTTP client for communicating with the Ollama API. After text is extracted from a document, the pipeline sends it to an Ollama-hosted LLM for AI-powered analysis—generating summaries, identifying topics, classifying document types, and extracting entities and keywords[^1][^2].

### Source Code Architecture

The `simple-pdf-extraction/src/` directory contains four modules that form a clean separation of concerns[^2]:

- `main.py` — The pipeline entry point that orchestrates the overall workflow: scanning the input directory, dispatching documents to the extractor, sending extracted text to the processor, and writing JSON output
- `extractor.py` — Contains format-specific extraction logic, dispatching to PyMuPDF, python-docx, python-pptx, or pytesseract based on MIME type detection
- `processor.py` — Handles AI-powered content analysis by sending extracted text to Ollama and parsing structured responses
- `ollama_lister.py` — Utility for querying available models on the Ollama server

### Output Structure

The pipeline produces one JSON file per input document in `data/output/simple-pdf-extraction/`, containing the full extracted content, document metadata, extraction method used, processing timestamp, word count, and AI analysis results[^2]. A sample output structure looks like:

```json
{
  "filename": "document.pdf",
  "filepath": "data/input/document.pdf",
  "mime_type": "application/pdf",
  "content": "Extracted text content...",
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "page_count": 10
  },
  "extraction_method": "pdf_text_extraction",
  "text_length": 5000,
  "word_count": 800,
  "ai_analysis": {
    "summary": "Document summary...",
    "topics": ["topic1", "topic2"],
    "document_type": "report",
    "language": "english",
    "confidence": 0.95
  },
  "entities": ["Entity1", "Entity2"],
  "keywords": ["keyword1", "keyword2"]
}
```

After all documents are processed, a `processing_report.json` is generated with aggregate statistics including total files processed, success/failure counts, document type distribution, and average word counts[^2].

## Connecting to LLMs via Ollama

The `simple-pdf-extraction` pipeline integrates with LLMs through [Ollama](https://ollama.com/), an open-source tool for running language models locally or connecting to cloud-hosted inference endpoints[^1][^2]. This architecture provides flexibility: users with GPU hardware (NVIDIA CUDA, Apple Metal) can run models locally for data privacy, while others can point to a remote Ollama-compatible API endpoint for cloud-hosted inference.

### Configuration

Connection is configured through environment variables in a `.env` file placed in the `simple-pdf-extraction` directory[^1][^2]:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_API_KEY=your-api-key-if-needed
OLLAMA_GENERATION_MODEL_NAME=gpt-oss20b-cloud
OLLAMA_EMBEDDING_MODEL_NAME=mxbai-embed-large

# Logging
LOG_LEVEL=INFO
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `OLLAMA_BASE_URL` | No | `http://localhost:11434` | URL of your Ollama instance[^2] |
| `OLLAMA_API_KEY` | Yes (if using Ollama) | — | API key for authentication[^2] |
| `OLLAMA_GENERATION_MODEL` | No | `gpt-oss20b-cloud` | LLM for chat/generation tasks[^2] |
| `OLLAMA_EMBEDDING_MODEL` | No | `mxbai-embed-large` | Model for vectorization[^2] |

The `OLLAMA_BASE_URL` can point to `localhost` for a local Ollama installation, a remote server on your network, or a cloud endpoint that exposes an Ollama-compatible API[^2]. This means the same pipeline code works whether you're running a quantized 7B model on a laptop GPU or routing requests to a hosted inference service.

### Structured Outputs

A key capability that Ollama provides is **structured outputs**—the ability to constrain a model's response to conform to a specific JSON schema[^8][^14]. Instead of parsing free-form natural language responses (which is error-prone), the pipeline can request that Ollama return results in a predefined structure by passing a JSON schema to the `format` parameter of the API call[^14].

For example, to extract structured analysis from a document, you can define a schema and pass it in the API request:

```bash
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-oss",
    "messages": [{"role": "user", "content": "Analyze this document..."}],
    "stream": false,
    "format": {
      "type": "object",
      "properties": {
        "summary": {"type": "string"},
        "topics": {"type": "array", "items": {"type": "string"}},
        "document_type": {"type": "string"},
        "confidence": {"type": "number"}
      },
      "required": ["summary", "topics"]
    }
  }'
```

This guarantees that the model's output will always be valid JSON matching the specified schema, making downstream processing reliable and repeatable[^8][^14]. Under the hood, Ollama uses constrained decoding (often leveraging Pydantic model capabilities) to enforce the schema at generation time[^5]. Use cases include parsing data from documents, extracting data from images, and structuring all language model responses with more reliability and consistency than basic JSON mode[^8].

## Approach 2: Chunking with Unstructured.io

The second pipeline, `simple-chunking-with-unstructured`, takes a fundamentally different approach using the **Unstructured** library (`unstructured[all-docs]`)[^1]. Rather than using format-specific libraries and writing custom extraction logic for each document type, Unstructured provides a unified API that handles PDFs, Word, PowerPoint, HTML, images, and more through a single interface[^1].

### Partitioning: From Documents to Elements

The core concept in Unstructured is **partitioning**—the process of breaking a document down into a list of typed `Element` objects that represent the semantic components of the source file[^7][^4]. Instead of treating a document as a wall of plain text, Unstructured preserves the document's semantic structure, giving you control over how each component is used downstream[^7].

When you call a partition function (e.g., `partition_pdf`, `partition_docx`, or the universal `partition`), Unstructured analyzes the document and returns a list of elements, each with a `type`, a unique `element_id`, the extracted `text`, and rich `metadata`[^7]. Here is an example element:

```json
{
  "type": "NarrativeText",
  "element_id": "5ef1d1117721f0472c1ad825991d7d37",
  "text": "The Unstructured API documentation covers the following API services:",
  "metadata": {
    "last_modified": "2024-05-01T14:15:22",
    "page_number": 1,
    "languages": ["eng"],
    "parent_id": "56f24319ae258b735cac3ec2a271b1d9",
    "filename": "Unstructured.html",
    "filetype": "text/html"
  }
}
```

### Element Types

Unstructured defines a rich taxonomy of element types that capture the semantic role of each piece of content[^7]:

| Element Type | Description |
|---|---|
| `Title` | Text element for capturing headings and titles[^7] |
| `NarrativeText` | Multiple well-formulated sentences; excludes headers, footers, captions[^7] |
| `ListItem` | A `NarrativeText` element that is part of a list[^7] |
| `Table` | Captured with raw text and optional HTML representation in metadata[^7] |
| `Image` | Image metadata and optionally Base64-encoded image data[^7] |
| `Header` / `Footer` | Document headers and footers[^7] |
| `FigureCaption` | Text associated with figure captions[^7] |
| `Formula` | Mathematical formulas in the document[^7] |
| `Address` / `EmailAddress` | Physical and email addresses[^7] |
| `CodeSnippet` | Code blocks within documents[^7] |
| `PageBreak` / `PageNumber` | Page structure markers[^7] |
| `UncategorizedText` | Free text not matching other categories[^7] |
| `CompositeElement` | Produced only by chunking; combines sequential elements into a single chunk[^7] |

This typed element system is powerful because it lets you filter and route content based on its semantic role. For instance, if you're building a summarization pipeline, you might only process `NarrativeText` elements while ignoring `Header`, `Footer`, and `PageNumber` elements[^7]. Each element also carries a `parent_id` that establishes hierarchy—a `NarrativeText` element might have a `Title` as its parent, enabling reconstruction of the document's outline[^7].

### Chunking Strategies

After partitioning, Unstructured can apply **chunking** to rearrange elements into appropriately sized passages for embedding models and retrieval systems[^19][^21]. The pipeline supports three modes via command-line arguments[^1]:

**No chunking** (default): Elements are output as-is from partitioning. Each element becomes its own unit. This is useful when you want maximum granularity.

**Basic chunking** (`--basic`): A simple size-based strategy that fills each chunk with whole elements up to a maximum character limit. When adding the next element would exceed `--max-chunk-size`, the current chunk is closed and a new one begins[^21].

**By-title chunking** (`--by-title`): A semantic strategy that preserves section boundaries. When a `Title` element is encountered, the current chunk is closed and a new section begins, even if there is room remaining in the current chunk[^19][^21]. This ensures that chunks respect the document's topical structure—content from two different sections never bleeds into a single chunk. The `--max-chunk-overlap` parameter enables a sliding window where trailing characters from one chunk are prepended to the next, providing context continuity for retrieval[^19].

Both strategies respect the `--max-chunk-size` hard limit. When chunking is applied, individual elements are combined into `CompositeElement` objects that preserve references to their original constituent elements via the `orig_elements` metadata field[^7].

## Benefits of Containerization

Both pipelines are packaged as Docker containers, and this is not merely a convenience—it addresses fundamental challenges in document processing[^1].

### System-Level Dependencies Beyond pip

Document processing libraries depend on native system packages that cannot be installed via `pip` alone[^1]:

- **Tesseract OCR** (`tesseract-ocr`, `libtesseract-dev`): The C++ engine that pytesseract calls. Must be installed via the system package manager (`apt install tesseract-ocr` on Debian/Ubuntu)[^20][^27]. Without it, any OCR call will fail with "tesseract is not installed or it's not in your path"[^22].
- **Tesseract language packs** (`tesseract-ocr-eng`, `tesseract-ocr-fra`, etc.): Additional packages for each supported language[^20]
- **Leptonica** (`libleptonica-dev`): Image processing library required by Tesseract[^18]
- **Poppler** or **MuPDF system libraries**: Low-level PDF rendering engines that some Python packages depend on
- **LibreOffice** or system font packages: Required for accurate rendering of Office documents
- **OpenCV system dependencies** (`libgl1-mesa-glx`, `libsm6`, `libxext6`): Required if image preprocessing is applied before OCR[^27]

The Unstructured pipeline adds even more dependencies. Its `unstructured[all-docs]` package bundles parsers for dozens of formats, each potentially requiring its own native library. The Unstructured team provides a pre-built Docker image (`downloads.unstructured.io/unstructured-io/unstructured:latest`) that includes all of these[^2].

### Why Docker

The project uses Docker for six specific reasons[^1]:

1. **Dependency Management** — Containers encapsulate all system dependencies (Tesseract, system libraries for PDF processing) in a single, reproducible image, eliminating version conflicts with the host system[^1]
2. **Reproducibility** — A container image guarantees identical behavior across different machines and environments, eliminating "it works on my machine" problems[^1]
3. **Isolation** — Document processing can be CPU- and memory-intensive. Containers allow resource limits to be applied without affecting the host[^1]
4. **Portability** — The same image runs on Windows, macOS, and Linux without modification[^1]
5. **Scalability** — Containerized pipelines integrate naturally with Docker Compose or Kubernetes for batch processing of large document collections[^1]
6. **Security** — Documents often contain sensitive information; containers add an isolation layer and can be run with restricted permissions[^1]

## Running the Pipelines

### Prerequisites

- Docker installed on your system (Docker Desktop for Windows/macOS, or `docker.io` and `docker-compose` packages for Linux)[^1]
- For AI features in `simple-pdf-extraction`: Ollama running locally or accessible via a URL[^1]

### Preparing Your Documents

On all platforms, start by creating the data directories and placing your documents in the input folder[^1]:

```bash
mkdir -p data/input
mkdir -p data/output
# Copy your documents to data/input
```

### Running Simple PDF Extraction

**macOS/Linux:**
```bash
cd simple-pdf-extraction
docker build -t simple-pdf-extraction .
docker run -v $(pwd)/../data:/data simple-pdf-extraction
```

**Windows:**
```cmd
cd simple-pdf-extraction
docker build -t simple-pdf-extraction .
docker run -v %cd%\..\data:/data simple-pdf-extraction
```

Alternatively, use Docker Compose from the `simple-pdf-extraction` directory[^2]:
```bash
docker-compose build
docker-compose run --rm pdf-extractor ./run.sh
```

Or use the convenience scripts from the repository root: `run-simple-pdf-extraction.sh` (Linux/macOS) or `run-simple-pdf-extraction.ps1` (Windows)[^1].

Results are saved in `data/output/simple-pdf-extraction/` as JSON files containing extracted content, metadata, and AI analysis[^1].

### Running Chunking with Unstructured

First, pull the Unstructured base image if needed[^2]:
```bash
# AMD64 (default)
docker pull downloads.unstructured.io/unstructured-io/unstructured:latest
# Apple Silicon / ARM64
docker pull --platform=linux/arm64 downloads.unstructured.io/unstructured-io/unstructured:latest
```

Then build and run[^1]:

```bash
cd simple-chunking-with-unstructured
docker build -t simple-chunking-unstructured .

# No chunking (elements as-is)
docker run -v $(pwd)/../data:/data simple-chunking-unstructured

# By-title chunking
docker run -v $(pwd)/../data:/data simple-chunking-unstructured \
  --by-title --max-chunk-size 1000 --max-chunk-overlap 100

# Basic chunking
docker run -v $(pwd)/../data:/data simple-chunking-unstructured \
  --basic --max-chunk-size 1500
```

Or use the convenience scripts: `run-simple-chunking-with-unstructed.sh` / `.ps1` from the repository root[^1].

Results are saved in `data/output/unstructured-*/` with each element or chunk as a separate JSON file in document-specific subdirectories[^1].

### Chunking Configuration

The Unstructured pipeline accepts these command-line arguments[^1]:

| Argument | Description |
|---|---|
| `--by-title` | Use title-based chunking (groups content under headings)[^1] |
| `--basic` | Use basic size-based chunking[^1] |
| `--max-chunk-size N` | Maximum characters per chunk (default: 1000)[^1] |
| `--max-chunk-overlap N` | Overlap between chunks (default: 0)[^1] |

## Choosing Between the Two Approaches

**Use Simple PDF Extraction when**[^1]:
- You need AI-powered content analysis (summaries, topic extraction, entity recognition)
- You want direct control over the extraction process for each format
- You're working with a smaller number of documents
- You need integration with Ollama for LLM-based analysis

**Use Chunking with Unstructured when**[^1]:
- You're building RAG or retrieval systems that need semantic chunking
- You need uniform handling across many document formats through a single API
- You want to preserve document structure as typed, hierarchical elements
- You're processing large volumes of diverse document types

Both pipelines serve as reference implementations. They can be adapted, extended, or combined—for example, using Unstructured for partitioning and chunking, then feeding chunks through Ollama for AI-enriched metadata[^1].


---

## References

1. [README.md](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/tree/main/DocumentProcessing/document-processing-pipeline#readme) - This project provides two example implementations of document processing pipelines that demonstrate ...

2. [README.md](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/DocumentProcessing/document-processing-pipeline/simple-chunking-with-unstructured/README.md) - Pull docker image first he AMD64 platform is the default. docker pull downloads.unstructured.iounstr...

4. [Partitioning - Unstructured Documentation](https://docs.unstructured.io/open-source/core-functionality/partitioning) - Partitioning functions in unstructured allow users to extract structured content from a raw unstruct...

5. [Structured LLM Output Using Ollama - Towards Data Science](https://towardsdatascience.com/structured-llm-output-using-ollama-73422889c7ad/) - By introducing structured outputs, Ollama now makes it possible to constrain a model's output to a s...

6. [python 3.x - i am building code to extact text from image if the pdf ...](https://stackoverflow.com/questions/78093872/i-am-building-code-to-extact-text-from-image-if-the-pdf-has-images-inside-it-py) - If you PyMuPDF, you do not need pytesseract, because there is a native Tesseract-OCR built into PyMu...

7. [Document elements and metadata - Unstructured](https://docs.unstructured.io/open-source/concepts/document-elements) - When you partition a document with Unstructured, the result is a list of document Element objects. T...

8. [Structured outputs · Ollama Blog](https://ollama.com/blog/structured-outputs) - Ollama now supports structured outputs making it possible to constrain a model's output to a specifi...

9. [Advanced PyMuPDF Text Extraction Techniques | Full Tutorial](https://www.youtube.com/watch?v=DSsqzKA_hPg) - learnpython #programming #pdfautomation Learn how to extract and structure text from PDF documents u...

14. [Structured Outputs - Ollama's documentation](https://docs.ollama.com/capabilities/structured-outputs) - Structured outputs let you enforce a JSON schema on model responses so you can reliably extract stru...

15. [How to extract text from a PDF using PyMuPDF and Python](https://www.nutrient.io/blog/extract-text-from-pdf-pymupdf/) - PyMuPDF is fast for basic PDF text extraction, while Nutrient DWS Processor API handles complex docu...

18. [PyMuPDF with tesseract OCR as External Content Extraction Engine](https://github.com/open-webui/open-webui/discussions/17621) - Example of External Content Extraction Engine. PyMuPDF with tesseract OCR as External Content Extrac...

19. [Chunking - Unstructured Documentation](https://docs.unstructured.io/ui/chunking) - Chunking rearranges the resulting document elements into manageable “chunks” to stay within the limi...

20. [From Image to Text in Seconds — Tesseract OCR in a Docker ...](https://dev.to/moni121189/from-image-to-text-in-seconds-tesseract-ocr-in-a-docker-container-1ohi) - In this tutorial, we'll containerize Tesseract so you can run OCR anywhere — no OS dependencies, no ...

21. [Chunking - Unstructured Documentation](https://docs.unstructured.io/open-source/core-functionality/chunking) - The by_title chunking strategy preserves section boundaries and optionally page boundaries as well. ...

22. [Pytesseract in a docker container cannot find Tesseract OCR - Reddit](https://www.reddit.com/r/docker/comments/bbyx1f/pytesseract_in_a_docker_container_cannot_find/) - I am working on OCR related project where I need to use pytesseract to do some OCR. The project is c...

27. [How do I add tesseract to my Docker container so i can use ...](https://stackoverflow.com/questions/73318168/how-do-i-add-tesseract-to-my-docker-container-so-i-can-use-pytesseract) - I am working on a project that requires me to run pytesseract on a docker container, but am unable t...


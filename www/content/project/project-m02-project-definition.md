+++
title = 'M02 Data Pipeline, CI/CD setup'
description = 'Establish a foundational data pipeline by ingesting a subset of the corpus, extracting and structuring text data, and initially storing it to a database, while continuously refining the systems architecture.'
weight = 20
submission = 'Monday Feb 22, 2026, Wednesday Feb 17, 2026'
percent = 15
+++
The goal of milestone M02 is to establish a foundation for the document processing pipeline by implementing basic ingestion, text extraction and chunking, metadata extraction, and vector embedding capabilities. This milestone aims to lay the groundwork for the subsequent development of more advanced features and integrations with other components of the system. By completing this milestone, the team will have successfully ingested a subset of the corpus, extracted relevant metadata and text embeddings, and written this data to a chosen database. This achievement will provide a solid foundation for further development and testing, enabling the team to iterate and refine the pipeline's capabilities as needed.

<!-- 
- Basic ingestion of PDFs/text (subset of corpus).
- Text extraction, chunking, basic metadata extraction.
- Vector embedding of text chunks.
- First data (metadata and vector embeddings) written to database (PostgreSQL, QDrant, Neo4j, or OpenSearch).
- Updated architecture diagram. -->

<!-- 

**Milestone:** Building a Document Processing Pipeline
**Deliverables:**

1. Basic ingestion of PDFs/text (subset of corpus)
2. Text extraction, chunking, basic metadata extraction
3. Vector embedding of text chunks
4. First data (metadata and vector embeddings) written to database (PostgreSQL, QDrant, Neo4j, or OpenSearch)
5. Updated architecture diagram -->

**Requirements:**

The pipeline should be able to read PDFs and text files from a specified input directory, extract relevant metadata, tokenize the extracted text into individual words or phrases, remove stop words, punctuation, and special characters, generate vector embeddings for each text chunk, and write the extracted data to a chosen database.

To accomplish this, the following components should be developed:

1. **Ingestion Module**: This module will read PDFs and text files from the input directory and extract relevant metadata.
2. **Text Extraction and Chunking Module**: This module will use a library like Tesseract-OCR, PDFMiner, or PyPDF2 to extract text from PDFs and tokenize it into individual words or phrases.
3. **Metadata Extraction Module**: This module will identify and extract relevant metadata from the documents, such as author, title, date created, and keywords.
4. **Vector Embedding Module**: This module will use a library like Gensim or spaCy to generate vector embeddings for each text chunk.
5. **Database Integration Module**: This module will choose one of the four supported databases (PostgreSQL, QDrant, Neo4j, or OpenSearch) and set it up for data storage.

**Acceptance Criteria:**

To ensure that the document processing pipeline is functioning correctly, the following criteria must be met:

1. The pipeline can read PDFs and text files from the input directory without errors.
2. Relevant metadata is extracted and stored correctly for at least 90% of documents.
3. Text extraction from PDFs works correctly (for 80% of documents).
4. Tokenization, stop word removal, and punctuation/special character removal work as expected.
5. Vector embeddings are generated successfully for each text chunk.
6. The chosen database is set up and functioning correctly.
7. Extracted data (metadata and vector embeddings) is written to the database without errors.

The architecture diagram should show the following components:

1. Input Directory
2. Ingestion Module
3. Text Extraction and Chunking Module
4. Metadata Extraction Module
5. Vector Embedding Module
6. Database Integration Module (with the chosen database)
7. Output Storage

The diagram should also illustrate the flow of data between these components, starting from the input directory and ending with the output storage in the database. This will provide a clear visual representation of how the document processing pipeline is structured and how data moves through it.

**Example Code:**

Use these code examples to build your solution. You are free to include any other framework, as long as it is freely available without licencing restrictions, and can be deployed in a containerized environment on premises. You may use APIs for cloudbased LLMs during development, but your solution needs be able to connect to an on-premises Ollama server.

- [Document Processing Pipeline using Python](../../blog/document-processing/)
- [Document Processing Pipeline using n8n](../../blog/ai-papers-workflow/)
- Examples of Vector Embedding of Text (forthcoming)
- How to Store and Retrieve Vectors in Databases (forthcoming)


**Containerization:**

Follow the examples to ensure every component of your solution is conainerized. Review [Topic 04 - Solution Deployment](../../topics/topic-04/).

**Evaluation:**
- Code is well-structured, modular, and follows best practices for readability and maintainability.
- The pipeline successfully ingests a subset of the corpus, extracts relevant metadata and text embeddings,
and writes this data to the chosen database without errors.
- The architecture diagram is clear, comprehensive, and accurately reflects the components and data flow of the
pipeline.
- Documentation (`README.md` file) includes clear instructions on how to deploy and run the solution.

**Submission:**
- Submit your code to the GitLab repository that is assigned to your team. (Only this repository will be considerd.)
- Due dates are posted on top of this page and in the Milestones Schedule.
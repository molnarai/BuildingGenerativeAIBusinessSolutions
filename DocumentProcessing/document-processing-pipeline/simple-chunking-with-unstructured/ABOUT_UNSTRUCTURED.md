# Unstructured

<https://docs.unstructured.io/welcome>

The unstructured Python library is an open source toolkit for transforming raw documents into structured representations suitable for downstream machine learning and information retrieval workflows. It focuses on partitioning heterogeneous document formats into typed elements, cleaning and normalizing those elements, extracting entities and fields, and optionally chunking them into segments that work well for retrieval-augmented generation (RAG) and similar applications.

## Partitioning into elements

At the core of the library is a partitioning API that takes an input document (for example, PDF, HTML, Word, or plain text) and returns a sequence of element objects, each describing a semantically meaningful region of content. These element classes distinguish between different roles in the document structure, such as narrative text, headings, tables, lists, and other layout-driven components, which allows downstream systems to treat them differently when indexing or generating responses.

The partitioning step abstracts over file formats so that the same logical element types are produced regardless of whether the content came from a PDF, web page, or office document. This normalization is critical for pipelines that must handle diverse sources while applying uniform logic for search, ranking, or summarization.

## Element classes

Each element in the partitioned output is an instance of a specific element class that encodes both the text and structural metadata. Common element kinds include classes for narrative or body text, title or heading text, list items, and table cells or full tables, among others, depending on the document type and partitioner used.

Element objects typically carry attributes such as their textual content, their position in the document, and other modality-specific metadata that can be used to reconstruct context or apply filters. Because the library standardizes these element classes across input formats, it becomes straightforward to apply the same cleaning, extraction, and chunking logic to all documents in a corpus.

## Chunking overview

Beyond partitioning, the library provides chunking utilities that group one or more elements into larger text blocks optimized for tasks like retrieval and large language model prompting. Chunking is applied after partitioning and uses the element boundaries and metadata to decide where to split and how much context to keep within each chunk.

The chunking APIs typically produce sequences of chunk objects that contain combined text from multiple elements plus associated metadata such as source identifiers and ordering. This makes it easy to store chunks in a vector database or search index while preserving linkage back to the original document structure.

## Main chunking methods

The first major chunking method focuses on size-based segmentation, where elements are concatenated until a configured token or character limit is reached, then a new chunk is started. This method respects element boundaries so that headings and their associated paragraphs tend to remain together, which is important for maintaining local context in retrieval workflows.

The second common method uses structure-aware rules, grouping elements according to their hierarchical relationships—such as attaching paragraphs to the nearest preceding heading or grouping list items under a common list title. This approach preserves document semantics by ensuring that each chunk corresponds to a coherent section rather than an arbitrary slice of text, which can improve relevance and answer quality in RAG systems.

## Cleaning and extraction functions

In addition to partitioning and chunking, the library offers a set of cleaning functions that operate on element content to remove or normalize unwanted text. Typical cleaning operations include stripping boilerplate, removing extra whitespace, normalizing punctuation, or filtering out navigation, headers, and footers that would otherwise pollute retrieval or summarization results.

The library also provides extraction functions aimed at pulling structured information out of the element set. These functions can be used to identify or extract entities, fields, or specific patterns from the partitioned elements so that downstream systems can work with structured data rather than raw text.

## Dependencies and deployment

The open source Python package relies on a collection of other open source projects to support parsing, conversion, and analysis across different document types and formats. Because these dependencies can require system-level libraries, native extensions, and external tools, configuring a complete environment from scratch can be nontrivial.

For that reason, it is often easiest to adopt a preconfigured container image that already includes the unstructured package and its dependencies. Using such an image simplifies installation, improves reproducibility across environments, and provides a stable base for building document processing and RAG pipelines that rely on the library’s partitioning, cleaning, extraction, and chunking capabilities.
#!/usr/bin/env python
TITLE = r"""
  _   _           _                   _                      _ 
 | | | |_ __  ___| |_ _ __ _   _  ___| |_ _   _ _ __ ___  __| |
 | | | | '_ \/ __| __| '__| | | |/ __| __| | | | '__/ _ \/ _` |
 | |_| | | | \__ \ |_| |  | |_| | (__| |_| |_| | | |  __/ (_| |
  \___/|_| |_|___/\__|_|   \__,_|\___|\__|\__,_|_|  \___|\__,_|
                                                               
Main entry point for the document processing pipeline.
Processes all documents in /data/input and saves results to /data/output.
"""

import os
import sys
print(f"Python version: {sys.version}")
print(f"Python path: {', '.join(sys.path)}")
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from tqdm import tqdm

from unstructured.partition.auto import partition
from unstructured.partition.image import partition_image
from unstructured.cleaners.core import replace_unicode_quotes


# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_input_files(input_dir: Path) -> List[Path]:
    """Get all supported document files from input directory."""
    supported_extensions = {'.pdf', '.docx', '.pptx', '.txt', '.jpg', '.jpeg', '.png', '.tiff'}
    files = []

    for file_path in input_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files.append(file_path)

    return sorted(files)


def program_slug(chunking_strategy: str, max_chunk_size: int, max_chunk_overlap: int) -> str:
    """Generate a slug for the program based on the parameters."""
    slug = "unstructured-elements" if chunking_strategy == "no-chunking" \
        else f"unstructured-chunking-{chunking_strategy}-size{max_chunk_size}-overlap{max_chunk_overlap}"
    return slug.replace("_", "-").lower()


def main(chunking_strategy: str, max_chunk_size: int, max_chunk_overlap: int):

    logger.info("Chunking strategy: %s", chunking_strategy)
    logger.info("Max chunk size: %s", max_chunk_size)
    logger.info("Max chunk overlap: %s", max_chunk_overlap)

    input_dir = Path('/data/input')
    output_dir = Path('/data/output', program_slug(chunking_strategy, max_chunk_size, max_chunk_overlap))

    # Ensure directories exist
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get input files
    files = get_input_files(input_dir)

    if not files:
        logger.info(f"No supported document files found in {input_dir}")
        return

    logger.info(f"Found {len(files)} documents to process")

    # Process each file
    for file_path in tqdm(files, desc="Processing documents"):
        try:
            logger.info(f"Processing: {file_path.name}")
            elements = []
            # Extract content
            if file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.tiff'}:
                elements = partition_image(file_path)
                logger.info(f"Using image partitioning produced {len(elements)} elements for: {file_path.name}")

            elif file_path.suffix.lower() in {'.pdf'}:
                if chunking_strategy in {"by_title", "basic"}:
                    elements = partition(
                        file_path,
                        content_type="application/pdf",
                        chunking_strategy=chunking_strategy,
                        max_chunk_overlap=max_chunk_overlap,
                        max_chunk_size=max_chunk_size,
                    )
                    logger.info(f"Using PDF partitioning produced {len(elements)} chunks for: {file_path.name}")
                else:
                    elements = partition(file_path, content_type="application/pdf")
                    logger.info(f"Using auto partitioning produced {len(elements)} elements for: {file_path.name}")
            
            else:
                if chunking_strategy in {"by_title", "basic"}:
                    elements = partition(
                        file_path,
                        chunking_strategy=chunking_strategy,
                        max_chunk_overlap=max_chunk_overlap,
                        max_chunk_size=max_chunk_size,
                    )
                    logger.info(f"Using PDF partitioning produced {len(elements)} chunks for: {file_path.name}")
                else:
                    elements = partition(file_path)
                    logger.info(f"Using auto partitioning produced {len(elements)} elements for: {file_path.name}")


            # Clean extracted text
            for element in elements:
                if hasattr(element, 'text') and element.text:
                    element.text = replace_unicode_quotes(element.text)

            doc_dir = output_dir / file_path.stem
            doc_dir.mkdir(parents=True, exist_ok=True)

            for j, element in enumerate(elements):
                logger.debug(f"Element type: {type(element)}")
                with open(doc_dir / f"{j:06d}_{element.id}.json", "w", encoding="utf-8") as f:
                    json.dump(element.to_dict(), f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(elements)} elements for {file_path.name} to {doc_dir}")

            # logger.info(f"Saved output to: {output_file.name}")

        except Exception as e:
            logger.error(f"Failed to process {file_path.name}: {str(e)}")
            continue

    # Generate summary report
    
    logger.info("Processing complete!")

if __name__ == '__main__':
    """Main processing function."""
    parser = argparse.ArgumentParser(description="Process documents with chunking options.")
    parser.add_argument(
        "--by-title",
        action="store_true",
        help="Use by_title chunking strategy",
    )
    parser.add_argument(
        "--basic",
        action="store_true",
        help="Use basic chunking strategy",
    )
    parser.add_argument(
        "--max-chunk-size",
        type=int,
        default=1000,
        help="Maximum chunk size",
    )
    parser.add_argument(
        "--max-chunk-overlap",
        type=int,
        default=0,
        help="Maximum chunk overlap",
    )
    args = parser.parse_args()

    chunking_strategy = "by_title" if args.by_title else "basic" if args.basic else "no-chunking"
    max_chunk_size = args.max_chunk_size
    max_chunk_overlap = args.max_chunk_overlap
    main(chunking_strategy, max_chunk_size, max_chunk_overlap)
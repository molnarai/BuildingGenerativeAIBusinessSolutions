#!/usr/bin/env python3
"""
Main entry point for the document processing pipeline.
Processes all documents in /data/input and saves results to /data/output.
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from extractor import DocumentExtractor
from processor import DocumentProcessor
from ollama_lister import OllamaModelLister

def get_input_files(input_dir: Path) -> List[Path]:
    """Get all supported document files from input directory."""
    supported_extensions = {'.pdf', '.docx', '.pptx', '.txt', '.jpg', '.jpeg', '.png', '.tiff'}
    files = []

    for file_path in input_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files.append(file_path)

    return sorted(files)

def program_slug() -> str:
    return "simple-pdf-extraction"
    # """Generate a slug for the program based on the filename."""
    # return os.path.basename(os.path.dirname(__file__)).replace('.py', '').lower().replace('_', '-')

def main():
    """Main processing function."""
    input_dir = Path('/data/input')
    output_dir = Path('/data/output', program_slug())

    # Ensure directories exist
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get input files
    files = get_input_files(input_dir)

    if not files:
        logger.info(f"No supported document files found in {input_dir}")
        return

    logger.info(f"Found {len(files)} documents to process")

    # Test Ollama connectivity and model availability
    ollama_lister = OllamaModelLister()
    ollama_info = ollama_lister.list_models()
    if ollama_info["ollama_configured"]:
        logger.info(f"Ollama Base URL: {ollama_info['base_url']}")
        logger.info(f"Available Models: {ollama_info['models']}")
        if ollama_info["target_model"]:
            if ollama_info["target_model_available"]:
                logger.info(f"Target model '{ollama_info['target_model']}' is available.")
            else:
                logger.warning(f"Target model '{ollama_info['target_model']}' is NOT available.")
        else:
            logger.warning("No target model specified in OLLAMA_MODEL environment variable.")

    # Initialize extractor and processor
    extractor = DocumentExtractor()
    processor = DocumentProcessor()

    # Process each file
    for file_path in tqdm(files, desc="Processing documents"):
        try:
            logger.info(f"Processing: {file_path.name}")

            # Extract content
            extracted_data = extractor.extract_content(file_path)

            # Process with external services if needed
            processed_data = processor.process_content(extracted_data)

            # Save output
            output_file = output_dir / f"{file_path.stem}_processed.json"
            processor.save_results(processed_data, output_file)

            logger.info(f"Saved output to: {output_file.name}")

        except Exception as e:
            logger.error(f"Failed to process {file_path.name}: {str(e)}")
            continue

    # Generate summary report
    processor.generate_summary_report(input_dir, output_dir)
    logger.info("Processing complete!")

if __name__ == '__main__':
    main()
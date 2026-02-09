#!/usr/bin/env python3
"""
Document processing module.
Handles post-processing of extracted content, including external AI processing.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processes extracted document content."""

    def __init__(self):
        self.ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_api_key = os.getenv('OLLAMA_API_KEY')
        self.ollama_generation_model = os.getenv('OLLAMA_GENERATION_MODEL', 'gpt-oss:20b-cloud')
        
        self.use_ollama = bool(self.ollama_base_url)

    def process_content(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process extracted content with optional AI enhancement.

        Args:
            extracted_data: Dictionary containing extracted content

        Returns:
            Processed data with additional metadata
        """
        processed = extracted_data.copy()

        # Add processing metadata
        processed['processed_at'] = datetime.now().isoformat()
        processed['text_length'] = len(extracted_data.get('content', ''))
        processed['word_count'] = len(extracted_data.get('content', '').split())

        # Use Ollama for content analysis if available
        if self.use_ollama and extracted_data.get('content'):
            try:
                ai_analysis = self._analyze_with_ollama(extracted_data['content'])
                processed['ai_analysis'] = ai_analysis
            except Exception as e:
                logger.warning(f"Failed to analyze with Ollama: {str(e)}")
                processed['ai_analysis'] = None
        else:
            processed['ai_analysis'] = None

        # Extract key information
        processed['summary'] = self._generate_summary(extracted_data['content'])
        processed['entities'] = self._extract_entities(extracted_data['content'])
        processed['keywords'] = self._extract_keywords(extracted_data['content'])

        return processed

    def _analyze_with_ollama(self, content: str) -> Dict[str, Any]:
        """
        Send content to Ollama for AI analysis.

        Args:
            content: Text content to analyze

        Returns:
            Analysis results from Ollama
        """
        if not content.strip():
            return {}

        # Truncate content if too long (adjust as needed)
        max_chars = 4000  # Adjust based on model context window
        truncated_content = content[:max_chars]
        if len(content) > max_chars:
            truncated_content += "\n[Content truncated for analysis...]"

        prompt = f"""Analyze the following document content and provide:
1. A brief summary (2-3 sentences)
2. Key topics or themes
3. Document type classification
4. Language detected

Document content:
{truncated_content}

Respond in JSON format and output JSON only:
{{
    "summary": "...",
    "topics": ["topic1", "topic2"],
    "document_type": "...",
    "language": "...",
    "confidence": 0.95
}}"""

        headers = {
            'Content-Type': 'application/json',
        }

        if self.ollama_api_key:
            headers['Authorization'] = f'Bearer {self.ollama_api_key}'

        payload = {
            "model": self.ollama_generation_model,
            "prompt": prompt,
            "format": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "topics": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "document_type": {"type": "string"},
                    "language": {"type": "string"},
                    "confidence": {"type": "number"}
                },
                "required": ["summary", "topics", "document_type", "language", "confidence"]
            },
            "stream": False,
            "options": {
                "temperature": 0.3,
                "max_tokens": 500
            }
        }

        response = requests.post(
            f"{self.ollama_base_url}/api/generate",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            try:
                # Parse JSON response
                raw_response = result.get('response', '{}')
                cleaned_response = self._extract_json(raw_response)
                ai_response = json.loads(cleaned_response)
                return ai_response
            except json.JSONDecodeError:
                logger.error("Failed to parse Ollama response as JSON")
                return {
                    'error': 'Invalid JSON response',
                    'raw_response': result.get('response', '')
                }
        else:
            logger.error(f"Ollama API error: {response.status_code} - {response.text}")
            if response.status_code == 404:
                return {'error': f'API error: 404 (model not found: {self.ollama_generation_model})'}
            return {'error': f'API error: {response.status_code}'}

    def _extract_json(self, raw_response: str) -> str:
        """Extract JSON from plain or fenced responses."""
        if not raw_response:
            return "{}"

        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()

        return cleaned

    def _generate_summary(self, content: str) -> str:
        """Generate a basic summary of the content."""
        if not content:
            return ""

        # Simple summarization - take first and last sentences
        sentences = content.split('.')
        if len(sentences) > 2:
            return f"{sentences[0].strip()}. ... {sentences[-2].strip()}."
        elif len(sentences) == 2:
            return content.strip()
        else:
            # For very short content, return as is
            return content[:200] + ("..." if len(content) > 200 else "")

    def _extract_entities(self, content: str) -> List[str]:
        """Extract potential entities (basic implementation)."""
        if not content:
            return []

        words = content.split()
        entities = []

        # Simple pattern matching for potential entities
        # This is a very basic implementation - consider using NLP libraries for better results
        for word in words:
            # Capitalized words might be entities
            if word and word[0].isupper() and len(word) > 2:
                entities.append(word)

        # Remove duplicates and return
        return list(set(entities))[:20]  # Limit to top 20

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content."""
        if not content:
            return []

        # Simple keyword extraction - common words to filter out
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

        words = content.lower().split()
        word_freq = {}

        for word in words:
            # Clean word and remove punctuation
            clean_word = ''.join(c for c in word if c.isalnum())

            if len(clean_word) > 3 and clean_word not in stop_words:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1

        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:10]]

    def save_results(self, processed_data: Dict[str, Any], output_path: Path):
        """Save processed data to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

    def generate_summary_report(self, input_dir: Path, output_dir: Path):
        """Generate a summary report of all processed documents."""
        report = {
            'processing_date': datetime.now().isoformat(),
            'input_directory': str(input_dir),
            'output_directory': str(output_dir),
            'processed_files': [],
            'total_files': 0,
            'successful_processed': 0,
            'failed_processed': 0,
            'document_types': {},
            'languages': {},
            'average_word_count': 0
        }

        # Collect all processed files
        output_files = list(output_dir.glob('*_processed.json'))
        report['total_files'] = len(output_files)

        word_counts = []

        for output_file in output_files:
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                file_info = {
                    'filename': data.get('file_name', 'unknown'),
                    'mime_type': data.get('mime_type', 'unknown'),
                    'word_count': data.get('word_count', 0),
                    'processed_at': data.get('processed_at'),
                    'extraction_method': data.get('extraction_method', 'unknown')
                }

                report['processed_files'].append(file_info)
                report['successful_processed'] += 1
                word_counts.append(data.get('word_count', 0))

                # Track document types
                doc_type = data.get('mime_type', 'unknown')
                report['document_types'][doc_type] = report['document_types'].get(doc_type, 0) + 1

                # Track languages if AI analysis was done
                if data.get('ai_analysis') and data['ai_analysis'].get('language'):
                    lang = data['ai_analysis']['language']
                    report['languages'][lang] = report['languages'].get(lang, 0) + 1

            except Exception as e:
                logger.error(f"Failed to read processed file {output_file}: {str(e)}")
                report['failed_processed'] += 1

        # Calculate average word count
        if word_counts:
            report['average_word_count'] = sum(word_counts) / len(word_counts)

        # Save the report
        report_path = output_dir / 'processing_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Processing report saved to: {report_path}")
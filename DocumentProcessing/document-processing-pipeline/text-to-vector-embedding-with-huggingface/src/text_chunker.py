from typing import List


class TextChunker:
    """
    A class for splitting text into chunks with configurable size and overlap.
    """

    def __init__(self, chunk_size: int = 200, overlap: int = 50, break_on_sentence: bool = True):
        """
        Initialize the TextChunker.

        Args:
            chunk_size: Maximum size of each chunk in characters
            overlap: Number of characters to overlap between chunks
            break_on_sentence: Whether to attempt breaking at sentence boundaries
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.break_on_sentence = break_on_sentence

    def chunk(self, text: str) -> List[str]:
        """
        Split text into fixed-size chunks with overlap.

        Args:
            text: The input text to chunk

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text) and self.break_on_sentence:
                last_period = chunk.rfind('.')
                if last_period > self.chunk_size // 2:
                    chunk = text[start:start + last_period + 1]
                    start = start + last_period + 1 - self.overlap
                else:
                    start = end - self.overlap
            else:
                start = end

            chunks.append(chunk.strip())

        return [c for c in chunks if c]

"""
Text chunking for RAG pipeline
"""

from typing import List, Dict, Any
import re
from core.config import settings


class TextChunker:
    """Chunks text into semantically meaningful segments"""

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    def chunk_text(
        self,
        text: str,
        document_id: str,
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Chunk text into overlapping segments
        
        Args:
            text: Full text to chunk
            document_id: ID of the source document
            metadata: Additional metadata to attach to chunks
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        if not text or not text.strip():
            return []

        # First, try to split by paragraphs
        paragraphs = self._split_by_paragraphs(text)
        
        chunks = []
        current_chunk = ""
        current_length = 0
        chunk_index = 0

        for para in paragraphs:
            para_length = len(para)
            
            # If paragraph fits in current chunk
            if current_length + para_length <= self.chunk_size:
                current_chunk += para + "\n\n"
                current_length += para_length + 2
            else:
                # Save current chunk if it has content
                if current_chunk.strip():
                    chunks.append(self._create_chunk(
                        current_chunk.strip(),
                        document_id,
                        chunk_index,
                        metadata
                    ))
                    chunk_index += 1
                
                # Start new chunk with overlap
                if self.chunk_overlap > 0 and chunks:
                    # Get last chunk's ending for overlap
                    last_chunk_text = chunks[-1]["text"]
                    overlap_text = last_chunk_text[-self.chunk_overlap:]
                    current_chunk = overlap_text + "\n\n" + para + "\n\n"
                    current_length = len(current_chunk)
                else:
                    current_chunk = para + "\n\n"
                    current_length = para_length + 2

        # Add final chunk
        if current_chunk.strip():
            chunks.append(self._create_chunk(
                current_chunk.strip(),
                document_id,
                chunk_index,
                metadata
            ))

        return chunks

    def _split_by_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        # Split by double newlines or single newline followed by capital letter
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Further split long paragraphs
        result = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if len(para) <= self.chunk_size:
                result.append(para)
            else:
                # Split long paragraphs by sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current = ""
                for sentence in sentences:
                    if len(current) + len(sentence) <= self.chunk_size:
                        current += sentence + " "
                    else:
                        if current:
                            result.append(current.strip())
                        current = sentence + " "
                if current:
                    result.append(current.strip())
        
        return result

    def _create_chunk(
        self,
        text: str,
        document_id: str,
        chunk_index: int,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a chunk dictionary"""
        chunk_id = f"{document_id}_chunk_{chunk_index}"
        
        chunk_data = {
            "chunk_id": chunk_id,
            "document_id": document_id,
            "text": text,
            "chunk_index": chunk_index,
            "char_count": len(text),
            "word_count": len(text.split()),
        }
        
        if metadata:
            chunk_data["metadata"] = metadata
        
        return chunk_data

"""
Complete document processing pipeline
"""

from typing import Dict, Any, List
from core.ingestion.pdf_processor import PDFProcessor
from core.ingestion.chunker import TextChunker
from services.watsonx_ai.client import WatsonxAIClient
from services.watsonx_data.client import WatsonxDataClient


class DocumentProcessor:
    """Complete pipeline for processing documents"""

    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.chunker = TextChunker()
        self.ai_client = WatsonxAIClient()
        self.data_client = WatsonxDataClient()

    def process_document(
        self,
        file_path: str,
        document_id: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process a document: extract, chunk, embed, and store
        
        Args:
            file_path: Path to PDF file
            document_id: Unique document identifier
            metadata: Additional document metadata
            
        Returns:
            Processing result with chunk count and status
        """
        try:
            # Step 1: Extract text from PDF
            extracted = self.pdf_processor.extract_text(file_path)
            
            # Step 2: Chunk text
            chunks = self.chunker.chunk_text(
                text=extracted["text"],
                document_id=document_id,
                metadata={
                    **(metadata or {}),
                    "total_pages": extracted["total_pages"],
                    "extraction_method": extracted.get("extraction_method")
                }
            )
            
            # Step 3: Generate embeddings
            embeddings = []
            for chunk in chunks:
                embedding = self.ai_client.generate_embedding(chunk["text"])
                embeddings.append(embedding)
            
            # Step 4: Store in watsonx.data
            self.data_client.store_chunks(chunks, embeddings)
            
            return {
                "success": True,
                "chunks_count": len(chunks),
                "total_pages": extracted["total_pages"],
                "chunks": chunks
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chunks_count": 0
            }

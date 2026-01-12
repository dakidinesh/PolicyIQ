"""
API routes for document management
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
import os
import uuid
from datetime import datetime

from models.schemas import DocumentResponse, DocumentStatus
from core.ingestion.pdf_processor import PDFProcessor
from core.ingestion.chunker import TextChunker
from services.watsonx_ai.client import WatsonxAIClient
from services.watsonx_data.client import WatsonxDataClient
from core.governance.audit_logger import AuditLogger

router = APIRouter()

# In-memory storage for documents (in production, use database)
documents_store = {}
processor = PDFProcessor()
chunker = TextChunker()

# Initialize clients (may fail if credentials not set, that's OK for now)
try:
    ai_client = WatsonxAIClient()
except Exception:
    ai_client = None

try:
    data_client = WatsonxDataClient()
except Exception:
    data_client = None

audit_logger = AuditLogger()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    document_type: str = None
):
    """
    Upload and process a PDF document
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate document ID
    doc_id = str(uuid.uuid4())
    
    # Save file temporarily
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{doc_id}.pdf")
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Create document record
    document = {
        "id": doc_id,
        "filename": file.filename,
        "document_type": document_type,
        "status": DocumentStatus.PENDING,
        "chunks_count": 0,
        "uploaded_at": datetime.now(),
        "processed_at": None,
        "metadata": {}
    }
    documents_store[doc_id] = document
    
    # Process document in background
    background_tasks.add_task(process_document, doc_id, file_path)
    
    return DocumentResponse(**document)


async def process_document(doc_id: str, file_path: str):
    """Process document: extract, chunk, embed, and store"""
    try:
        # Update status
        documents_store[doc_id]["status"] = DocumentStatus.PROCESSING
        
        # Extract text from PDF
        extracted = processor.extract_text(file_path)
        
        # Chunk text
        chunks = chunker.chunk_text(
            text=extracted["text"],
            document_id=doc_id,
            metadata={
                "filename": documents_store[doc_id]["filename"],
                "total_pages": extracted["total_pages"],
                "document_type": documents_store[doc_id].get("document_type")
            }
        )
        
        # Generate embeddings
        embeddings = []
        if ai_client:
            for chunk in chunks:
                try:
                    embedding = ai_client.generate_embedding(chunk["text"])
                    embeddings.append(embedding)
                except Exception as e:
                    # If embedding fails, use dummy embedding
                    embeddings.append([0.0] * 768)
        else:
            # No AI client, use dummy embeddings
            embeddings = [[0.0] * 768] * len(chunks)
        
        # Store in watsonx.data
        if data_client:
            try:
                data_client.store_chunks(chunks, embeddings)
            except Exception as e:
                # Log error but continue
                documents_store[doc_id]["metadata"]["storage_error"] = str(e)
        
        # Update document record
        documents_store[doc_id]["status"] = DocumentStatus.COMPLETED
        documents_store[doc_id]["chunks_count"] = len(chunks)
        documents_store[doc_id]["processed_at"] = datetime.now()
        
        # Clean up temp file
        os.remove(file_path)
        
    except Exception as e:
        documents_store[doc_id]["status"] = DocumentStatus.FAILED
        documents_store[doc_id]["metadata"]["error"] = str(e)


@router.get("/", response_model=List[DocumentResponse])
async def list_documents():
    """List all uploaded documents"""
    return [DocumentResponse(**doc) for doc in documents_store.values()]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Get a specific document"""
    if document_id not in documents_store:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return DocumentResponse(**documents_store[document_id])


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its chunks"""
    if document_id not in documents_store:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete from watsonx.data
    data_client.delete_document(document_id)
    
    # Remove from store
    del documents_store[document_id]
    
    return {"message": "Document deleted successfully"}

"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentUpload(BaseModel):
    """Document upload request"""
    filename: str
    document_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    """Document response"""
    id: str
    filename: str
    document_type: Optional[str] = None
    status: DocumentStatus
    chunks_count: int = 0
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class Citation(BaseModel):
    """Citation for an answer"""
    document_id: str
    document_name: str
    section: Optional[str] = None
    page_number: Optional[int] = None
    chunk_id: str
    relevance_score: float
    excerpt: str


class QuestionRequest(BaseModel):
    """Question request"""
    question: str = Field(..., min_length=1, max_length=1000)
    context: Optional[Dict[str, Any]] = None


class AnswerResponse(BaseModel):
    """Answer response"""
    answer: str
    explanation: str
    citations: List[Citation]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    manual_review_recommended: bool = False
    reasoning_steps: Optional[List[str]] = None


class AuditLogEntry(BaseModel):
    """Audit log entry"""
    id: str
    timestamp: datetime
    question: str
    answer: str
    citations: List[Citation]
    confidence_score: float
    user_id: Optional[str] = None
    llm_prompt: Optional[str] = None
    llm_response: Optional[str] = None
    retrieved_sources: List[Dict[str, Any]]
    document_versions: Dict[str, str]


class AuditLogQuery(BaseModel):
    """Audit log query"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_confidence: Optional[float] = None
    document_id: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

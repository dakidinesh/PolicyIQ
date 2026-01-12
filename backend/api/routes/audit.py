"""
API routes for audit logs
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from models.schemas import AuditLogEntry, AuditLogQuery
from core.governance.audit_logger import AuditLogger

router = APIRouter()

audit_logger = AuditLogger()


@router.get("/logs", response_model=List[AuditLogEntry])
async def get_audit_logs(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_confidence: Optional[float] = None,
    document_id: Optional[str] = None,
    limit: int = 100
):
    """
    Retrieve audit logs with optional filters
    """
    try:
        logs = audit_logger.get_logs(
            start_date=start_date,
            end_date=end_date,
            min_confidence=min_confidence,
            document_id=document_id,
            limit=limit
        )
        
        return [AuditLogEntry(**log) for log in logs]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving logs: {str(e)}")


@router.get("/logs/{log_id}", response_model=AuditLogEntry)
async def get_audit_log(log_id: str):
    """
    Get a specific audit log entry
    """
    log = audit_logger.get_log_by_id(log_id)
    
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    
    return AuditLogEntry(**log)

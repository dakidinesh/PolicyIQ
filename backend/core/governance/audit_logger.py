"""
Audit logging for governance and compliance
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import sqlite3
from pathlib import Path
from core.config import settings


class AuditLogger:
    """Logs all interactions for audit and governance"""

    def __init__(self, db_path: str = "audit_logs.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for audit logs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                citations TEXT,
                confidence_score REAL,
                user_id TEXT,
                llm_prompt TEXT,
                llm_response TEXT,
                retrieved_sources TEXT,
                document_versions TEXT,
                reasoning_steps TEXT,
                manual_review_recommended INTEGER
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON audit_logs(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_confidence 
            ON audit_logs(confidence_score)
        """)
        
        conn.commit()
        conn.close()

    def log_interaction(
        self,
        question: str,
        answer: str,
        citations: List[Dict[str, Any]],
        confidence_score: float,
        llm_prompt: Optional[str] = None,
        llm_response: Optional[str] = None,
        retrieved_sources: Optional[List[Dict[str, Any]]] = None,
        document_versions: Optional[Dict[str, str]] = None,
        reasoning_steps: Optional[List[str]] = None,
        manual_review_recommended: bool = False,
        user_id: Optional[str] = None
    ) -> str:
        """
        Log an interaction
        
        Args:
            question: User question
            answer: Generated answer
            citations: List of citations
            confidence_score: Confidence score
            llm_prompt: LLM prompt used
            llm_response: LLM response
            retrieved_sources: Retrieved document chunks
            document_versions: Document version mapping
            reasoning_steps: Steps in reasoning process
            manual_review_recommended: Whether manual review is needed
            user_id: Optional user identifier
            
        Returns:
            Log entry ID
        """
        import uuid
        log_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_logs (
                id, timestamp, question, answer, citations,
                confidence_score, user_id, llm_prompt, llm_response,
                retrieved_sources, document_versions, reasoning_steps,
                manual_review_recommended
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            log_id,
            timestamp,
            question,
            answer,
            json.dumps(citations),
            confidence_score,
            user_id,
            llm_prompt,
            llm_response,
            json.dumps(retrieved_sources or []),
            json.dumps(document_versions or {}),
            json.dumps(reasoning_steps or []),
            1 if manual_review_recommended else 0
        ))
        
        conn.commit()
        conn.close()
        
        return log_id

    def get_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_confidence: Optional[float] = None,
        document_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Retrieve audit logs with filters
        
        Args:
            start_date: Start date filter
            end_date: End date filter
            min_confidence: Minimum confidence score
            document_id: Filter by document ID
            limit: Maximum number of results
            
        Returns:
            List of audit log entries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM audit_logs WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        
        if min_confidence is not None:
            query += " AND confidence_score >= ?"
            params.append(min_confidence)
        
        if document_id:
            query += " AND retrieved_sources LIKE ?"
            params.append(f"%{document_id}%")
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        logs = []
        for row in rows:
            log = dict(row)
            # Parse JSON fields
            log["citations"] = json.loads(log.get("citations", "[]"))
            log["retrieved_sources"] = json.loads(log.get("retrieved_sources", "[]"))
            log["document_versions"] = json.loads(log.get("document_versions", "{}"))
            log["reasoning_steps"] = json.loads(log.get("reasoning_steps", "[]"))
            log["manual_review_recommended"] = bool(log.get("manual_review_recommended", 0))
            logs.append(log)
        
        conn.close()
        return logs

    def get_log_by_id(self, log_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific log entry by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM audit_logs WHERE id = ?", (log_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            log = dict(row)
            # Parse JSON fields
            log["citations"] = json.loads(log.get("citations", "[]"))
            log["retrieved_sources"] = json.loads(log.get("retrieved_sources", "[]"))
            log["document_versions"] = json.loads(log.get("document_versions", "{}"))
            log["reasoning_steps"] = json.loads(log.get("reasoning_steps", "[]"))
            log["manual_review_recommended"] = bool(log.get("manual_review_recommended", 0))
            return log
        
        return None

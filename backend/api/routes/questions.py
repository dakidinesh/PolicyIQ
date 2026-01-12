"""
API routes for question answering
"""

from fastapi import APIRouter, HTTPException
from models.schemas import QuestionRequest, AnswerResponse
from core.agent.reasoning_loop import ReasoningLoop
from core.governance.audit_logger import AuditLogger

router = APIRouter()

# Initialize reasoning loop (may fail if clients not configured)
try:
    reasoning_loop = ReasoningLoop()
except Exception as e:
    reasoning_loop = None
    import warnings
    warnings.warn(f"Failed to initialize ReasoningLoop: {str(e)}")

audit_logger = AuditLogger()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an answer with citations
    """
    if not reasoning_loop:
        raise HTTPException(
            status_code=503,
            detail="Reasoning loop not initialized. Please check watsonx.ai and watsonx.data configuration."
        )
    
    try:
        # Process question through reasoning loop
        result = await reasoning_loop.process_question(
            question=request.question,
            context=request.context
        )
        
        # Log interaction for audit
        log_id = audit_logger.log_interaction(
            question=request.question,
            answer=result["answer"],
            citations=result["citations"],
            confidence_score=result["confidence_score"],
            llm_prompt=result.get("llm_prompt"),
            llm_response=result.get("llm_response"),
            retrieved_sources=result.get("retrieved_sources", []),
            document_versions=result.get("document_versions", {}),
            reasoning_steps=result.get("reasoning_steps", []),
            manual_review_recommended=result["manual_review_recommended"]
        )
        
        # Format response
        return AnswerResponse(
            answer=result["answer"],
            explanation=result["explanation"],
            citations=result["citations"],
            confidence_score=result["confidence_score"],
            manual_review_recommended=result["manual_review_recommended"],
            reasoning_steps=result.get("reasoning_steps")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

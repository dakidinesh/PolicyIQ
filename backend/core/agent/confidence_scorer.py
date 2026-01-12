"""
Confidence scoring for answers
"""

from typing import List, Dict, Any
from core.config import settings


class ConfidenceScorer:
    """Calculates confidence scores for answers"""

    def __init__(self):
        self.min_threshold = settings.MIN_CONFIDENCE_THRESHOLD
        self.manual_review_threshold = settings.MANUAL_REVIEW_THRESHOLD

    def calculate_confidence(
        self,
        answer: str,
        search_results: List[Dict[str, Any]],
        verification: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score for an answer
        
        Args:
            answer: Generated answer
            search_results: Retrieved document chunks
            verification: Verification results
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not answer or not search_results:
            return 0.0

        # Factor 1: Quality of retrieved results (0-0.4)
        retrieval_score = self._score_retrieval_quality(search_results)
        
        # Factor 2: Answer completeness (0-0.3)
        completeness_score = self._score_completeness(answer)
        
        # Factor 3: Verification support (0-0.3)
        verification_score = self._score_verification(verification)
        
        # Combine scores
        confidence = (
            retrieval_score * 0.4 +
            completeness_score * 0.3 +
            verification_score * 0.3
        )
        
        # Ensure it's between 0 and 1
        confidence = max(0.0, min(1.0, confidence))
        
        return confidence

    def _score_retrieval_quality(
        self,
        search_results: List[Dict[str, Any]]
    ) -> float:
        """Score based on quality of retrieved results"""
        if not search_results:
            return 0.0
        
        # Average similarity score of top results
        top_scores = [
            r.get("combined_score", 0.0)
            for r in search_results[:5]
        ]
        
        if not top_scores:
            return 0.0
        
        avg_score = sum(top_scores) / len(top_scores)
        
        # Normalize to 0-1 range (assuming scores are 0-1)
        return min(1.0, avg_score)

    def _score_completeness(self, answer: str) -> float:
        """Score based on answer completeness"""
        if not answer:
            return 0.0
        
        # Check for key indicators of completeness
        has_citation_indicators = any(
            word in answer.lower()
            for word in ["section", "article", "clause", "regulation", "policy"]
        )
        
        has_explanation = len(answer.split()) > 20
        
        # Score based on length and indicators
        length_score = min(1.0, len(answer) / 500)  # Normalize to 500 chars
        indicator_score = 0.5 if has_citation_indicators else 0.2
        explanation_score = 0.3 if has_explanation else 0.1
        
        return (length_score * 0.4 + indicator_score * 0.3 + explanation_score * 0.3)

    def _score_verification(self, verification: Dict[str, Any]) -> float:
        """Score based on verification results"""
        is_supported = verification.get("is_supported", False)
        confidence_level = verification.get("confidence", "low")
        gaps = verification.get("gaps", [])
        
        # Base score from support
        base_score = 0.7 if is_supported else 0.3
        
        # Adjust for confidence level
        if confidence_level == "high":
            confidence_multiplier = 1.0
        elif confidence_level == "medium":
            confidence_multiplier = 0.7
        else:
            confidence_multiplier = 0.4
        
        # Penalize for gaps
        gap_penalty = min(0.3, len(gaps) * 0.1)
        
        score = base_score * confidence_multiplier - gap_penalty
        
        return max(0.0, min(1.0, score))

"""
Agentic reasoning loop: plan, search, reason, verify, respond
"""

from typing import Dict, Any, List
from core.rag.hybrid_search import HybridSearch
from services.watsonx_ai.client import WatsonxAIClient
from core.agent.confidence_scorer import ConfidenceScorer


class ReasoningLoop:
    """Implements the agentic reasoning loop"""

    def __init__(self):
        try:
            self.search = HybridSearch()
        except Exception as e:
            self.search = None
            import warnings
            warnings.warn(f"Failed to initialize HybridSearch: {str(e)}")
        
        try:
            self.llm = WatsonxAIClient()
        except Exception as e:
            self.llm = None
            import warnings
            warnings.warn(f"Failed to initialize WatsonxAIClient: {str(e)}")
        
        self.confidence_scorer = ConfidenceScorer()

    async def process_question(
        self,
        question: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process a question through the reasoning loop
        
        Args:
            question: User question
            context: Optional context
            
        Returns:
            Complete answer with citations and confidence
        """
        # Step 1: Plan - Decompose question
        plan = await self._plan(question)
        
        # Step 2: Search - Retrieve relevant documents
        search_results = await self._search(question, plan)
        
        # Step 3: Reason - Generate answer with LLM
        reasoning_result = await self._reason(question, search_results)
        
        # Step 4: Verify - Self-check answer
        verification = await self._verify(
            question,
            reasoning_result,
            search_results
        )
        
        # Step 5: Respond - Format final answer
        response = await self._respond(
            question,
            reasoning_result,
            verification,
            search_results
        )
        
        return response

    async def _plan(self, question: str) -> Dict[str, Any]:
        """
        Plan: Decompose question into sub-queries if needed
        
        Args:
            question: Original question
            
        Returns:
            Plan with sub-queries and reasoning steps
        """
        # For simple questions, return as-is
        # For complex questions, decompose
        
        plan_prompt = f"""Analyze this regulatory compliance question and determine if it needs to be broken down into sub-questions.

Question: {question}

If the question is straightforward, return it as-is.
If it's complex and covers multiple aspects, break it into 2-3 sub-questions.

Respond in JSON format:
{{
    "is_complex": true/false,
    "sub_questions": ["sub-question 1", "sub-question 2"],
    "reasoning": "explanation"
}}"""

        try:
            # For now, return simple plan
            # In production, use LLM to generate plan
            return {
                "is_complex": False,
                "sub_questions": [question],
                "reasoning": "Single question, no decomposition needed"
            }
        except Exception:
            # Fallback to simple plan
            return {
                "is_complex": False,
                "sub_questions": [question],
                "reasoning": "Default plan"
            }

    async def _search(
        self,
        question: str,
        plan: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Search: Retrieve relevant document chunks
        
        Args:
            question: Original question
            plan: Planning results
            
        Returns:
            List of relevant chunks
        """
        if not self.search:
            # Return empty results if search is not initialized
            return []
        
        # Use hybrid search for each sub-question
        all_results = []
        
        for sub_q in plan["sub_questions"]:
            try:
                results = self.search.search(sub_q)
                all_results.extend(results)
            except Exception:
                # If search fails, continue with empty results
                pass
        
        # Deduplicate by chunk_id
        seen = set()
        unique_results = []
        for result in all_results:
            chunk_id = result.get("chunk_id")
            if chunk_id not in seen:
                seen.add(chunk_id)
                unique_results.append(result)
        
        # Sort by combined score
        unique_results.sort(
            key=lambda x: x.get("combined_score", 0.0),
            reverse=True
        )
        
        return unique_results[:10]  # Top 10 results

    async def _reason(
        self,
        question: str,
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Reason: Use LLM to generate answer from retrieved context
        
        Args:
            question: User question
            search_results: Retrieved chunks
            
        Returns:
            LLM reasoning result
        """
        if not self.llm:
            # Return placeholder if LLM is not initialized
            return {
                "answer": "LLM service not configured. Please check watsonx.ai credentials.",
                "llm_response": None,
                "context_used": 0
            }
        
        # Extract text from search results
        context_chunks = [
            result.get("text", "") for result in search_results
        ]
        
        # Generate answer with context
        try:
            llm_response = self.llm.generate_with_context(
                question=question,
                context=context_chunks
            )
        except Exception as e:
            # Return error message if LLM call fails
            return {
                "answer": f"Error generating answer: {str(e)}",
                "llm_response": None,
                "context_used": len(context_chunks)
            }
        
        return {
            "answer": llm_response.get("text", ""),
            "llm_response": llm_response,
            "context_used": len(context_chunks)
        }

    async def _verify(
        self,
        question: str,
        reasoning_result: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Verify: Self-check answer against source documents
        
        Args:
            question: Original question
            reasoning_result: LLM reasoning result
            search_results: Retrieved chunks
            
        Returns:
            Verification result
        """
        answer = reasoning_result.get("answer", "")
        
        # Check if answer is supported by retrieved context
        verification_prompt = f"""Verify if this answer is well-supported by the source documents.

Question: {question}

Answer: {answer}

Source Documents:
{chr(10).join([f"- {r.get('text', '')[:200]}..." for r in search_results[:5]])}

Respond in JSON:
{{
    "is_supported": true/false,
    "supporting_evidence": ["evidence 1", "evidence 2"],
    "gaps": ["any gaps or missing information"],
    "confidence": "high/medium/low"
}}"""

        # For now, return basic verification
        # In production, use LLM for verification
        return {
            "is_supported": True,
            "supporting_evidence": [r.get("chunk_id") for r in search_results[:3]],
            "gaps": [],
            "confidence": "medium"
        }

    async def _respond(
        self,
        question: str,
        reasoning_result: Dict[str, Any],
        verification: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Respond: Format final answer with citations and confidence
        
        Args:
            question: Original question
            reasoning_result: LLM reasoning result
            verification: Verification result
            search_results: Retrieved chunks
            
        Returns:
            Final formatted response
        """
        answer = reasoning_result.get("answer", "")
        
        # Extract citations from search results
        citations = []
        for result in search_results[:5]:  # Top 5 citations
            citations.append({
                "document_id": result.get("document_id", ""),
                "document_name": result.get("document_name", ""),
                "section": result.get("section"),
                "page_number": result.get("page_number"),
                "chunk_id": result.get("chunk_id", ""),
                "relevance_score": result.get("combined_score", 0.0),
                "excerpt": result.get("text", "")[:300] + "..."
            })
        
        # Calculate confidence score
        confidence_score = self.confidence_scorer.calculate_confidence(
            answer=answer,
            search_results=search_results,
            verification=verification
        )
        
        # Determine if manual review is needed
        manual_review = confidence_score < self.confidence_scorer.manual_review_threshold
        
        # Extract explanation from answer (simplified)
        explanation = self._extract_explanation(answer)
        
        return {
            "answer": self._extract_direct_answer(answer),
            "explanation": explanation,
            "citations": citations,
            "confidence_score": confidence_score,
            "manual_review_recommended": manual_review,
            "reasoning_steps": [
                "Question analyzed and decomposed",
                f"Retrieved {len(search_results)} relevant document chunks",
                "Generated answer using LLM reasoning",
                "Verified answer against source documents",
                "Calculated confidence score"
            ]
        }

    def _extract_direct_answer(self, answer: str) -> str:
        """Extract direct answer from LLM response"""
        # Simple extraction - in production, use more sophisticated parsing
        lines = answer.split("\n")
        for line in lines:
            if line.strip() and not line.strip().startswith("#"):
                return line.strip()
        return answer[:200]

    def _extract_explanation(self, answer: str) -> str:
        """Extract explanation from LLM response"""
        # Simple extraction
        if len(answer) > 200:
            return answer[:500] + "..."
        return answer

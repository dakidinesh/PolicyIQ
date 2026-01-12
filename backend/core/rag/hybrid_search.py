"""
Hybrid search combining vector and keyword search
"""

from typing import List, Dict, Any
from services.watsonx_data.client import WatsonxDataClient
from services.watsonx_ai.client import WatsonxAIClient
from core.config import settings


class HybridSearch:
    """Hybrid search combining vector similarity and keyword matching"""

    def __init__(self):
        try:
            self.data_client = WatsonxDataClient()
        except Exception:
            self.data_client = None
            import warnings
            warnings.warn("WatsonxDataClient not initialized. Search will return empty results.")
        
        try:
            self.ai_client = WatsonxAIClient()
        except Exception:
            self.ai_client = None
            import warnings
            warnings.warn("WatsonxAIClient not initialized. Embeddings will use fallback.")
        
        self.keyword_weight = settings.KEYWORD_WEIGHT
        self.vector_weight = settings.VECTOR_WEIGHT
        self.max_results = settings.MAX_RETRIEVAL_RESULTS
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD

    def search(
        self,
        query: str,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining vector and keyword results
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with combined scores
        """
        top_k = top_k or self.max_results

        # If clients are not initialized, return empty results
        if not self.data_client or not self.ai_client:
            return []

        # Generate query embedding
        try:
            query_embedding = self.ai_client.generate_embedding(query)
        except Exception:
            # If embedding fails, return empty results
            return []

        # Perform vector search
        try:
            vector_results = self.data_client.vector_search(
                query_embedding=query_embedding,
                top_k=top_k * 2,  # Get more results for reranking
                threshold=self.similarity_threshold
            )
        except Exception:
            vector_results = []

        # Perform keyword search
        try:
            keyword_results = self.data_client.keyword_search(
                query=query,
                top_k=top_k * 2
            )
        except Exception:
            keyword_results = []

        # Combine and rerank results
        combined_results = self._combine_results(
            vector_results,
            keyword_results,
            top_k
        )

        return combined_results

    def _combine_results(
        self,
        vector_results: List[Dict[str, Any]],
        keyword_results: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """
        Combine vector and keyword results with weighted scoring
        
        Args:
            vector_results: Results from vector search
            keyword_results: Results from keyword search
            top_k: Number of final results
            
        Returns:
            Combined and reranked results
        """
        # Create a dictionary to store combined scores
        combined_scores = {}

        # Process vector results
        for result in vector_results:
            chunk_id = result.get("chunk_id")
            vector_score = result.get("similarity", 0.0)
            
            if chunk_id not in combined_scores:
                combined_scores[chunk_id] = {
                    "chunk": result,
                    "vector_score": 0.0,
                    "keyword_score": 0.0,
                    "combined_score": 0.0
                }
            
            combined_scores[chunk_id]["vector_score"] = vector_score
            combined_scores[chunk_id]["chunk"] = result

        # Process keyword results
        for result in keyword_results:
            chunk_id = result.get("chunk_id")
            keyword_score = result.get("relevance", 0.0)
            
            if chunk_id not in combined_scores:
                combined_scores[chunk_id] = {
                    "chunk": result,
                    "vector_score": 0.0,
                    "keyword_score": 0.0,
                    "combined_score": 0.0
                }
            
            combined_scores[chunk_id]["keyword_score"] = keyword_score
            combined_scores[chunk_id]["chunk"] = result

        # Calculate combined scores
        for chunk_id, scores in combined_scores.items():
            combined_score = (
                self.vector_weight * scores["vector_score"] +
                self.keyword_weight * scores["keyword_score"]
            )
            scores["combined_score"] = combined_score

        # Sort by combined score and return top_k
        sorted_results = sorted(
            combined_scores.values(),
            key=lambda x: x["combined_score"],
            reverse=True
        )[:top_k]

        # Format results
        formatted_results = []
        for item in sorted_results:
            chunk = item["chunk"]
            chunk["combined_score"] = item["combined_score"]
            chunk["vector_score"] = item["vector_score"]
            chunk["keyword_score"] = item["keyword_score"]
            formatted_results.append(chunk)

        return formatted_results

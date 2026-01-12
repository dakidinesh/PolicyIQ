"""
IBM watsonx.ai client for LLM interactions
"""

from ibm_watson_machine_learning import APIClient
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Dict, Any, List, Optional
import json
from core.config import settings


class WatsonxAIClient:
    """Client for interacting with IBM watsonx.ai"""

    def __init__(self):
        self.api_key = settings.WATSONX_AI_API_KEY
        self.url = settings.WATSONX_AI_URL
        self.project_id = settings.WATSONX_AI_PROJECT_ID
        self.model = settings.WATSONX_AI_MODEL
        
        # Initialize client only if credentials are available
        self.client = None
        self._use_direct_api = False  # Flag to use direct API instead of SDK
        
        if self.api_key and self.project_id:
            try:
                # Try to initialize WML client
                # Note: Some versions have threading issues, so we'll use direct API as fallback
                authenticator = IAMAuthenticator(self.api_key)
                
                # Initialize WML client
                self.client = APIClient({
                    "url": self.url,
                    "authenticator": authenticator
                })
                self.client.set.default_project(self.project_id)
            except Exception as e:
                # If SDK fails, we'll use direct REST API calls
                import warnings
                warnings.warn(f"SDK initialization failed, will use direct API: {str(e)}")
                self.client = None
                self._use_direct_api = True

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # Note: This is a placeholder. Actual implementation depends on
        # watsonx.ai embedding API. You may need to use a different approach
        # or use sentence-transformers as a fallback.
        try:
            # Example API call structure (adjust based on actual API)
            payload = {
                "model_id": settings.EMBEDDING_MODEL,
                "inputs": [text],
                "parameters": {}
            }
            
            # This would be the actual API call
            # response = self.client.deployments.score(...)
            # For now, return placeholder
            raise NotImplementedError(
                "Embedding generation needs to be implemented based on "
                "actual watsonx.ai embedding API"
            )
        except (NotImplementedError, Exception) as e:
            # Fallback to sentence-transformers if available
            try:
                from sentence_transformers import SentenceTransformer
                # Use a default model if the configured one fails
                try:
                    model = SentenceTransformer(settings.EMBEDDING_MODEL)
                except Exception:
                    # Fallback to a common model
                    model = SentenceTransformer('all-MiniLM-L6-v2')
                return model.encode(text).tolist()
            except ImportError:
                # If sentence-transformers is not available, return a dummy embedding
                # This allows the code to run but embeddings won't work properly
                import warnings
                warnings.warn(
                    "sentence-transformers not available. Using dummy embeddings. "
                    "Install with: pip install sentence-transformers"
                )
                # Return a dummy embedding vector
                return [0.0] * settings.EMBEDDING_DIMENSION

    def generate_completion(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.1,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate text completion using watsonx.ai LLM
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_prompt: Optional system prompt
            
        Returns:
            Dictionary with generated text and metadata
        """
        # Check if we have credentials (even if SDK client failed, we can use direct API)
        if not self.api_key or not self.project_id:
            error_msg = "watsonx.ai credentials missing. "
            if not self.api_key:
                error_msg += "WATSONX_AI_API_KEY is missing in .env file. "
            if not self.project_id:
                error_msg += "WATSONX_AI_PROJECT_ID is missing in .env file. "
            error_msg += "Run 'python test_credentials.py' to diagnose."
            raise Exception(error_msg)
        
        try:
            # Construct the prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            # Prepare parameters for watsonx.ai foundation models
            model_params = {
                "decoding_method": "greedy",
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            }

            # Use watsonx.ai foundation models API
            # Use direct REST API (more reliable than SDK)
            import requests
            
            # Skip SDK if we had initialization issues or prefer direct API
            use_direct_api = self._use_direct_api or not self.client
            
            if not use_direct_api:
                # Try SDK first if client is available
                try:
                    from ibm_watson_machine_learning.foundation_models import ModelInference
                    
                    model_inference = ModelInference(
                        model_id=self.model,
                        params=model_params,
                        credentials={
                            "apikey": self.api_key,
                            "url": self.url
                        },
                        project_id=self.project_id
                    )
                    
                    response = model_inference.generate(
                        prompt=full_prompt,
                        params=model_params
                    )
                    
                    # Extract generated text
                    generated_text = ""
                    if isinstance(response, dict):
                        generated_text = response.get("results", [{}])[0].get("generated_text", "")
                    elif isinstance(response, str):
                        generated_text = response
                    elif hasattr(response, 'results') and response.results:
                        generated_text = response.results[0].generated_text
                    else:
                        generated_text = str(response)
                    
                    return {
                        "text": generated_text,
                        "model": self.model,
                        "usage": {
                            "prompt_tokens": len(full_prompt.split()),
                            "completion_tokens": len(generated_text.split()),
                            "total_tokens": len(full_prompt.split()) + len(generated_text.split())
                        }
                    }
                except (ImportError, AttributeError, Exception) as sdk_error:
                    # Fall through to direct API
                    use_direct_api = True
                    sdk_error_msg = str(sdk_error)
            
            if use_direct_api:
                # Fallback: Use direct REST API call
                import requests
                
                try:
                    # Get IAM token - use standard IAM endpoint
                    token_url = "https://iam.cloud.ibm.com/identity/token"
                    token_data = {
                        "apikey": self.api_key,
                        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
                    }
                    
                    token_response = requests.post(
                        token_url,
                        data=token_data,
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        timeout=10
                    )
                    
                    if token_response.status_code != 200:
                        error_data = token_response.json() if token_response.headers.get('content-type', '').startswith('application/json') else {}
                        error_msg = error_data.get("errorMessage", f"HTTP {token_response.status_code}")
                        raise Exception(f"API key validation failed: {error_msg}. Please check your API key in .env file.")
                    
                    token = token_response.json().get("access_token")
                    
                    if not token:
                        raise Exception("Failed to get access token from response")
                    
                    # Call foundation models API
                    # Construct the correct endpoint URL
                    # Format: https://{region}.ml.cloud.ibm.com/ml/v1/text/generation
                    if "/ml/v1" not in self.url:
                        # Add /ml/v1 if not present
                        base_url = self.url.rstrip('/') + "/ml/v1"
                    else:
                        base_url = self.url.rstrip('/')
                    
                    api_url = f"{base_url}/text/generation?version=2023-05-29"
                    
                    headers = {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model_id": self.model,
                        "input": full_prompt,
                        "parameters": model_params,
                        "project_id": self.project_id
                    }
                    
                    api_response = requests.post(api_url, json=payload, headers=headers, timeout=30)
                    api_response.raise_for_status()
                    result = api_response.json()
                    
                    generated_text = result.get("results", [{}])[0].get("generated_text", "")
                    
                    return {
                        "text": generated_text,
                        "model": self.model,
                        "usage": result.get("usage", {
                            "prompt_tokens": len(full_prompt.split()),
                            "completion_tokens": len(generated_text.split()),
                            "total_tokens": len(full_prompt.split()) + len(generated_text.split())
                        })
                    }
                    
                except Exception as api_error:
                    # If both methods fail, raise with helpful error
                    error_msg = f"API error: {str(api_error)}"
                    if 'sdk_error_msg' in locals():
                        error_msg = f"SDK error: {sdk_error_msg}. {error_msg}"
                    raise Exception(f"Failed to generate completion: {error_msg}")
                
        except Exception as e:
            raise Exception(f"Error generating completion: {str(e)}")

    def generate_with_context(
        self,
        question: str,
        context: List[str],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate answer with retrieved context
        
        Args:
            question: User question
            context: Retrieved context chunks
            system_prompt: Optional system prompt
            
        Returns:
            Generated response with metadata
        """
        # Construct prompt with context
        context_text = "\n\n".join([
            f"[Context {i+1}]:\n{chunk}" for i, chunk in enumerate(context)
        ])
        
        prompt = f"""Based on the following regulatory documents and policies, answer the question accurately and cite specific sections.

{context_text}

Question: {question}

Please provide:
1. A direct answer
2. A brief explanation
3. Specific citations (document names, section numbers, article numbers)
4. Your confidence level (high/medium/low)

Answer:"""

        return self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt or self._get_default_system_prompt(),
            max_tokens=1500,
            temperature=0.1
        )

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt for compliance QA"""
        return """You are PolicyIQ, an expert regulatory compliance assistant for banking and finance.

Your role:
- Provide accurate answers based on regulatory documents (GDPR, SOC2, PCI-DSS, etc.)
- Always cite specific sections, articles, or clauses
- Indicate confidence levels honestly
- Flag when information is unclear or requires manual review
- Focus on compliance and regulatory requirements

Be precise, cite sources, and prioritize accuracy over completeness."""

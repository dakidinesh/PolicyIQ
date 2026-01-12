"""
Configuration management using Pydantic settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "PolicyIQ"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # watsonx.ai
    WATSONX_AI_API_KEY: Optional[str] = None
    WATSONX_AI_URL: str = "https://us-south.ml.cloud.ibm.com"
    WATSONX_AI_PROJECT_ID: Optional[str] = None
    WATSONX_AI_MODEL: str = "meta-llama/llama-2-70b-chat"

    # watsonx.data
    WATSONX_DATA_URL: Optional[str] = None
    WATSONX_DATA_USERNAME: Optional[str] = None
    WATSONX_DATA_PASSWORD: Optional[str] = None
    WATSONX_DATA_DATABASE: str = "policyiq_db"

    # Embedding
    EMBEDDING_MODEL: str = "ibm/slate-125m-english-rtrvr"
    EMBEDDING_DIMENSION: int = 768
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # RAG
    MAX_RETRIEVAL_RESULTS: int = 10
    SIMILARITY_THRESHOLD: float = 0.7
    KEYWORD_WEIGHT: float = 0.3
    VECTOR_WEIGHT: float = 0.7

    # Confidence
    MIN_CONFIDENCE_THRESHOLD: float = 0.6
    MANUAL_REVIEW_THRESHOLD: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

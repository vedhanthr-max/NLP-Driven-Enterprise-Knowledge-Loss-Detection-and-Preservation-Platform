import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Knowledge Loss Detection & Preservation Platform"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./knowledge_loss.db")
    
    # JWT Authentication
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "knowledge_loss_secret_key_change_in_production_2026_secure")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_HASH_ROUNDS: int = 12
    
    # Document Uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx", "txt", "md"]
    
    # NLP & Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    NER_MODEL: str = "en_core_web_md"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    
    # Risk Calculation Weights
    WEIGHT_CRITICALITY: float = 0.30
    WEIGHT_UNIQUENESS: float = 0.25
    WEIGHT_DEPENDENCY: float = 0.20
    WEIGHT_DOCUMENTATION_GAP: float = 0.15
    WEIGHT_AVAILABILITY_RISK: float = 0.10
    
    # Risk Level Thresholds
    THRESHOLD_LOW: float = 30.0
    THRESHOLD_MEDIUM: float = 60.0
    THRESHOLD_HIGH: float = 80.0
    # > 80.0 is CRITICAL
    
    # ML Models directory
    ML_MODEL_DIR: str = "ml_models"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

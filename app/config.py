"""
Configuration settings for the ecommerce application.
"""

from typing import List, Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./ecommerce.db"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security Configuration
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Payment Gateway Configuration
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None
    PAYPAL_MODE: str = "sandbox"  # or live
    
    # Cryptocurrency Configuration
    ETHEREUM_NETWORK: str = "testnet"  # or mainnet
    ETHEREUM_PRIVATE_KEY: Optional[str] = None
    BITCOIN_NETWORK: str = "testnet"  # or mainnet
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@ecommerce.com"
    
    # AI/ML Configuration
    RECOMMENDATION_MODEL_PATH: str = "models/recommendation_model.pkl"
    SIMILARITY_THRESHOLD: float = 0.7
    RECOMMENDATION_LIMIT: int = 10
    
    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    
    # Application Configuration
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3003", "http://localhost:8000", "http://127.0.0.1:8000", "null"]
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Modern Ecommerce Platform"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    

    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("models", exist_ok=True) 
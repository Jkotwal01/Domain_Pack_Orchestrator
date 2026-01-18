"""
Core configuration module using Pydantic Settings.
Manages application configuration from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Falls back to default values if not set.
    """
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "domain_config_db"
    COLLECTION_NAME: str = "yaml_configs"
    
    # Logging Configuration
    LOG_FILE_PATH: str = "logs/app.log"
    LOG_LEVEL: str = "INFO"
    
    # Application Configuration
    APP_NAME: str = "Domain Config Backend"
    APP_VERSION: str = "1.0.0"
    
    # LLM Configuration
    LLM_PROVIDER: str = "groq"  # openai, groq, anthropic
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.1  # Low for deterministic output
    LLM_MAX_TOKENS: int = 2000
    LLM_TIMEOUT: int = 30
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

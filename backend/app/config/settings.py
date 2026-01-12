from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Environment
    environment: str = "development"  # development, production
    
    # Database
    google_application_credentials: Optional[str] = None
    instance_connection_name: Optional[str] = None
    db_port: str = "5432"
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_pass: Optional[str] = None
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    
    # Application
    app_name: str = "AlgoSensei"
    debug: bool = False
    
    # CORS
    extension_url: Optional[str] = None
    
    # Google AI/Gemini
    google_api_key: Optional[str] = ""
    google_genai_use_vertexai: int = 0  # 0 = False, 1 = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True, 
        case_sensitive=False,
        extra="ignore",
    )
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings singleton.
    Use this function instead of instantiating Settings() directly.
    
    Example usage in FastAPI:
        from fastapi import Depends
        from app.config.settings import get_settings, Settings
        
        @app.get("/")
        def read_root(settings: Settings = Depends(get_settings)):
            return {"app": settings.app_name}
    """
    return Settings()

settings = get_settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    google_application_credentials: Optional[str] = None
    instance_connection_name: Optional[str] = None
    db_port: Optional[str] = "5432"
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_pass: Optional[str] = None
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    app_name: str = "AlgoSensei"
    debug: bool = False
    
    # CORS
    frontend_url: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database configuration
    app_db_user: str = "ai_chat_user"
    app_db_password: str = "password"
    app_db_name: str = "ai_chat"
    postgres_host: str = "database"
    postgres_port: int = 5432
    
    @property
    def database_url(self) -> str:
        return f"postgres://{self.app_db_user}:{self.app_db_password}@{self.postgres_host}:{self.postgres_port}/{self.app_db_name}"
    
    # JWT configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # AI configuration
    openai_api_key: str
    
    # Application configuration
    app_name: str = "AI Customer Messaging System"
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()

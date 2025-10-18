from pydantic_settings import BaseSettings
from typing import Optional


class PostgresSettings(BaseSettings):
    USER: str
    PASSWORD: str
    DB: str
    HOST: str
    PORT: int
    
    @property
    def database_url(self) -> str:
        return f"postgres://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
    
    
    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):    
    db: PostgresSettings = PostgresSettings()

    # JWT configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    
    # AI configuration
    openai_api_key: str
    
    # Application configuration
    app_name: str = "AI Customer Messaging System"
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]
    
    # Superadmin configuration
    superadmin_email: str
    superadmin_password: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()

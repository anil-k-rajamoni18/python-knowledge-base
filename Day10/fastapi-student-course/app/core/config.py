# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from functools import lru_cache


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "FastAPI Student Course API"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str  # e.g., sqlite+aiosqlite:///./db_data/app.db

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Initial superuser
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Ensures settings are cached and loaded once."""
    return Settings()

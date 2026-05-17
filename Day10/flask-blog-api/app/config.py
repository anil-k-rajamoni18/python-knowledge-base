# app/config.py
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # CORS
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day;50 per hour"

    # RQ / Redis
    REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

    # Pagination default
    POSTS_PER_PAGE = int(os.environ.get("POSTS_PER_PAGE", 10))

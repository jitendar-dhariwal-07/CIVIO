"""
Application configuration using pydantic-settings.
All secrets and environment-specific values are loaded from environment
variables or a .env file located in the backend directory.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the CIVIO backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = "CIVIO"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENV: str = "development"

    # ── Server ───────────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── Database (PostgreSQL) ────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://civio_user:civio_password@localhost:5432/civio_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_ECHO: bool = False

    # ── Redis ────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL: int = 3600

    # ── Celery (Background Tasks) ────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # ── Google Gemini AI ─────────────────────────────────────────────────
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_TEMPERATURE: float = 0.3
    GEMINI_MAX_OUTPUT_TOKENS: int = 4096

    # ── Google Translate API ─────────────────────────────────────────────
    GOOGLE_TRANSLATE_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""

    # ── AWS Services ─────────────────────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "ap-south-1"

    # ── JWT / Auth ───────────────────────────────────────────────────────
    JWT_SECRET: str = "change-me-in-production-use-a-long-random-string"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # ── CORS ─────────────────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

    # ── Embeddings (Complaint Duplicate Detection) ───────────────────────
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    DUPLICATE_THRESHOLD: float = 0.85
    DUPLICATE_LOCATION_RADIUS_KM: float = 5.0
    DUPLICATE_TIME_WINDOW_DAYS: int = 7

    # ── Hotspot Detection ────────────────────────────────────────────────
    HOTSPOT_EPS: float = 0.01  # DBSCAN eps parameter
    HOTSPOT_MIN_SAMPLES: int = 3  # DBSCAN min_samples
    HOTSPOT_MIN_COMPLAINTS: int = 5  # Minimum complaints to form a hotspot
    HOTSPOT_ANALYSIS_DAYS: int = 30  # Look back period

    # ── Complaint Categories ────────────────────────────────────────────
    COMPLAINT_CATEGORIES: List[str] = [
        "water",
        "electricity",
        "road",
        "sanitation",
        "transport",
        "parks",
        "other"
    ]

    # ── Complaint Priorities ────────────────────────────────────────────
    COMPLAINT_PRIORITIES: List[str] = ["low", "medium", "high", "critical"]

    # ── File Uploads ─────────────────────────────────────────────────────
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"
    ALLOWED_UPLOAD_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]

    # ── Supported Languages ──────────────────────────────────────────────
    SUPPORTED_LANGUAGES: List[str] = ["en", "hi", "ta", "te", "kn", "ml", "bn", "mr"]
    DEFAULT_LANGUAGE: str = "en"

    # ── Pagination ───────────────────────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # ── Rate Limiting ────────────────────────────────────────────────────
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # ── Logging ──────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    # ── Scheme Database ──────────────────────────────────────────────────
    SCHEMES_CACHE_TTL_MINUTES: int = 60  # Cache scheme data for 1 hour
    STATES_SUPPORTED: List[str] = [
        "Delhi", "Karnataka", "Tamil Nadu", "Maharashtra", "Gujarat",
        "Rajasthan", "Uttar Pradesh", "Madhya Pradesh", "West Bengal",
        "Telangana"  # Add more states as needed
    ]

    def __init__(self, **data):
        super().__init__(**data)
        # Create upload directory if it doesn't exist
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings instance so .env is read only once."""
    return Settings()


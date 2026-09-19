from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Personalized Learning Engine"
    app_version: str = "0.1.0"
    environment: str = Field(default="development")

    documents_dir: str = Field(default="data/documents")

    max_upload_size_mb: int = Field(default=25)

    allowed_file_types: tuple[str, ...] = (".pdf",)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
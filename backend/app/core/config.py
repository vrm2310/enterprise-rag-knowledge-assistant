from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise RAG Knowledge Assistant API"
    app_version: str = "0.1.0"
    app_description: str = (
        "Backend API for document ingestion, semantic search, and AI-powered chat."
    )
    app_env: str = "development"

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
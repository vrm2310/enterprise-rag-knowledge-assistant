from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -----------------------------
    # Application
    # -----------------------------
    app_name: str = "Enterprise RAG Knowledge Assistant API"
    app_version: str = "0.1.0"
    app_description: str = (
        "Backend API for document ingestion, semantic search, and AI-powered chat."
    )
    app_env: str = "development"

    # -----------------------------
    # PostgreSQL
    # -----------------------------
    postgres_db: str = ""
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_host: str = ""
    postgres_port: int = 5432

    # -----------------------------
    # Redis
    # -----------------------------
    redis_host: str = ""
    redis_port: int = 6379

    # -----------------------------
    # Qdrant
    # -----------------------------
    qdrant_host: str = ""
    qdrant_port: int = 6333
    qdrant_collection: str = ""

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -----------------------------
    # JWT
    # -----------------------------
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    upload_dir: str = "uploads"

    embedding_model: str = "BAAI/bge-small-en-v1.5"


settings = Settings()
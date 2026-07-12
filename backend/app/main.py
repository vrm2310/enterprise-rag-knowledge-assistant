from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine

from app.auth.router import router as auth_router

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(auth_router)

@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {"message": settings.app_name}

@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/health/db", tags=["Health"])
def database_health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain text password."""
    return password_hash.hash(password)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return password_hash.verify(password, hashed_password)

def create_access_token(subject: str) -> str:
    """Create a JWT access token."""

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT."""

    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
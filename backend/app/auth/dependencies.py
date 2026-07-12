from uuid import UUID

from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.repository import UserRepository
from app.core.security import decode_access_token, oauth2_scheme
from app.db.session import get_db


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Return the authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_uuid = UUID(user_id)

    except (JWTError, ValueError) as exc:
        raise credentials_exception from exc

    repository = UserRepository(db)

    user = repository.get_by_id(user_uuid)

    if user is None:
        raise credentials_exception

    return user
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.repository import UserRepository
from app.auth.schemas import UserCreate
from app.core.security import hash_password


class UserService:
    """Business logic for user management."""

    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user."""

        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise ValueError("A user with this email already exists.")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        return self.repository.create(user)
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.repository import UserRepository
from app.auth.schemas import UserCreate
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.core.security import create_access_token, hash_password, verify_password


class UserService:
    """Business logic for user management."""

    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user."""

        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise UserAlreadyExistsError("A user with this email already exists.")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        return self.repository.create(user)
    
    def login_user(self, email: str, password: str) -> str:
        """Authenticate user and return JWT access token."""

        user = self.repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError("Invalid email or password.")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password.")

        access_token = create_access_token(
            subject=str(user.id),
        )

        return access_token
class UserAlreadyExistsError(Exception):
    """Raised when registering with an existing email."""


class InvalidCredentialsError(Exception):
    """Raised when email or password is incorrect."""
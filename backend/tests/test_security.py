from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing() -> None:
    password = "SuperSecret123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_create_and_decode_token() -> None:
    token = create_access_token("123")

    payload = decode_access_token(token)

    assert payload["sub"] == "123"
    assert "exp" in payload
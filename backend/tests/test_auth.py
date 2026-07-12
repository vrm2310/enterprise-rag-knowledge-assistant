from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Vyom",
            "email": "vyom@example.com",
            "password": "SuperSecret123",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == "vyom@example.com"
    assert body["full_name"] == "Vyom"


def test_duplicate_registration(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "full_name": "Vyom",
            "email": "duplicate@example.com",
            "password": "SuperSecret123",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Vyom",
            "email": "duplicate@example.com",
            "password": "SuperSecret123",
        },
    )

    assert response.status_code == 409


def test_login_success(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "full_name": "Login User",
            "email": "login@example.com",
            "password": "Password123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    token = response.json()

    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_login_invalid_password(client: TestClient):
    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_current_user(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "full_name": "Current User",
            "email": "current@example.com",
            "password": "Password123",
        },
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "current@example.com",
            "password": "Password123",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == "current@example.com"


def test_current_user_without_token(client: TestClient):
    response = client.get("/auth/me")

    assert response.status_code == 401
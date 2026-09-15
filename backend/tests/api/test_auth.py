from fastapi.testclient import TestClient


def test_register_user(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "CorrectHorseBatteryStaple!",
            "first_name": "New",
            "last_name": "User",
            "organization_name": "Test University",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "newuser@example.com"
    assert data["first_name"] == "New"
    assert data["last_name"] == "User"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_rejects_short_password(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "short@example.com",
            "password": "short",
            "first_name": "Short",
            "last_name": "Password",
            "organization_name": "Test University",
        },
    )

    assert response.status_code == 422

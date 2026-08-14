def test_create_user(test_user):
    data = test_user["response"]
    input_data = test_user["input"]

    assert data["username"] == input_data["username"]
    assert data["email"] == input_data["email"]
    assert "password" not in data
    assert "hashed_password" not in data

def test_login(client, test_user):
    input_data = test_user["input"]

    response = client.post(
        "/auth/login",
        data={
            "username": input_data["username"],
            "password": input_data["password"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    input_data = test_user["input"]

    response = client.post(
        "/auth/login",
        data={
            "username": input_data["username"],
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "does_not_exist",
            "password": "password123"
        }
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    response = client.get("/users/")

    assert response.status_code == 401


def test_protected_endpoint_with_invalid_token(client):
    response = client.get(
        "/users/",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 401
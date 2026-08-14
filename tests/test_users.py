def test_get_users(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["username"] == test_user["input"]["username"]
    assert "email" not in data[0]


def test_get_own_user(client, test_user):
    user_id = test_user["response"]["id"]

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["username"] == test_user["input"]["username"]
    assert data["email"] == test_user["input"]["email"]


def test_get_other_user_forbidden(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/users/",
        json={
            "username": "other_test_user",
            "email": "other@example.com",
            "password": "password123"
        }
    )

    other_user_id = response.json()["id"]

    response = client.get(
        f"/users/{other_user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_update_own_user(client, test_user):
    user_id = test_user["response"]["id"]

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": f"updated_{test_user['input']['username']}",
            "email": f"updated_{test_user['input']['email']}",
            "password": "newpassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == f"updated_{test_user['input']['username']}"
    assert data["email"] == f"updated_{test_user['input']['email']}"
    assert "hashed_password" not in data


def test_update_other_user_forbidden(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/users/",
        json={
            "username": "other_test_user",
            "email": "other@example.com",
            "password": "password123"
        }
    )

    other_user_id = response.json()["id"]

    response = client.put(
        f"/users/{other_user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "hacked_user",
            "email": "hacked@example.com",
            "password": "hackedpassword"
        }
    )

    assert response.status_code == 403


def test_delete_own_user(client, test_user):
    user_id = test_user["response"]["id"]

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "User deleted successfully"


def test_delete_other_user_forbidden(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/users/",
        json={
            "username": "other_test_user",
            "email": "other@example.com",
            "password": "password123"
        }
    )

    other_user_id = response.json()["id"]

    response = client.delete(
        f"/users/{other_user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
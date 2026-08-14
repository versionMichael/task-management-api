def test_create_project(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Project",
            "description": "Test project description"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Project"
    assert data["description"] == "Test project description"
    assert data["owner_id"] == test_user["response"]["id"]


def test_get_projects(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Project",
            "description": "Test project description"
        }
    )

    response = client.get(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["name"] == "Test Project"
    assert data[0]["description"] == "Test project description"


def test_get_own_project(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Project",
            "description": "Test project description"
        }
    )

    project_id = response.json()["id"]

    response = client.get(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == project_id
    assert data["name"] == "Test Project"
    assert data["description"] == "Test project description"
    assert data["owner_id"] == test_user["response"]["id"]


def test_get_other_users_project_forbidden(client, test_user):
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
            "username": "other_project_user",
            "email": "other_project_user@example.com",
            "password": "password123"
        }
    )

    other_user_id = response.json()["id"]

    response = client.post(
        "/auth/login",
        data={
            "username": "other_project_user",
            "password": "password123"
        }
    )

    other_token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "name": "Other User Project",
            "description": "Project owned by another user"
        }
    )

    project_id = response.json()["id"]

    response = client.get(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_update_own_project(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Project",
            "description": "Original description"
        }
    )

    project_id = response.json()["id"]

    response = client.put(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Project",
            "description": "Updated description"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Project"
    assert data["description"] == "Updated description"
    assert data["owner_id"] == test_user["response"]["id"]


def test_update_other_users_project_forbidden(client, test_user):
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
            "username": "other_update_user",
            "email": "other_update_user@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "other_update_user",
            "password": "password123"
        }
    )

    other_token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "name": "Other User Project",
            "description": "Original description"
        }
    )

    project_id = response.json()["id"]

    response = client.put(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hacked Project",
            "description": "Hacked description"
        }
    )

    assert response.status_code == 403


def test_delete_own_project(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Project To Delete",
            "description": "This project will be deleted"
        }
    )

    project_id = response.json()["id"]

    response = client.delete(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Project deleted successfully"


def test_delete_other_users_project_forbidden(client, test_user):
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
            "username": "other_delete_user",
            "email": "other_delete_user@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "other_delete_user",
            "password": "password123"
        }
    )

    other_token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "name": "Other User Project",
            "description": "Project to protect"
        }
    )

    project_id = response.json()["id"]

    response = client.delete(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_get_project_tasks(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["input"]["username"],
            "password": test_user["input"]["password"]
        }
    )

    token = response.json()["access_token"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Task Project",
            "description": "Project for testing tasks"
        }
    )

    project_id = response.json()["id"]

    response = client.get(
        f"/projects/{project_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
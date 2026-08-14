def test_create_task(client, test_user):
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

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Task",
            "description": "Test task description",
            "project_id": project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["description"] == "Test task description"
    assert data["project_id"] == project_id
    assert data["assigned_to"] == test_user["response"]["id"]


def test_get_tasks(client, test_user):
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

    client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Task",
            "description": "Test task description",
            "project_id": project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["title"] == "Test Task"
    assert data[0]["description"] == "Test task description"


def test_get_own_task(client, test_user):
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

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Task",
            "description": "Test task description",
            "project_id": project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Test Task"
    assert data["description"] == "Test task description"
    assert data["project_id"] == project_id
    assert data["assigned_to"] == test_user["response"]["id"]


def test_create_task_in_other_users_project_forbidden(client, test_user):
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
            "username": "other_task_user",
            "email": "other_task_user@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "other_task_user",
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

    other_project_id = response.json()["id"]

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Unauthorized Task",
            "description": "Should not be created",
            "project_id": other_project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    assert response.status_code == 403


def test_get_other_users_task_forbidden(client, test_user):
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
            "username": "other_get_task_user",
            "email": "other_get_task_user@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "other_get_task_user",
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

    other_project_id = response.json()["id"]

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "title": "Other User Task",
            "description": "Task owned by another user's project",
            "project_id": other_project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_update_own_task(client, test_user):
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

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Original Task",
            "description": "Original description",
            "project_id": project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Task",
            "description": "Updated description",
            "project_id": project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"
    assert data["project_id"] == project_id
    assert data["assigned_to"] == test_user["response"]["id"]


def test_update_other_users_task_forbidden(client, test_user):
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
            "username": "other_update_task_user",
            "email": "other_update_task_user@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "other_update_task_user",
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

    other_project_id = response.json()["id"]

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "title": "Other User Task",
            "description": "Original description",
            "project_id": other_project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Hacked Task",
            "description": "Hacked description",
            "project_id": other_project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    assert response.status_code == 403


def test_move_task_to_own_project(client, test_user):
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
            "name": "Original Project",
            "description": "Original project"
        }
    )

    original_project_id = response.json()["id"]

    response = client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "New Project",
            "description": "New project"
        }
    )

    new_project_id = response.json()["id"]

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Movable Task",
            "description": "Task to move",
            "project_id": original_project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Moved Task",
            "description": "Task has been moved",
            "project_id": new_project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == new_project_id
    assert data["title"] == "Moved Task"


def test_delete_own_task(client, test_user):
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

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Task To Delete",
            "description": "This task will be deleted",
            "project_id": project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Task deleted successfully"


def test_delete_other_users_task_forbidden(client, test_user):
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
            "username": "other_delete_task_user",
            "email": "other_delete_task_user@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "other_delete_task_user",
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

    other_project_id = response.json()["id"]

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "title": "Other User Task",
            "description": "Task to protect",
            "project_id": other_project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_get_task_user(client, test_user):
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

    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Assigned Task",
            "description": "Task assigned to test user",
            "project_id": project_id,
            "assigned_to": test_user["response"]["id"]
        }
    )

    task_id = response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}/user",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == test_user["response"]["id"]
    assert data["username"] == test_user["input"]["username"]
    assert data["email"] == test_user["input"]["email"]
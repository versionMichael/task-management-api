import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app as fastapi_app
from app.database import Base

import app.routers.user
import app.routers.project
import app.routers.task
import app.routers.auth
import app.utils.auth

from dotenv import load_dotenv
import os

import uuid

load_dotenv(".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=test_engine
)


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        app.routers.user,
        "SessionLocal",
        TestingSessionLocal
    )

    monkeypatch.setattr(
        app.routers.project,
        "SessionLocal",
        TestingSessionLocal
    )

    monkeypatch.setattr(
        app.routers.task,
        "SessionLocal",
        TestingSessionLocal
    )

    monkeypatch.setattr(
        app.routers.auth,
        "SessionLocal",
        TestingSessionLocal
    )

    monkeypatch.setattr(
        app.utils.auth,
        "SessionLocal",
        TestingSessionLocal
    )

    
    Base.metadata.create_all(bind=test_engine)

    with TestClient(fastapi_app) as client:
        yield client

    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def test_user(client):

    unique_id = uuid.uuid4().hex
    user_data={
        "username": f"testuser_{unique_id}",
        "email" : f"{unique_id}@example.com",
        "password": "password123"
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 200

    return {
        "input": user_data,
        "response": response.json()
    }
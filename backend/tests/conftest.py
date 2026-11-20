import os
import secrets

os.environ.setdefault("JWT_SECRET", secrets.token_hex(32))
os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.core.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def headers(client):
    data = {"email": "ciclista@example.com", "password": "Strong-password-123", "alias": "Ciclista"}
    assert client.post("/api/users/register", json=data).status_code == 201
    token = client.post("/api/users/login", json={k: data[k] for k in ("email", "password")}).json()
    return {"Authorization": "Bearer " + token["access_token"]}

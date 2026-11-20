"""Comprobación HTTP contra el esquema PostgreSQL migrado en CI."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

with TestClient(app) as client:
    assert client.get("/ready").status_code == 200
    assert len(client.get("/api/cycleways").json()) == 4
    data = {"email": f"ci-{uuid4().hex}@example.com", "alias": "CI", "password": uuid4().hex}
    assert client.post("/api/users/register", json=data).status_code == 201
    credentials = {key: data[key] for key in ("email", "password")}
    token = client.post("/api/users/login", json=credentials).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.put("/api/parking/1/favorite", headers=headers).status_code == 204
    assert len(client.get("/api/parking/favorites", headers=headers).json()) == 1
    for _ in range(2):
        assert (
            client.put(
                "/api/billing/subscription", headers=headers, json={"plan_code": "plus"}
            ).status_code
            == 200
        )
    assert len(client.get("/api/billing/invoices", headers=headers).json()) == 1
    export = client.get("/api/billing/favorites.csv", headers=headers)
    assert export.status_code == 200
    assert "Punto de estacionamiento A" in export.text
    assert client.post("/api/users/logout", headers=headers).status_code == 204
    assert client.get("/api/users/me", headers=headers).status_code == 401
print("Migraciones y flujo HTTP con base migrada: OK")

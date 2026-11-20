from app.modules.cycleways.models import Cycleway
from app.modules.reports.models import ModerationAction
from app.modules.users.models import User


def test_report_requires_session_and_valid_coordinates(client, db, headers):
    db.add(
        Cycleway(
            name="Tramo", district="Barranco", geometry=[[-12.1, -77.0]], source="Demo", length_km=1
        )
    )
    db.commit()
    data = {
        "cycleway_id": 1,
        "category": "Obstáculo",
        "description": "Obstáculo de demostración",
        "latitude": -12.1,
        "longitude": -77.0,
    }
    assert client.post("/api/reports", json=data).status_code == 401
    assert (
        client.post("/api/reports", json={**data, "latitude": 999}, headers=headers).status_code
        == 422
    )
    assert (
        client.post("/api/reports", json={**data, "cycleway_id": 999}, headers=headers).status_code
        == 404
    )
    result = client.post("/api/reports", json=data, headers=headers)
    assert result.status_code == 201
    assert result.json()["status"] == "pending"
    assert "user_id" not in result.json()
    assert client.get("/api/reports").json() == []
    assert client.get("/api/reports/pending", headers=headers).status_code == 403
    assert (
        client.patch(
            "/api/reports/1/moderate", headers=headers, json={"status": "published"}
        ).status_code
        == 403
    )
    user = db.get(User, 1)
    user.role = "moderator"
    db.commit()
    assert len(client.get("/api/reports/pending", headers=headers).json()) == 1
    assert (
        client.patch(
            "/api/reports/1/moderate", headers=headers, json={"status": "published"}
        ).status_code
        == 200
    )
    assert len(client.get("/api/reports").json()) == 1
    assert db.get(ModerationAction, 1).moderator_id == 1
    assert (
        client.patch(
            "/api/reports/1/moderate", headers=headers, json={"status": "rejected"}
        ).status_code
        == 409
    )

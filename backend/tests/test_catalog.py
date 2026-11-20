from app.modules.cycleways.models import Cycleway
from app.modules.parking.models import Parking


def test_filters_details_and_missing(client, db):
    db.add(
        Cycleway(
            name="Tramo demo",
            district="Barranco",
            condition="Sin verificar",
            geometry=[[-12.1, -77.0], [-12.11, -77.01]],
            length_km=1.2,
            source="Demo",
        )
    )
    db.commit()
    assert len(client.get("/api/cycleways?district=Barranco").json()) == 1
    assert client.get("/api/cycleways?district=Otro").json() == []
    assert client.get("/api/cycleways/999").status_code == 404
    assert client.get("/api/cycleways/1").json()["is_demo"] is True


def test_favorites_are_unique_private_and_removable(client, db, headers):
    db.add(
        Parking(
            name="Parking demo",
            district="Barranco",
            latitude=-12.1,
            longitude=-77.0,
            address="Referencial",
            source="Demo",
        )
    )
    db.commit()
    assert client.put("/api/parking/1/favorite").status_code == 401
    for _ in range(2):
        assert client.put("/api/parking/1/favorite", headers=headers).status_code == 204
    assert len(client.get("/api/parking/favorites", headers=headers).json()) == 1
    client.post(
        "/api/users/register",
        json={"email": "other@example.com", "password": "Another-password", "alias": "Otro"},
    )
    token = client.post(
        "/api/users/login", json={"email": "other@example.com", "password": "Another-password"}
    ).json()["access_token"]
    assert (
        client.get("/api/parking/favorites", headers={"Authorization": f"Bearer {token}"}).json()
        == []
    )
    assert client.delete("/api/parking/1/favorite", headers=headers).status_code == 204
    assert client.get("/api/parking/favorites", headers=headers).json() == []
    assert client.get("/api/parking/999").status_code == 404

from app.showcase import seed_showcase


def test_demo_subscription_is_private_idempotent_and_exports_only_own_favorites(
    client, db, headers
):
    seed_showcase(db)
    plans = client.get("/api/billing/plans").json()
    assert plans["mode"] == "demo"
    assert client.get("/api/billing/subscription").status_code == 401
    assert client.get("/api/billing/invoices", headers=headers).json() == []
    assert client.get("/api/billing/favorites.csv", headers=headers).status_code == 403
    for _ in range(2):
        response = client.put(
            "/api/billing/subscription", headers=headers, json={"plan_code": "plus"}
        )
        assert response.json()["plan_code"] == "plus"
        assert response.json()["mode"] == "demo"
    invoices = client.get("/api/billing/invoices", headers=headers).json()
    assert len(invoices) == 1
    assert invoices[0]["amount_centavos"] == 990
    assert invoices[0]["status"] == "simulated"
    empty = client.get("/api/billing/favorites.csv", headers=headers)
    assert empty.status_code == 200
    assert len(empty.text.strip().splitlines()) == 1
    client.put("/api/parking/1/favorite", headers=headers)
    export = client.get("/api/billing/favorites.csv", headers=headers)
    assert "Punto de estacionamiento A" in export.text
    assert "Punto de estacionamiento B" not in export.text
    assert (
        client.put(
            "/api/billing/subscription", headers=headers, json={"plan_code": "paid"}
        ).status_code
        == 422
    )
    client.put("/api/billing/subscription", headers=headers, json={"plan_code": "free"})
    assert client.get("/api/billing/favorites.csv", headers=headers).status_code == 403
    assert len(client.get("/api/billing/invoices", headers=headers).json()) == 2
    # Otras cuentas no reciben estos comprobantes ni la suscripción.
    data = {"email": "second-billing@example.com", "alias": "Otro", "password": "Long-password-123"}
    client.post("/api/users/register", json=data)
    token = client.post(
        "/api/users/login", json={k: data[k] for k in ("email", "password")}
    ).json()["access_token"]
    other = {"Authorization": "Bearer " + token}
    assert client.get("/api/billing/invoices", headers=other).json() == []
    assert client.get("/api/billing/subscription", headers=other).json()["plan_code"] == "free"

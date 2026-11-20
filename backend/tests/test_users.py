def test_register_duplicate_and_no_role_escalation(client):
    data = {"email": "ana@example.com", "password": "Very-good-password", "alias": "Ana"}
    result = client.post("/api/users/register", json=data)
    assert result.status_code == 201
    assert "password_hash" not in result.json()
    assert result.json()["role"] == "cyclist"
    assert client.post("/api/users/register", json=data).status_code == 409
    assert client.post("/api/users/register", json={**data, "role": "moderator"}).status_code == 422


def test_auth_profile_and_persisted_logout(client, headers):
    assert client.get("/api/users/me").status_code == 401
    assert client.get("/api/users/me", headers=headers).status_code == 200
    result = client.patch(
        "/api/users/me", headers=headers, json={"alias": "Mi bicicleta", "district": "Miraflores"}
    )
    assert result.json()["district"] == "Miraflores"
    assert client.post("/api/users/logout", headers=headers).status_code == 204
    assert client.get("/api/users/me", headers=headers).status_code == 401


def test_wrong_password_and_malformed_token(client):
    assert (
        client.post(
            "/api/users/login", json={"email": "nobody@example.com", "password": "wrong-password"}
        ).status_code
        == 401
    )
    assert (
        client.get("/api/users/me", headers={"Authorization": "Bearer invalid"}).status_code == 401
    )

def test_register_and_login(client):
    register_payload = {"email": "user@example.com", "password": "securepass"}
    response = client.post("/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "id" in data

    response = client.post("/login", json=register_payload)
    assert response.status_code == 200
    token_data = response.json()
    assert token_data["token_type"] == "bearer"
    assert token_data["access_token"]

    auth_headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_response = client.get("/me", headers=auth_headers)
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "user@example.com"

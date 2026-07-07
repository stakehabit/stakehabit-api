def test_create_habit(client):
    user_payload = {"email": "habit@example.com", "password": "habitpass"}
    client.post("/register", json=user_payload)
    login_response = client.post("/login", json=user_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    habit_payload = {
        "title": "Read more",
        "frequency": "daily",
        "target_days_per_week": 5,
        "is_active": True,
    }
    response = client.post("/habits", json=habit_payload, headers=headers)
    assert response.status_code == 201
    habit = response.json()
    assert habit["title"] == "Read more"
    assert habit["frequency"] == "daily"
    assert habit["target_days_per_week"] == 5

    list_response = client.get("/habits", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

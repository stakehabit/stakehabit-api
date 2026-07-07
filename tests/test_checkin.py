def test_duplicate_checkin_prevention(client):
    user_payload = {"email": "checkin@example.com", "password": "checkinpass"}
    client.post("/register", json=user_payload)
    login_response = client.post("/login", json=user_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    habit_payload = {
        "title": "Exercise",
        "frequency": "daily",
        "target_days_per_week": 7,
        "is_active": True,
    }
    habit_response = client.post("/habits", json=habit_payload, headers=headers)
    habit_id = habit_response.json()["id"]

    first_checkin = client.post(f"/habits/{habit_id}/checkins", json={}, headers=headers)
    assert first_checkin.status_code == 201
    duplicate_response = client.post(f"/habits/{habit_id}/checkins", json={}, headers=headers)
    assert duplicate_response.status_code == 400
    assert "already exists" in duplicate_response.json()["detail"].lower()

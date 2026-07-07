from datetime import date, timedelta


def test_streak_calculation(client):
    user_payload = {"email": "streak@example.com", "password": "streakpass"}
    client.post("/register", json=user_payload)
    login_response = client.post("/login", json=user_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    habit_payload = {
        "title": "Meditate",
        "frequency": "daily",
        "target_days_per_week": 7,
        "is_active": True,
    }
    habit_response = client.post("/habits", json=habit_payload, headers=headers)
    habit_id = habit_response.json()["id"]

    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    client.post(f"/habits/{habit_id}/checkins", json={"date": two_days_ago.isoformat()}, headers=headers)
    client.post(f"/habits/{habit_id}/checkins", json={"date": yesterday.isoformat()}, headers=headers)
    client.post(f"/habits/{habit_id}/checkins", json={"date": today.isoformat()}, headers=headers)

    streak_response = client.get(f"/habits/{habit_id}/streak", headers=headers)
    assert streak_response.status_code == 200
    streak_data = streak_response.json()
    assert streak_data["current_streak"] == 3
    assert streak_data["longest_streak"] == 3
    assert streak_data["total_completed_checkins"] == 3

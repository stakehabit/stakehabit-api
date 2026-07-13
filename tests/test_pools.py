from datetime import date, timedelta


def test_pool_flow(client):
    user_payload = {"email": "pool@example.com", "password": "poolpass"}
    client.post("/register", json=user_payload)
    login_response = client.post("/login", json=user_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    pool_payload = {
        "title": "Streak Pool",
        "description": "Daily goals with shared stakes",
        "duration": 14,
        "stake_amount": "10.0000000",
        "currency": "USD",
        "max_participants": 5,
        "winner_split": 80,
        "charity": "help",
        "creator_address": "GABCDEF1234567890",
    }
    response = client.post("/pools", json=pool_payload, headers=headers)
    assert response.status_code == 201
    pool = response.json()
    assert pool["title"] == "Streak Pool"

    list_response = client.get("/pools")
    assert list_response.status_code == 200
    assert any(item["id"] == pool["id"] for item in list_response.json())

    join_payload = {"wallet_address": "GUSER0000000001"}
    join_response = client.post(f"/pools/{pool['id']}/join", json=join_payload)
    assert join_response.status_code == 200

    duplicate_response = client.post(f"/pools/{pool['id']}/join", json=join_payload)
    assert duplicate_response.status_code == 400
    assert "already joined" in duplicate_response.json()["detail"].lower()

    checkin_payload = {"wallet_address": "GUSER0000000001", "check_in_date": date.today().isoformat()}
    checkin_response = client.post(f"/pools/{pool['id']}/checkin", json=checkin_payload)
    assert checkin_response.status_code == 201

    history_response = client.get(f"/pools/{pool['id']}/checkins/GUSER0000000001")
    assert history_response.status_code == 200
    assert len(history_response.json()) == 1

    # Check that participant leaderboard is available
    participants_response = client.get(f"/pools/{pool['id']}/participants")
    assert participants_response.status_code == 200
    participants = participants_response.json()
    assert participants[0]["wallet_address"] == "GUSER0000000001"
    assert participants[0]["days_completed"] == 1


def test_checkin_duplicate_same_day(client):
    user_payload = {"email": "pool2@example.com", "password": "pool2pass"}
    client.post("/register", json=user_payload)
    login_response = client.post("/login", json=user_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    pool_payload = {
        "title": "Duplicate Checkin Pool",
        "description": "Ensure duplicates are blocked",
        "duration": 7,
        "stake_amount": "5.0000000",
        "currency": "USD",
        "max_participants": 3,
        "winner_split": 50,
        "charity": "care",
        "creator_address": "GCREATOR00000001",
    }
    pool = client.post("/pools", json=pool_payload, headers=headers).json()

    wallet_address = "GUSERCHECK000001"
    client.post(f"/pools/{pool['id']}/join", json={"wallet_address": wallet_address})
    first_checkin = client.post(
        f"/pools/{pool['id']}/checkin",
        json={"wallet_address": wallet_address, "check_in_date": date.today().isoformat()},
    )
    assert first_checkin.status_code == 201

    duplicate = client.post(
        f"/pools/{pool['id']}/checkin",
        json={"wallet_address": wallet_address, "check_in_date": date.today().isoformat()},
    )
    assert duplicate.status_code == 400
    assert "already exists" in duplicate.json()["detail"].lower()

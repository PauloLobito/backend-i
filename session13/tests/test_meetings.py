from tests.conftest import client, meeting_data, action_item_data, created_meeting


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_meeting_success(meeting_data):
    r = client.post("/meetings", json=meeting_data)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == meeting_data["title"]
    assert data["owner"] == meeting_data["owner"]
    assert data["date"] == meeting_data["date"]
    assert "id" in data


def test_create_meeting_missing_title():
    payload = {"date": "2026-03-10", "owner": "Jorge"}
    r = client.post("/meetings", json=payload)
    assert r.status_code == 422


def test_create_meeting_invalid_date():
    payload = {"title": "Planning", "date": "invalid-date", "owner": "Jorge"}
    r = client.post("/meetings", json=payload)
    assert r.status_code == 422


def test_create_action_item_success(created_meeting, action_item_data):
    meeting_id = created_meeting["id"]
    r = client.post(
        f"/meetings/{meeting_id}/action-items",
        json=action_item_data,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["description"] == action_item_data["description"]
    assert data["owner"] == action_item_data["owner"]
    assert data["due_date"] == action_item_data["due_date"]


def test_create_action_item_meeting_not_found(action_item_data):
    r = client.post(
        "/meetings/nonexistent-id/action-items",
        json=action_item_data,
    )
    assert r.status_code == 404


def test_list_meetings(client, created_meeting):
    r = client.get("/meetings")
    assert r.status_code == 200
    data = r.json()
    assert "total" in data
    assert "items" in data
    assert data["total"] >= 1


def test_list_meetings_with_owner(client, created_meeting):
    r = client.get("/meetings?owner=Jorge")
    assert r.status_code == 200
    data = r.json()
    for item in data["items"]:
        assert item["owner"] == "Jorge"


def test_list_meetings_pagination(client):
    r = client.get("/meetings?limit=5&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert data["limit"] == 5
    assert data["offset"] == 0


def test_get_meeting_by_id(created_meeting):
    meeting_id = created_meeting["id"]
    r = client.get(f"/meetings/{meeting_id}")
    assert r.status_code == 200
    assert r.json()["id"] == meeting_id


def test_get_meeting_not_found():
    r = client.get("/meetings/nonexistent-id")
    assert r.status_code == 404

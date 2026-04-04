import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def meeting_data():
    return {
        "title": "Planning",
        "date": "2026-03-10",
        "owner": "Jorge",
        "participants": ["Ana", "Bruno"],
    }


@pytest.fixture
def action_item_data():
    return {
        "description": "Review documentation",
        "owner": "Jorge",
        "due_date": "2026-03-15",
    }


@pytest.fixture
def created_meeting(client, meeting_data):
    response = client.post("/meetings", json=meeting_data)
    return response.json()

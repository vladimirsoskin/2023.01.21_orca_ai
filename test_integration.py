import json

from fastapi.testclient import TestClient
import pytest

from events.cache_db import init_cache
from main import app

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def init_test():
    init_cache()


def test_get_list():
    response = client.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert data.get("list") is not None
    assert len(data.get("list")) == 50
    assert data.get("left") == 50
    assert data.get("amount") == 100


def test_get_list_limit():
    response = client.get("/events?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data.get("list") is not None
    assert len(data.get("list")) == 10
    assert data.get("left") == 90
    assert data.get("amount") == 100


def test_get_list_correct_pages():
    response = client.get("/events?limit=100")
    assert response.status_code == 200
    data = response.json()
    all_events = data.get("list")
    assert all_events is not None
    assert len(all_events) == 100
    assert data.get("left") == 0
    assert data.get("amount") == 100

    response = client.get("/events?limit=50")
    assert response.status_code == 200
    data = response.json()
    events_page_1 = data.get("list")
    assert events_page_1 is not None
    assert len(events_page_1) == 50
    assert data.get("left") == 50
    assert data.get("amount") == 100

    response = client.get(f"/events?limit=50&anchor={events_page_1[-1].get('id')}")
    assert response.status_code == 200
    data = response.json()
    events_page_2 = data.get("list")
    assert events_page_2 is not None
    assert len(events_page_2) == 50
    assert data.get("left") == 0
    assert data.get("amount") == 100

    paginated = [*events_page_1, *events_page_2]
    assert len(paginated) == len(all_events) and json.dumps(paginated) == json.dumps(all_events)

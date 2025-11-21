import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_get_tasks_response_code(client: TestClient):
    resp = client.get("/tasks")
    assert resp.status_code == 200, "Invalid response status code for GET /tasks"


def test_get_tasks_response_format(client: TestClient):
    resp = client.get("/tasks")
    resp_json = resp.json()
    assert isinstance(resp_json, dict)
    assert "result" in resp_json
    assert isinstance(resp_json["result"], list)


def test_get_query_parameters(client: TestClient):
    resp = client.get("/tasks", params={"is_completed": True})
    resp_json = resp.json()
    assert all([task["is_completed"] for task in resp_json["result"]])

    resp = client.get("/tasks", params={"is_completed": False})
    resp_json = resp.json()
    assert all([not task["is_completed"] for task in resp_json["result"]])

    resp = client.get("/tasks", params={"min_priority": 1, "max_priority": 5})
    resp_json = resp.json()
    assert all([1 <= task["priority"] <= 5 for task in resp_json["result"]])

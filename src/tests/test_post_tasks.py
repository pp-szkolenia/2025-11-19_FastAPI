import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_post_tasks(client: TestClient):
    payload = {"description": "Test description", "priority": 3, "is_completed": True}
    resp = client.post("/tasks", json=payload)
    resp_json = resp.json()

    assert resp.status_code == 201, "Invalid response status code for POST /tasks"
    assert isinstance(resp_json, dict)
    assert "message" in resp_json and "details" in resp_json

    new_task_id = resp_json["details"]["task_id"]
    new_task_resp = client.get(f"/tasks/{new_task_id}")
    new_task_resp_json = new_task_resp.json()
    assert new_task_resp_json["result"]["description"] == "Test description"

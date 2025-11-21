import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def create_task_and_get_id(client: TestClient):
    payload = {"description": "test for update", "priority": 1, "is_completed": True}
    resp = client.post("/tasks", json=payload)
    new_task_id = resp.json()["details"]["task_id"]
    return new_task_id


def test_update_task(client: TestClient):
    new_task_id = create_task_and_get_id(client)

    payload = {"description": "updated description", "priority": 3, "is_completed": False}
    resp = client.put(f"/tasks/{new_task_id}", json=payload)
    resp_json_new_value = resp.json()["new_value"]

    assert resp.status_code == 200
    assert resp_json_new_value["description"] == "updated description"
    assert resp_json_new_value["priority"] == 3
    assert resp_json_new_value["is_completed"] is False

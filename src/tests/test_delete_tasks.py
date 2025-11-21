import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def create_task_and_get_id(client: TestClient):
    payload = {"description": "test for delete", "priority": 1, "is_completed": True}
    resp = client.post("/tasks", json=payload)
    new_task_id = resp.json()["details"]["task_id"]
    return new_task_id


def test_delete_task(client: TestClient):
    new_task_id = create_task_and_get_id(client)

    resp = client.delete(f"/tasks/{new_task_id}")
    assert resp.status_code == 204

    resp = client.get(f"/tasks/{new_task_id}")
    assert resp.status_code == 404

from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from app.models import TaskBody
from app.utils import get_item_by_id, get_item_index_by_id


tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_completed": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_completed": False}
]

router = APIRouter()


@router.get("/tasks")
def get_tasks():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": tasks_data})


@router.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    target_task = get_item_by_id(tasks_data, task_id)
    if not target_task:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return JSONResponse(content={"result": target_task}, status_code=status.HTTP_200_OK)


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(body: TaskBody):
    new_task = body.model_dump()
    new_task_id = max(task["id"] for task in tasks_data) + 1
    new_task["id"] = new_task_id
    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}

@router.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int):
    target_index = get_item_index_by_id(tasks_data, task_id)
    if target_index is None:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    tasks_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/tasks/{task_id}")
def update_task_by_id(task_id: int, body: TaskBody):
    target_index = get_item_index_by_id(tasks_data, task_id)

    if target_index is None:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    updated_task = body.model_dump()
    updated_task["id"] = task_id
    tasks_data[target_index] = updated_task

    message = {"message": f"Task with id {task_id} updated", "new_value": updated_task}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)


from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


def get_item_by_id(items_list, item_id):
    return next((item for item in items_list if item["id"] == item_id), None)

def get_item_index_by_id(items_list, item_id):
    return next((i for i, item in enumerate(items_list) if item["id"] == item_id), None)


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
    is_completed: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool


tasks_data = [
    {"id": 1, "description": "Learn FastAPI", "priority": 3, "is_completed": True},
    {"id": 2, "description": "Do exercises", "priority": 2, "is_completed": False}
]

users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False}
]


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/tasks")
def get_tasks():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": tasks_data})


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    target_task = get_item_by_id(tasks_data, task_id)
    if not target_task:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return JSONResponse(content={"result": target_task}, status_code=status.HTTP_200_OK)


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(body: TaskBody):
    new_task = body.model_dump()
    new_task_id = max(task["id"] for task in tasks_data) + 1
    new_task["id"] = new_task_id
    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}

@app.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int):
    target_index = get_item_index_by_id(tasks_data, task_id)
    if target_index is None:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    tasks_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/users")
def get_users():
    return JSONResponse(content={"result": users_data}, status_code=status.HTTP_200_OK)


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    target_user = get_item_by_id(users_data, user_id)
    if not target_user:
        message = {"error": f"User with id {user_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    JSONResponse(content={"result": target_user}, status_code=status.HTTP_200_OK)


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(body: UserBody):
    new_user = body.model_dump()
    new_user_id = max(user["id"] for user in users_data) + 1
    new_user["id"] = new_user_id
    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}


@app.delete("/users/{user_id}")
def delete_user_by_id(user_id: int):
    target_index = get_item_index_by_id(tasks_data, user_id)
    if target_index is None:
        message = {"error": f"User with id {user_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    users_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

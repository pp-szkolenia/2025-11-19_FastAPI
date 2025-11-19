from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class TaskBody(BaseModel):
    description: str
    priority: int
    is_completed: bool


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
    return {"result": tasks_data}


@app.post("/tasks")
def create_task(body: TaskBody):
    new_task = body.model_dump()
    new_task_id = max(task["id"] for task in tasks_data) + 1
    new_task["id"] = new_task_id
    tasks_data.append(new_task)

    return {"message": "New task added", "details": new_task}


@app.get("/users")
def get_users():
    return {"result": users_data}


@app.post("/users")
def create_user(body: UserBody):
    new_user = body.model_dump()
    new_user_id = max(user["id"] for user in users_data) + 1
    new_user["id"] = new_user_id
    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}

from pydantic import BaseModel


class TaskBody(BaseModel):
    description: str
    priority: int | None = None
    is_completed: bool = False


class UserBody(BaseModel):
    username: str
    password: str
    is_admin: bool


class TaskResponse(BaseModel):
    task_id: int
    description: str
    priority: int | None = None
    is_completed: bool


class GetSingleTaskResponse(BaseModel):
    result: TaskResponse


class GetAllTasksResponse(BaseModel):
    result: list[TaskResponse]


class PostTaskResponse(BaseModel):
    message: str
    details: TaskResponse


class PutTaskResponse(BaseModel):
    message: str
    new_value: TaskResponse


class UserResponse(BaseModel):
    user_id: int
    username: str
    password: str
    is_admin: bool


class GetSingleUserResponse(BaseModel):
    result: UserResponse


class GetAllUsersResponse(BaseModel):
    result: list[UserResponse]


class PostUserResponse(BaseModel):
    message: str
    details: UserResponse


class PutUserResponse(BaseModel):
    message: str
    new_value: UserResponse


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int

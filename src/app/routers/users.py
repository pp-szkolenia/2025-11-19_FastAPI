from fastapi import APIRouter, HTTPException, status, Response
from fastapi.responses import JSONResponse

from app.models import UserBody
from app.utils import get_item_by_id, get_item_index_by_id


users_data = [
    {"id": 1, "username": "Andrzej", "password": "qwerty123", "is_admin": True},
    {"id": 2, "username": "Andżela", "password": "hasło1!", "is_admin": False}
]

router = APIRouter(prefix="/users")


@router.get("", tags=["users"])
def get_users():
    return JSONResponse(content={"result": users_data}, status_code=status.HTTP_200_OK)


@router.get("/{user_id}", tags=["users"])
def get_user_by_id(user_id: int):
    target_user = get_item_by_id(users_data, user_id)
    if not target_user:
        message = {"error": f"User with id {user_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    JSONResponse(content={"result": target_user}, status_code=status.HTTP_200_OK)


@router.post("", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(body: UserBody):
    new_user = body.model_dump()
    new_user_id = max(user["id"] for user in users_data) + 1
    new_user["id"] = new_user_id
    users_data.append(new_user)

    return {"message": "New user added", "details": new_user}


@router.delete("/{user_id}", tags=["users"])
def delete_user_by_id(user_id: int):
    target_index = get_item_index_by_id(users_data, user_id)
    if target_index is None:
        message = {"error": f"User with id {user_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    users_data.pop(target_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{user_id}", tags=["users"])
def update_user_by_id(user_id: int, body: UserBody):
    target_index = get_item_index_by_id(users_data, user_id)

    if target_index is None:
        message = {"error": f"User with id {user_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    updated_user = body.model_dump()
    updated_user["id"] = user_id
    users_data[target_index] = updated_user

    message = {"message": f"User with id {user_id} updated", "new_value": updated_user}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)

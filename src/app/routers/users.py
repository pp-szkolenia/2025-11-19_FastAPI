from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc, desc
from typing import Literal

from app.models import (UserBody, UserResponse, GetSingleUserResponse,
                        GetAllUsersResponse, PostUserResponse, PutUserResponse,
                        TokenData)
from db.orm import get_session
from db.models import User
from app.utils import hash_password_in_body
from app import oauth2


router = APIRouter(prefix="/users")


@router.get("", tags=["users"], response_model=GetAllUsersResponse)
def get_users(session: Session = Depends(get_session),
              is_admin: bool | None = None,
              min_password_length: int | None = None,
              sort_by_username: Literal["asc", "desc", None] = Query(
                  None, alias="sortByUsername"
              ),
              user_data: TokenData = Depends(oauth2.get_current_user)):
    if not user_data.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can perform this operation"
        )

    with session:
        users_query = select(User)

        if is_admin is not None:
            users_query = users_query.where(User.is_admin.is_(is_admin))
        if min_password_length is not None:
            users_query = users_query.where(func.char_length(User.password) >= min_password_length)
        if sort_by_username is not None:
            if sort_by_username == "asc":
                sort_func = asc
            elif sort_by_username == "desc":
                sort_func = desc
            users_query = users_query.order_by(sort_func(User.username))

        users_data = session.scalars(users_query).all()

    response_users_data = [
        UserResponse(user_id=user.id_number, username=user.username,
                     password=user.password, is_admin=user.is_admin)
        for user in users_data
    ]
    return {"result": response_users_data}


@router.get("/{user_id}", tags=["users"],
            response_model=GetSingleUserResponse)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    with session:
        stmt = select(User).where(User.id_number == user_id)
        target_user = session.scalars(stmt).first()

    if not target_user:
        message = {"error": f"User with id {user_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    response_target_user = UserResponse(
        user_id=target_user.id_number, username=target_user.username,
        password=target_user.password, is_admin=target_user.is_admin
    )
    return {"result": response_target_user}


@router.post("", status_code=status.HTTP_201_CREATED,
             tags=["users"], response_model=PostUserResponse)
def create_user(body: UserBody, session: Session = Depends(get_session)):
    body = hash_password_in_body(body)

    assert isinstance(body.password, str)

    new_user = User(**body.model_dump())
    with session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    response_new_user = UserResponse(
        user_id=new_user.id_number, username=new_user.username,
        password=new_user.password, is_admin=new_user.is_admin
    )
    return {"message": "New user added", "details": response_new_user}


@router.delete("/{user_id}", tags=["users"])
def delete_user_by_id(user_id: int, session: Session = Depends(get_session)):
    with session:
        stmt = select(User).where(User.id_number == user_id)
        target_user = session.scalars(stmt).first()

        if not target_user:
            message = {"error": f"User with id {user_id} does not exist"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        else:
            session.delete(target_user)
            session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{user_id}", tags=["users"],
            response_model=PutUserResponse)
def update_user_by_id(user_id: int, body: UserBody, session: Session = Depends(get_session),
                      user_data: TokenData = Depends(oauth2.get_current_user)):
    if not (user_data.is_admin or user_data.user_id == user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform this operation")
    with session:
        stmt = select(User).where(User.id_number == user_id)
        target_user = session.scalars(stmt).first()

        if not target_user:
            message = {"error": f"User with id {user_id} does not exist"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        else:
            updated_user = target_user
            body = hash_password_in_body(body)
            for field, value in body.model_dump().items():
                setattr(updated_user, field, value)
            session.commit()
            session.refresh(updated_user)
    response_updated_user = UserResponse(
        user_id=updated_user.id_number, username=updated_user.username,
        password=updated_user.password, is_admin=updated_user.is_admin
    )

    return {"message": f"User with id {user_id} updated",
            "new_value": response_updated_user}

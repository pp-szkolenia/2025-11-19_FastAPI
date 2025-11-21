from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, between, asc, desc
from typing import Literal

from app.models import (TaskBody, TaskResponse, GetAllTasksResponse,
                        GetSingleTaskResponse, PostTaskResponse, PutTaskResponse,
                        TokenData)
from db.orm import get_session
from db.models import Task
from app import oauth2


router = APIRouter()


@router.get("/tasks", response_model=GetAllTasksResponse)
def get_tasks(session: Session = Depends(get_session),
              is_completed: bool | None = None,
              min_priority: int = 1, max_priority: int = 5,
              sort_by_description: Literal["asc", "desc", None] = Query(
                  None, alias="sortByDescription"
              )):
    with session:
        tasks_query = select(Task)

        if is_completed is not None:
            tasks_query = tasks_query.where(Task.is_completed == is_completed)
        tasks_query = tasks_query.where(between(Task.priority, min_priority, max_priority))

        if sort_by_description is not None:
            if sort_by_description == "asc":
                sort_func = asc
            elif sort_by_description == "desc":
                sort_func = desc

            tasks_query = tasks_query.order_by(sort_func(Task.description))

        tasks_data = session.scalars(tasks_query).all()

    response_tasks_data = [
        TaskResponse(task_id=task.id_number, description=task.description,
                     priority=task.priority, is_completed=task.is_completed)
        for task in tasks_data
    ]

    return {"result": response_tasks_data}


@router.get("/tasks/{task_id}", response_model=GetSingleTaskResponse)
def get_task_by_id(task_id: int, session: Session = Depends(get_session)):
    with session:
        stmt = select(Task).where(Task.id_number == task_id)
        target_task = session.scalars(stmt).first()

    if not target_task:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    response_target_task = TaskResponse(
        task_id=target_task.id_number, description=target_task.description,
        priority=target_task.priority, is_completed=target_task.is_completed
    )
    return {"result": response_target_task}


@router.post("/tasks", status_code=status.HTTP_201_CREATED,
             response_model=PostTaskResponse)
def create_task(body: TaskBody, session: Session = Depends(get_session),
                user_data: TokenData = Depends(oauth2.get_current_user)):
    new_task = Task(**body.model_dump())
    with session:
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

    response_new_task = TaskResponse(
        task_id=new_task.id_number, description=new_task.description,
        priority=new_task.priority, is_completed=new_task.is_completed
    )
    return {"message": f"New task added by user {user_data.user_id}",
            "details": response_new_task}


@router.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int, session: Session = Depends(get_session),
                      _: TokenData = Depends(oauth2.get_current_user)):
    with session:
        stmt = select(Task).where(Task.id_number == task_id)
        target_task = session.scalars(stmt).first()

    if not target_task:
        message = {"error": f"Task with id {task_id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    else:
        session.delete(target_task)
        session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/tasks/{task_id}", response_model=PutTaskResponse)
def update_task_by_id(task_id: int, body: TaskBody, session: Session = Depends(get_session),
                      user_data: TokenData = Depends(oauth2.get_current_user)):
    with session:
        stmt = select(Task).where(Task.id_number == task_id)
        target_task = session.scalars(stmt).first()

        if not target_task:
            message = {"error": f"Task with id {task_id} does not exist"}
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        else:
            updated_task = target_task
            for field, value in body.model_dump().items():
                setattr(updated_task, field, value)
            session.commit()
            session.refresh(updated_task)
    response_updated_task = TaskResponse(
        task_id=updated_task.id_number, description=updated_task.description,
        priority=updated_task.priority, is_completed=updated_task.is_completed
    )
    return {"message": f"Task with id {task_id} updated by user {user_data.user_id}",
            "new_value": response_updated_task}

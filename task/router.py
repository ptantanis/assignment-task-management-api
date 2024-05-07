from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud
from .schemas import Task, TaskCreate, TaskFilter, TaskUpdate
from database.database import get_db, engine


router = APIRouter()


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task=task)


@router.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    new_version = Task.model_validate(db_task).model_copy(
        update=task_update.model_dump(exclude_unset=True)
    )
    new_version.version += 1

    return crud.update_task(db, task=new_version)


@router.post("/tasks/{task_id}/undo", response_model=Task)
def undo_task(task_id: UUID, db: Session = Depends(get_db)):
    return crud.undo_task(db, task_id=task_id)


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get("/tasks", response_model=list[Task])
def search_tasks(task_filter: TaskFilter = Depends(), db: Session = Depends(get_db)):
    users = crud.search_tasks(db, task_filter=task_filter)
    return users

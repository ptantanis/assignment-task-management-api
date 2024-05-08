from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from task.errors import CannotUndoTaskError, TaskNotFoundError, TaskVersionConflict
from . import crud
from .schemas import Task, TaskCreate, TaskFilter, TaskUpdate
from database.database import get_db


router = APIRouter()


@router.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task=task)


@router.patch(
    "/tasks/{task_id}", response_model=Task, summary="Partial update task properties"
)
def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    new_version = Task.model_validate(db_task).model_copy(
        update=task_update.model_dump(exclude_unset=True)
    )
    new_version.version += 1
    try:
        return crud.update_task(db, task=new_version)
    except TaskVersionConflict:
        raise HTTPException(status_code=500, detail="Task version conflicted during update")


@router.post(
    "/tasks/{task_id}/undo", response_model=Task, summary="Undo last task update"
)
def undo_task(task_id: UUID, db: Session = Depends(get_db)):
    try:
        return crud.undo_task(db, task_id=task_id)
    except CannotUndoTaskError:
        raise HTTPException(
            status_code=400, detail="Cannot undo task because only one task version"
        )
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.get("/tasks/{task_id}", response_model=Task, summary="Retrieve task by ID")
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get("/tasks", response_model=list[Task], summary="Retrieve tasks by filter")
def search_tasks(task_filter: TaskFilter = Depends(), db: Session = Depends(get_db)):
    users = crud.search_tasks(db, task_filter=task_filter)
    return users

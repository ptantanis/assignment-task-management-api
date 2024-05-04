from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schemas


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def search_tasks(db: Session, task_filter: schemas.TaskFilter):
    query = db.query(models.Task)

    filter = []
    if task_filter.title is not None:
        filter.append(models.Task.title == task_filter.title)

    if task_filter.due_date is not None:
        filter.append(models.Task.due_date == task_filter.due_date)

    if task_filter.status is not None:
        filter.append(models.Task.status == task_filter.status)

    if task_filter.is_deleted is not None:
        filter.append(models.Task.is_deleted == task_filter.is_deleted)

    return query.filter(and_(*filter)).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

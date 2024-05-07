from uuid import UUID
from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schemas


def get_task(db: Session, task_id: UUID):
    return (
        db.query(models.Task)
        .filter(and_(models.Task.id == task_id, models.Task.is_current == True))
        .first()
    )


def search_tasks(db: Session, task_filter: schemas.TaskFilter):
    query = db.query(models.Task)

    filter = [
        models.Task.is_current == True,
        models.Task.is_deleted == task_filter.is_deleted,
    ]
    if task_filter.title is not None:
        filter.append(models.Task.title == task_filter.title)

    if task_filter.due_date is not None:
        filter.append(models.Task.due_date == task_filter.due_date)

    if task_filter.status is not None:
        filter.append(models.Task.status == task_filter.status)

    if task_filter.created_by is not None:
        filter.append(models.Task.created_by == task_filter.created_by)

    if task_filter.updated_by is not None:
        filter.append(models.Task.updated_by == task_filter.updated_by)

    return query.filter(and_(*filter)).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        **task.model_dump(), version=1, is_current=True, is_deleted=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: schemas.Task):
    _update_previous_task_is_current_false(db, task)

    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def undo_task(db: Session, task_id: UUID):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise Exception("task not found")
    if db_task.version == 1:
        raise Exception("Cannot undo")

    db.query(models.Task).filter(
        and_(models.Task.id == task_id, models.Task.version == (db_task.version - 1))
    ).update({models.Task.is_current: True}, synchronize_session=False)

    db.query(models.Task).filter(
        and_(models.Task.id == task_id, models.Task.version == db_task.version)
    ).delete(synchronize_session=False)
    db.commit()
    return get_task(db, task_id=task_id)


def _update_previous_task_is_current_false(db: Session, task: schemas.Task):
    db.query(models.Task).filter(
        and_(models.Task.id == task.id, models.Task.version == (task.version - 1))
    ).update({models.Task.is_current: False}, synchronize_session=False)

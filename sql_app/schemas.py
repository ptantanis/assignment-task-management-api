from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    status: str
    is_deleted: bool


class TaskFilter(BaseModel):
    title: Optional[str] = None
    due_date:  Optional[datetime] = None
    status:  Optional[str] = None
    is_deleted:  Optional[bool] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

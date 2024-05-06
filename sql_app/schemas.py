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
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    is_deleted: Optional[bool] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class TaskCreate(TaskBase):
    created_by: str
    pass


class Task(TaskBase):
    id: int
    created_by: str
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True

from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    status: TaskStatusEnum
    is_deleted: bool


class TaskFilter(BaseModel):
    title: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatusEnum] = None
    is_deleted: Optional[bool] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class TaskCreate(TaskBase):
    created_by: str
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatusEnum] = None
    is_deleted: Optional[bool] = None
    updated_by: str


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    version: int
    is_current: bool
    created_by: str
    updated_by: Optional[str] = None

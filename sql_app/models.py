from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum

from sql_app.schemas import TaskStatusEnum

from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime)
    status = Column(Enum(TaskStatusEnum), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)

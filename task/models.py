import uuid
from sqlalchemy import UUID, Boolean, Column, Integer, String, DateTime, Enum, BINARY

from .schemas import TaskStatusEnum

from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version = Column(Integer, primary_key=True)
    is_current = Column(Boolean, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime)
    status = Column(Enum(TaskStatusEnum), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)

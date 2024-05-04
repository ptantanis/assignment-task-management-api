from sqlalchemy import Boolean, Column, Integer, String, DateTime

from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    due_date = Column(DateTime)
    status = Column(String)
    is_deleted = Column(Boolean, default=False)



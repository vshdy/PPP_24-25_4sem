from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base
import enum
from sqlalchemy import Enum as SQLAEnum

class TaskStatusEnum(str, enum.Enum):
    running = "running"
    completed = "completed"
    failed = "failed"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String)   
    charset = Column(String)
    max_length = Column(Integer)
    status = Column(SQLAEnum(TaskStatusEnum), default=TaskStatusEnum.running)
    progress = Column(Float, default=0.0)
    result = Column(String, nullable=True)

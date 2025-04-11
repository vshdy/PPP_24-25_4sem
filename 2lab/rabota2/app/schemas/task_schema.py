from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    hash: str
    charset: str
    max_length: int

class TaskStatusResponse(BaseModel):
    status: str
    progress: int
    result: Optional[str] = None
    task_id: str

    class Config:
        orm_mode = True

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.models.task_model import Task
from app.services.task_service import brute_force_task
from typing import Optional

router = APIRouter()

class BruteForceRequest(BaseModel):
    hash: str
    charset: str
    max_length: int

class TaskStatusResponse(BaseModel):
    status: str
    progress: float
    result: Optional[str] = None

@router.post("/brut_hash")
async def start_bruteforce(request: BruteForceRequest):
    db = SessionLocal()
    task = Task(hash=request.hash, charset=request.charset, max_length=request.max_length)
    db.add(task)
    db.commit()
    db.refresh(task)
    brute_force_task.delay(task.id, request.hash, request.charset, request.max_length)
    
    return {"task_id": task.id}

@router.get("/get_status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": task.status, "progress": task.progress, "result": task.result}

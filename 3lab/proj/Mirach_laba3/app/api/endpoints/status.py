from fastapi import APIRouter
from app.services.state import get_task_status

router = APIRouter()

@router.get("/status/{task_id}")
def get_status(task_id: str):
    status = get_task_status(task_id)
    return status or {"detail": "Task not found"}

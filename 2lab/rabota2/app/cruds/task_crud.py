from sqlalchemy.orm import Session
from app.models.task_model import Task, TaskStatusEnum


def create_task(db: Session, task_id: str, hash: str, charset: str, max_length: int):
    db_task = Task(task_id=task_id, hash=hash, charset=charset, max_length=max_length)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task_by_id(db: Session, task_db_id: int):
    return db.query(Task).filter(Task.id == task_db_id).first()

def update_task_status(db: Session, task_db_id: int, status: TaskStatusEnum, result: str = None, progress: float = None):
    db_task = db.query(Task).filter(Task.id == task_db_id).first()
    if db_task:
        db_task.status = status
        if result is not None:
            db_task.result = result
        if progress is not None:
            db_task.progress = progress
        db.commit()
        db.refresh(db_task)
    return db_task



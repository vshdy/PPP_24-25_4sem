import json
from app.db.redis_db import redis

def set_task_status(task_id: str, status: str, progress: int = 0, result=None, user_id: str = None, operation: str = None):
    redis.set(task_id, json.dumps({
        "status": status,
        "progress": progress,
        "result": result,
        "user_id": user_id,
        "operation": operation
    }))

    if user_id:
        key = f"user:{user_id}:tasks"

        if task_id.encode() not in redis.lrange(key, 0, -1):
            redis.rpush(key, task_id)



def get_task_status(task_id: str):
    raw = redis.get(task_id)
    return json.loads(raw) if raw else None

def get_user_task_ids(user_id: str):
    return [task.decode() for task in redis.lrange(f"user:{user_id}:tasks", 0, -1)]

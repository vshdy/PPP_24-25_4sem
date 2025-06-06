from fastapi import APIRouter, WebSocket
from app.services.state import get_user_task_ids, get_task_status
from app.db.redis_db import redis
import asyncio
import json

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_by_user(websocket: WebSocket, user_id: str):
    await websocket.accept()
    last_sent = {}

    task_ids = get_user_task_ids(user_id)
    for task_id in task_ids:
        status = get_task_status(task_id)
        if status and status["status"] == "COMPLETED":
            redis.lrem(f"user:{user_id}:tasks", 0, task_id)

    try:
        while True:
            task_ids = get_user_task_ids(user_id)

            for task_id in task_ids:
                status = get_task_status(task_id)
                if not status:
                    continue

                current = json.dumps(status)

                if task_id not in last_sent or last_sent[task_id] != current:
                    await websocket.send_json({"task_id": task_id, **status})
                    last_sent[task_id] = current

            await asyncio.sleep(1)
    except Exception as e:
        print("WebSocket ошибка:", e)
        await websocket.close()




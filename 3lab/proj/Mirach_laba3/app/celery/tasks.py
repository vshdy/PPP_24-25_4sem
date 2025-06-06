from celery import Celery
import time
from app.db.redis_db import redis_socket_path
from app.services.encryption import encrypt_and_encode, decode_and_decrypt
from app.services.state import set_task_status

celery_app = Celery(
    "worker",
    broker=f"redis+socket://{redis_socket_path}",
    backend="db+sqlite:///results.sqlite3"
)

@celery_app.task
def encode_task(payload, task_id):
    user_id = payload.get("user_id", "unknown")

    set_task_status(task_id, "STARTED", 10, user_id=user_id, operation="encode")
    time.sleep(1)

    set_task_status(task_id, "PROGRESS", 40, user_id=user_id, operation="encode")
    time.sleep(1)

    set_task_status(task_id, "PROGRESS", 70, user_id=user_id, operation="encode")
    time.sleep(1)

    result = encrypt_and_encode(payload["text"], payload["key"])

    set_task_status(task_id, "COMPLETED", 100, result=result, user_id=user_id, operation="encode")

@celery_app.task
def decode_task(payload, task_id):
    user_id = payload.get("user_id", "unknown")

    set_task_status(task_id, "STARTED", 10, user_id=user_id, operation="decode")
    time.sleep(1)

    set_task_status(task_id, "PROGRESS", 30, user_id=user_id, operation="decode")
    time.sleep(1)

    set_task_status(task_id, "PROGRESS", 80, user_id=user_id, operation="decode")
    time.sleep(1)

    result = decode_and_decrypt(payload)

    set_task_status(task_id, "COMPLETED", 100, result=result, user_id=user_id, operation="decode")




from fastapi import APIRouter, Depends
from app.schemas.schemas import EncodeRequest, DecodeRequest, EncodeResponse, DecodeResponse
from app.celery.tasks import encode_task, decode_task
from uuid import uuid4
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/encode", response_model=EncodeResponse)
def encode(req: EncodeRequest, user=Depends(get_current_user)):
    task_id = str(uuid4())
    payload = req.dict()
    payload["user_id"] = str(user["id"])
    encode_task.delay(payload, task_id)
    return {"task_id": task_id}

@router.post("/decode", response_model=DecodeResponse)
def decode(req: DecodeRequest, user=Depends(get_current_user)):
    task_id = str(uuid4())
    payload = req.dict()
    payload["user_id"] = str(user["id"])
    decode_task.delay(payload, task_id)
    return {"task_id": task_id}

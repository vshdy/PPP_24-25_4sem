from fastapi import WebSocket
from typing import Dict
import asyncio

store: Dict[str, WebSocket] = {}

async def handle_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    store[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except:
        store.pop(user_id, None)

def get_socket(user_id: str) -> WebSocket | None:
    return store.get(user_id)

async def send_to_user(user_id: str, message: dict):
    socket = get_socket(user_id)
    if socket:
        await socket.send_json(message)

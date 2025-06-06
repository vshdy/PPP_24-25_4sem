from fastapi import FastAPI
from app.api.routes import router as api_router
from app.websocket.routes import router as ws_router

app = FastAPI()
app.include_router(api_router)
app.include_router(ws_router)

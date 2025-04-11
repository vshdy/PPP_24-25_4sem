from fastapi import FastAPI
from app.api.task_api import router as task_api_router
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(task_api_router)

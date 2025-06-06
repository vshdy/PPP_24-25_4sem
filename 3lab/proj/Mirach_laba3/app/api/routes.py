from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.encrypt import router as encrypt_router
from app.api.endpoints.status import router as status_router 

router = APIRouter()
router.include_router(auth_router)
router.include_router(encrypt_router)
router.include_router(status_router) 

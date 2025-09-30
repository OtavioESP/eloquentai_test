from fastapi import APIRouter
from .endpoints import router as users_router
from .endpoints import chat_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/v1/users", tags=["users"])
api_router.include_router(chat_router, prefix="/v1/chat", tags=["chat"])

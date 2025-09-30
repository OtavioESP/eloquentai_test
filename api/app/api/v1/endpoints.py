from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.services.auth_service import AuthService
from database import test_connection

router = APIRouter()

auth_service = AuthService()

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None

@router.post("/login", response_model=LoginResponse)
async def login(user_credentials: UserLogin):
    login_result = auth_service.login_user(user_credentials.username, user_credentials.password)
    
    if not login_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=login_result["message"]
        )
    
    return login_result

@router.post("/unlogged", response_model=LoginResponse)
async def unlogged():
    return auth_service.unlogged_user()

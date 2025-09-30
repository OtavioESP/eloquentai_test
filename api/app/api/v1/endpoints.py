from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService

router = APIRouter()

auth_service = AuthService()
chat_service = ChatService()

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None
    chat: Optional[str] = None

@router.post("/login", response_model=LoginResponse)
async def login(user_credentials: UserLogin):
    login_result = auth_service.login_user(user_credentials.username, user_credentials.password)
    
    if not login_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=login_result["message"]
        )
    
    chatUUID = chat_service.create_new_chat(login_result["user"]["id"])
    login_result["chat"] = chatUUID
    return login_result

@router.post("/unlogged", response_model=LoginResponse)
async def unlogged():

    chatUUID = chat_service.create_new_chat()
    login_result = auth_service.unlogged_user()
    login_result["chat"] = chatUUID

    return login_result


chat_router = APIRouter()

class ChatResponse(BaseModel):
    success: bool
    message: str
    ai_message: str

class Match(BaseModel):
    id: str
    score: float
    metadata: Optional[dict]

class ChatResponse(BaseModel):
    query: str
    matches: List[Match]
    error: Optional[dict]

class ChatRequest(BaseModel):
    message: str
    chatUUID: str


@chat_router.post("/send/message")
async def send_chat_message(request_body: ChatRequest):
    message_content = request_body.message
    chatUUID = request_body.chatUUID
    message_response = await chat_service.send_message(chatUUID, message_content)
    return message_response

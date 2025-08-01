from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import get_settings
from app.user.application.user_service import UserService
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container

settings = get_settings()

router = APIRouter(prefix="/user", tags=["user"])

# OPTIONS 메소드 핸들러 추가 - preflight 요청 처리
@router.options("/login")
async def options_login():
    return {"message": "OK"}

@router.options("/login/test")
async def options_login_test():
    return {"message": "OK"}

class LoginRequest(BaseModel):
    code:str

class LoginTestRequest(BaseModel):
    type:str

@router.post("/login")
@inject
def login(request: LoginRequest, user_service: UserService = Depends(Provide[Container.user_service])):
    result, token, user = user_service.login(request.code)
    if(result):
        return {
            "access_token": token["access_token"], 
            "refresh_token": token["refresh_token"],
            "user": user.model_dump(mode='json')
        }
    else:  
        raise HTTPException(status_code=401, detail="Invalid code")

@router.post("/login/test")
@inject
def login_test(request: LoginTestRequest, user_service: UserService = Depends(Provide[Container.user_service])):
    result, token, user = user_service.login_test(request.type)
    if(result):
        return {
            "access_token": token["access_token"], 
            "refresh_token": token["refresh_token"],
            "user": user.model_dump(mode='json')
        }
    else:  
        raise HTTPException(status_code=401, detail="Invalid code")
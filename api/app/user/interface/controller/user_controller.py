from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import get_settings
from app.user.application.user_service import UserService
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container

settings = get_settings()

router = APIRouter(prefix="/user", tags=["user"])

class LoginRequest(BaseModel):
    code:str

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
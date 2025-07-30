from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.config import get_settings
from app.user.application.user_service import UserService
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container

settings = get_settings()

router = APIRouter(prefix="/stock-price", tags=["stock-price"])

@router.get("/")
# @inject
def stock_price(name:str=Query(None)):
    print(name)

    return {"message": "Hello, World!"}
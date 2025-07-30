from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.config import get_settings
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.dart.application.corp_code_service import DartCorpCodeService

settings = get_settings()

router = APIRouter(prefix="/stock-price", tags=["stock-price"])

@router.get("/")
# @inject
def stock_price(
    name:str=Query(None), 
    corp_code_service: DartCorpCodeService = Depends(Provide[Container.corp_code_service])
    ):
    
    print(name)

    return {"message": "Hello, World!"}
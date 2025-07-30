from fastapi import APIRouter, Query
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from app.stock_price.application.stock_price_service import StockPriceService

router = APIRouter(prefix="/stock-price", tags=["stock-price"])

@router.get("/")
@inject
def stock_price(
    name:str=Query(None), 
    stock_price_service: StockPriceService = Depends(Provide[Container.stock_price_service])
    ):
    stock_price = stock_price_service.get_by_corp_name(name)
    
    return stock_price.model_dump()
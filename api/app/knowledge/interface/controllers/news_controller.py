from fastapi import APIRouter, Depends, Path
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.knowledge.application.news_service import NewsService
from app.knowledge.domain.news import CreateNewsBody

router = APIRouter(prefix="/knowledge/news", tags=["news"])

@router.options("/{type}/latest")
async def options_get_latest_news_date(type: str):
    return {"message": "OK"}

@router.options("/{type}/latest")
async def options_get_latest_news_date(type: str):
    return {"message": "OK"}

@router.get("/{type}/latest", status_code=201, response_model=str)
@inject
def get_latest_news_date(
    news_service: NewsService = Depends(Provide[Container.news_service]),
    type: str = Path(..., description="Type of news"),
):
    news = news_service.find_latest(type)
    if(news is None):
        return "2025-05-01"

    return news.date

@router.post("/", status_code=201)
@inject
async def create_news(
    news: CreateNewsBody,
    news_service: NewsService = Depends(Provide[Container.news_service]),
):
    await news_service.create_news(news.news)
    return {"status": "success"}
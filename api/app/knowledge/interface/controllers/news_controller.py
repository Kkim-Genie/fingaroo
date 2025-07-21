from fastapi import APIRouter, Depends, Path, Request
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from app.containers import Container
from app.knowledge.application.news_service import NewsService
from app.knowledge.domain.news import News, CreateNewsBodyElem, CreateNewsBody

router = APIRouter(prefix="/knowledge/news", tags=["news"])

@router.get("/{type}/latest", status_code=201, response_model=str)
@inject
def get_latest_news_date(
    news_service: NewsService = Depends(Provide[Container.news_service]),
    type: str = Path(..., description="Type of news"),
):
    news = news_service.find_latest(type)

    return news.date

@router.post("/", status_code=201)
@inject
def create_news(
    news: CreateNewsBody,
    news_service: NewsService = Depends(Provide[Container.news_service]),
):
    news_service.create_news(news.news)
from langchain_core.tools import tool
from app.config import get_settings
from app.knowledge.infra.repository.news_repo import NewsRepository
from app.knowledge.application.embeddings_service import EmbeddingsService
from app.knowledge.infra.repository.embeddings_repo import EmbeddingsRepository
from app.knowledge.infra.repository.daily_market_condition_repo import DailyMarketConditionRepository
from app.knowledge.application.daily_market_condition_service import DailyMarketConditionService

settings = get_settings()

@tool
def search_daily_report(date: str) -> str:
    """
    YYYY-MM-DD 형식의 날짜를 입력받아 해당 날짜의 일간 시황을 검색합니다.
    """
    embeddings_repo = EmbeddingsRepository()
    embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)
    daily_market_condition_repo = DailyMarketConditionRepository()
    news_repo = NewsRepository()
    daily_market_condition_service = DailyMarketConditionService(daily_market_condition_repo=daily_market_condition_repo, news_repo=news_repo, embeddings_service=embeddings_service)
    daily_market_condition_list = daily_market_condition_service.find_by_date(date)

    result_str = "\n".join([f"""<document>
    <date>{report.date}</date>
    <content>{report.content}</content>
    </document>\n""" for report in daily_market_condition_list])

    return result_str
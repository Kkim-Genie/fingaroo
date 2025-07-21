from langchain_core.tools import tool
from app.config import get_settings
from app.knowledge.infra.repository.news_repo import NewsRepository
from app.knowledge.application.news_service import NewsService
from app.knowledge.application.embeddings_service import EmbeddingsService
from app.knowledge.infra.repository.embeddings_repo import EmbeddingsRepository

settings = get_settings()

@tool
def search_news(date: str) -> str:
    """
    YYYY-MM-DD 형식의 날짜를 입력받아 해당 날짜의 뉴스를 검색합니다.
    """
    embeddings_repo = EmbeddingsRepository()
    embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)
    news_repo = NewsRepository()
    news_service = NewsService(news_repo=news_repo, embeddings_service=embeddings_service)
    news_list = news_service.find_by_date(date)

    result_str = "\n".join([f"""<document>
    <title>{news.title}</title>
    <link>{news.link}</link>
    <date>{news.date}</date>
    <content>{news.content}</content>
    </document>\n""" for news in news_list])

    return result_str
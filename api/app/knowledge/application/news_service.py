from app.knowledge.domain.repository.news_repo import INewsRepository
from app.knowledge.infra.db_models.news import News
from datetime import datetime
from app.utils.id_utils import generate_nanoid
from app.knowledge.domain.news import CreateNewsBodyElem
from app.knowledge.application.embeddings_service import EmbeddingsService
from app.knowledge.infra.db_models.embeddings import Embeddings

class NewsService:
    def __init__(
        self,
        news_repo: INewsRepository,
        embeddings_service: EmbeddingsService,
    ):
        self.news_repo = news_repo    
        self.embeddings_service = embeddings_service

    def get_first(self) -> News:
        return self.news_repo.get_first()

    def find_by_date(self, date: str) -> list[News]:
        return self.news_repo.find_by_date(date)

    def create(self, news: News):
        return self.news_repo.create(news)

    def find_latest(self, type:str) -> News:
        return self.news_repo.get_latest_news(type)

    async def create_news(self, news_list: list[CreateNewsBodyElem]):
        # Pydantic 모델을 SQLAlchemy 모델로 변환
        db_news_list = []
        embeddings_list = []
        for news_item in news_list:
            news_id = generate_nanoid()
            db_news = News(
                id=news_id,
                title=news_item.title,
                content=news_item.content,
                type=news_item.type,
                link=news_item.link,
                date=news_item.date,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            embedding_contet = f"<document><title>{news_item.title}</title><date>{news_item.date}</date><content>{news_item.content}</content></document>"
            embedding_vector = await self.embeddings_service.make_embeddings(embedding_contet)
            embeddings = Embeddings(
                id=generate_nanoid(),
                date=news_item.date,
                origin_id=news_id,
                origin_type="news",
                content=embedding_contet,
                embedding=embedding_vector
            )
            db_news_list.append(db_news)
            embeddings_list.append(embeddings)

        self.news_repo.create_news(db_news_list)
        self.embeddings_service.create_many(embeddings_list)
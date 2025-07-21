from app.knowledge.domain.repository.daily_market_condition_repo import IDailyMarketConditionRepository
from app.knowledge.infra.db_models.embeddings import Embeddings
from app.knowledge.infra.db_models.daily_market_condition import DailyMarketCondition
from app.utils.knowledge_utils import make_daily_report_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from app.utils.id_utils import generate_nanoid
from datetime import datetime
from app.knowledge.domain.repository.news_repo import INewsRepository
from app.config import get_settings
from app.knowledge.application.embeddings_service import EmbeddingsService

settings = get_settings()

class DailyMarketConditionService:
    def __init__(
        self,
        daily_market_condition_repo: IDailyMarketConditionRepository,
        news_repo: INewsRepository,
        embeddings_service: EmbeddingsService,
    ):
        self.daily_market_condition_repo = daily_market_condition_repo    
        self.news_repo = news_repo
        self.embeddings_service = embeddings_service

    def get_first(self) -> DailyMarketCondition:
        return self.daily_market_condition_repo.get_first()

    def find_by_date(self, date: str) -> list[DailyMarketCondition]:
        return self.daily_market_condition_repo.find_by_date(date)

    def create(self, date_string: str):
        contexts = self.news_repo.get_daily_report_contexts(date_string)
        prompt = make_daily_report_prompt(date_string, contexts)

        llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)
        response = llm.invoke(prompt)
        content = response.content

        report_id = generate_nanoid()
        report = DailyMarketCondition(
            id=report_id,
            date=date_string,
            content=content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.daily_market_condition_repo.create(report)

        embedding = self.embeddings_service.make_embeddings([content], "document")

        embeddings = Embeddings(
            id=generate_nanoid(),
            date=date_string,
            origin_id=report_id,
            origin_type="daily_market_condition",
            content=content,
            embedding=embedding
        )

        self.embeddings_service.create(embeddings)


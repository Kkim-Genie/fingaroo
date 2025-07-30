from app.knowledge.domain.repository.daily_report_repo import IDailyReportRepository
from app.knowledge.infra.db_models.embeddings import Embeddings
from app.knowledge.infra.db_models.daily_report import DailyReport
from app.utils.knowledge_utils import make_daily_report_prompt
from langchain_naver import ChatClovaX
from app.utils.id_utils import generate_nanoid
from datetime import datetime
from app.knowledge.domain.repository.news_repo import INewsRepository
from app.config import get_settings
from app.knowledge.application.embeddings_service import EmbeddingsService

settings = get_settings()

class DailyReportService:
    def __init__(
        self,
        daily_report_repo: IDailyReportRepository,
        news_repo: INewsRepository,
        embeddings_service: EmbeddingsService,
    ):
        self.daily_report_repo = daily_report_repo    
        self.news_repo = news_repo
        self.embeddings_service = embeddings_service

    def get_first(self) -> DailyReport:
        return self.daily_report_repo.get_first()

    def find_by_date(self, date: str) -> list[DailyReport]:
        return self.daily_report_repo.find_by_date(date)

    async def create(self, date_string: str):
        contexts = self.news_repo.get_daily_report_contexts(date_string)
        prompt = make_daily_report_prompt(date_string, contexts)

        llm = ChatClovaX(
            model=settings.LLM_MODEL_BASE, 
            api_key=settings.CLOVASTUDIO_API_KEY
        )
        response = llm.invoke(prompt)
        content = response.content

        report_id = generate_nanoid()
        report = DailyReport(
            id=report_id,
            date=date_string,
            content=content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.daily_report_repo.create(report)

        embedding = await self.embeddings_service.make_embeddings(content)

        embeddings = Embeddings(
            id=generate_nanoid(),
            date=date_string,
            origin_id=report_id,
            origin_type="daily_report",
            content=content,
            embedding=embedding
        )

        self.embeddings_service.create(embeddings)


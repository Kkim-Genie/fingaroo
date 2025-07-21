from app.knowledge.domain.repository.daily_market_condition_repo import IDailyMarketConditionRepository
from app.knowledge.infra.db_models.embeddings import Embeddings
from app.knowledge.infra.db_models.daily_market_condition import DailyMarketCondition
from app.utils.knowledge_utils import make_daily_report_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from app.utils.id_utils import generate_nanoid
from datetime import datetime, timedelta
from app.knowledge.domain.repository.news_repo import INewsRepository
from app.config import get_settings
from app.knowledge.application.embeddings_service import EmbeddingsService
from app.knowledge.domain.repository.weekly_report_repo import IWeeklyReportRepository
from app.knowledge.infra.db_models.weekly_report import WeeklyReport
from app.utils.knowledge_utils import make_weekly_report_prompt


settings = get_settings()

class WeeklyReportService:
    def __init__(
        self,
        weekly_report_repo: IWeeklyReportRepository,
        daily_market_condition_repo: IDailyMarketConditionRepository,
        news_repo: INewsRepository,
        embeddings_service: EmbeddingsService,
    ):
        self.weekly_report_repo = weekly_report_repo
        self.daily_market_condition_repo = daily_market_condition_repo    
        self.news_repo = news_repo
        self.embeddings_service = embeddings_service

    def get_first(self) -> WeeklyReport:
        return self.weekly_report_repo.get_first()

    def find_by_end_date(self, date: str) -> WeeklyReport:
        return self.weekly_report_repo.find_by_end_date(date)

    def create(self, end_date_string: str):
        news_contexts, news_ids = self.news_repo.get_weekly_report_contexts(end_date_string)
        market_contexts, market_analysis_ids = self.daily_market_condition_repo.get_weekly_report_contexts(end_date_string)
        prompt = make_weekly_report_prompt(end_date_string, news_contexts, market_contexts)

        llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)
        response = llm.invoke(prompt)
        content = response.content

        start_date = datetime.strptime(end_date_string, '%Y-%m-%d').date() - timedelta(days=6)

        report_id = generate_nanoid()
        report = WeeklyReport(
            id=report_id,
            start_date=start_date.isoformat(),
            end_date=end_date_string,
            content=content,
            market_analysis_ids=market_analysis_ids,
            news_ids=news_ids,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.weekly_report_repo.create(report)

        embedding = self.embeddings_service.make_embeddings([content], "document")

        embeddings = Embeddings(
            id=generate_nanoid(),
            date=end_date_string,
            origin_id=report_id,
            origin_type="weekly_report",
            content=content,
            embedding=embedding
        )

        self.embeddings_service.create(embeddings)
        self.embeddings_service.delete_embeddings_based_weekly_report(end_date_string)


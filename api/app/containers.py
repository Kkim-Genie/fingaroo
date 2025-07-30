from dependency_injector import containers, providers

from app.knowledge.infra.repository.embeddings_repo import EmbeddingsRepository
from app.knowledge.application.embeddings_service import EmbeddingsService
from app.knowledge.infra.repository.news_repo import NewsRepository
from app.knowledge.application.news_service import NewsService
from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.application.report_principal_service import DartReportPrincipalService
from app.dart.application.report_economy_service import DartReportEconomyService
from app.dart.application.report_event_service import DartReportEventService
from app.knowledge.infra.repository.daily_market_condition_repo import DailyMarketConditionRepository
from app.knowledge.application.daily_market_condition_service import DailyMarketConditionService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.dart",
            "app.knowledge",
        ],
        modules=[
            "app.dart.interface.controllers.dart_controller",
            "app.chat.interface.controllers.chat_controller",
            "app.knowledge.interface.controllers.news_controller",
        ]
    )

    corp_code_repo = providers.Factory(DartCorpCodeRepository)
    corp_code_service = providers.Factory(DartCorpCodeService, corp_code_repo=corp_code_repo)
    dart_report_principal_service = providers.Factory(DartReportPrincipalService, corp_code_service=corp_code_service)
    dart_report_economy_service = providers.Factory(DartReportEconomyService, corp_code_service=corp_code_service)
    dart_report_event_service = providers.Factory(DartReportEventService, corp_code_service=corp_code_service)

    embeddings_repo = providers.Factory(EmbeddingsRepository)
    embeddings_service = providers.Factory(EmbeddingsService, embeddings_repo=embeddings_repo)

    news_repo = providers.Factory(NewsRepository)
    news_service = providers.Factory(NewsService, news_repo=news_repo, embeddings_service=embeddings_service)

    daily_market_condition_repo = providers.Factory(DailyMarketConditionRepository)
    daily_market_condition_service = providers.Factory(DailyMarketConditionService, daily_market_condition_repo=daily_market_condition_repo, news_repo=news_repo, embeddings_service=embeddings_service)

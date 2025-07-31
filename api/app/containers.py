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
from app.knowledge.infra.repository.daily_report_repo import DailyReportRepository
from app.knowledge.application.daily_report_service import DailyReportService
from app.user.infra.repository.user_repo import UserRepository
from app.user.application.user_service import UserService
from app.stock_price.application.stock_price_service import StockPriceService
from app.invest_log.infra.repository.user_asset_repo import UserAssetRepository
from app.invest_log.application.user_asset_service import UserAssetService
from app.invest_log.infra.repository.invest_log_repo import InvestLogRepository
from app.invest_log.application.invest_log_service import InvestLogService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.dart",
            "app.chat",
            "app.knowledge",
            "app.user",
        ],
        modules=[
            "app.dart.interface.controllers.dart_controller",
            "app.chat.interface.controllers.chat_controller",
            "app.knowledge.interface.controllers.news_controller",
            "app.user.interface.controller.user_controller",
            "app.stock_price.interface.controller.stock_price_controller",
            "app.invest_log.interface.controller.user_asset_controller",
            "app.invest_log.interface.controller.invest_log_controller",
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

    daily_report_repo = providers.Factory(DailyReportRepository)
    daily_report_service = providers.Factory(DailyReportService, daily_report_repo=daily_report_repo, news_repo=news_repo, embeddings_service=embeddings_service)

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)

    stock_price_service = providers.Factory(StockPriceService, corp_code_service=corp_code_service)

    user_asset_repo = providers.Factory(UserAssetRepository)
    user_asset_service = providers.Factory(UserAssetService, user_asset_repo=user_asset_repo)

    invest_log_repo = providers.Factory(InvestLogRepository)
    invest_log_service = providers.Factory(InvestLogService, invest_log_repo=invest_log_repo)
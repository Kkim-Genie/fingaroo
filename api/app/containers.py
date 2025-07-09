from dependency_injector import containers, providers

from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.application.report_principal_service import DartReportPrincipalService
from app.dart.application.report_economy_service import DartReportEconomyService
from app.dart.application.report_event_service import DartReportEventService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.dart",
        ],
        modules=[
            "app.dart.interface.controllers.dart_controller",
            "app.chat.interface.controllers.chat_controller"
        ]
    )

    corp_code_repo = providers.Factory(DartCorpCodeRepository)
    corp_code_service = providers.Factory(DartCorpCodeService, corp_code_repo=corp_code_repo)
    dart_report_principal_service = providers.Factory(DartReportPrincipalService, corp_code_service=corp_code_service)
    dart_report_economy_service = providers.Factory(DartReportEconomyService, corp_code_service=corp_code_service)
    dart_report_event_service = providers.Factory(DartReportEventService, corp_code_service=corp_code_service)
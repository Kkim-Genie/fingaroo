from langchain_core.tools import tool
from app.config import get_settings
from app.dart.domain.company_merge import get_company_merge_description
from app.dart.application.report_event_service import DartReportEventService
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository

settings = get_settings()

tool_description = f"""
### tool description
{get_company_merge_description()}

### tool input
corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
"""

@tool(description=tool_description)
def company_merge_tool(corp_name: str, bgn_de: str, end_de: str) -> str:
    # Initialize services
    corp_code_repo = DartCorpCodeRepository()
    corp_code_service = DartCorpCodeService(corp_code_repo=corp_code_repo)
    dart_report_event_service = DartReportEventService(corp_code_service=corp_code_service)

    # Get both capital decision data
    result = dart_report_event_service.get_company_merge(corp_name, bgn_de, end_de)

    result_str = f"<dart_result>{result.model_dump_json()}</dart_result>"

    return result_str
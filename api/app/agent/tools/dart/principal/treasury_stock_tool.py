from langchain_core.tools import tool
from app.config import get_settings
from app.dart.application.report_principal_service import DartReportPrincipalService
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository
from app.dart.domain.treasury_stock import get_treasury_stock_description

settings = get_settings()

tool_description = f"""
### tool description
{get_treasury_stock_description()}

### tool input
corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
bsns_year: int,  # 사업연도(4자리, 예: 2023)
reprt_code: str  # 보고서 코드(1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011)
"""

@tool(description=tool_description)
def treasury_stock_tool(corp_name: str, bsns_year: int, reprt_code: str) -> str:
    # Initialize services
    corp_code_repo = DartCorpCodeRepository()
    corp_code_service = DartCorpCodeService(corp_code_repo=corp_code_repo)
    dart_report_principal_service = DartReportPrincipalService(corp_code_service=corp_code_service)

    # Get both capital decision data
    result = dart_report_principal_service.get_treasury_stock(corp_name, bsns_year, reprt_code)

    result_str = f"<dart_result>{result.model_dump_json()}</dart_result>"

    return result_str
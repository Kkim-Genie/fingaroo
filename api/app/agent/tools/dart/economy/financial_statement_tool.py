from langchain_core.tools import tool
from app.config import get_settings
from app.dart.domain.financial_statement import get_financial_statement_description
from app.dart.application.report_economy_service import DartReportEconomyService
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository

settings = get_settings()

tool_description = f"""
### tool description
{get_financial_statement_description()}

### tool input
corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
bsns_year: int,  # 사업연도(4자리, 예: 2023)
reprt_code: str  # 보고서 코드(1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011)
fs_div: str  # 재무제표 구분(OFS: 재무상태표, IS: 손익계산서, CF: 현금흐름표)
"""

@tool(description=tool_description)
def financial_statement_tool(corp_name: str, bsns_year: int, reprt_code: str, fs_div: str) -> str:
    # Initialize services
    corp_code_repo = DartCorpCodeRepository()
    corp_code_service = DartCorpCodeService(corp_code_repo=corp_code_repo)
    dart_report_economy_service = DartReportEconomyService(corp_code_service=corp_code_service)

    # Get both capital decision data
    result = dart_report_economy_service.get_financial_statement(corp_name, bsns_year, reprt_code, fs_div)

    result_str = f"<dart_result>{result.model_dump_json()}</dart_result>"

    return result_str
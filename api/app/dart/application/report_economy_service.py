import requests
from app.config import get_settings
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.domain.single_company_account import DartSingleCompanyAccount
from app.dart.domain.multi_company_account import DartMultiCompanyAccount
from app.dart.domain.financial_statement import DartFinancialStatement
from app.dart.domain.single_financial_indicator import DartSingleFinancialIndicator

settings = get_settings()

class DartReportEconomyService:
    def __init__(
        self,
        corp_code_service: DartCorpCodeService,
    ):
        self.corp_code_service = corp_code_service

    def _build_dart_params(self, corp_code: str, bsns_year: int, reprt_code: str) -> dict:
        """DART API 공통 파라미터를 구성합니다."""
        return {
            "crtfc_key": settings.DART_API_KEY,
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code
        }

    def get_single_company_account(
        self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str  # 보고서 코드(예: 11011, 11012, 11013, 11014)
    ) -> DartSingleCompanyAccount:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code
        
        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        response = requests.get("https://opendart.fss.or.kr/api/fnlttSinglAcnt.json", params=params)
        result = response.json()
        return DartSingleCompanyAccount(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_multi_company_account(
        self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str  # 보고서 코드(예: 11011, 11012, 11013, 11014)
    ) -> DartMultiCompanyAccount:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        response = requests.get("https://opendart.fss.or.kr/api/fnlttMultiAcnt.json", params=params)
        result = response.json()
        return DartMultiCompanyAccount(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_financial_statement(
        self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str,  # 보고서 코드(예: 11011, 11012, 11013, 11014)
        fs_div: str  # 개별/연결구분 (OFS:재무제표, CFS:연결재무제표)
    ) -> DartFinancialStatement:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        params["fs_div"] = fs_div

        response = requests.get("https://opendart.fss.or.kr/api/fnlttSinglAcnt.json", params=params)
        result = response.json()

        return DartFinancialStatement(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_single_financial_indicator(
        self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str,  # 보고서 코드(예: 11011, 11012, 11013, 11014)
        idx_cl_code: str,  # 지표분류코드 (수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000)
    ) -> DartSingleFinancialIndicator:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        params["idx_cl_code"] = idx_cl_code

        response = requests.get("https://opendart.fss.or.kr/api/fnlttSinglIndx.json", params=params)
        result = response.json()
        return DartSingleFinancialIndicator(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )
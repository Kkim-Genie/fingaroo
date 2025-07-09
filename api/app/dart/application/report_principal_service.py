from app.dart.application.corp_code_service import DartCorpCodeService
import requests
from app.config import get_settings
from app.dart.domain.changed_capital import DartChangedCapital
from app.dart.domain.dividend import DartDividend
from app.dart.domain.treasury_stock import DartTreasuryStock
from app.dart.domain.total_stock import DartTotalStock
from app.dart.domain.multi_financial_indicator import DartMultiFinancialIndicator

settings = get_settings()

class DartReportPrincipalService:
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

    def get_changed_capital(self, 
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str  # 보고서 코드(예: 11011, 11012, 11013, 11014)
    ) -> DartChangedCapital:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code
        
        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        response = requests.get("https://opendart.fss.or.kr/api/irdsSttus.json", params=params)
        result = response.json()
        return DartChangedCapital(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_dividend(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str  # 보고서 코드(예: 11011, 11012, 11013, 11014)
    ) -> DartDividend:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code
        
        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        response = requests.get("https://opendart.fss.or.kr/api/alotMatter.json", params=params)
        result = response.json()
        return DartDividend(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_treasury_stock(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str  # 보고서 코드(예: 11011, 11012, 11013, 11014)
    ) -> DartTreasuryStock:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code
        
        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        response = requests.get("https://opendart.fss.or.kr/api/tesstkAcqsDspsSttus.json", params=params)
        result = response.json()
        print(result)
        return DartTreasuryStock(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_total_stock(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str  # 보고서 코드(예: 11011, 11012, 11013, 11014)
    ) -> DartTotalStock:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code
        
        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        response = requests.get("https://opendart.fss.or.kr/api/stockTotqySttus.json", params=params)
        result = response.json()
        return DartTotalStock(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_multi_financial_indicator(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bsns_year: int,  # 사업연도(4자리, 예: 2023)
        reprt_code: str,  # 보고서 코드(예: 11011, 11012, 11013, 11014)
        idx_cl_code: str  # 지표분류코드 (수익성지표: M210000, 안정성지표: M220000, 성장성지표: M230000, 활동성지표: M240000)
    ) -> DartMultiFinancialIndicator:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bsns_year, reprt_code)
        params["idx_cl_code"] = idx_cl_code

        response = requests.get("https://opendart.fss.or.kr/api/fnlttCmpnyIndx.json", params=params)
        result = response.json()
        return DartMultiFinancialIndicator(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )
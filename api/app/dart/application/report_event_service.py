from app.config import get_settings
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.domain.paid_capital_decision import DartPaidCapitalDecision
from app.dart.domain.free_capital_decision import DartFreeCapitalDecision
from app.dart.domain.both_capital_decision import DartBothCapitalDecision
from app.dart.domain.law_suit import DartLawSuit
from app.dart.domain.convertible_bond import DartConvertibleBond
from app.dart.domain.stock_buyback import DartStockBuyback
from app.dart.domain.stock_retirement import DartStockRetirement
from app.dart.domain.company_merge import DartCompanyMerge
from app.dart.domain.company_divide import DartCompanyDivide
from app.dart.domain.company_divide_merge import DartCompanyDivideMerge
import requests

settings = get_settings()

class DartReportEventService:
    def __init__(
        self,
        corp_code_service: DartCorpCodeService,
    ):
        self.corp_code_service = corp_code_service

    def _build_dart_params(self, corp_code: str, bgn_de: str, end_de: str) -> dict:
        """DART API 공통 파라미터를 구성합니다."""
        return {
            "crtfc_key": settings.DART_API_KEY,
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de
        }

    def get_paid_capital_decision(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartPaidCapitalDecision:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/piicDecsn.json", params=params)
        result = response.json()
        return DartPaidCapitalDecision(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_free_capital_decision(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartFreeCapitalDecision:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/fricDecsn.json", params=params)
        result = response.json()
        return DartFreeCapitalDecision(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_both_capital_decision(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartBothCapitalDecision:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/pifricDecsn.json", params=params)
        result = response.json()
        return DartBothCapitalDecision(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_law_suit(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartLawSuit:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/lwstLg.json", params=params)
        result = response.json()
        return DartLawSuit(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_convertible_bond(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartConvertibleBond:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/cvbdIsDecsn.json", params=params)
        result = response.json()
        return DartConvertibleBond(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_stock_buyback(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartStockBuyback:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/tsstkAqDecsn.json", params=params)
        result = response.json()
        return DartStockBuyback(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_stock_retirement(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartStockRetirement:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/tsstkDpDecsn.json", params=params)
        result = response.json()
        return DartStockRetirement(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_company_merge(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartCompanyMerge:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/cmpMgDecsn.json", params=params)
        result = response.json()
        print(result)
        return DartCompanyMerge(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_company_divide(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartCompanyDivide:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/cmpDvDecsn.json", params=params)
        result = response.json()
        return DartCompanyDivide(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )

    def get_company_divide_merge(self,
        corp_name: str,  # 조회할 회사명 (내부적으로 고유번호로 변환)
        bgn_de: str,  # 시작일(최초접수일)	(검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
        end_de: str  # 종료일(최초접수일)(검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공)
    ) -> DartCompanyDivideMerge:
        obj = self.corp_code_service.find_by_corp_name(corp_name)
        corp_code = obj.corp_code

        params = self._build_dart_params(corp_code, bgn_de, end_de)

        response = requests.get("https://opendart.fss.or.kr/api/cmpDvmgDecsn.json", params=params)
        result = response.json()
        return DartCompanyDivideMerge(
            status=result["status"],
            message=result["message"],
            list=result.get("list", [])
        )
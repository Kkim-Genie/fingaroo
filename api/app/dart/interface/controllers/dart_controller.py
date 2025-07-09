from datetime import datetime
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.containers import Container
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.application.report_principal_service import DartReportPrincipalService
from app.dart.domain.changed_capital import DartChangedCapital
from app.dart.domain.dividend import DartDividend
from app.dart.domain.treasury_stock import DartTreasuryStock
from app.dart.domain.total_stock import DartTotalStock
from app.dart.domain.single_company_account import DartSingleCompanyAccount
from app.dart.domain.multi_company_account import DartMultiCompanyAccount
from app.dart.domain.financial_statement import DartFinancialStatement
from app.dart.domain.single_financial_indicator import DartSingleFinancialIndicator
from app.dart.domain.multi_financial_indicator import DartMultiFinancialIndicator
from app.dart.application.report_economy_service import DartReportEconomyService
from app.dart.application.report_event_service import DartReportEventService
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

router = APIRouter(prefix="/dart")

class DartCorpCodeResponse(BaseModel):
    id: str
    corp_code: str
    corp_name: str
    corp_eng_name: str
    stock_code: str | None
    created_at: datetime
    updated_at: datetime

class DartChangedCapitalResponse(BaseModel):
    status: str
    message: str
    list: list


@router.get("", status_code=201, response_model=DartCorpCodeResponse)
@inject
def get_first(
    corp_code_service: DartCorpCodeService = Depends(Provide[Container.corp_code_service]),
):
    corp_code = corp_code_service.find_by_corp_name("신세계")

    return corp_code

@router.get("/changed-capital", status_code=201, response_model=DartChangedCapital)
@inject
def get_changed_capital(
    dart_report_principal_service: DartReportPrincipalService = Depends(Provide[Container.dart_report_principal_service]),
):
    result = dart_report_principal_service.get_changed_capital("더본코리아", 2024, "11011")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result


@router.get("/dividend", status_code=201, response_model=DartDividend)
@inject
def get_dividend(
    dart_report_principal_service: DartReportPrincipalService = Depends(Provide[Container.dart_report_principal_service]),
):
    result = dart_report_principal_service.get_dividend("더본코리아", 2024, "11011")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/treasury-stock", status_code=201, response_model=DartTreasuryStock)
@inject
def get_treasury_stock(
    dart_report_principal_service: DartReportPrincipalService = Depends(Provide[Container.dart_report_principal_service]),
):
    result = dart_report_principal_service.get_treasury_stock("더본코리아", 2024, "11011")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/total-stock", status_code=201, response_model=DartTotalStock)
@inject
def get_total_stock(
    dart_report_principal_service: DartReportPrincipalService = Depends(Provide[Container.dart_report_principal_service]),
):
    result = dart_report_principal_service.get_total_stock("더본코리아", 2024, "11011")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/single-company-account", status_code=201, response_model=DartSingleCompanyAccount)
@inject
def get_single_company_account(
    dart_report_economy_service: DartReportEconomyService = Depends(Provide[Container.dart_report_economy_service]),
):
    result = dart_report_economy_service.get_single_company_account("더본코리아", 2024, "11011")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/multi-company-account", status_code=201, response_model=DartMultiCompanyAccount)
@inject
def get_multi_company_account(
    dart_report_economy_service: DartReportEconomyService = Depends(Provide[Container.dart_report_economy_service]),
):
    result = dart_report_economy_service.get_multi_company_account("더본코리아", 2024, "11011")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result
    
@router.get("/financial-statement", status_code=201, response_model=DartFinancialStatement)
@inject
def get_financial_statement(
    dart_report_economy_service: DartReportEconomyService = Depends(Provide[Container.dart_report_economy_service]),
):
    result = dart_report_economy_service.get_financial_statement("더본코리아", 2024, "11011", "OFS")
    print(result)

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/single-financial-indicator", status_code=201, response_model=DartSingleFinancialIndicator)
@inject
def get_single_financial_indicator(
    dart_report_economy_service: DartReportEconomyService = Depends(Provide[Container.dart_report_economy_service]),
):
    result = dart_report_economy_service.get_single_financial_indicator("더본코리아", 2024, "11011", "M210000")
    
    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/multi-financial-indicator", status_code=201, response_model=DartMultiFinancialIndicator)
@inject
def get_multi_financial_indicator(
    dart_report_principal_service: DartReportPrincipalService = Depends(Provide[Container.dart_report_principal_service]),
):
    result = dart_report_principal_service.get_multi_financial_indicator("더본코리아", 2024, "11011", "M210000")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/paid-capital-decision", status_code=201, response_model=DartPaidCapitalDecision)
@inject
def get_paid_capital_decision(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_paid_capital_decision("3S", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/free-capital-decision", status_code=201, response_model=DartFreeCapitalDecision)
@inject
def get_free_capital_decision(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_free_capital_decision("미원상사", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/both-capital-decision", status_code=201, response_model=DartBothCapitalDecision)
@inject
def get_both_capital_decision(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_both_capital_decision("헬릭스미스", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/law-suit", status_code=201, response_model=DartLawSuit)
@inject
def get_law_suit(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_law_suit("HD한국조선해양", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/convertible-bond", status_code=201, response_model=DartConvertibleBond)
@inject
def get_convertible_bond(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_convertible_bond("풀무원", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/stock-buyback", status_code=201, response_model=DartStockBuyback)
@inject
def get_stock_buyback(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_stock_buyback("현대자동차", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/stock-retirement", status_code=201, response_model=DartStockRetirement)
@inject
def get_stock_retirement(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_stock_retirement("미원상사", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/company-merge", status_code=201, response_model=DartCompanyMerge)
@inject
def get_company_merge(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_company_merge("POSCO홀딩스", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/company-divide", status_code=201, response_model=DartCompanyDivide)
@inject
def get_company_divide(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_company_divide("NAVER", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result

@router.get("/company-divide-merge", status_code=201, response_model=DartCompanyDivideMerge)
@inject
def get_company_divide_merge(
    dart_report_event_service: DartReportEventService = Depends(Provide[Container.dart_report_event_service]),
):
    result = dart_report_event_service.get_company_divide_merge("포스코에너지", "20150101", "20201231")

    if result.status == "013":
        return {
            "status": "no_data",
            "message": "조회된 데이터가 없습니다.",
            "list": []
        }

    return result
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import Field


class DartChangedCapitalItem(BaseModel):
    recept_no: Optional[str] = Field(default=None)   # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)   # 법인구분 (Y:유가, K:코스닥, N:코넥스, E:기타)
    corp_code: Optional[str] = Field(default=None)   # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)   # 법인명
    isu_dcrs_de: Optional[str] = Field(default=None)   # 주식변경 감소일자
    isu_dcrs_stle: Optional[str] = Field(default=None)   # 발행 감소 형태
    isu_dcrs_stock_knd: Optional[str] = Field(default=None)   # 발행 감소 주식 종류
    isu_dcrs_qy: Optional[str] = Field(default=None)   # 발행 감소 수량
    isu_dcrs_mstvdv_fval_amount: Optional[str] = Field(default=None)   # 발행 감소 주당 액면 가액
    isu_dcrs_mstvdv_amount: Optional[str] = Field(default=None)   # 발행 감소 주당 가액
    stlm_dt: Optional[str] = Field(default=None)   # 결산기준일 (YYYY-MM-DD)

class DartChangedCapital(BaseModel):
    status: str #000 정상 013 데이터 없음
    message: str # 메시지
    list: list[DartChangedCapitalItem]

def get_changed_capital_description():
    return """
    자본금 변동

    이 API는 기업의 자본금 변화에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 기업코드: 공시대상회사의 고유번호 (8자리)
       - 법인명: 공시대상회사명

    2. 자본금 감소 정보
       - 주식변경 감소일자: 자본금 감소가 발생한 날짜
       - 발행 감소 형태: 자본금 감소의 형태 (예: 주식소각, 주식병합 등)
       - 발행 감소 주식 종류: 감소 대상 주식 종류 (보통주, 우선주 등)
       - 발행 감소 수량: 감소되는 주식 수량
       - 발행 감소 주당 액면 가액: 감소 주식의 주당 액면가액
       - 발행 감소 주당 가액: 감소 주식의 주당 실제 가액
       - 결산기준일: 해당 공시의 결산 기준일

    자본금 감소의 주요 형태:
    - 주식소각: 회사가 보유한 자기주식을 소각하여 자본금 감소
    - 주식병합: 여러 주식을 하나로 합쳐서 총 주식수 감소
    - 자본감소: 회사가 자본금을 줄여서 주주에게 현금 배당
    - 무상감자: 주주에게 대가 없이 자본금 감소

    활용 방안:
    - 기업의 자본구조 변화 분석
    - 주주 가치에 미치는 영향 평가
    - 기업의 재무 정책 변화 추적
    - 투자 위험도 평가
    - 기업의 자본 효율성 분석
    - 주가 변동 요인 분석
    """
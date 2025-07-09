from pydantic import BaseModel, Field
from typing import Optional

class DartFreeCapitalDecisionItem(BaseModel):
    recept_no: Optional[str] = Field(default=None)  # 접수번호
    corp_cls: Optional[str] = Field(default=None)  # 법인구분
    corp_code: Optional[str] = Field(default=None)  # 고유번호
    corp_name: Optional[str] = Field(default=None)  # 회사명
    nstk_ostk_cnt: Optional[str] = Field(default=None)  # 신주의 종류와 수(보통주식)
    nstk_estk_cnt: Optional[str] = Field(default=None)  # 신주의 종류와 수(기타주식)
    fv_ps: Optional[str] = Field(default=None)  # 1주당 액면가액(원)
    bfic_tisstk_ostk: Optional[str] = Field(default=None)  # 증자전 발행주식총수(보통주식)
    bfic_tisstk_estk: Optional[str] = Field(default=None)  # 증자전 발행주식총수(기타주식)
    nstk_asstd: Optional[str] = Field(default=None)  # 신주배정기준일
    nstk_ascnt_ps_ostk: Optional[str] = Field(default=None)  # 1주당 신주배정 주식수(보통주식)
    nstk_ascnt_ps_estk: Optional[str] = Field(default=None)  # 1주당 신주배정 주식수(기타주식)
    nstk_dividkr: Optional[str] = Field(default=None)  # 신주의 배당기산일
    nstk_dlprd: Optional[str] = Field(default=None)  # 신주권교부예정일
    nstk_lstprd: Optional[str] = Field(default=None)  # 신주의 상장 예정일
    bddd: Optional[str] = Field(default=None)  # 
    od_a_a_t_t: Optional[str] = Field(default=None)  # 사외이사 참석여부(참석)
    od_a_a_t_b: Optional[str] = Field(default=None)  # 사외이사 참석여부(불참)
    adt_a_atn: Optional[str] = Field(default=None)  # 감사(사외이원)참석 여부

class DartFreeCapitalDecision(BaseModel):
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: list[DartFreeCapitalDecisionItem]  # 결과 리스트

def get_free_capital_decision_description():
    return """
    무상증자 결정

    이 API는 기업의 무상증자 결정에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호
       - 법인구분: 기업의 법인 구분
       - 고유번호: 기업의 고유 식별번호
       - 회사명: 공시대상회사명

    2. 무상증자 정보
       - 신주의 종류와 수(보통주식): 무상증자로 발행되는 보통주식 수량
       - 신주의 종류와 수(기타주식): 무상증자로 발행되는 기타주식 수량
       - 1주당 액면가액: 신주의 주당 액면가액

    3. 증자 전 주식 정보
       - 증자전 발행주식총수(보통주식): 무상증자 전 보통주식 총수
       - 증자전 발행주식총수(기타주식): 무상증자 전 기타주식 총수

    4. 신주 배정 정보
       - 신주배정기준일: 무상증자 배정 기준일
       - 1주당 신주배정 주식수(보통주식): 보통주식 보유자 1주당 배정되는 신주 수
       - 1주당 신주배정 주식수(기타주식): 기타주식 보유자 1주당 배정되는 신주 수

    5. 신주 관련 일정
       - 신주의 배당기산일: 신주의 배당 계산 기준일
       - 신주권교부예정일: 신주권 발행 예정일
       - 신주의 상장 예정일: 신주 상장 예정일

    6. 이사회 정보
       - 이사회결의일: 무상증자 결정일
       - 사외이사 참석여부: 참석 및 불참 인원수
       - 감사 참석여부: 감사 또는 감사위원 참석 여부

    무상증자의 주요 특징:
    - 주주에게 대가 없이 주식 배정
    - 기존 주주 비례 배정
    - 자본금 증가 없이 주식수만 증가
    - 주가 희석 효과 발생
    - 주주 가치 변화 없음

    무상증자의 목적:
    - 주가 조정
    - 유동성 증대
    - 주주 수 증가
    - 배당 정책 조정
    - 기업 가치 재평가

    무상증자의 영향:
    - 주가 하락 (희석 효과)
    - 주식수 증가
    - 배당률 조정
    - 거래량 변화
    - 투자자 심리 변화

    활용 방안:
    - 기업의 자본정책 분석
    - 주주 가치 변화 추적
    - 주가 변동 요인 분석
    - 투자 의사결정 지원
    - 기업 재무 전략 파악
    - 주주 구조 변화 모니터링
    - 배당 정책 변화 분석
    - 기업 가치 평가
    - 투자 위험도 평가
    - 포트폴리오 최적화
    """
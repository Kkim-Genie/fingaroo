from pydantic import BaseModel, Field
from typing import Optional

class DartTotalStockItem(BaseModel):
    rcpt_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 (Y:유가, K:코스닥, N:코넥스, E:기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 회사명
    se: Optional[str] = Field(default=None)  # 구분(증권의종류, 합계, 비교)
    isu_stock_totay: Optional[str] = Field(default=None)  # I. 발행할 주식의 총수
    now_to_isu_stock_totay: Optional[str] = Field(default=None)  # II. 현재까지 발행한 주식의 총수
    now_to_dcrs_stock_totay: Optional[str] = Field(default=None)  # III. 현재까지 감소한 주식의 총수
    redc: Optional[str] = Field(default=None)  # 감자
    profit_incnr: Optional[str] = Field(default=None)  # 이익소각
    rdmsk_repy: Optional[str] = Field(default=None)  # 상환주식의 상환
    etc: Optional[str] = Field(default=None)  # 기타
    istc_totay: Optional[str] = Field(default=None)  # IV. 발행주식의 총수(III-III)
    tesstk_co: Optional[str] = Field(default=None)  # V. 자기주식수
    distb_stock_co: Optional[str] = Field(default=None)  # VI. 유통주식수(IV-V)
    stlm_dt: Optional[str] = Field(default=None)  # 결산기준일 (YYYY-MM-DD)

class DartTotalStock(BaseModel):
    status: str # 에러 및 정보 코드
    message: str # 에러 및 정보 메시지
    list: list[DartTotalStockItem]

def get_total_stock_description():
    return """
    주식총수 현황

    이 API는 기업의 주식총수 현황에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 고유번호: 공시대상회사의 고유번호 (8자리)
       - 회사명: 공시대상회사명
       - 구분: 증권의 종류, 합계, 비교 구분
       - 결산기준일: 주식총수 산정 기준일

    2. 주식 발행 정보
       - 발행할 주식의 총수: 정관에 명시된 최대 발행 가능 주식수
       - 현재까지 발행한 주식의 총수: 실제로 발행된 주식의 총수

    3. 주식 감소 정보
       - 현재까지 감소한 주식의 총수: 감소된 주식의 총수
       - 감자: 자본감소로 인한 주식 감소
       - 이익소각: 이익소각으로 인한 주식 감소
       - 상환주식의 상환: 상환주식 상환으로 인한 주식 감소
       - 기타: 기타 사유로 인한 주식 감소

    4. 주식 현황
       - 발행주식의 총수: 현재 발행된 주식의 총수 (발행총수 - 감소총수)
       - 자기주식수: 회사가 보유한 자기주식 수량
       - 유통주식수: 실제 시장에서 거래 가능한 주식 수량 (발행총수 - 자기주식수)

    주식총수 현황의 중요성:
    - 기업의 자본규모 파악
    - 주주 지분율 계산
    - 주가 지표 산정 (EPS, BPS 등)
    - 기업 가치 평가
    - 투자 의사결정 지원

    주식 발행의 주요 목적:
    - 자금조달
    - 기업 확장
    - M&A
    - 경영진 보상
    - 주주 가치 증대

    주식 감소의 주요 사유:
    - 자본감소: 재무 건전성 개선
    - 이익소각: 주주 환원
    - 상환주식 상환: 상환조건 충족
    - 기타: 법적 요구사항 등

    자기주식의 주요 용도:
    - 주가 안정화
    - 주주 환원
    - 경영진 보상
    - M&A
    - 자본구조 조정

    유통주식수의 중요성:
    - 시장 가격 형성
    - 거래량 결정
    - 유동성 지표
    - 투자자 접근성

    주식총수 변동의 영향:
    - 주주 지분율 변화
    - 주가 지표 변화
    - 기업 가치 변화
    - 투자자 심리 변화

    활용 방안:
    - 기업의 자본규모 분석
    - 주주 지분율 추적
    - 주가 지표 산정
    - 기업 가치 평가
    - 투자 의사결정 지원
    - 포트폴리오 최적화
    - 기업 재무 분석
    - 주식 투자 전략 수립
    - 기업 지배구조 분석
    - 주주 가치 변화 모니터링
    - 기업 성장성 평가
    - 투자 위험도 평가
    - 시장 점유율 분석
    - 경쟁사 비교 분석
    - 산업별 분석
    """
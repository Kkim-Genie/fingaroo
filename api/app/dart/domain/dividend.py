from pydantic import BaseModel, Field
from typing import Optional

class DartDividendItem(BaseModel):
    rcpt_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 (Y:유가, K:코스닥, N:코넥스, E:기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 법인명
    se: Optional[str] = Field(default=None)  # 구분 (유상증자, 전환권행사 등)
    stock_knd: Optional[str] = Field(default=None)  # 주식 종류 (보통주 등)
    thstrm: Optional[str] = Field(default=None)  # 당기 (9,999,999,999)
    frmtrm: Optional[str] = Field(default=None)  # 전기 (9,999,999,999)
    lwfr: Optional[str] = Field(default=None)  # 전전기 (9,999,999,999)
    stlm_dt: Optional[str] = Field(default=None)  # 결산기준일 (YYYY-MM-DD)

class DartDividend(BaseModel):
    status: str # 000 정상, 013 데이터 없음
    message: str # 메시지
    list: list[DartDividendItem]

def get_dividend_description():
    return """
    배당

    이 API는 기업의 배당에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 기업코드: 공시대상회사의 고유번호 (8자리)
       - 법인명: 공시대상회사명

    2. 배당 구분 정보
       - 구분: 배당의 종류 (유상증자, 전환권행사, 현금배당, 주식배당 등)
       - 주식 종류: 배당 대상 주식 종류 (보통주, 우선주 등)

    3. 배당 금액 정보
       - 당기: 현재 회계연도의 배당 금액
       - 전기: 이전 회계연도의 배당 금액
       - 전전기: 전전 회계연도의 배당 금액
       - 결산기준일: 해당 배당의 결산 기준일

    배당의 주요 형태:
    - 현금배당: 주주에게 현금으로 배당 지급
    - 주식배당: 주주에게 주식으로 배당 지급
    - 중간배당: 회계연도 중간에 지급하는 배당
    - 기말배당: 회계연도 말에 지급하는 배당
    - 특별배당: 특별한 사유로 지급하는 배당

    배당 정책의 중요성:
    - 주주 가치 극대화
    - 기업의 수익성 지표
    - 투자자 수익률 결정
    - 기업의 재무 건전성 반영
    - 경영진의 주주 친화적 정책

    배당 관련 주요 지표:
    - 배당수익률: 주가 대비 배당 비율
    - 배당성향: 순이익 대비 배당 비율
    - 배당지급률: 배당 지급 가능 여부
    - 배당성장률: 배당 증가율

    활용 방안:
    - 기업의 수익성 분석
    - 주주 가치 평가
    - 투자 수익률 계산
    - 기업 재무 건전성 평가
    - 배당 정책 변화 추적
    - 투자 의사결정 지원
    - 포트폴리오 최적화
    - 기업 가치 평가
    - 배당 투자 전략 수립
    - 기업 경영 성과 분석
    """
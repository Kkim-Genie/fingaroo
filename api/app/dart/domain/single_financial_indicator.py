from pydantic import BaseModel, Field
from typing import Optional

class DartSingleFinancialIndicatorItem(BaseModel):
    reprt_code: Optional[str] = Field(default=None)  # 보고서 코드
    bsns_year: Optional[str] = Field(default=None)  # 사업 연도
    corp_code: Optional[str] = Field(default=None)  # 고유번호(8자리)
    stock_code: Optional[str] = Field(default=None)  # 종목 코드(6자리)
    stlm_dt: Optional[str] = Field(default=None)  # 결산기준일 (YYYY-MM-DD)
    idx_cl_code: Optional[str] = Field(default=None)  # 지표분류코드
    idx_cl_nm: Optional[str] = Field(default=None)  # 지표분류명
    idx_code: Optional[str] = Field(default=None)  # 지표코드
    idx_nm: Optional[str] = Field(default=None)  # 지표명
    idx_val: Optional[str] = Field(default=None)  # 지표값

class DartSingleFinancialIndicator(BaseModel):
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: list[DartSingleFinancialIndicatorItem]  # 결과 리스트

def get_single_financial_indicator_description():
    return """
    단일회사 재무지표

    이 API는 개별 기업의 재무지표를 조회할 수 있는 기능을 제공합니다.

    주요 정보:
    
    1. 기업 및 보고서 정보
       - 보고서 코드: 재무제표 보고서 식별 코드
       - 사업 연도: 해당 재무지표의 사업연도
       - 고유번호: 기업의 고유번호 (8자리)
       - 종목 코드: 상장회사의 종목코드 (6자리)
       - 결산기준일: 재무지표의 결산 기준일

    2. 재무지표 정보
       - 지표분류코드: 재무지표의 분류 코드
       - 지표분류명: 재무지표의 분류 명칭
       - 지표코드: 개별 지표의 고유 코드
       - 지표명: 재무지표의 명칭
       - 지표값: 해당 지표의 수치

    재무지표의 주요 분류:

    1. 수익성지표
       - 매출총이익률: 매출 대비 매출총이익 비율
       - 영업이익률: 매출 대비 영업이익 비율
       - 순이익률: 매출 대비 순이익 비율
       - ROA(총자산수익률): 총자산 대비 순이익 비율
       - ROE(자기자본수익률): 자기자본 대비 순이익 비율

    2. 안정성지표
       - 유동비율: 유동자산 대비 유동부채 비율
       - 부채비율: 자기자본 대비 부채 비율
       - 자기자본비율: 총자산 대비 자기자본 비율
       - 이자보상배율: 영업이익 대비 이자비용 비율

    3. 성장성지표
       - 매출증가율: 전년 대비 매출 증가율
       - 영업이익증가율: 전년 대비 영업이익 증가율
       - 순이익증가율: 전년 대비 순이익 증가율
       - 자산증가율: 전년 대비 총자산 증가율

    4. 활동성지표
       - 총자산회전율: 총자산 대비 매출 비율
       - 재고자산회전율: 재고자산 대비 매출 비율
       - 매출채권회전율: 매출채권 대비 매출 비율
       - 매입채무회전율: 매입채무 대비 매출 비율

    단일회사 재무지표의 주요 특징:
    - 개별 기업의 재무지표 조회
    - 표준화된 지표 체계 제공
    - 분기별, 반기별, 연간 데이터 제공
    - 지표별 분류 체계 제공
    - 시계열 분석 가능

    재무지표 분석의 중요성:
    - 기업의 재무 건전성 평가
    - 수익성 및 성장성 분석
    - 투자 가치 판단
    - 경영 성과 평가
    - 위험도 평가
    - 투자 의사결정 지원

    재무지표 해석 시 고려사항:
    - 산업 평균과의 비교
    - 경쟁사와의 비교
    - 시계열 변화 추이
    - 경제 환경의 영향
    - 기업의 특수성

    활용 방안:
    - 기업 재무 건전성 평가
    - 투자 가치 분석
    - 경영 성과 분석
    - 위험도 평가
    - 투자 의사결정 지원
    - 기업 가치 평가
    - 신용도 평가
    - 재무 예측 모델 구축
    - 경영진 평가
    - 기업 전략 분석
    - 투자 포트폴리오 구성
    - ESG 평가
    """
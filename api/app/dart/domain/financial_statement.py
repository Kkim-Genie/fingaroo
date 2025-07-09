from pydantic import BaseModel, Field
from typing import Optional

class DartFinancialStatementItem(BaseModel):
    rcpt_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    reprt_code: Optional[str] = Field(default=None)  # 보고서 코드
    bsns_year: Optional[str] = Field(default=None)  # 사업 연도
    corp_code: Optional[str] = Field(default=None)  # 고유번호(8자리)
    sj_div: Optional[str] = Field(default=None)  # 재무제표구분
    sj_nm: Optional[str] = Field(default=None)  # 재무제표명
    account_id: Optional[str] = Field(default=None)  # 계정ID
    account_nm: Optional[str] = Field(default=None)  # 계정명
    account_detail: Optional[str] = Field(default=None)  # 계정상세
    thstrm_nm: Optional[str] = Field(default=None)  # 당기명
    thstrm_amount: Optional[str] = Field(default=None)  # 당기금액
    thstrm_add_amount: Optional[str] = Field(default=None)  # 당기누적금액
    frmtrm_nm: Optional[str] = Field(default=None)  # 전기명
    frmtrm_amount: Optional[str] = Field(default=None)  # 전기금액
    frmtrm_q_nm: Optional[str] = Field(default=None)  # 전기명(분/반기)
    frmtrm_q_amount: Optional[str] = Field(default=None)  # 전기금액(분/반기)
    frmtrm_add_amount: Optional[str] = Field(default=None)  # 전기누적금액
    bfefrmtrm_nm: Optional[str] = Field(default=None)  # 전전기명
    bfefrmtrm_amount: Optional[str] = Field(default=None)  # 전전기금액
    ord: Optional[str] = Field(default=None)  # 계정과목 정렬순서
    currency: Optional[str] = Field(default=None)  # 통화 단위

class DartFinancialStatement(BaseModel):
    status: str # 000 정상, 013 데이터 없음
    message: str # 메시지
    list: list[DartFinancialStatementItem]

def get_financial_statement_description():
    return """
    재무제표

    이 API는 기업의 재무제표에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 및 보고서 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 보고서 코드: 재무제표 보고서 식별 코드
       - 사업 연도: 해당 재무제표의 사업연도
       - 고유번호: 기업의 고유번호 (8자리)

    2. 재무제표 구분 정보
       - 재무제표구분: 재무제표의 종류 구분
       - 재무제표명: 재무제표의 명칭
       - 계정ID: 계정과목의 고유 식별자
       - 계정명: 계정과목의 명칭
       - 계정상세: 계정과목의 상세 내용

    3. 당기 재무 정보
       - 당기명: 당기 회계연도 명칭
       - 당기금액: 당기 해당 계정과목의 금액
       - 당기누적금액: 당기 누적 금액 (분기별 보고의 경우)

    4. 전기 재무 정보
       - 전기명: 전기 회계연도 명칭
       - 전기금액: 전기 해당 계정과목의 금액
       - 전기명(분/반기): 전기 분기/반기 명칭
       - 전기금액(분/반기): 전기 분기/반기 금액
       - 전기누적금액: 전기 누적 금액

    5. 전전기 재무 정보
       - 전전기명: 전전기 회계연도 명칭
       - 전전기금액: 전전기 해당 계정과목의 금액

    6. 기타 정보
       - 계정과목 정렬순서: 재무제표 내 표시 순서
       - 통화 단위: 금액 표시 통화

    재무제표의 주요 구성:
    - 재무상태표(대차대조표): 자산, 부채, 자본의 상태
    - 손익계산서: 수익, 비용, 손익의 흐름
    - 현금흐름표: 현금의 유입과 유출
    - 자본변동표: 자본의 변동 내역
    - 주석: 재무제표의 부속명세서

    주요 재무 지표:
    - 수익성 지표: 매출총이익률, 영업이익률, 순이익률
    - 안정성 지표: 유동비율, 부채비율, 자기자본비율
    - 성장성 지표: 매출증가율, 자산증가율, 순이익증가율
    - 효율성 지표: 총자산회전율, 재고자산회전율, 매출채권회전율

    재무제표 분석의 중요성:
    - 기업의 재무 건전성 평가
    - 수익성 및 성장성 분석
    - 투자 가치 판단
    - 경쟁사 비교 분석
    - 위험도 평가
    - 신용도 평가

    활용 방안:
    - 기업 가치 평가
    - 투자 의사결정 지원
    - 신용 평가
    - 경영 성과 분석
    - 재무 건전성 모니터링
    - 경쟁사 벤치마킹
    - 산업별 비교 분석
    - 재무 예측 모델 구축
    - 위험 관리
    - M&A 가치 평가
    - 투자 포트폴리오 최적화
    """
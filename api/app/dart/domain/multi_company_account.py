from pydantic import BaseModel, Field
from typing import Optional

class DartMultiCompanyAccountItem(BaseModel):
    rcpt_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    bsns_year: Optional[str] = Field(default=None)  # 사업 연도
    stock_code: Optional[str] = Field(default=None)  # 종목 코드(6자리)
    reprt_code: Optional[str] = Field(default=None)  # 보고서 코드
    account_nm: Optional[str] = Field(default=None)  # 계정명
    fs_div: Optional[str] = Field(default=None)  # 개별/연결구분 (OFS:재무제표, CFS:연결재무제표)
    fs_nm: Optional[str] = Field(default=None)  # 개별/연결명
    sj_div: Optional[str] = Field(default=None)  # 재무제표구분 (BS:재무상태표, IS:손익계산서)
    sj_nm: Optional[str] = Field(default=None)  # 재무제표명
    thstrm_nm: Optional[str] = Field(default=None)  # 당기명
    thstrm_dt: Optional[str] = Field(default=None)  # 당기일자
    thstrm_amount: Optional[str] = Field(default=None)  # 당기금액
    thstrm_add_amount: Optional[str] = Field(default=None)  # 당기누적금액
    frmtrm_nm: Optional[str] = Field(default=None)  # 전기명
    frmtrm_dt: Optional[str] = Field(default=None)  # 전기일자
    frmtrm_amount: Optional[str] = Field(default=None)  # 전기금액
    frmtrm_add_amount: Optional[str] = Field(default=None)  # 전기누적금액
    bfefrmtrm_nm: Optional[str] = Field(default=None)  # 전전기명
    bfefrmtrm_dt: Optional[str] = Field(default=None)  # 전전기일자
    bfefrmtrm_amount: Optional[str] = Field(default=None)  # 전전기금액
    ord: Optional[str] = Field(default=None)  # 계정과목 정렬순서
    currency: Optional[str] = Field(default=None)  # 통화 단위

class DartMultiCompanyAccount(BaseModel):
    status: str # 000 정상, 013 데이터 없음
    message: str # 메시지
    list: list[DartMultiCompanyAccountItem]

def get_multi_company_account_description():
    return """
    다중회사 계정

    이 API는 여러 기업의 재무제표 계정 정보를 일괄 조회할 수 있는 기능을 제공합니다.

    주요 정보:
    
    1. 기업 및 보고서 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 사업 연도: 해당 재무제표의 사업연도
       - 종목 코드: 주식 종목 코드 (6자리)
       - 보고서 코드: 재무제표 보고서 식별 코드

    2. 계정 정보
       - 계정명: 재무제표 계정과목의 명칭
       - 계정과목 정렬순서: 재무제표 내 표시 순서
       - 통화 단위: 금액 표시 통화

    3. 재무제표 구분 정보
       - 개별/연결구분: OFS(개별재무제표), CFS(연결재무제표)
       - 개별/연결명: 재무제표의 구분 명칭
       - 재무제표구분: BS(재무상태표), IS(손익계산서)
       - 재무제표명: 재무제표의 명칭

    4. 당기 재무 정보
       - 당기명: 당기 회계연도 명칭
       - 당기일자: 당기 재무제표 기준일
       - 당기금액: 당기 해당 계정과목의 금액
       - 당기누적금액: 당기 누적 금액 (분기별 보고의 경우)

    5. 전기 재무 정보
       - 전기명: 전기 회계연도 명칭
       - 전기일자: 전기 재무제표 기준일
       - 전기금액: 전기 해당 계정과목의 금액
       - 전기누적금액: 전기 누적 금액

    6. 전전기 재무 정보
       - 전전기명: 전전기 회계연도 명칭
       - 전전기일자: 전전기 재무제표 기준일
       - 전전기금액: 전전기 해당 계정과목의 금액

    다중회사 계정의 주요 특징:
    - 여러 기업의 재무정보를 한 번에 조회
    - 개별재무제표와 연결재무제표 구분 제공
    - 재무상태표와 손익계산서 구분 제공
    - 시계열 데이터 제공 (당기, 전기, 전전기)
    - 표준화된 계정과목 체계

    재무제표 구분의 중요성:
    - 개별재무제표: 개별 법인의 재무상태
    - 연결재무제표: 지배기업과 종속기업을 하나의 경제적 실체로 보고
    - 재무상태표: 자산, 부채, 자본의 상태
    - 손익계산서: 수익, 비용, 손익의 흐름

    활용 방안:
    - 기업 간 재무 비교 분석
    - 산업별 벤치마킹
    - 투자 포트폴리오 분석
    - 경쟁사 분석
    - 기업 가치 평가
    - 재무 건전성 비교
    - 성장성 및 수익성 비교
    - 위험도 평가
    - 투자 의사결정 지원
    - 재무 예측 모델 구축
    - 시장 분석 및 트렌드 파악
    - ESG 평가 및 비교
    """
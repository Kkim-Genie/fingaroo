from pydantic import BaseModel, Field
from typing import Optional

class DartTreasuryStockItem(BaseModel):
    rcpt_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 (Y:유가, K:코스닥, N:코넥스, E:기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 법인명
    acqs_mth1: Optional[str] = Field(default=None)  # 취득방법 대분류 (배당가능이익범위 이내 취득, 기타취득, 총계 등)
    acqs_mth2: Optional[str] = Field(default=None)  # 취득방법 중분류 (직접취득, 신탁계약에 의한취득, 기타취득, 총계 등)
    acqs_mth3: Optional[str] = Field(default=None)  # 취득방법 소분류 (장내직접취득, 장외직접취득, 공개매수, 주식매수청구권행사, 수탁자보유물량, 현물보유취득, 기타취득, 소계, 총계 등)
    stock_knd: Optional[str] = Field(default=None)  # 주식 종류 (보통주, 우선주 등)
    bsis_qy: Optional[str] = Field(default=None)  # 기초 수량 (9,999,999,999)
    change_qy_acqs: Optional[str] = Field(default=None)  # 변동 수량 취득 (9,999,999,999)
    change_qy_dsps: Optional[str] = Field(default=None)  # 변동 수량 처분 (9,999,999,999)
    change_qy_incnr: Optional[str] = Field(default=None)  # 변동 수량 소각 (9,999,999,999)
    trmend_qy: Optional[str] = Field(default=None)  # 기말 수량 (9,999,999,999)
    rm: Optional[str] = Field(default=None)  # 비고
    stlm_dt: Optional[str] = Field(default=None)  # 결산기준일 (YYYY-MM-DD)

class DartTreasuryStock(BaseModel):
    status: str # 000 정상, 013 데이터 없음
    message: str # 메시지
    list: list[DartTreasuryStockItem]

def get_treasury_stock_description():
    return """
    자기주식 현황

    이 API는 기업의 자기주식 현황에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 고유번호: 공시대상회사의 고유번호 (8자리)
       - 법인명: 공시대상회사명
       - 결산기준일: 자기주식 현황 산정 기준일

    2. 취득 방법 분류
       - 대분류: 배당가능이익범위 이내 취득, 기타취득, 총계
       - 중분류: 직접취득, 신탁계약에 의한 취득, 기타취득, 총계
       - 소분류: 
         * 장내직접취득: 시장에서 직접 매수
         * 장외직접취득: 장외 거래를 통한 매수
         * 공개매수: 공개매수를 통한 취득
         * 주식매수청구권행사: 주식매수청구권 행사
         * 수탁자보유물량: 신탁계약에 의한 수탁자 보유
         * 현물보유취득: 현물 출자 등으로 인한 취득
         * 기타취득: 기타 방법으로 인한 취득

    3. 주식 종류
       - 보통주: 일반적인 주식
       - 우선주: 우선권이 있는 주식
       - 기타: 기타 종류의 주식

    4. 수량 현황
       - 기초 수량: 기간 시작 시점의 보유 수량
       - 변동 수량 취득: 기간 중 취득한 수량
       - 변동 수량 처분: 기간 중 처분한 수량
       - 변동 수량 소각: 기간 중 소각한 수량
       - 기말 수량: 기간 종료 시점의 보유 수량

    5. 기타 정보
       - 비고: 추가 설명 사항

    자기주식의 주요 취득 방법:
    - 배당가능이익범위 이내 취득: 법정 한도 내에서의 취득
    - 기타취득: 법정 한도 외에서의 취득
    - 직접취득: 회사가 직접 매수
    - 신탁계약에 의한 취득: 신탁회사를 통한 취득
    - 장내직접취득: 시장에서 직접 매수
    - 장외직접취득: 장외 거래를 통한 매수
    - 공개매수: 공개매수를 통한 취득
    - 주식매수청구권행사: 주주가 청구권을 행사한 경우
    - 수탁자보유물량: 신탁계약에 의한 수탁자 보유
    - 현물보유취득: 현물 출자 등으로 인한 취득

    자기주식의 주요 용도:
    - 주가 안정화
    - 주주 환원
    - 경영진 보상
    - M&A
    - 자본구조 조정
    - 투자 기회 활용
    - 재무 건전성 개선

    자기주식 취득의 제한사항:
    - 배당가능이익 범위 내 취득 한도
    - 이사회 승인 필요
    - 공시 의무
    - 취득 방법 제한
    - 취득 기간 제한

    자기주식의 영향:
    - 긍정적 영향: 주가 안정화, 주주 가치 증대
    - 부정적 영향: 자금 유출, 재무 건전성 악화
    - 시장 영향: 유통주식수 감소, 거래량 변화

    활용 방안:
    - 기업의 자본정책 분석
    - 주주 가치 변화 추적
    - 주가 변동 요인 분석
    - 투자 의사결정 지원
    - 기업 재무 전략 파악
    - 자금조달 전략 분석
    - 기업 가치 평가
    - 투자 위험도 평가
    - 포트폴리오 최적화
    - 기업 지배구조 변화 모니터링
    - 기업 성장성 평가
    - 시장 점유율 분석
    - 경쟁사 비교 분석
    - 산업별 분석
    - 기업 재무 건전성 평가
    """
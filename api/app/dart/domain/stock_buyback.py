from pydantic import BaseModel, Field
from typing import Optional

class DartStockBuybackItem(BaseModel):
    rcept_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 공시대상회사명
    aqpln_stk_ostk: Optional[str] = Field(default=None)  # 취득예정주식(주)(보통주식)
    aqpln_stk_estk: Optional[str] = Field(default=None)  # 취득예정주식(주)(기타주식)
    aqpln_prc_ostk: Optional[str] = Field(default=None)  # 취득예정금액(원)(보통주식)
    aqpln_prc_estk: Optional[str] = Field(default=None)  # 취득예정금액(원)(기타주식)
    aqexpd_bgd: Optional[str] = Field(default=None)  # 취득예상기간(시작일)
    aqexpd_edd: Optional[str] = Field(default=None)  # 취득예상기간(종료일)
    hdexpd_bgd: Optional[str] = Field(default=None)  # 보유예상기간(시작일)
    hdexpd_edd: Optional[str] = Field(default=None)  # 보유예상기간(종료일)
    aq_pp: Optional[str] = Field(default=None)  # 취득목적
    aq_mth: Optional[str] = Field(default=None)  # 취득방법
    cs_iv_bk: Optional[str] = Field(default=None)  # 위탁투자중개업자
    aq_wtn_div_ostk: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(보통주식))
    aq_wtn_div_ostk_rt: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%)))
    aq_wtn_div_estk: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(기타주식))
    aq_wtn_div_estk_rt: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%)))
    eaq_ostk: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(기타취득(주)(보통주식))
    eaq_ostk_rt: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(기타취득(주)(비율(%)))
    eaq_estk: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(기타취득(주)(기타주식))
    eaq_estk_rt: Optional[str] = Field(default=None)  # 취득 전 자기주식 보유현황(기타취득(주)(비율(%)))
    aq_dd: Optional[str] = Field(default=None)  # 취득결정일
    od_a_at_t: Optional[str] = Field(default=None)  # 사외이사참석여부(참석(명))
    od_a_at_b: Optional[str] = Field(default=None)  # 사외이사참석여부(불참(명))
    adt_a_atn: Optional[str] = Field(default=None)  # 감사(사외이사가 아닌 감사위원)참석여부
    d1_prodlm_ostk: Optional[str] = Field(default=None)  # 1일 매수 주문수량 한도(보통주식)
    d1_prodlm_estk: Optional[str] = Field(default=None)  # 1일 매수 주문수량 한도(기타주식)

class DartStockBuyback(BaseModel):
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: list[DartStockBuybackItem]  # 결과 리스트

def get_stock_buyback_description():
    return """
    자사주 매입(자기주식 취득)

    이 API는 기업의 자사주 매입에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 고유번호: 공시대상회사의 고유번호 (8자리)
       - 회사명: 공시대상회사명

    2. 취득 예정 정보
       - 취득예정주식(보통주식): 취득 예정인 보통주식 수량
       - 취득예정주식(기타주식): 취득 예정인 기타주식 수량
       - 취득예정금액(보통주식): 보통주식 취득 예정 금액
       - 취득예정금액(기타주식): 기타주식 취득 예정 금액

    3. 취득 및 보유 기간
       - 취득예상기간: 취득 시작일부터 종료일까지
       - 보유예상기간: 보유 시작일부터 종료일까지

    4. 취득 관련 정보
       - 취득목적: 자기주식 취득의 목적
       - 취득방법: 자기주식 취득 방식
       - 위탁투자중개업자: 취득을 위탁하는 증권사
       - 취득결정일: 자기주식 취득 결정일

    5. 취득 전 자기주식 보유현황
       - 배당가능이익 범위 내 취득:
         * 보통주식 수량 및 비율
         * 기타주식 수량 및 비율
       - 기타취득:
         * 보통주식 수량 및 비율
         * 기타주식 수량 및 비율

    6. 기타 정보
       - 이사회 정보: 사외이사 참석정보, 감사 참석정보
       - 1일 매수 주문수량 한도: 보통주식 및 기타주식별 일일 매수 한도

    자기주식 취득의 주요 목적:
    - 주주가치 극대화
    - 주가 안정화
    - 배당 정책 조정
    - 경영진 보상
    - 자본구조 최적화
    - M&A 자금 확보

    자기주식 취득의 주요 방법:
    - 시장매수: 시장에서 직접 매수
    - 공개매수: 공개매수 제도를 통한 매수
    - 대량매매: 대량매매를 통한 매수
    - 제3자 배정: 특정인으로부터 매수

    자기주식 취득의 영향:
    - 긍정적 영향: 주가 상승, EPS 증가, ROE 개선
    - 부정적 영향: 현금 유출, 투자 기회 상실
    - 시장 영향: 투자자 심리 개선, 거래량 증가

    자기주식 취득의 제한사항:
    - 배당가능이익 범위 내 취득 한도
    - 일일 매수 수량 한도
    - 보유 기간 제한
    - 이사회 승인 필요

    활용 방안:
    - 기업의 자본정책 분석
    - 주주 가치 변화 추적
    - 주가 변동 요인 분석
    - 투자 의사결정 지원
    - 기업 재무 전략 파악
    - 배당 정책 변화 분석
    - 기업 가치 평가
    - 투자 위험도 평가
    - 포트폴리오 최적화
    - 기업 지배구조 변화 모니터링
    """
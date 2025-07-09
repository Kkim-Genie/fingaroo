from pydantic import BaseModel, Field
from typing import Optional

class DartStockRetirementItem(BaseModel):
    rcept_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 공시대상회사명
    dppln_stk_ostk: Optional[str] = Field(default=None)  # 처분예정주식(주)(보통주식)
    dppln_stk_estk: Optional[str] = Field(default=None)  # 처분예정주식(주)(기타주식)
    dpstk_prc_ostk: Optional[str] = Field(default=None)  # 처분 대상 주식가격(원)(보통주식)
    dpstk_prc_estk: Optional[str] = Field(default=None)  # 처분 대상 주식가격(원)(기타주식)
    dppln_prc_ostk: Optional[str] = Field(default=None)  # 처분예정금액(원)(보통주식)
    dppln_prc_estk: Optional[str] = Field(default=None)  # 처분예정금액(원)(기타주식)
    dpprpd_bgd: Optional[str] = Field(default=None)  # 처분예정기간(시작일)
    dpprpd_edd: Optional[str] = Field(default=None)  # 처분예정기간(종료일)
    dp_pp: Optional[str] = Field(default=None)  # 처분목적
    dp_m_mkt: Optional[str] = Field(default=None)  # 처분방법(시장을 통한 매도(주))
    dp_m_ovtm: Optional[str] = Field(default=None)  # 처분방법(시간외대량매매(주))
    dp_m_otc: Optional[str] = Field(default=None)  # 처분방법(장외처분(주))
    dp_m_etc: Optional[str] = Field(default=None)  # 처분방법(기타(주))
    cs_iv_bk: Optional[str] = Field(default=None)  # 위탁투자중개업자
    aq_wtn_div_ostk: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(보통주식))
    aq_wtn_div_ostk_rt: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%)))
    aq_wtn_div_estk: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(기타주식))
    aq_wtn_div_estk_rt: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%)))
    eaq_ostk: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(기타취득(주)(보통주식))
    eaq_ostk_rt: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(기타취득(주)(비율(%)))
    eaq_estk: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(기타취득(주)(기타주식))
    eaq_estk_rt: Optional[str] = Field(default=None)  # 처분 전 자기주식 보유현황(기타취득(주)(비율(%)))
    dp_dd: Optional[str] = Field(default=None)  # 처분결정일
    od_a_at_t: Optional[str] = Field(default=None)  # 사외이사참석여부(참석(명))
    od_a_at_b: Optional[str] = Field(default=None)  # 사외이사참석여부(불참(명))
    adt_a_atn: Optional[str] = Field(default=None)  # 감사(사외이사가 아닌 감사위원)참석여부
    d1_slodlm_ostk: Optional[str] = Field(default=None)  # 1일 매도 주문수량 한도(보통주식)
    d1_slodlm_estk: Optional[str] = Field(default=None)  # 1일 매도 주문수량 한도(기타주식)

class DartStockRetirement(BaseModel):
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: list[DartStockRetirementItem]  # 결과 리스트

def get_stock_retirement_description():
    return """
    자기주식 처분

    이 API는 기업의 자기주식 처분에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 고유번호: 공시대상회사의 고유번호 (8자리)
       - 회사명: 공시대상회사명

    2. 처분 예정 정보
       - 처분예정주식(보통주식): 처분 예정인 보통주식 수량
       - 처분예정주식(기타주식): 처분 예정인 기타주식 수량
       - 처분 대상 주식가격: 보통주식 및 기타주식의 처분 가격
       - 처분예정금액: 보통주식 및 기타주식의 처분 예정 금액

    3. 처분 기간
       - 처분예정기간: 처분 시작일부터 종료일까지

    4. 처분 관련 정보
       - 처분목적: 자기주식 처분의 목적
       - 처분방법:
         * 시장을 통한 매도: 일반 시장 매도
         * 시간외대량매매: 시간외 대량매매를 통한 처분
         * 장외처분: 장외 거래를 통한 처분
         * 기타: 기타 방법을 통한 처분
       - 위탁투자중개업자: 처분을 위탁하는 증권사
       - 처분결정일: 자기주식 처분 결정일

    5. 처분 전 자기주식 보유현황
       - 배당가능이익 범위 내 취득:
         * 보통주식 수량 및 비율
         * 기타주식 수량 및 비율
       - 기타취득:
         * 보통주식 수량 및 비율
         * 기타주식 수량 및 비율

    6. 기타 정보
       - 이사회 정보: 사외이사 참석정보, 감사 참석정보
       - 1일 매도 주문수량 한도: 보통주식 및 기타주식별 일일 매도 한도

    자기주식 처분의 주요 목적:
    - 자금조달
    - 주가 안정화
    - 자본구조 조정
    - 투자 기회 활용
    - 재무 건전성 개선
    - 경영진 보상

    자기주식 처분의 주요 방법:
    - 시장매도: 시장에서 직접 매도
    - 시간외대량매매: 시간외 대량매매를 통한 매도
    - 장외처분: 장외 거래를 통한 매도
    - 제3자 양도: 특정인에게 양도

    자기주식 처분의 영향:
    - 긍정적 영향: 자금조달, 재무 건전성 개선
    - 부정적 영향: 주가 하락, 주주 가치 분산
    - 시장 영향: 투자자 심리 변화, 거래량 증가

    자기주식 처분의 제한사항:
    - 일일 매도 수량 한도
    - 처분 기간 제한
    - 이사회 승인 필요
    - 공시 의무

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
    """
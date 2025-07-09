from pydantic import BaseModel
from typing import List

class DartBothCapitalDecisionItem(BaseModel):
    rcept_no: str  # 접수번호(14자리)
    corp_cls: str  # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
    corp_code: str  # 공시대상회사의 고유번호(8자리)
    corp_name: str  # 공시대상회사명
    piic_nstk_ostk_cnt: str  # 유상증자(신주의 종류와 수(보통주식 (주)))
    piic_nstk_estk_cnt: str  # 유상증자(신주의 종류와 수(기타주식 (주)))
    piic_fv_ps: str  # 유상증자(1주당 액면가액 (원))
    piic_bfic_tisstk_ostk: str  # 유상증자(증자전 발행주식총수 (주)(보통주식 (주)))
    piic_bfic_tisstk_estk: str  # 유상증자(증자전 발행주식총수 (주)(기타주식 (주)))
    piic_fdpp_fclt: str  # 유상증자(자금조달의 목적(시설자금 (원)))
    piic_fdpp_bsninh: str  # 유상증자(자금조달의 목적(영업양수자금 (원)))
    piic_fdpp_op: str  # 유상증자(자금조달의 목적(운영자금 (원)))
    piic_fdpp_dtrp: str  # 유상증자(자금조달의 목적(채무상환자금 (원)))
    piic_fdpp_ocsa: str  # 유상증자(자금조달의 목적(타법인 증권 취득자금 (원)))
    piic_fdpp_etc: str  # 유상증자(자금조달의 목적(기타자금 (원)))
    piic_ic_mthn: str  # 유상증자(증자방식)
    fric_nstk_ostk_cnt: str  # 무상증자(신주의 종류와 수(보통주식 (주)))
    fric_nstk_estk_cnt: str  # 무상증자(신주의 종류와 수(기타주식 (주)))
    fric_fv_ps: str  # 무상증자(1주당 액면가액 (원))
    fric_bfic_tisstk_ostk: str  # 무상증자(증자전 발행주식총수(보통주식 (주)))
    fric_bfic_tisstk_estk: str  # 무상증자(증자전 발행주식총수(기타주식 (주)))
    fric_nstk_asstd: str  # 무상증자(신주배정기준일)
    fric_nstk_ascnt_ps_ostk: str  # 무상증자(1주당 신주배정 주식수(보통주식 (주)))
    fric_nstk_ascnt_ps_estk: str  # 무상증자(1주당 신주배정 주식수(기타주식 (주)))
    fric_nstk_dividrk: str  # 무상증자(신주의 배당기산일)
    fric_nstk_dlprd: str  # 무상증자(신주권교부예정일)
    fric_nstk_lstprd: str  # 무상증자(신주의 상장 예정일)
    fric_bddd: str  # 무상증자(이사회결의일(결정일))
    fric_od_a_at_t: str  # 무상증자(사외이사 참석여부(참석(명)))
    fric_od_a_at_b: str  # 무상증자(사외이사 참석여부(불참(명)))
    fric_adt_a_atn: str  # 무상증자(감사(감사위원)참석 여부)
    ssl_at: str  # 공매도 해당여부
    ssl_bgd: str  # 공매도 시작일
    ssl_edd: str  # 공매도 종료일

class DartBothCapitalDecision(BaseModel):
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: List[DartBothCapitalDecisionItem]  # 결과 리스트

def get_both_capital_decision_description():
    return """
    유상증자 및 무상증자 결정

    이 API는 기업의 유상증자와 무상증자 결정에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 기업코드: 공시대상회사의 고유번호 (8자리)
       - 기업명: 공시대상회사명

    2. 유상증자 정보
       - 신주 발행 정보: 보통주식 및 기타주식 발행 수량
       - 액면가액: 1주당 액면가액
       - 증자전 발행주식총수: 증자 전 보통주식 및 기타주식 총수
       - 자금조달 목적별 금액:
         * 시설자금: 새로운 시설 투자 자금
         * 영업양수자금: 다른 기업 인수 자금
         * 운영자금: 일상 운영 자금
         * 채무상환자금: 기존 부채 상환 자금
         * 타법인 증권 취득자금: 다른 기업 주식 매입 자금
         * 기타자금: 기타 용도 자금
       - 증자방식: 유상증자 방식

    3. 무상증자 정보
       - 신주 배정 정보: 보통주식 및 기타주식 배정 수량
       - 액면가액: 1주당 액면가액
       - 증자전 발행주식총수: 증자 전 보통주식 및 기타주식 총수
       - 신주배정기준일: 무상증자 배정 기준일
       - 1주당 신주배정 주식수: 보통주식 및 기타주식별 배정 비율
       - 신주의 배당기산일: 배당 계산 기준일
       - 신주권교부예정일: 신주권 발행 예정일
       - 신주의 상장 예정일: 신주 상장 예정일
       - 이사회결의일: 무상증자 결정일
       - 사외이사 참석정보: 참석 및 불참 인원수
       - 감사 참석정보: 감사 또는 감사위원 참석 여부

    4. 공매도 관련 정보
       - 공매도 해당여부: 공매도 대상 여부
       - 공매도 시작일: 공매도 시작 날짜
       - 공매도 종료일: 공매도 종료 날짜

    활용 방안:
    - 기업의 자본금 변동 분석
    - 주주 가치 변화 추적
    - 기업의 재무 전략 파악
    - 투자 의사결정 지원
    - 기업 지배구조 변화 모니터링
    """
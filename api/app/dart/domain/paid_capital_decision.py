from pydantic import BaseModel, Field
from typing import Optional

class DartPaidCapitalDecisionItem(BaseModel):
    recept_no: Optional[str] = Field(default=None)  # 접수번호
    corp_cls: Optional[str] = Field(default=None)  # 법인구분
    corp_code: Optional[str] = Field(default=None)  # 고유번호
    corp_name: Optional[str] = Field(default=None)  # 회사명
    nstk_ostk_cnt: Optional[str] = Field(default=None)  # 신주의 종류와 수(보통주식)
    nstk_estk_cnt: Optional[str] = Field(default=None)  # 신주의 종류와 수(기타주식)
    fv_ps: Optional[str] = Field(default=None)  # 1주당 액면가액(원)
    bfic_tisstk_ostk: Optional[str] = Field(default=None)  # 증자전 발행주식총수(보통주식)
    bfic_tisstk_estk: Optional[str] = Field(default=None)  # 증자전 발행주식총수(기타주식)
    fdpp_fclt: Optional[str] = Field(default=None)  # 자금조달의 목적(시설자금)
    fdpp_bsninh: Optional[str] = Field(default=None)  # 자금조달의 목적(영업양수자금)
    fdpp_op: Optional[str] = Field(default=None)  # 자금조달의 목적(운영자금)
    fdpp_dtrp: Optional[str] = Field(default=None)  # 자금조달의 목적(채무상환자금)
    fdpp_ocsa: Optional[str] = Field(default=None)  # 자금조달의 목적(타법인 증권 취득자금)
    fdpp_etc: Optional[str] = Field(default=None)  # 자금조달의 목적(기타자금)
    ic_mthn: Optional[str] = Field(default=None)  # 증자방식
    ssl_at: Optional[str] = Field(default=None)  # 공매도 해당여부
    ssl_bgd: Optional[str] = Field(default=None)  # 공매도 시작일
    ssl_edd: Optional[str] = Field(default=None)  # 공매도 종료일

class DartPaidCapitalDecision(BaseModel):
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: list[DartPaidCapitalDecisionItem]  # 결과 리스트

def get_paid_capital_decision_description():
    return """
    유상증자 결정

    이 API는 기업의 유상증자 결정에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호
       - 법인구분: 기업의 법인 구분
       - 고유번호: 기업의 고유 식별번호
       - 회사명: 공시대상회사명

    2. 유상증자 정보
       - 신주의 종류와 수(보통주식): 유상증자로 발행되는 보통주식 수량
       - 신주의 종류와 수(기타주식): 유상증자로 발행되는 기타주식 수량
       - 1주당 액면가액: 신주의 주당 액면가액

    3. 증자 전 주식 정보
       - 증자전 발행주식총수(보통주식): 유상증자 전 보통주식 총수
       - 증자전 발행주식총수(기타주식): 유상증자 전 기타주식 총수

    4. 자금조달 목적별 금액
       - 시설자금: 새로운 시설 투자 자금
       - 영업양수자금: 다른 기업 인수 자금
       - 운영자금: 일상 운영 자금
       - 채무상환자금: 기존 부채 상환 자금
       - 타법인 증권 취득자금: 다른 기업 주식 매입 자금
       - 기타자금: 기타 용도 자금

    5. 증자 관련 정보
       - 증자방식: 유상증자의 구체적인 방식
       - 공매도 해당여부: 공매도 대상 여부
       - 공매도 시작일: 공매도 시작 날짜
       - 공매도 종료일: 공매도 종료 날짜

    유상증자의 주요 특징:
    - 주주에게 대가를 받고 주식 발행
    - 자본금 증가
    - 기존 주주 우선권 제공
    - 주가 희석 효과 발생
    - 기업 가치 증가

    유상증자의 주요 방식:
    - 일반공모: 일반 투자자 대상 공모
    - 제3자 배정증자: 특정인 대상 배정
    - 주주배정증자: 기존 주주 대상 배정
    - 전환사채 전환: 전환사채의 주식 전환
    - 신주인수권부사채: 신주인수권부사채의 전환

    자금조달 목적의 중요성:
    - 시설자금: 생산능력 확대, 기술개발 투자
    - 영업양수자금: M&A, 사업 확장
    - 운영자금: 일상 경영 활동
    - 채무상환자금: 재무 구조 개선
    - 타법인 증권 취득자금: 전략적 투자
    - 기타자금: 기타 경영 목적

    유상증자의 영향:
    - 긍정적 영향: 자금조달, 사업 확장, 재무 건전성 개선
    - 부정적 영향: 주가 희석, 주주 가치 분산
    - 시장 영향: 투자자 심리 변화, 거래량 증가

    활용 방안:
    - 기업의 자금조달 전략 분석
    - 주주 가치 변화 추적
    - 기업 재무 전략 파악
    - 투자 의사결정 지원
    - 기업 성장성 평가
    - 주가 변동 요인 분석
    - 기업 가치 평가
    - 투자 위험도 평가
    - 포트폴리오 최적화
    - M&A 트랜잭션 분석
    - 기업 지배구조 변화 모니터링
    """
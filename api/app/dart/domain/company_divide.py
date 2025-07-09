from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class DartCompanyDivideItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    rcept_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 공시대상회사명
    dv_mth: Optional[str] = Field(default=None)  # 분할방법
    dv_impef: Optional[str] = Field(default=None)  # 분할의 중요영향 및 효과
    dv_rt: Optional[str] = Field(default=None)  # 분할비율
    dv_trfbsnprt_cn: Optional[str] = Field(default=None)  # 분할로 이전할 사업 및 재산의 내용
    atdv_excmp_cmpnm: Optional[str] = Field(default=None)  # 분할 후 존속회사(회사명)
    atdvfdtl_tast: Optional[str] = Field(default=None)  # 분할 후 존속회사(분할후 재무내용(원)(자산총계))
    atdvfdtl_tdbt: Optional[str] = Field(default=None)  # 분할 후 존속회사(분할후 재무내용(원)(부채총계))
    atdvfdtl_teqt: Optional[str] = Field(default=None)  # 분할 후 존속회사(분할후 재무내용(원)(자본총계))
    atdvfdtl_cpt: Optional[str] = Field(default=None)  # 분할 후 존속회사(분할후 재무내용(원)(자본금))
    atdvfdtl_std: Optional[str] = Field(default=None)  # 분할 후 존속회사(분할후 재무내용(원)(현재기준))
    atdv_excmp_exbsn_rsl: Optional[str] = Field(default=None)  # 분할 후 존속회사(존속사업부문 최근 사업연도매출액(원))
    atdv_excmp_mbsn: Optional[str] = Field(default=None)  # 분할 후 존속회사(주요사업)
    atdv_excmp_atdv_lstmn_atn: Optional[str] = Field(default=None)  # 분할 후 존속회사(분할 후 상장유지 여부)
    dvfcmp_cmpnm: Optional[str] = Field(default=None)  # 분할설립회사(회사명)
    ffdtl_tast: Optional[str] = Field(default=None)  # 분할설립회사(설립시 재무내용(원)(자산총계))
    ffdtl_tdbt: Optional[str] = Field(default=None)  # 분할설립회사(설립시 재무내용(원)(부채총계))
    ffdtl_teqt: Optional[str] = Field(default=None)  # 분할설립회사(설립시 재무내용(원)(자본총계))
    ffdtl_cpt: Optional[str] = Field(default=None)  # 분할설립회사(설립시 재무내용(원)(자본금))
    ffdtl_std: Optional[str] = Field(default=None)  # 분할설립회사(설립시 재무내용(원)(현재기준))
    dvfcmp_nbsn_rsl: Optional[str] = Field(default=None)  # 분할설립회사(신설사업부문 최근 사업연도 매출액(원))
    dvfcmp_mbsn: Optional[str] = Field(default=None)  # 분할설립회사(주요사업)
    dvfcmp_rlst_atn: Optional[str] = Field(default=None)  # 분할설립회사(재상장신청 여부)
    abcr_crrt: Optional[str] = Field(default=None)  # 감자에 관한 사항(감자비율(%))
    abcr_osprpd_bgd: Optional[str] = Field(default=None)  # 감자에 관한 사항(구주권 제출기간(시작일))
    abcr_osprpd_edd: Optional[str] = Field(default=None)  # 감자에 관한 사항(구주권 제출기간(종료일))
    abcr_trspprpd_bgd: Optional[str] = Field(default=None)  # 감자에 관한 사항(매매거래정지 예정기간(시작일))
    abcr_trspprpd_edd: Optional[str] = Field(default=None)  # 감자에 관한 사항(매매거래정지 예정기간(종료일))
    abcr_nstkascnd: Optional[str] = Field(default=None)  # 감자에 관한 사항(신주배정조건)
    abcr_shstkcnt_rt_at_rs: Optional[str] = Field(default=None)  # 감자에 관한 사항(주주 주식수 비례여부 및 사유)
    abcr_nstkasstd: Optional[str] = Field(default=None)  # 감자에 관한 사항(신주배정기준일)
    abcr_nstkdlprd: Optional[str] = Field(default=None)  # 감자에 관한 사항(신주권교부예정일)
    abcr_nstklstprd: Optional[str] = Field(default=None)  # 감자에 관한 사항(신주의 상장예정일)
    gmtsck_prd: Optional[str] = Field(default=None)  # 주주총회 예정일
    cdobprpd_bgd: Optional[str] = Field(default=None)  # 채권자 이의제출기간(시작일)
    cdobprpd_edd: Optional[str] = Field(default=None)  # 채권자 이의제출기간(종료일)
    dvdt: Optional[str] = Field(default=None)  # 분할기일
    dvrgsprd: Optional[str] = Field(default=None)  # 분할등기 예정일
    bddd: Optional[str] = Field(default=None)  # 이사회결의일(결정일)
    od_a_at_t: Optional[str] = Field(default=None)  # 사외이사참석여부(참석(명))
    od_a_at_b: Optional[str] = Field(default=None)  # 사외이사참석여부(불참(명))
    adt_a_atn: Optional[str] = Field(default=None)  # 감사(사외이사가 아닌 감사위원) 참석여부
    popt_ctr_atn: Optional[str] = Field(default=None)  # 풋옵션 등 계약 체결여부
    popt_ctr_cn: Optional[str] = Field(default=None)  # 계약내용
    rs_sm_atn: Optional[str] = Field(default=None)  # 증권신고서 제출대상 여부
    ex_sm_r: Optional[str] = Field(default=None)  # 제출을 면제받은 경우 그 사유

class DartCompanyDivide(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: List[DartCompanyDivideItem]  # 결과 리스트

def get_company_divide_description():
    return """
    기업 분할

    이 API는 기업의 분할에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 기업코드: 공시대상회사의 고유번호 (8자리)
       - 기업명: 공시대상회사명

    2. 분할 개요
       - 분할방법: 분할의 구체적인 방법
       - 분할의 중요영향 및 효과: 분할이 미치는 영향
       - 분할비율: 분할 비율
       - 분할로 이전할 사업 및 재산의 내용: 분할 대상 사업 및 재산

    3. 분할 후 존속회사 정보
       - 회사명: 분할 후 존속하는 회사명
       - 주요사업: 존속회사의 주요 사업
       - 분할 후 상장유지 여부: 상장 지위 유지 여부
       - 분할 후 재무내용:
         * 자산총계, 부채총계, 자본총계, 자본금
         * 현재기준 (재무상태 기준일)
       - 존속사업부문 매출액: 분할 후 남은 사업부문의 매출액

    4. 분할설립 회사 정보
       - 회사명: 분할로 새로 설립되는 회사명
       - 주요사업: 신설회사의 주요 사업
       - 재상장신청 여부: 신설회사의 상장 신청 여부
       - 설립시 재무내용:
         * 자산총계, 부채총계, 자본총계, 자본금
         * 현재기준 (재무상태 기준일)
       - 신설사업부문 매출액: 분할로 이전되는 사업부문의 매출액

    5. 감자 관련 정보
       - 감자비율: 자본금 감소 비율
       - 구주권 제출기간: 기존 주권 제출 기간
       - 매매거래정지 예정기간: 주식 거래 정지 기간
       - 신주배정조건: 신주 배정 조건
       - 주주 주식수 비례여부 및 사유: 주주별 배정 비례 여부
       - 신주배정기준일: 신주 배정 기준일
       - 신주권교부예정일: 신주권 발행 예정일
       - 신주의 상장예정일: 신주 상장 예정일

    6. 분할 일정
       - 주주총회 예정일: 분할 승인을 위한 주주총회 일정
       - 채권자 이의제출기간: 채권자의 이의 제출 기간
       - 분할기일: 실제 분할이 이루어지는 날짜
       - 분할등기 예정일: 분할 등기 예정일

    7. 기타 중요 정보
       - 이사회 정보: 이사회결의일, 사외이사 참석정보, 감사 참석정보
       - 풋옵션 등 계약: 풋옵션 계약 체결 여부 및 내용
       - 증권신고서: 제출대상 여부, 면제 사유

    기업 분할의 주요 형태:
    - 분할설립: 기업을 분할하여 새로운 회사 설립
    - 분할합병: 기업을 분할하여 다른 회사와 합병
    - 물적분할: 사업부문을 분할하여 별도 회사로 분리
    - 인적분할: 기존 회사를 해산하고 새로운 회사들로 분할

    분할의 주요 목적:
    - 사업 포커스 강화
    - 경영 효율성 증대
    - 주주 가치 극대화
    - 규제 회피
    - 세금 절약
    - 경영진 보상

    활용 방안:
    - 기업 구조조정 분석
    - 주주 가치 변화 추적
    - 기업 가치 평가
    - 투자 위험도 평가
    - 기업 지배구조 변화 모니터링
    - 사업 포트폴리오 최적화 분석
    - 기업 재무 건전성 평가
    - 시장 경쟁구조 변화 분석
    """
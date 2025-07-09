from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class DartCompanyMergeItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    rcept_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 공시대상회사명
    mg_mth: Optional[str] = Field(default=None)  # 합병방법
    mg_stn: Optional[str] = Field(default=None)  # 합병형태
    mg_pp: Optional[str] = Field(default=None)  # 합병목적
    mg_rt: Optional[str] = Field(default=None)  # 합병비율
    mg_rt_bs: Optional[str] = Field(default=None)  # 합병비율 산출근거
    exevl_atn: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가 여부)
    exevl_bs_rs: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(근거 및 사유)
    exevl_intn: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가기관의 명칭)
    exevl_pd: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가 기간)
    exevl_op: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가 의견)
    mgnstk_ostk_cnt: Optional[str] = Field(default=None)  # 합병신주의 종류와 수(주)(보통주식)
    mgnstk_cstk_cnt: Optional[str] = Field(default=None)  # 합병신주의 종류와 수(주)(종류주식)
    mgptncmp_cmpnm: Optional[str] = Field(default=None)  # 합병상대회사(회사명)
    mgptncmp_mbsn: Optional[str] = Field(default=None)  # 합병상대회사(주요사업)
    mgptncmp_rl_cmpn: Optional[str] = Field(default=None)  # 합병상대회사(회사와의 관계)
    rbsnfdtl_tast: Optional[str] = Field(default=None)  # 합병상대회사(최근 사업연도 재무내용(원)(자산총계))
    rbsnfdtl_tdbt: Optional[str] = Field(default=None)  # 합병상대회사(최근 사업연도 재무내용(원)(부채총계))
    rbsnfdtl_teqt: Optional[str] = Field(default=None)  # 합병상대회사(최근 사업연도 재무내용(원)(자본총계))
    rbsnfdtl_cpt: Optional[str] = Field(default=None)  # 합병상대회사(최근 사업연도 재무내용(원)(자본금))
    rbsnfdtl_sl: Optional[str] = Field(default=None)  # 합병상대회사(최근 사업연도 재무내용(원)(매출액))
    rbsnfdtl_nic: Optional[str] = Field(default=None)  # 합병상대회사(최근 사업연도 재무내용(원)(당기순이익))
    eadtat_intn: Optional[str] = Field(default=None)  # 합병상대회사(외부감사 여부(기관명))
    eadtat_op: Optional[str] = Field(default=None)  # 합병상대회사(외부감사 여부(감사의견))
    nmgcmp_cmpnm: Optional[str] = Field(default=None)  # 신설합병회사(회사명)
    ffdtl_tast: Optional[str] = Field(default=None)  # 신설합병회사(설립시 재무내용(원)(자산총계))
    ffdtl_tdbt: Optional[str] = Field(default=None)  # 신설합병회사(설립시 재무내용(원)(부채총계))
    ffdtl_teqt: Optional[str] = Field(default=None)  # 신설합병회사(설립시 재무내용(원)(자본총계))
    ffdtl_cpt: Optional[str] = Field(default=None)  # 신설합병회사(설립시 재무내용(원)(자본금))
    ffdtl_std: Optional[str] = Field(default=None)  # 신설합병회사(설립시 재무내용(원)(현재기준))
    nmgcmp_nbsn_rsl: Optional[str] = Field(default=None)  # 신설합병회사(신설사업부문 최근 사업연도 매출액(원))
    nmgcmp_mbsn: Optional[str] = Field(default=None)  # 신설합병회사(주요사업)
    nmgcmp_rlst_atn: Optional[str] = Field(default=None)  # 신설합병회사(재상장신청 여부)
    mgsc_mgctrd: Optional[str] = Field(default=None)  # 합병일정(합병계약일)
    mgsc_shddstd: Optional[str] = Field(default=None)  # 합병일정(주주확정기준일)
    mgsc_shclspd_bgd: Optional[str] = Field(default=None)  # 합병일정(주주명부 폐쇄기간(시작일))
    mgsc_shclspd_edd: Optional[str] = Field(default=None)  # 합병일정(주주명부 폐쇄기간(종료일))
    mgsc_mgop_rcpd_bgd: Optional[str] = Field(default=None)  # 합병일정(합병반대의사통지 접수기간(시작일))
    mgsc_mgop_rcpd_edd: Optional[str] = Field(default=None)  # 합병일정(합병반대의사통지 접수기간(종료일))
    mgsc_gmtsck_prd: Optional[str] = Field(default=None)  # 합병일정(주주총회예정일자)
    mgsc_aprskh_expd_bgd: Optional[str] = Field(default=None)  # 합병일정(주식매수청구권 행사기간(시작일))
    mgsc_aprskh_expd_edd: Optional[str] = Field(default=None)  # 합병일정(주식매수청구권 행사기간(종료일))
    mgsc_osprpd_bgd: Optional[str] = Field(default=None)  # 합병일정(구주권 제출기간(시작일))
    mgsc_osprpd_edd: Optional[str] = Field(default=None)  # 합병일정(구주권 제출기간(종료일))
    mgsc_trspprpd_bgd: Optional[str] = Field(default=None)  # 합병일정(매매거래 정지예정기간(시작일))
    mgsc_trspprpd_edd: Optional[str] = Field(default=None)  # 합병일정(매매거래 정지예정기간(종료일))
    mgsc_cdobprpd_bgd: Optional[str] = Field(default=None)  # 합병일정(채권자이의 제출기간(시작일))
    mgsc_cdobprpd_edd: Optional[str] = Field(default=None)  # 합병일정(채권자이의 제출기간(종료일))
    mgsc_mgdt: Optional[str] = Field(default=None)  # 합병일정(합병기일)
    mgsc_ergmd: Optional[str] = Field(default=None)  # 합병일정(종료보고 총회일)
    mgsc_mgrgsprd: Optional[str] = Field(default=None)  # 합병일정(합병등기예정일자)
    mgsc_nstkdlprd: Optional[str] = Field(default=None)  # 합병일정(신주권교부예정일)
    mgsc_nstklstprd: Optional[str] = Field(default=None)  # 합병일정(신주의 상장예정일)
    bdlst_atn: Optional[str] = Field(default=None)  # 우회상장 해당 여부
    otcpr_bdlst_sf_atn: Optional[str] = Field(default=None)  # 타법인의 우회상장 요건 충족여부
    aprskh_plnprc: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(매수예정가격)
    aprskh_pym_plpd_mth: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(지급예정시기, 지급방법)
    aprskh_ctref: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(계약에 미치는 효력)
    bddd: Optional[str] = Field(default=None)  # 이사회결의일(결정일)
    od_a_at_t: Optional[str] = Field(default=None)  # 사외이사참석여부(참석(명))
    od_a_at_b: Optional[str] = Field(default=None)  # 사외이사참석여부(불참(명))
    adt_a_atn: Optional[str] = Field(default=None)  # 감사(사외이사가 아닌 감사위원) 참석여부
    popt_ctr_atn: Optional[str] = Field(default=None)  # 풋옵션 등 계약 체결여부
    popt_ctr_cn: Optional[str] = Field(default=None)  # 계약내용
    rs_sm_atn: Optional[str] = Field(default=None)  # 증권신고서 제출대상 여부
    ex_sm_r: Optional[str] = Field(default=None)  # 제출을 면제받은 경우 그 사유

class DartCompanyMerge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: List[DartCompanyMergeItem]  # 결과 리스트

def get_company_merge_description():
    return """
    기업 합병

    이 API는 기업의 합병에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 기업코드: 공시대상회사의 고유번호 (8자리)
       - 기업명: 공시대상회사명

    2. 합병 개요
       - 합병방법: 합병의 구체적인 방법
       - 합병형태: 합병의 형태 (흡수합병, 신설합병 등)
       - 합병목적: 합병의 목적
       - 합병비율: 합병 비율 및 산출근거

    3. 외부평가 정보
       - 외부평가 여부: 외부평가 실시 여부
       - 외부평가기관: 평가기관의 명칭
       - 외부평가 기간: 평가 수행 기간
       - 외부평가 의견: 평가 결과 및 의견
       - 근거 및 사유: 외부평가 실시 근거

    4. 합병신주 정보
       - 보통주식 수량: 합병으로 발행되는 보통주식 수
       - 종류주식 수량: 합병으로 발행되는 종류주식 수

    5. 합병상대회사 정보
       - 회사명: 합병상대회사명
       - 주요사업: 합병상대회사의 주요 사업
       - 회사와의 관계: 합병상대회사와의 관계
       - 최근 사업연도 재무내용:
         * 자산총계, 부채총계, 자본총계, 자본금
         * 매출액, 당기순이익
       - 외부감사 여부: 외부감사 기관명 및 감사의견

    6. 신설합병회사 정보 (신설합병의 경우)
       - 회사명: 신설합병회사명
       - 주요사업: 신설합병회사의 주요 사업
       - 재상장신청 여부: 상장 신청 여부
       - 설립시 재무내용:
         * 자산총계, 부채총계, 자본총계, 자본금
         * 현재기준 (재무상태 기준일)
       - 신설사업부문 매출액: 신설회사의 사업부문 매출액

    7. 합병 일정
       - 합병계약일: 합병계약 체결일
       - 주주확정기준일: 주주 확정 기준일
       - 주주명부 폐쇄기간: 주주명부 폐쇄 기간
       - 합병반대의사통지 접수기간: 반대 의사 통지 기간
       - 주주총회예정일자: 합병 승인을 위한 주주총회
       - 주식매수청구권 행사기간: 매수청구권 행사 기간
       - 구주권 제출기간: 기존 주권 제출 기간
       - 매매거래 정지예정기간: 주식 거래 정지 기간
       - 채권자이의 제출기간: 채권자 이의 제출 기간
       - 합병기일: 실제 합병이 이루어지는 날짜
       - 종료보고 총회일: 합병 완료 보고 총회
       - 합병등기예정일자: 합병 등기 예정일
       - 신주권교부예정일: 신주권 발행 예정일
       - 신주의 상장예정일: 신주 상장 예정일

    8. 기타 중요 정보
       - 우회상장 관련: 우회상장 해당 여부, 타법인 우회상장 요건 충족여부
       - 주식매수청구권: 매수예정가격, 지급예정시기 및 방법, 계약에 미치는 효력
       - 이사회 정보: 이사회결의일, 사외이사 참석정보, 감사 참석정보
       - 풋옵션 등 계약: 풋옵션 계약 체결 여부 및 내용
       - 증권신고서: 제출대상 여부, 면제 사유

    기업 합병의 주요 형태:
    - 흡수합병: 한 회사가 다른 회사를 흡수하여 존속
    - 신설합병: 두 회사가 해산하고 새로운 회사 설립
    - 동등합병: 비슷한 규모의 회사 간 합병
    - 불균등합병: 규모가 다른 회사 간 합병

    합병의 주요 목적:
    - 시너지 효과 창출
    - 시장 지배력 확대
    - 비용 절감
    - 사업 다각화
    - 규모의 경제 실현
    - 경쟁력 강화

    활용 방안:
    - 기업 가치 평가
    - 시너지 효과 분석
    - 주주 가치 변화 추적
    - 투자 위험도 평가
    - 시장 경쟁구조 변화 분석
    - 기업 재무 건전성 평가
    - 기업 지배구조 변화 모니터링
    - M&A 트렌드 분석
    """
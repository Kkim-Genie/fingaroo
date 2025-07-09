from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class DartCompanyDivideMergeItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    rcept_no: Optional[str] = Field(default=None)  # 접수번호(14자리)
    corp_cls: Optional[str] = Field(default=None)  # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
    corp_code: Optional[str] = Field(default=None)  # 공시대상회사의 고유번호(8자리)
    corp_name: Optional[str] = Field(default=None)  # 공시대상회사명
    dvmg_mth: Optional[str] = Field(default=None)  # 분할합병 방법
    dvmg_impef: Optional[str] = Field(default=None)  # 분할합병의 중요영향 및 효과
    dv_trfbsnprt_cn: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할로 이전할 사업 및 재산의 내용)
    atdv_excmp_cmpnm: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(회사명))
    atdvfdtl_tast: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자산총계)))
    atdvfdtl_tdbt: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(부채총계)))
    atdvfdtl_teqt: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자본총계)))
    atdvfdtl_cpt: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자본금)))
    atdvfdtl_std: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(현재기준)))
    atdv_excmp_exbsn_rsl: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(존속사업부문 최근 사업연도매출액(원)))
    atdv_excmp_mbsn: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(주요사업))
    atdv_excmp_atdv_lstmn_atn: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할 후 존속회사(분할 후 상장유지 여부))
    dvfcmp_cmpnm: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(회사명))
    ffdtl_tast: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자산총계)))
    ffdtl_tdbt: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(부채총계)))
    ffdtl_teqt: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자본총계)))
    ffdtl_cpt: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자본금)))
    ffdtl_std: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(현재기준)))
    dvfcmp_nbsn_rsl: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(신설사업부문 최근 사업연도 매출액(원)))
    dvfcmp_mbsn: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(주요사업))
    dvfcmp_atdv_lstmn_at: Optional[str] = Field(default=None)  # 분할에 관한 사항(분할설립 회사(분할후 상장유지여부))
    abcr_crrt: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(감자비율(%)))
    abcr_osprpd_bgd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(구주권 제출기간(시작일)))
    abcr_osprpd_edd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(구주권 제출기간(종료일)))
    abcr_trspprpd_bgd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(매매거래정지 예정기간(시작일)))
    abcr_trspprpd_edd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(매매거래정지 예정기간(종료일)))
    abcr_nstkascnd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(신주배정조건))
    abcr_shstkcnt_rt_at_rs: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(주주 주식수 비례여부 및 사유))
    abcr_nstkasstd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(신주배정기준일))
    abcr_nstkdlprd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(신주권교부예정일))
    abcr_nstklstprd: Optional[str] = Field(default=None)  # 분할에 관한 사항(감자에 관한 사항(신주의 상장예정일))
    mg_stn: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병형태)
    mgptncmp_cmpnm: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(회사명))
    mgptncmp_mbsn: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(주요사업))
    mgptncmp_rl_cmpn: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(회사와의 관계))
    rbsnfdtl_tast: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자산총계)))
    rbsnfdtl_tdbt: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(부채총계)))
    rbsnfdtl_teqt: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자본총계)))
    rbsnfdtl_cpt: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자본금)))
    rbsnfdtl_sl: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(매출액)))
    rbsnfdtl_nic: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(당기순이익)))
    eadtat_intn: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(외부감사 여부(기관명)))
    eadtat_op: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병상대 회사(외부감사 여부(감사의견)))
    dvmgnstk_ostk_cnt: Optional[str] = Field(default=None)  # 합병에 관한 사항(분할합병신주의 종류와 수(주)(보통주식))
    dvmgnstk_cstk_cnt: Optional[str] = Field(default=None)  # 합병에 관한 사항(분할합병신주의 종류와 수(주)(종류주식))
    nmgcmp_cmpnm: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병신설 회사(회사명))
    nmgcmp_cpt: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병신설 회사(자본금(원)))
    nmgcmp_mbsn: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병신설 회사(주요사업))
    nmgcmp_rlst_atn: Optional[str] = Field(default=None)  # 합병에 관한 사항(합병신설 회사(재상장신청 여부))
    dvmg_rt: Optional[str] = Field(default=None)  # 분할합병비율
    dvmg_rt_bs: Optional[str] = Field(default=None)  # 분할합병비율 산출근거
    exevl_atn: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가 여부)
    exevl_bs_rs: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(근거 및 사유)
    exevl_intn: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가기관의 명칭)
    exevl_pd: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가 기간)
    exevl_op: Optional[str] = Field(default=None)  # 외부평가에 관한 사항(외부평가 의견)
    dvmgsc_dvmgctrd: Optional[str] = Field(default=None)  # 분할합병일정(분할합병계약일)
    dvmgsc_shddstd: Optional[str] = Field(default=None)  # 분할합병일정(주주확정기준일)
    dvmgsc_shclspd_bgd: Optional[str] = Field(default=None)  # 분할합병일정(주주명부 폐쇄기간(시작일))
    dvmgsc_shclspd_edd: Optional[str] = Field(default=None)  # 분할합병일정(주주명부 폐쇄기간(종료일))
    dvmgsc_dvmgop_rcpd_bgd: Optional[str] = Field(default=None)  # 분할합병일정(분할합병반대의사통지 접수기간(시작일))
    dvmgsc_dvmgop_rcpd_edd: Optional[str] = Field(default=None)  # 분할합병일정(분할합병반대의사통지 접수기간(종료일))
    dvmgsc_gmtsck_prd: Optional[str] = Field(default=None)  # 분할합병일정(주주총회예정일자)
    dvmgsc_aprskh_expd_bgd: Optional[str] = Field(default=None)  # 분할합병일정(주식매수청구권 행사기간(시작일))
    dvmgsc_aprskh_expd_edd: Optional[str] = Field(default=None)  # 분할합병일정(주식매수청구권 행사기간(종료일))
    dvmgsc_cdobprpd_bgd: Optional[str] = Field(default=None)  # 분할합병일정(채권자 이의 제출기간(시작일))
    dvmgsc_cdobprpd_edd: Optional[str] = Field(default=None)  # 분할합병일정(채권자 이의 제출기간(종료일))
    dvmgsc_dvmgdt: Optional[str] = Field(default=None)  # 분할합병일정(분할합병기일)
    dvmgsc_ergmd: Optional[str] = Field(default=None)  # 분할합병일정(종료보고 총회일)
    dvmgsc_dvmgrgsprd: Optional[str] = Field(default=None)  # 분할합병일정(분할합병등기예정일)
    bdlst_atn: Optional[str] = Field(default=None)  # 우회상장 해당 여부
    otcpr_bdlst_sf_atn: Optional[str] = Field(default=None)  # 타법인의 우회상장 요건 충족여부
    aprskh_exrq: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(행사요건)
    aprskh_plnprc: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(매수예정가격)
    aprskh_ex_pc_mth_pd_pl: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(행사절차, 방법, 기간, 장소)
    aprskh_pym_plpd_mth: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(지급예정시기, 지급방법)
    aprskh_lmt: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용)
    aprskh_ctref: Optional[str] = Field(default=None)  # 주식매수청구권에 관한 사항(계약에 미치는 효력)
    bddd: Optional[str] = Field(default=None)  # 이사회결의일(결정일)
    od_a_at_t: Optional[str] = Field(default=None)  # 사외이사참석여부(참석(명))
    od_a_at_b: Optional[str] = Field(default=None)  # 사외이사참석여부(불참(명))
    adt_a_atn: Optional[str] = Field(default=None)  # 감사(사외이사가 아닌 감사위원) 참석여부
    popt_ctr_atn: Optional[str] = Field(default=None)  # 풋옵션 등 계약 체결여부
    popt_ctr_cn: Optional[str] = Field(default=None)  # 계약내용
    rs_sm_atn: Optional[str] = Field(default=None)  # 증권신고서 제출대상 여부
    ex_sm_r: Optional[str] = Field(default=None)  # 제출을 면제받은 경우 그 사유

class DartCompanyDivideMerge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: List[DartCompanyDivideMergeItem]  # 결과 리스트

def get_company_divide_merge_description():
    return """
    기업 분할합병

    이 API는 기업의 분할합병에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호 (14자리)
       - 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)
       - 기업코드: 공시대상회사의 고유번호 (8자리)
       - 기업명: 공시대상회사명

    2. 분할합병 개요
       - 분할합병 방법: 분할합병의 구체적인 방법
       - 분할합병의 중요영향 및 효과: 분할합병이 미치는 영향
       - 분할합병비율: 분할합병 비율 및 산출근거

    3. 분할 관련 정보
       - 분할로 이전할 사업 및 재산의 내용
       - 분할 후 존속회사 정보:
         * 회사명, 주요사업, 상장유지 여부
         * 분할 후 재무내용 (자산총계, 부채총계, 자본총계, 자본금)
         * 존속사업부문 매출액
       - 분할설립 회사 정보:
         * 회사명, 주요사업, 상장유지 여부
         * 설립시 재무내용 (자산총계, 부채총계, 자본총계, 자본금)
         * 신설사업부문 매출액

    4. 합병 관련 정보
       - 합병형태: 합병의 형태
       - 합병상대 회사 정보:
         * 회사명, 주요사업, 회사와의 관계
         * 최근 사업연도 재무내용 (자산총계, 부채총계, 자본총계, 자본금, 매출액, 당기순이익)
         * 외부감사 여부 및 감사의견
       - 합병신설 회사 정보:
         * 회사명, 자본금, 주요사업, 재상장신청 여부
       - 분할합병신주 정보: 보통주식 및 종류주식 수량

    5. 감자 관련 정보
       - 감자비율, 구주권 제출기간
       - 매매거래정지 예정기간
       - 신주배정조건, 신주배정기준일
       - 신주권교부예정일, 신주의 상장예정일

    6. 분할합병 일정
       - 분할합병계약일, 주주확정기준일
       - 주주명부 폐쇄기간
       - 분할합병반대의사통지 접수기간
       - 주주총회예정일자
       - 주식매수청구권 행사기간
       - 채권자 이의 제출기간
       - 분할합병기일, 종료보고 총회일, 분할합병등기예정일

    7. 기타 중요 정보
       - 외부평가 정보: 외부평가 여부, 기관명, 평가기간, 평가의견
       - 우회상장 관련: 우회상장 해당 여부, 타법인 우회상장 요건 충족여부
       - 주식매수청구권: 행사요건, 매수예정가격, 행사절차, 지급방법
       - 이사회 정보: 이사회결의일, 사외이사 참석정보, 감사 참석정보
       - 증권신고서: 제출대상 여부, 면제 사유

    분할합병의 주요 형태:
    - 분할합병: 기업을 분할하여 일부를 다른 회사와 합병
    - 분할설립: 기업을 분할하여 새로운 회사 설립
    - 합병신설: 두 회사가 합병하여 새로운 회사 설립

    활용 방안:
    - 기업 구조조정 분석
    - 주주 가치 변화 추적
    - 기업 가치 평가
    - 투자 위험도 평가
    - 기업 지배구조 변화 모니터링
    - 시장 경쟁구조 변화 분석
    - 기업 재무 건전성 평가
    """
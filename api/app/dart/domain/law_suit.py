from pydantic import BaseModel, Field
from typing import Optional

class DartLawSuitItem(BaseModel):
    recept_no: Optional[str] = Field(default=None)  # 접수번호
    corp_cls: Optional[str] = Field(default=None)  # 법인구분
    corp_code: Optional[str] = Field(default=None)  # 고유번호
    corp_name: Optional[str] = Field(default=None)  # 회사명
    icnm: Optional[str] = Field(default=None)  # 사건의 명칭
    ac_ap: Optional[str] = Field(default=None)  # 원고·신청인
    rq_cn: Optional[str] = Field(default=None)  # 청구내용
    cpct: Optional[str] = Field(default=None)  # 관할법원
    ft_ctp: Optional[str] = Field(default=None)  # 항후대책
    lgd: Optional[str] = Field(default=None)  # 제기일자
    cfd: Optional[str] = Field(default=None)  # 확인일자

class DartLawSuit(BaseModel):
    status: str  # 에러 및 정보 코드
    message: str  # 에러 및 정보 메시지
    list: list[DartLawSuitItem]  # 결과 리

def get_law_suit_description():
    return """
    소송

    이 API는 기업의 소송에 대한 상세 정보를 제공합니다.

    주요 정보:
    
    1. 기업 기본 정보
       - 접수번호: 공시 접수 번호
       - 법인구분: 기업의 법인 구분
       - 고유번호: 기업의 고유 식별번호
       - 회사명: 공시대상회사명

    2. 소송 사건 정보
       - 사건의 명칭: 소송 사건의 명칭
       - 원고·신청인: 소송의 원고 또는 신청인
       - 청구내용: 소송의 주요 청구 내용
       - 관할법원: 소송을 담당하는 법원

    3. 소송 진행 정보
       - 항후대책: 기업의 대응 방안 및 전략
       - 제기일자: 소송이 제기된 날짜
       - 확인일자: 소송 사실을 확인한 날짜

    소송의 주요 유형:
    - 민사소송: 계약 분쟁, 손해배상 등
    - 행정소송: 행정처분에 대한 소송
    - 형사소송: 형사 관련 소송
    - 특허소송: 지적재산권 관련 소송
    - 노동소송: 노동 관련 분쟁
    - 상사소송: 상업 관련 분쟁

    소송이 기업에 미치는 영향:
    - 재무적 영향: 손해배상금, 법무비용
    - 평판적 영향: 기업 이미지 하락
    - 경영적 영향: 경영진의 시간과 자원 소모
    - 주가 영향: 투자자 심리 악화
    - 사업적 영향: 계약 관계 악화

    소송 위험 평가 요소:
    - 소송 규모: 청구 금액의 크기
    - 소송 성격: 소송의 복잡성과 중요도
    - 법적 근거: 소송의 법적 타당성
    - 기업 대응력: 법무 역량과 전략
    - 외부 환경: 법원 판례, 법령 변화

    활용 방안:
    - 기업 리스크 평가
    - 투자 위험도 분석
    - 기업 가치 평가
    - 법무 비용 예측
    - 평판 리스크 관리
    - 투자 의사결정 지원
    - 기업 지배구조 평가
    - ESG 리스크 분석
    - 신용도 평가
    - 포트폴리오 리스크 관리
    - 기업 경영 성과 분석
    - 법적 환경 변화 모니터링
    """
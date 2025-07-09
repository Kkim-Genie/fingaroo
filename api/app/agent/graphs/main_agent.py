from typing import Literal
from app.agent.states.basic_state import GraphState
from app.agent.graphs.search_agent import search_agent
from app.agent.graphs.dart_agent import dart_agent
from app.agent.graphs.stock_price_agent import stock_price_agent
from langgraph_supervisor import create_supervisor
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings

settings = get_settings()

def main_agent():
    llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)
    supervisor = create_supervisor(
        agents=[search_agent(), dart_agent(), stock_price_agent()],
        model=llm,
        state_schema=GraphState,
        output_mode='full_history',
        prompt="""
        당신이 가지고 있는 assistant들은 다음과 같습니다

        1. search_agent: 경제관련된 다양한 정보를 검색합니다. 답변을 하기 위한 충분한 정보가 있을 경우 실행하지 않습니다. 경제와 관련없는 내용도 검색하지 않습니다. 세부 검색 기능들은 아래와 같습니다.
            - 네이버 뉴스 검색
            - google finance에서 기본 기업 정보 검색
            -> search_agent 노드를 선택했다면 검색할 search_query또한 생성해야 합니다.

        2. dart_agent: dart api를 통해 한국 기업 관련 여러 재무 정보 및 이벤트 정보를 조회합니다.
            - 특정 기업의 유상증자 및 무상증자 결정 정보 검색
            - 특정 기업의 자본금 변동 정보 검색
            - 특정 기업의 분할합병 정보 검색
            - 특정 기업의 분할 정보 검색
            - 특정 기업의 합병 정보 검색
            - 특정 기업의 전환사채 정보 검색
            - 특정 기업의 배당 정보 검색
            - 특정 기업의 재무제표 정보 검색
            - 특정 기업의 무상증자 결정 정보 검색
            - 특정 기업의 소송 정보 검색
            - 특정 기업의 다중회사 계정 정보 검색
            - 특정 기업의 다중회사 재무지표 정보 검색
            - 특정 기업의 유상증자 결정 정보 검색
            - 특정 기업의 단일회사 재무지표 정보 검색
            - 특정 기업의 단일회사 계정 정보 검색
            - 특정 기업의 자사주매입 정보 검색
            - 특정 기업의 자기주식 처분 결정 정보 검색
            - 특정 기업의 주식총수 현황 정보 검색
            - 특정 기업의 자기주식 현황 정보 검색

        3. stock_price_agent: 여러 기업/ETF의 주가 데이터를 검색합니다.
            - 지표의 id 및 기본정보 검색
            - 지표의 id를 기반하여 주가 데이터 검색

        이 assistant들이 협력하도록 하세요.

        추가 지시 사항
        1. search_agent는 경제와 관련한 검색만 수행합니다. 경제와 관련없는 내용이라면 절대 사용하지 않습니다
        2. 사용할 sub agent가 없을 경우 본인이 직접 답변합니다.
        3. 답변은 markdown 형식으로 작성합니다. 
        """
    )

    main_agent = supervisor.compile()

    return main_agent
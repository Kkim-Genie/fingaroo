from app.agent.states.basic_state import GraphState
from app.agent.graphs.search_agent import search_agent
from app.agent.graphs.dart_agent import dart_agent
from app.agent.graphs.stock_price_agent import stock_price_agent
from app.agent.graphs.chartdata_agent import chartdata_agent
from langgraph_supervisor import create_supervisor
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings
from langgraph.checkpoint.memory import MemorySaver

settings = get_settings()
checkpointer = MemorySaver()

def main_agent():
    llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)
    supervisor = create_supervisor(
        agents=[search_agent(), dart_agent(), stock_price_agent(), chartdata_agent()],
        model=llm,
        state_schema=GraphState,
        output_mode='full_history',
        prompt="""
        당신이 가지고 있는 assistant들은 다음과 같습니다

        1. search_agent: 경제와 관련되었거나 추가적인 인터넷 검색이 필요할 떄 사용합니다. 세부 검색 기능들은 아래와 같습니다.
            - 네이버 뉴스 검색
            - google finance에서 기본 기업 정보 검색
            - 경제 관련 뉴스 검색(날짜를 기준으로 검색)

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

        4. chartdata_agent: user는 여러 지표의 time series데이터를 담고 있는 차트데이터를 가지고 있습니다. 해당 agent는 이러한 차트데이터를 관리합니다.
            - 차트데이터에 지표 추가

        이 assistant들이 협력하도록 하세요.

        추가 지시 사항
        1. 모든 질문에 대한 최족적인 답변은 반드시 `markdown` 형식으로 작성합니다. 
        2. 일반적인 뉴스, 시황, 흐름에 관한 질문이 들어올 시 search_agent를 통해 검색합니다. 어떤 종류의 뉴스를 원하는지 물어보지 않고 search_agent를 사용합니다. (예: 저번주 월요일 뉴스 알려줘)
        3. 경제와 관련하지 않은 내용을 질문했다면 다른 agent를 사용하지 말고 자체적으로 판단하여 답변합니다.
        """
    )

    main_agent = supervisor.compile(checkpointer=checkpointer)

    return main_agent